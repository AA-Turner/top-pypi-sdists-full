# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111llll1_opy_, bstack1ll11llll_opy_, bstack1l111ll111_opy_, bstack11lll111l1_opy_, \
    bstack111lll11l1l_opy_
from bstack_utils.measure import measure
def bstack11lll11l1_opy_(bstack1llllll11l11_opy_):
    for driver in bstack1llllll11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1lll111l_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack1l1l11l1ll_opy_(driver, status, reason=bstack1l11l11_opy_ (u"ࠬ࠭ῧ")):
    bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
    if bstack11l11llll_opy_.bstack11111l11ll_opy_():
        return
    bstack1lll11ll11_opy_ = bstack1llll11ll1_opy_(bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩῨ"), bstack1l11l11_opy_ (u"ࠧࠨῩ"), status, reason, bstack1l11l11_opy_ (u"ࠨࠩῪ"), bstack1l11l11_opy_ (u"ࠩࠪΎ"))
    driver.execute_script(bstack1lll11ll11_opy_)
@measure(event_name=EVENTS.bstack1l1lll111l_opy_, stage=STAGE.bstack1lll11l1_opy_)
def bstack1l11111l1l_opy_(page, status, reason=bstack1l11l11_opy_ (u"ࠪࠫῬ")):
    try:
        if page is None:
            return
        bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
        if bstack11l11llll_opy_.bstack11111l11ll_opy_():
            return
        bstack1lll11ll11_opy_ = bstack1llll11ll1_opy_(bstack1l11l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ῭"), bstack1l11l11_opy_ (u"ࠬ࠭΅"), status, reason, bstack1l11l11_opy_ (u"࠭ࠧ`"), bstack1l11l11_opy_ (u"ࠧࠨ῰"))
        page.evaluate(bstack1l11l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ῱"), bstack1lll11ll11_opy_)
    except Exception as e:
        print(bstack1l11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢῲ"), e)
def bstack1llll11ll1_opy_(type, name, status, reason, bstack1ll1111ll_opy_, bstack11llll1l1l_opy_):
    bstack1llllll1l_opy_ = {
        bstack1l11l11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪῳ"): type,
        bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧῴ"): {}
    }
    if type == bstack1l11l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ῵"):
        bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩῶ")][bstack1l11l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ῷ")] = bstack1ll1111ll_opy_
        bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫῸ")][bstack1l11l11_opy_ (u"ࠩࡧࡥࡹࡧࠧΌ")] = json.dumps(str(bstack11llll1l1l_opy_))
    if type == bstack1l11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫῺ"):
        bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧΏ")][bstack1l11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪῼ")] = name
    if type == bstack1l11l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ´"):
        bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ῾")][bstack1l11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῿")] = status
        if status == bstack1l11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ ") and str(reason) != bstack1l11l11_opy_ (u"ࠥࠦ "):
            bstack1llllll1l_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ ")][bstack1l11l11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ ")] = json.dumps(str(reason))
    bstack1ll11l11ll_opy_ = bstack1l11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ ").format(json.dumps(bstack1llllll1l_opy_))
    return bstack1ll11l11ll_opy_
def bstack11111llll_opy_(url, config, logger, bstack111l11ll_opy_=False):
    hostname = bstack1ll11llll_opy_(url)
    is_private = bstack11lll111l1_opy_(hostname)
    try:
        if is_private or bstack111l11ll_opy_:
            file_path = bstack11l111llll1_opy_(bstack1l11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ "), bstack1l11l11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ "), logger)
            if os.environ.get(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ ")) and eval(
                    os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ "))):
                return
            if (bstack1l11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ ") in config and not config[bstack1l11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ ")]):
                os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ​")] = str(True)
                bstack1llllll11lll_opy_ = {bstack1l11l11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ‌"): hostname}
                bstack111lll11l1l_opy_(bstack1l11l11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ‍"), bstack1l11l11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ‎"), bstack1llllll11lll_opy_, logger)
    except Exception as e:
        pass
def bstack11lll1l1ll_opy_(caps, bstack1llllll11ll1_opy_):
    if bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ‏") in caps:
        caps[bstack1l11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ‐")][bstack1l11l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ‑")] = True
        if bstack1llllll11ll1_opy_:
            caps[bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ‒")][bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ–")] = bstack1llllll11ll1_opy_
    else:
        caps[bstack1l11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭—")] = True
        if bstack1llllll11ll1_opy_:
            caps[bstack1l11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ―")] = bstack1llllll11ll1_opy_
def bstack11111111111_opy_(bstack111l111l11_opy_):
    bstack1llllll11l1l_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ‖"), bstack1l11l11_opy_ (u"ࠫࠬ‗"))
    if bstack1llllll11l1l_opy_ == bstack1l11l11_opy_ (u"ࠬ࠭‘") or bstack1llllll11l1l_opy_ == bstack1l11l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ’"):
        threading.current_thread().testStatus = bstack111l111l11_opy_
    else:
        if bstack111l111l11_opy_ == bstack1l11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ‚"):
            threading.current_thread().testStatus = bstack111l111l11_opy_