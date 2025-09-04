# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111lll1ll11_opy_, bstack1l1ll111ll_opy_, bstack1l11l1lll_opy_, bstack1l1ll111l_opy_, \
    bstack11l11l1l111_opy_
from bstack_utils.measure import measure
def bstack11l11l111_opy_(bstack1lllll1ll1ll_opy_):
    for driver in bstack1lllll1ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack1l11111l1l_opy_(driver, status, reason=bstack1111l1l_opy_ (u"ࠬ࠭ῧ")):
    bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
    if bstack1l1ll11l1_opy_.bstack11111l1111_opy_():
        return
    bstack11lll11ll1_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩῨ"), bstack1111l1l_opy_ (u"ࠧࠨῩ"), status, reason, bstack1111l1l_opy_ (u"ࠨࠩῪ"), bstack1111l1l_opy_ (u"ࠩࠪΎ"))
    driver.execute_script(bstack11lll11ll1_opy_)
@measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
def bstack1l11l11l1l_opy_(page, status, reason=bstack1111l1l_opy_ (u"ࠪࠫῬ")):
    try:
        if page is None:
            return
        bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
        if bstack1l1ll11l1_opy_.bstack11111l1111_opy_():
            return
        bstack11lll11ll1_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ῭"), bstack1111l1l_opy_ (u"ࠬ࠭΅"), status, reason, bstack1111l1l_opy_ (u"࠭ࠧ`"), bstack1111l1l_opy_ (u"ࠧࠨ῰"))
        page.evaluate(bstack1111l1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ῱"), bstack11lll11ll1_opy_)
    except Exception as e:
        print(bstack1111l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢῲ"), e)
def bstack1ll1l1l1l_opy_(type, name, status, reason, bstack1lll111l1_opy_, bstack1l1l1ll1ll_opy_):
    bstack11llll11l_opy_ = {
        bstack1111l1l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪῳ"): type,
        bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧῴ"): {}
    }
    if type == bstack1111l1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ῵"):
        bstack11llll11l_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩῶ")][bstack1111l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ῷ")] = bstack1lll111l1_opy_
        bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫῸ")][bstack1111l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧΌ")] = json.dumps(str(bstack1l1l1ll1ll_opy_))
    if type == bstack1111l1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫῺ"):
        bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧΏ")][bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪῼ")] = name
    if type == bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ´"):
        bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ῾")][bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῿")] = status
        if status == bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ ") and str(reason) != bstack1111l1l_opy_ (u"ࠥࠦ "):
            bstack11llll11l_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ ")][bstack1111l1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ ")] = json.dumps(str(reason))
    bstack1111l1l11_opy_ = bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ ").format(json.dumps(bstack11llll11l_opy_))
    return bstack1111l1l11_opy_
def bstack1l1l1111l1_opy_(url, config, logger, bstack111llll1_opy_=False):
    hostname = bstack1l1ll111ll_opy_(url)
    is_private = bstack1l1ll111l_opy_(hostname)
    try:
        if is_private or bstack111llll1_opy_:
            file_path = bstack111lll1ll11_opy_(bstack1111l1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ "), bstack1111l1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ "), logger)
            if os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ ")) and eval(
                    os.environ.get(bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ "))):
                return
            if (bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ ") in config and not config[bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ ")]):
                os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ​")] = str(True)
                bstack1lllll1ll111_opy_ = {bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ‌"): hostname}
                bstack11l11l1l111_opy_(bstack1111l1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ‍"), bstack1111l1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ‎"), bstack1lllll1ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1l1lll1l1_opy_(caps, bstack1lllll1ll11l_opy_):
    if bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ‏") in caps:
        caps[bstack1111l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ‐")][bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ‑")] = True
        if bstack1lllll1ll11l_opy_:
            caps[bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ‒")][bstack1111l1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ–")] = bstack1lllll1ll11l_opy_
    else:
        caps[bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭—")] = True
        if bstack1lllll1ll11l_opy_:
            caps[bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ―")] = bstack1lllll1ll11l_opy_
def bstack1lllllll1l11_opy_(bstack111l11llll_opy_):
    bstack1lllll1ll1l1_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ‖"), bstack1111l1l_opy_ (u"ࠫࠬ‗"))
    if bstack1lllll1ll1l1_opy_ == bstack1111l1l_opy_ (u"ࠬ࠭‘") or bstack1lllll1ll1l1_opy_ == bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ’"):
        threading.current_thread().testStatus = bstack111l11llll_opy_
    else:
        if bstack111l11llll_opy_ == bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ‚"):
            threading.current_thread().testStatus = bstack111l11llll_opy_