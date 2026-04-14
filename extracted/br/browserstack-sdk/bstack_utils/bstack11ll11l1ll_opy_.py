# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lll1llllll1_opy_, bstack1111ll111l_opy_, bstack1l111l11l_opy_, bstack1ll11lll1l_opy_, \
    bstack1llll11l11l1_opy_
from bstack_utils.measure import measure
def bstack11ll111lll_opy_(bstack1ll11lll1l11_opy_):
    for driver in bstack1ll11lll1l11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lllll1lll_opy_, stage=STAGE.bstack1l11llll1_opy_)
def bstack1llll111l_opy_(driver, status, reason=bstack1l111l_opy_ (u"ࠬ࠭⛒")):
    global_config = Config.bstack1ll11ll111_opy_()
    if global_config.bstack1lll111ll11_opy_():
        return
    bstack1l1llll1l_opy_ = bstack1ll11l11ll_opy_(bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⛓"), bstack1l111l_opy_ (u"ࠧࠨ⛔"), status, reason, bstack1l111l_opy_ (u"ࠨࠩ⛕"), bstack1l111l_opy_ (u"ࠩࠪ⛖"))
    driver.execute_script(bstack1l1llll1l_opy_)
@measure(event_name=EVENTS.bstack1lllll1lll_opy_, stage=STAGE.bstack1l11llll1_opy_)
def bstack11lll111l1_opy_(page, status, reason=bstack1l111l_opy_ (u"ࠪࠫ⛗")):
    try:
        if page is None:
            return
        global_config = Config.bstack1ll11ll111_opy_()
        if global_config.bstack1lll111ll11_opy_():
            return
        bstack1l1llll1l_opy_ = bstack1ll11l11ll_opy_(bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⛘"), bstack1l111l_opy_ (u"ࠬ࠭⛙"), status, reason, bstack1l111l_opy_ (u"࠭ࠧ⛚"), bstack1l111l_opy_ (u"ࠧࠨ⛛"))
        page.evaluate(bstack1l111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⛜"), bstack1l1llll1l_opy_)
    except Exception as e:
        print(bstack1l111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ⛝"), e)
def bstack1ll11l11ll_opy_(type, name, status, reason, bstack1l1l1lllll_opy_, bstack1llllll111_opy_):
    bstack1l11l1l1l_opy_ = {
        bstack1l111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ⛞"): type,
        bstack1l111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛟"): {}
    }
    if type == bstack1l111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⛠"):
        bstack1l11l1l1l_opy_[bstack1l111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⛡")][bstack1l111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⛢")] = bstack1l1l1lllll_opy_
        bstack1l11l1l1l_opy_[bstack1l111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⛣")][bstack1l111l_opy_ (u"ࠩࡧࡥࡹࡧࠧ⛤")] = json.dumps(str(bstack1llllll111_opy_))
    if type == bstack1l111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⛥"):
        bstack1l11l1l1l_opy_[bstack1l111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛦")][bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⛧")] = name
    if type == bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⛨"):
        bstack1l11l1l1l_opy_[bstack1l111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛩")][bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⛪")] = status
        if status == bstack1l111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⛫") and str(reason) != bstack1l111l_opy_ (u"ࠥࠦ⛬"):
            bstack1l11l1l1l_opy_[bstack1l111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛭")][bstack1l111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⛮")] = json.dumps(str(reason))
    bstack1l1l1111ll_opy_ = bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ⛯").format(json.dumps(bstack1l11l1l1l_opy_))
    return bstack1l1l1111ll_opy_
def bstack1ll1l1lll1_opy_(url, config, logger, bstack111111l11l_opy_=False):
    hostname = bstack1111ll111l_opy_(url)
    is_private = bstack1ll11lll1l_opy_(hostname)
    try:
        if is_private or bstack111111l11l_opy_:
            file_path = bstack1lll1llllll1_opy_(bstack1l111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⛰"), bstack1l111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⛱"), logger)
            if os.environ.get(bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⛲")) and eval(
                    os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ⛳"))):
                return
            if (bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⛴") in config and not config[bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⛵")]):
                os.environ[bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⛶")] = str(True)
                bstack1ll11lll111l_opy_ = {bstack1l111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ⛷"): hostname}
                bstack1llll11l11l1_opy_(bstack1l111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⛸"), bstack1l111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ⛹"), bstack1ll11lll111l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11lll11ll_opy_):
    if bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⛺") in caps:
        caps[bstack1l111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⛻")][bstack1l111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ⛼")] = True
        if bstack1ll11lll11ll_opy_:
            caps[bstack1l111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⛽")][bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⛾")] = bstack1ll11lll11ll_opy_
    else:
        caps[bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭⛿")] = True
        if bstack1ll11lll11ll_opy_:
            caps[bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ✀")] = bstack1ll11lll11ll_opy_
def bstack1ll1l111ll1l_opy_(bstack1lll1lll1ll_opy_):
    bstack1ll11lll11l1_opy_ = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ✁"), bstack1l111l_opy_ (u"ࠫࠬ✂"))
    if bstack1ll11lll11l1_opy_ == bstack1l111l_opy_ (u"ࠬ࠭✃") or bstack1ll11lll11l1_opy_ == bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ✄"):
        threading.current_thread().testStatus = bstack1lll1lll1ll_opy_
    else:
        if bstack1lll1lll1ll_opy_ == bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ✅"):
            threading.current_thread().testStatus = bstack1lll1lll1ll_opy_