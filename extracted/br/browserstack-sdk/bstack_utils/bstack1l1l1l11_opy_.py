# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111lll1l11l_opy_, bstack11l11l111l_opy_, bstack11l1llllll_opy_, bstack1l11l1l1ll_opy_, \
    bstack11l11l1llll_opy_
from bstack_utils.measure import measure
def bstack111111ll_opy_(bstack1llllll1l1ll_opy_):
    for driver in bstack1llllll1l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack1l1l111lll_opy_)
def bstack1lllll1l11_opy_(driver, status, reason=bstack1ll1ll_opy_ (u"ࠬ࠭ῧ")):
    bstack1llll11l_opy_ = Config.bstack1l11llllll_opy_()
    if bstack1llll11l_opy_.bstack1111l1l11l_opy_():
        return
    bstack1lll1111ll_opy_ = bstack11ll111l11_opy_(bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩῨ"), bstack1ll1ll_opy_ (u"ࠧࠨῩ"), status, reason, bstack1ll1ll_opy_ (u"ࠨࠩῪ"), bstack1ll1ll_opy_ (u"ࠩࠪΎ"))
    driver.execute_script(bstack1lll1111ll_opy_)
@measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack1l1l111lll_opy_)
def bstack1lll11l111_opy_(page, status, reason=bstack1ll1ll_opy_ (u"ࠪࠫῬ")):
    try:
        if page is None:
            return
        bstack1llll11l_opy_ = Config.bstack1l11llllll_opy_()
        if bstack1llll11l_opy_.bstack1111l1l11l_opy_():
            return
        bstack1lll1111ll_opy_ = bstack11ll111l11_opy_(bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ῭"), bstack1ll1ll_opy_ (u"ࠬ࠭΅"), status, reason, bstack1ll1ll_opy_ (u"࠭ࠧ`"), bstack1ll1ll_opy_ (u"ࠧࠨ῰"))
        page.evaluate(bstack1ll1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ῱"), bstack1lll1111ll_opy_)
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢῲ"), e)
def bstack11ll111l11_opy_(type, name, status, reason, bstack1llllll1l_opy_, bstack1111l1l11_opy_):
    bstack11l1lllll1_opy_ = {
        bstack1ll1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪῳ"): type,
        bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧῴ"): {}
    }
    if type == bstack1ll1ll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ῵"):
        bstack11l1lllll1_opy_[bstack1ll1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩῶ")][bstack1ll1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ῷ")] = bstack1llllll1l_opy_
        bstack11l1lllll1_opy_[bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫῸ")][bstack1ll1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧΌ")] = json.dumps(str(bstack1111l1l11_opy_))
    if type == bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫῺ"):
        bstack11l1lllll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧΏ")][bstack1ll1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪῼ")] = name
    if type == bstack1ll1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ´"):
        bstack11l1lllll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ῾")][bstack1ll1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῿")] = status
        if status == bstack1ll1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ ") and str(reason) != bstack1ll1ll_opy_ (u"ࠥࠦ "):
            bstack11l1lllll1_opy_[bstack1ll1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ ")][bstack1ll1ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ ")] = json.dumps(str(reason))
    bstack111l111l_opy_ = bstack1ll1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ ").format(json.dumps(bstack11l1lllll1_opy_))
    return bstack111l111l_opy_
def bstack1lll11ll11_opy_(url, config, logger, bstack1l1l11ll_opy_=False):
    hostname = bstack11l11l111l_opy_(url)
    is_private = bstack1l11l1l1ll_opy_(hostname)
    try:
        if is_private or bstack1l1l11ll_opy_:
            file_path = bstack111lll1l11l_opy_(bstack1ll1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ "), bstack1ll1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ "), logger)
            if os.environ.get(bstack1ll1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ ")) and eval(
                    os.environ.get(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ "))):
                return
            if (bstack1ll1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ ") in config and not config[bstack1ll1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ ")]):
                os.environ[bstack1ll1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ​")] = str(True)
                bstack1llllll1l11l_opy_ = {bstack1ll1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ‌"): hostname}
                bstack11l11l1llll_opy_(bstack1ll1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ‍"), bstack1ll1ll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ‎"), bstack1llllll1l11l_opy_, logger)
    except Exception as e:
        pass
def bstack1lllll1ll1_opy_(caps, bstack1llllll1l111_opy_):
    if bstack1ll1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ‏") in caps:
        caps[bstack1ll1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ‐")][bstack1ll1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ‑")] = True
        if bstack1llllll1l111_opy_:
            caps[bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ‒")][bstack1ll1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ–")] = bstack1llllll1l111_opy_
    else:
        caps[bstack1ll1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭—")] = True
        if bstack1llllll1l111_opy_:
            caps[bstack1ll1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ―")] = bstack1llllll1l111_opy_
def bstack1111111l11l_opy_(bstack111l11l111_opy_):
    bstack1llllll1l1l1_opy_ = bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ‖"), bstack1ll1ll_opy_ (u"ࠫࠬ‗"))
    if bstack1llllll1l1l1_opy_ == bstack1ll1ll_opy_ (u"ࠬ࠭‘") or bstack1llllll1l1l1_opy_ == bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ’"):
        threading.current_thread().testStatus = bstack111l11l111_opy_
    else:
        if bstack111l11l111_opy_ == bstack1ll1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ‚"):
            threading.current_thread().testStatus = bstack111l11l111_opy_