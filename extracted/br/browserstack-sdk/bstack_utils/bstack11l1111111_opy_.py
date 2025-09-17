# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll11lll1_opy_, bstack1l1l1l11ll_opy_, bstack1l11111ll_opy_, bstack111l1l1l1_opy_, \
    bstack111lll11l11_opy_
from bstack_utils.measure import measure
def bstack1l11l1ll_opy_(bstack1lllll1ll11l_opy_):
    for driver in bstack1lllll1ll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll1111_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack1l1l111l1_opy_(driver, status, reason=bstack1l11ll1_opy_ (u"ࠪࠫῥ")):
    bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
    if bstack111lllll11_opy_.bstack11111l1l1l_opy_():
        return
    bstack11llllll_opy_ = bstack1ll1llllll_opy_(bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧῦ"), bstack1l11ll1_opy_ (u"ࠬ࠭ῧ"), status, reason, bstack1l11ll1_opy_ (u"࠭ࠧῨ"), bstack1l11ll1_opy_ (u"ࠧࠨῩ"))
    driver.execute_script(bstack11llllll_opy_)
@measure(event_name=EVENTS.bstack1llll1111_opy_, stage=STAGE.bstack11lllll111_opy_)
def bstack1llllll11l_opy_(page, status, reason=bstack1l11ll1_opy_ (u"ࠨࠩῪ")):
    try:
        if page is None:
            return
        bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
        if bstack111lllll11_opy_.bstack11111l1l1l_opy_():
            return
        bstack11llllll_opy_ = bstack1ll1llllll_opy_(bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬΎ"), bstack1l11ll1_opy_ (u"ࠪࠫῬ"), status, reason, bstack1l11ll1_opy_ (u"ࠫࠬ῭"), bstack1l11ll1_opy_ (u"ࠬ࠭΅"))
        page.evaluate(bstack1l11ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ`"), bstack11llllll_opy_)
    except Exception as e:
        print(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ῰"), e)
def bstack1ll1llllll_opy_(type, name, status, reason, bstack11l1l11l_opy_, bstack1l1ll1l11_opy_):
    bstack1ll1ll11_opy_ = {
        bstack1l11ll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ῱"): type,
        bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬῲ"): {}
    }
    if type == bstack1l11ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬῳ"):
        bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧῴ")][bstack1l11ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ῵")] = bstack11l1l11l_opy_
        bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩῶ")][bstack1l11ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬῷ")] = json.dumps(str(bstack1l1ll1l11_opy_))
    if type == bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩῸ"):
        bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬΌ")][bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨῺ")] = name
    if type == bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧΏ"):
        bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨῼ")][bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭´")] = status
        if status == bstack1l11ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ῾") and str(reason) != bstack1l11ll1_opy_ (u"ࠣࠤ῿"):
            bstack1ll1ll11_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ ")][bstack1l11ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ ")] = json.dumps(str(reason))
    bstack11111ll11_opy_ = bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ ").format(json.dumps(bstack1ll1ll11_opy_))
    return bstack11111ll11_opy_
def bstack1l11l111_opy_(url, config, logger, bstack1lll111l_opy_=False):
    hostname = bstack1l1l1l11ll_opy_(url)
    is_private = bstack111l1l1l1_opy_(hostname)
    try:
        if is_private or bstack1lll111l_opy_:
            file_path = bstack111ll11lll1_opy_(bstack1l11ll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ "), bstack1l11ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ "), logger)
            if os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ ")) and eval(
                    os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ "))):
                return
            if (bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ ") in config and not config[bstack1l11ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ ")]):
                os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ ")] = str(True)
                bstack1lllll1ll111_opy_ = {bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ "): hostname}
                bstack111lll11l11_opy_(bstack1l11ll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ​"), bstack1l11ll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ‌"), bstack1lllll1ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l11lll_opy_(caps, bstack1lllll1ll1l1_opy_):
    if bstack1l11ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‍") in caps:
        caps[bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ‎")][bstack1l11ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ‏")] = True
        if bstack1lllll1ll1l1_opy_:
            caps[bstack1l11ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ‐")][bstack1l11ll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ‑")] = bstack1lllll1ll1l1_opy_
    else:
        caps[bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ‒")] = True
        if bstack1lllll1ll1l1_opy_:
            caps[bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ–")] = bstack1lllll1ll1l1_opy_
def bstack1lllllll1l11_opy_(bstack1111lll1l1_opy_):
    bstack1lllll1l1lll_opy_ = bstack1l11111ll_opy_(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ—"), bstack1l11ll1_opy_ (u"ࠩࠪ―"))
    if bstack1lllll1l1lll_opy_ == bstack1l11ll1_opy_ (u"ࠪࠫ‖") or bstack1lllll1l1lll_opy_ == bstack1l11ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ‗"):
        threading.current_thread().testStatus = bstack1111lll1l1_opy_
    else:
        if bstack1111lll1l1_opy_ == bstack1l11ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ‘"):
            threading.current_thread().testStatus = bstack1111lll1l1_opy_