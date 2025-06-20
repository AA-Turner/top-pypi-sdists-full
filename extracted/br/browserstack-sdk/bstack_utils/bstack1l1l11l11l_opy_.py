# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111111ll_opy_, bstack11l1ll1ll1_opy_, bstack111ll1lll_opy_, bstack11l1l11l_opy_, \
    bstack11l111l11l1_opy_
from bstack_utils.measure import measure
def bstack1ll11l1ll_opy_(bstack1111111llll_opy_):
    for driver in bstack1111111llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll1111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack11l1l1l11l_opy_(driver, status, reason=bstack11ll11_opy_ (u"ࠬ࠭ỹ")):
    bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
    if bstack1l1ll1llll_opy_.bstack1111ll11l1_opy_():
        return
    bstack11ll11l11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩỺ"), bstack11ll11_opy_ (u"ࠧࠨỻ"), status, reason, bstack11ll11_opy_ (u"ࠨࠩỼ"), bstack11ll11_opy_ (u"ࠩࠪỽ"))
    driver.execute_script(bstack11ll11l11_opy_)
@measure(event_name=EVENTS.bstack1l1ll1111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
def bstack11lll1l11l_opy_(page, status, reason=bstack11ll11_opy_ (u"ࠪࠫỾ")):
    try:
        if page is None:
            return
        bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
        if bstack1l1ll1llll_opy_.bstack1111ll11l1_opy_():
            return
        bstack11ll11l11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧỿ"), bstack11ll11_opy_ (u"ࠬ࠭ἀ"), status, reason, bstack11ll11_opy_ (u"࠭ࠧἁ"), bstack11ll11_opy_ (u"ࠧࠨἂ"))
        page.evaluate(bstack11ll11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤἃ"), bstack11ll11l11_opy_)
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢἄ"), e)
def bstack11l1lll11_opy_(type, name, status, reason, bstack111lll111_opy_, bstack11ll111lll_opy_):
    bstack1l11l1111_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪἅ"): type,
        bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧἆ"): {}
    }
    if type == bstack11ll11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧἇ"):
        bstack1l11l1111_opy_[bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩἈ")][bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ἁ")] = bstack111lll111_opy_
        bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫἊ")][bstack11ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧἋ")] = json.dumps(str(bstack11ll111lll_opy_))
    if type == bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫἌ"):
        bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧἍ")][bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἎ")] = name
    if type == bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩἏ"):
        bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪἐ")][bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨἑ")] = status
        if status == bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩἒ") and str(reason) != bstack11ll11_opy_ (u"ࠥࠦἓ"):
            bstack1l11l1111_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧἔ")][bstack11ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬἕ")] = json.dumps(str(reason))
    bstack1l1ll11ll_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ἖").format(json.dumps(bstack1l11l1111_opy_))
    return bstack1l1ll11ll_opy_
def bstack1l1lll11ll_opy_(url, config, logger, bstack1ll1lll111_opy_=False):
    hostname = bstack11l1ll1ll1_opy_(url)
    is_private = bstack11l1l11l_opy_(hostname)
    try:
        if is_private or bstack1ll1lll111_opy_:
            file_path = bstack11l111111ll_opy_(bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ἗"), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧἘ"), logger)
            if os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧἙ")) and eval(
                    os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨἚ"))):
                return
            if (bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨἛ") in config and not config[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩἜ")]):
                os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫἝ")] = str(True)
                bstack1111111ll1l_opy_ = {bstack11ll11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ἞"): hostname}
                bstack11l111l11l1_opy_(bstack11ll11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ἟"), bstack11ll11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧἠ"), bstack1111111ll1l_opy_, logger)
    except Exception as e:
        pass
def bstack1lll1lllll_opy_(caps, bstack111111l1111_opy_):
    if bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫἡ") in caps:
        caps[bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬἢ")][bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫἣ")] = True
        if bstack111111l1111_opy_:
            caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧἤ")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩἥ")] = bstack111111l1111_opy_
    else:
        caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ἦ")] = True
        if bstack111111l1111_opy_:
            caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἧ")] = bstack111111l1111_opy_
def bstack11111l1ll1l_opy_(bstack111l11l1l1_opy_):
    bstack1111111lll1_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧἨ"), bstack11ll11_opy_ (u"ࠫࠬἩ"))
    if bstack1111111lll1_opy_ == bstack11ll11_opy_ (u"ࠬ࠭Ἢ") or bstack1111111lll1_opy_ == bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧἫ"):
        threading.current_thread().testStatus = bstack111l11l1l1_opy_
    else:
        if bstack111l11l1l1_opy_ == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧἬ"):
            threading.current_thread().testStatus = bstack111l11l1l1_opy_