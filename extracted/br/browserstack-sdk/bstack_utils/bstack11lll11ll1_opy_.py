# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1111ll1l_opy_, bstack1l1l1l1ll_opy_, bstack1l111l1l_opy_, bstack11l1l1l1l1_opy_, \
    bstack11l111lll1l_opy_
from bstack_utils.measure import measure
def bstack1ll11lll11_opy_(bstack1llllll1l111_opy_):
    for driver in bstack1llllll1l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack11ll111111_opy_(driver, status, reason=bstack1l1l1ll_opy_ (u"ࠬ࠭῵")):
    bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
    if bstack1l1l1111l1_opy_.bstack1111l11111_opy_():
        return
    bstack1l1l1lll1l_opy_ = bstack111ll1l1_opy_(bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩῶ"), bstack1l1l1ll_opy_ (u"ࠧࠨῷ"), status, reason, bstack1l1l1ll_opy_ (u"ࠨࠩῸ"), bstack1l1l1ll_opy_ (u"ࠩࠪΌ"))
    driver.execute_script(bstack1l1l1lll1l_opy_)
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1llll111ll_opy_(page, status, reason=bstack1l1l1ll_opy_ (u"ࠪࠫῺ")):
    try:
        if page is None:
            return
        bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
        if bstack1l1l1111l1_opy_.bstack1111l11111_opy_():
            return
        bstack1l1l1lll1l_opy_ = bstack111ll1l1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧΏ"), bstack1l1l1ll_opy_ (u"ࠬ࠭ῼ"), status, reason, bstack1l1l1ll_opy_ (u"࠭ࠧ´"), bstack1l1l1ll_opy_ (u"ࠧࠨ῾"))
        page.evaluate(bstack1l1l1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ῿"), bstack1l1l1lll1l_opy_)
    except Exception as e:
        print(bstack1l1l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ "), e)
def bstack111ll1l1_opy_(type, name, status, reason, bstack111111ll1_opy_, bstack1l1ll11ll1_opy_):
    bstack111llllll_opy_ = {
        bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ "): type,
        bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ "): {}
    }
    if type == bstack1l1l1ll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ "):
        bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ ")][bstack1l1l1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ ")] = bstack111111ll1_opy_
        bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ ")][bstack1l1l1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ ")] = json.dumps(str(bstack1l1ll11ll1_opy_))
    if type == bstack1l1l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ "):
        bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ ")][bstack1l1l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ ")] = name
    if type == bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ​"):
        bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ‌")][bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ‍")] = status
        if status == bstack1l1l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ‎") and str(reason) != bstack1l1l1ll_opy_ (u"ࠥࠦ‏"):
            bstack111llllll_opy_[bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ‐")][bstack1l1l1ll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ‑")] = json.dumps(str(reason))
    bstack1lll11ll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ‒").format(json.dumps(bstack111llllll_opy_))
    return bstack1lll11ll_opy_
def bstack11l11lll_opy_(url, config, logger, bstack1ll1llll1_opy_=False):
    hostname = bstack1l1l1l1ll_opy_(url)
    is_private = bstack11l1l1l1l1_opy_(hostname)
    try:
        if is_private or bstack1ll1llll1_opy_:
            file_path = bstack11l1111ll1l_opy_(bstack1l1l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ–"), bstack1l1l1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ—"), logger)
            if os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ―")) and eval(
                    os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ‖"))):
                return
            if (bstack1l1l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ‗") in config and not config[bstack1l1l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ‘")]):
                os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ’")] = str(True)
                bstack1llllll1l11l_opy_ = {bstack1l1l1ll_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ‚"): hostname}
                bstack11l111lll1l_opy_(bstack1l1l1ll_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ‛"), bstack1l1l1ll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ“"), bstack1llllll1l11l_opy_, logger)
    except Exception as e:
        pass
def bstack1l11l1l1ll_opy_(caps, bstack1llllll11ll1_opy_):
    if bstack1l1l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ”") in caps:
        caps[bstack1l1l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ„")][bstack1l1l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ‟")] = True
        if bstack1llllll11ll1_opy_:
            caps[bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ†")][bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ‡")] = bstack1llllll11ll1_opy_
    else:
        caps[bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭•")] = True
        if bstack1llllll11ll1_opy_:
            caps[bstack1l1l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ‣")] = bstack1llllll11ll1_opy_
def bstack11111111l1l_opy_(bstack111l111lll_opy_):
    bstack1llllll11lll_opy_ = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ․"), bstack1l1l1ll_opy_ (u"ࠫࠬ‥"))
    if bstack1llllll11lll_opy_ == bstack1l1l1ll_opy_ (u"ࠬ࠭…") or bstack1llllll11lll_opy_ == bstack1l1l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ‧"):
        threading.current_thread().testStatus = bstack111l111lll_opy_
    else:
        if bstack111l111lll_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ "):
            threading.current_thread().testStatus = bstack111l111lll_opy_