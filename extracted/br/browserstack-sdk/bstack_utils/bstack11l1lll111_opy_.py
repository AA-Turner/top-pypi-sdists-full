# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l111ll1_opy_, bstack111ll11ll_opy_, bstack1l11l1l1ll_opy_, bstack1l1lll1111_opy_, \
    bstack11l11111l1l_opy_
from bstack_utils.measure import measure
def bstack11l11ll11l_opy_(bstack1lllll1lll1l_opy_):
    for driver in bstack1lllll1lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l1ll1_opy_, stage=STAGE.bstack11111lll_opy_)
def bstack11l1ll1l_opy_(driver, status, reason=bstack1111lll_opy_ (u"ࠧࠨῢ")):
    bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
    if bstack1ll111ll11_opy_.bstack1111l1l1ll_opy_():
        return
    bstack11l11l11l1_opy_ = bstack1111ll1ll_opy_(bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫΰ"), bstack1111lll_opy_ (u"ࠩࠪῤ"), status, reason, bstack1111lll_opy_ (u"ࠪࠫῥ"), bstack1111lll_opy_ (u"ࠫࠬῦ"))
    driver.execute_script(bstack11l11l11l1_opy_)
@measure(event_name=EVENTS.bstack11l1l1ll1_opy_, stage=STAGE.bstack11111lll_opy_)
def bstack1ll11ll11_opy_(page, status, reason=bstack1111lll_opy_ (u"ࠬ࠭ῧ")):
    try:
        if page is None:
            return
        bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
        if bstack1ll111ll11_opy_.bstack1111l1l1ll_opy_():
            return
        bstack11l11l11l1_opy_ = bstack1111ll1ll_opy_(bstack1111lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩῨ"), bstack1111lll_opy_ (u"ࠧࠨῩ"), status, reason, bstack1111lll_opy_ (u"ࠨࠩῪ"), bstack1111lll_opy_ (u"ࠩࠪΎ"))
        page.evaluate(bstack1111lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦῬ"), bstack11l11l11l1_opy_)
    except Exception as e:
        print(bstack1111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤ῭"), e)
def bstack1111ll1ll_opy_(type, name, status, reason, bstack11l1111l11_opy_, bstack1l1l1lll_opy_):
    bstack11lllllll_opy_ = {
        bstack1111lll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ΅"): type,
        bstack1111lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ`"): {}
    }
    if type == bstack1111lll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ῰"):
        bstack11lllllll_opy_[bstack1111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ῱")][bstack1111lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨῲ")] = bstack11l1111l11_opy_
        bstack11lllllll_opy_[bstack1111lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ῳ")][bstack1111lll_opy_ (u"ࠫࡩࡧࡴࡢࠩῴ")] = json.dumps(str(bstack1l1l1lll_opy_))
    if type == bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭῵"):
        bstack11lllllll_opy_[bstack1111lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩῶ")][bstack1111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬῷ")] = name
    if type == bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫῸ"):
        bstack11lllllll_opy_[bstack1111lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬΌ")][bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪῺ")] = status
        if status == bstack1111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫΏ") and str(reason) != bstack1111lll_opy_ (u"ࠧࠨῼ"):
            bstack11lllllll_opy_[bstack1111lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ´")][bstack1111lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ῾")] = json.dumps(str(reason))
    bstack1l11111ll_opy_ = bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭῿").format(json.dumps(bstack11lllllll_opy_))
    return bstack1l11111ll_opy_
def bstack11l11111ll_opy_(url, config, logger, bstack11ll11ll11_opy_=False):
    hostname = bstack111ll11ll_opy_(url)
    is_private = bstack1l1lll1111_opy_(hostname)
    try:
        if is_private or bstack11ll11ll11_opy_:
            file_path = bstack11l1l111ll1_opy_(bstack1111lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ "), bstack1111lll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ "), logger)
            if os.environ.get(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ ")) and eval(
                    os.environ.get(bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ "))):
                return
            if (bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ ") in config and not config[bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ ")]):
                os.environ[bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ ")] = str(True)
                bstack1lllll1llll1_opy_ = {bstack1111lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ "): hostname}
                bstack11l11111l1l_opy_(bstack1111lll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ "), bstack1111lll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ "), bstack1lllll1llll1_opy_, logger)
    except Exception as e:
        pass
def bstack11l111l1l_opy_(caps, bstack1llllll11111_opy_):
    if bstack1111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ ") in caps:
        caps[bstack1111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ​")][bstack1111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭‌")] = True
        if bstack1llllll11111_opy_:
            caps[bstack1111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‍")][bstack1111lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ‎")] = bstack1llllll11111_opy_
    else:
        caps[bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ‏")] = True
        if bstack1llllll11111_opy_:
            caps[bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ‐")] = bstack1llllll11111_opy_
def bstack1llllllllll1_opy_(bstack1111lll1ll_opy_):
    bstack1lllll1lllll_opy_ = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ‑"), bstack1111lll_opy_ (u"࠭ࠧ‒"))
    if bstack1lllll1lllll_opy_ == bstack1111lll_opy_ (u"ࠧࠨ–") or bstack1lllll1lllll_opy_ == bstack1111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ—"):
        threading.current_thread().testStatus = bstack1111lll1ll_opy_
    else:
        if bstack1111lll1ll_opy_ == bstack1111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ―"):
            threading.current_thread().testStatus = bstack1111lll1ll_opy_