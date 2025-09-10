# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11l1llll_opy_, bstack1111111l_opy_, bstack1111l1l11_opy_, bstack1l1l1l11l_opy_, \
    bstack11l11l11l1l_opy_
from bstack_utils.measure import measure
def bstack11l111ll1l_opy_(bstack1lllll1ll111_opy_):
    for driver in bstack1lllll1ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1111ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1l11lllll1_opy_(driver, status, reason=bstack1ll11ll_opy_ (u"ࠫࠬῦ")):
    bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
    if bstack1l111111l1_opy_.bstack11111llll1_opy_():
        return
    bstack1l11lllll_opy_ = bstack1ll1ll1ll_opy_(bstack1ll11ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨῧ"), bstack1ll11ll_opy_ (u"࠭ࠧῨ"), status, reason, bstack1ll11ll_opy_ (u"ࠧࠨῩ"), bstack1ll11ll_opy_ (u"ࠨࠩῪ"))
    driver.execute_script(bstack1l11lllll_opy_)
@measure(event_name=EVENTS.bstack1l1111ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1l11ll11l_opy_(page, status, reason=bstack1ll11ll_opy_ (u"ࠩࠪΎ")):
    try:
        if page is None:
            return
        bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
        if bstack1l111111l1_opy_.bstack11111llll1_opy_():
            return
        bstack1l11lllll_opy_ = bstack1ll1ll1ll_opy_(bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ῥ"), bstack1ll11ll_opy_ (u"ࠫࠬ῭"), status, reason, bstack1ll11ll_opy_ (u"ࠬ࠭΅"), bstack1ll11ll_opy_ (u"࠭ࠧ`"))
        page.evaluate(bstack1ll11ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ῰"), bstack1l11lllll_opy_)
    except Exception as e:
        print(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨ῱"), e)
def bstack1ll1ll1ll_opy_(type, name, status, reason, bstack1llll1llll_opy_, bstack1l1ll111l1_opy_):
    bstack111ll111l_opy_ = {
        bstack1ll11ll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩῲ"): type,
        bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ῳ"): {}
    }
    if type == bstack1ll11ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ῴ"):
        bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ῵")][bstack1ll11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬῶ")] = bstack1llll1llll_opy_
        bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪῷ")][bstack1ll11ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭Ὸ")] = json.dumps(str(bstack1l1ll111l1_opy_))
    if type == bstack1ll11ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪΌ"):
        bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ὼ")][bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩΏ")] = name
    if type == bstack1ll11ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨῼ"):
        bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ´")][bstack1ll11ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ῾")] = status
        if status == bstack1ll11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ῿") and str(reason) != bstack1ll11ll_opy_ (u"ࠤࠥ "):
            bstack111ll111l_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ ")][bstack1ll11ll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ ")] = json.dumps(str(reason))
    bstack111111l1_opy_ = bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ ").format(json.dumps(bstack111ll111l_opy_))
    return bstack111111l1_opy_
def bstack1ll1ll1l1l_opy_(url, config, logger, bstack1lll1ll111_opy_=False):
    hostname = bstack1111111l_opy_(url)
    is_private = bstack1l1l1l11l_opy_(hostname)
    try:
        if is_private or bstack1lll1ll111_opy_:
            file_path = bstack11l11l1llll_opy_(bstack1ll11ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ "), bstack1ll11ll_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ "), logger)
            if os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ ")) and eval(
                    os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ "))):
                return
            if (bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ ") in config and not config[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ ")]):
                os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ ")] = str(True)
                bstack1lllll1l1lll_opy_ = {bstack1ll11ll_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ​"): hostname}
                bstack11l11l11l1l_opy_(bstack1ll11ll_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭‌"), bstack1ll11ll_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭‍"), bstack1lllll1l1lll_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1l111_opy_(caps, bstack1lllll1ll11l_opy_):
    if bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ‎") in caps:
        caps[bstack1ll11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ‏")][bstack1ll11ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ‐")] = True
        if bstack1lllll1ll11l_opy_:
            caps[bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭‑")][bstack1ll11ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ‒")] = bstack1lllll1ll11l_opy_
    else:
        caps[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ–")] = True
        if bstack1lllll1ll11l_opy_:
            caps[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ—")] = bstack1lllll1ll11l_opy_
def bstack1llllll1l111_opy_(bstack1111ll1lll_opy_):
    bstack1lllll1ll1l1_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭―"), bstack1ll11ll_opy_ (u"ࠪࠫ‖"))
    if bstack1lllll1ll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠫࠬ‗") or bstack1lllll1ll1l1_opy_ == bstack1ll11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭‘"):
        threading.current_thread().testStatus = bstack1111ll1lll_opy_
    else:
        if bstack1111ll1lll_opy_ == bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭’"):
            threading.current_thread().testStatus = bstack1111ll1lll_opy_