# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllll1llll1_opy_, bstack1llll1ll1_opy_, bstack11l11l11_opy_, bstack11ll11ll1l_opy_, \
    bstack1lllll1l1111_opy_
from bstack_utils.measure import measure
def bstack1l11l11l_opy_(bstack1ll11ll11l11_opy_):
    for driver in bstack1ll11ll11l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack111ll11111_opy_)
def bstack11ll1l1111_opy_(driver, status, reason=bstack1l1111l_opy_ (u"ࠬ࠭⛮")):
    global_config = Config.bstack111111l1ll_opy_()
    if global_config.bstack1ll1l1l11l1_opy_():
        return
    bstack1lllll1111_opy_ = bstack1l11111l11_opy_(bstack1l1111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⛯"), bstack1l1111l_opy_ (u"ࠧࠨ⛰"), status, reason, bstack1l1111l_opy_ (u"ࠨࠩ⛱"), bstack1l1111l_opy_ (u"ࠩࠪ⛲"))
    driver.execute_script(bstack1lllll1111_opy_)
@measure(event_name=EVENTS.bstack1ll11ll1l1_opy_, stage=STAGE.bstack111ll11111_opy_)
def bstack1l1llll1l1_opy_(page, status, reason=bstack1l1111l_opy_ (u"ࠪࠫ⛳")):
    try:
        if page is None:
            return
        global_config = Config.bstack111111l1ll_opy_()
        if global_config.bstack1ll1l1l11l1_opy_():
            return
        bstack1lllll1111_opy_ = bstack1l11111l11_opy_(bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⛴"), bstack1l1111l_opy_ (u"ࠬ࠭⛵"), status, reason, bstack1l1111l_opy_ (u"࠭ࠧ⛶"), bstack1l1111l_opy_ (u"ࠧࠨ⛷"))
        page.evaluate(bstack1l1111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⛸"), bstack1lllll1111_opy_)
    except Exception as e:
        print(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ⛹"), e)
def bstack1l11111l11_opy_(type, name, status, reason, bstack111l11ll1_opy_, bstack11ll111ll_opy_):
    bstack1ll1lll1l_opy_ = {
        bstack1l1111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ⛺"): type,
        bstack1l1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛻"): {}
    }
    if type == bstack1l1111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⛼"):
        bstack1ll1lll1l_opy_[bstack1l1111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⛽")][bstack1l1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⛾")] = bstack111l11ll1_opy_
        bstack1ll1lll1l_opy_[bstack1l1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⛿")][bstack1l1111l_opy_ (u"ࠩࡧࡥࡹࡧࠧ✀")] = json.dumps(str(bstack11ll111ll_opy_))
    if type == bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ✁"):
        bstack1ll1lll1l_opy_[bstack1l1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ✂")][bstack1l1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ✃")] = name
    if type == bstack1l1111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ✄"):
        bstack1ll1lll1l_opy_[bstack1l1111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ✅")][bstack1l1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ✆")] = status
        if status == bstack1l1111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ✇") and str(reason) != bstack1l1111l_opy_ (u"ࠥࠦ✈"):
            bstack1ll1lll1l_opy_[bstack1l1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ✉")][bstack1l1111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ✊")] = json.dumps(str(reason))
    bstack111l1lll1_opy_ = bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ✋").format(json.dumps(bstack1ll1lll1l_opy_))
    return bstack111l1lll1_opy_
def bstack11l1l1ll1l_opy_(url, config, logger, bstack1l1l1l11l_opy_=False):
    hostname = bstack1llll1ll1_opy_(url)
    is_private = bstack11ll11ll1l_opy_(hostname)
    try:
        if is_private or bstack1l1l1l11l_opy_:
            file_path = bstack1lllll1llll1_opy_(bstack1l1111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ✌"), bstack1l1111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ✍"), logger)
            if os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ✎")) and eval(
                    os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ✏"))):
                return
            if (bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ✐") in config and not config[bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ✑")]):
                os.environ[bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ✒")] = str(True)
                bstack1ll11ll11l1l_opy_ = {bstack1l1111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ✓"): hostname}
                bstack1lllll1l1111_opy_(bstack1l1111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ✔"), bstack1l1111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ✕"), bstack1ll11ll11l1l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11ll11lll_opy_):
    if bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ✖") in caps:
        caps[bstack1l1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ✗")][bstack1l1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ✘")] = True
        if bstack1ll11ll11lll_opy_:
            caps[bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ✙")][bstack1l1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ✚")] = bstack1ll11ll11lll_opy_
    else:
        caps[bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭✛")] = True
        if bstack1ll11ll11lll_opy_:
            caps[bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ✜")] = bstack1ll11ll11lll_opy_
def bstack1ll1l111111l_opy_(bstack1lll1l1l1ll_opy_):
    bstack1ll11ll11ll1_opy_ = bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ✝"), bstack1l1111l_opy_ (u"ࠫࠬ✞"))
    if bstack1ll11ll11ll1_opy_ == bstack1l1111l_opy_ (u"ࠬ࠭✟") or bstack1ll11ll11ll1_opy_ == bstack1l1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ✠"):
        threading.current_thread().testStatus = bstack1lll1l1l1ll_opy_
    else:
        if bstack1lll1l1l1ll_opy_ == bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ✡"):
            threading.current_thread().testStatus = bstack1lll1l1l1ll_opy_