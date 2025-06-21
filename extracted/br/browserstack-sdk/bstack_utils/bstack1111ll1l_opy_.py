# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l1l1111_opy_, bstack1l1lll111_opy_, bstack111l1ll1l_opy_, bstack1l11lll1l_opy_, \
    bstack11l111l1l11_opy_
from bstack_utils.measure import measure
def bstack1l1llll1l1_opy_(bstack1111111llll_opy_):
    for driver in bstack1111111llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1111ll11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
def bstack1111ll1ll_opy_(driver, status, reason=bstack1l1l1l1_opy_ (u"࠭ࠧỺ")):
    bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
    if bstack11lll11111_opy_.bstack11111lll11_opy_():
        return
    bstack11llll11l_opy_ = bstack11l11ll1_opy_(bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪỻ"), bstack1l1l1l1_opy_ (u"ࠨࠩỼ"), status, reason, bstack1l1l1l1_opy_ (u"ࠩࠪỽ"), bstack1l1l1l1_opy_ (u"ࠪࠫỾ"))
    driver.execute_script(bstack11llll11l_opy_)
@measure(event_name=EVENTS.bstack1111ll11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
def bstack11llll1l_opy_(page, status, reason=bstack1l1l1l1_opy_ (u"ࠫࠬỿ")):
    try:
        if page is None:
            return
        bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
        if bstack11lll11111_opy_.bstack11111lll11_opy_():
            return
        bstack11llll11l_opy_ = bstack11l11ll1_opy_(bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨἀ"), bstack1l1l1l1_opy_ (u"࠭ࠧἁ"), status, reason, bstack1l1l1l1_opy_ (u"ࠧࠨἂ"), bstack1l1l1l1_opy_ (u"ࠨࠩἃ"))
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥἄ"), bstack11llll11l_opy_)
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣἅ"), e)
def bstack11l11ll1_opy_(type, name, status, reason, bstack1111ll11_opy_, bstack1ll111lll_opy_):
    bstack1l11ll11l_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫἆ"): type,
        bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨἇ"): {}
    }
    if type == bstack1l1l1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨἈ"):
        bstack1l11ll11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪἉ")][bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧἊ")] = bstack1111ll11_opy_
        bstack1l11ll11l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬἋ")][bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨἌ")] = json.dumps(str(bstack1ll111lll_opy_))
    if type == bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬἍ"):
        bstack1l11ll11l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨἎ")][bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫἏ")] = name
    if type == bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪἐ"):
        bstack1l11ll11l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫἑ")][bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩἒ")] = status
        if status == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪἓ") and str(reason) != bstack1l1l1l1_opy_ (u"ࠦࠧἔ"):
            bstack1l11ll11l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨἕ")][bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭἖")] = json.dumps(str(reason))
    bstack1111l111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ἗").format(json.dumps(bstack1l11ll11l_opy_))
    return bstack1111l111_opy_
def bstack1ll1l11l11_opy_(url, config, logger, bstack1lllll1l11_opy_=False):
    hostname = bstack1l1lll111_opy_(url)
    is_private = bstack1l11lll1l_opy_(hostname)
    try:
        if is_private or bstack1lllll1l11_opy_:
            file_path = bstack11l1l1l1111_opy_(bstack1l1l1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨἘ"), bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨἙ"), logger)
            if os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨἚ")) and eval(
                    os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩἛ"))):
                return
            if (bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩἜ") in config and not config[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪἝ")]):
                os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ἞")] = str(True)
                bstack111111l1111_opy_ = {bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪ἟"): hostname}
                bstack11l111l1l11_opy_(bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨἠ"), bstack1l1l1l1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨἡ"), bstack111111l1111_opy_, logger)
    except Exception as e:
        pass
def bstack11ll11l1l_opy_(caps, bstack1111111lll1_opy_):
    if bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬἢ") in caps:
        caps[bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ἣ")][bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬἤ")] = True
        if bstack1111111lll1_opy_:
            caps[bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨἥ")][bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἦ")] = bstack1111111lll1_opy_
    else:
        caps[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧἧ")] = True
        if bstack1111111lll1_opy_:
            caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫἨ")] = bstack1111111lll1_opy_
def bstack11111l1ll1l_opy_(bstack111l1ll1ll_opy_):
    bstack1111111ll1l_opy_ = bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨἩ"), bstack1l1l1l1_opy_ (u"ࠬ࠭Ἢ"))
    if bstack1111111ll1l_opy_ == bstack1l1l1l1_opy_ (u"࠭ࠧἫ") or bstack1111111ll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨἬ"):
        threading.current_thread().testStatus = bstack111l1ll1ll_opy_
    else:
        if bstack111l1ll1ll_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨἭ"):
            threading.current_thread().testStatus = bstack111l1ll1ll_opy_