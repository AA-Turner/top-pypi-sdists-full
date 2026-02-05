# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l1lll111_opy_, bstack11l1lll1_opy_, bstack111ll1l1_opy_, bstack1ll1l111_opy_, \
    bstack111l11l1l11_opy_
from bstack_utils.measure import measure
def bstack111l1l11_opy_(bstack1lll1ll11ll1_opy_):
    for driver in bstack1lll1ll11ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
def bstack1lllll1l1_opy_(driver, status, reason=bstack11l1ll1_opy_ (u"࠭ࠧⅾ")):
    bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
    if bstack11lll111l_opy_.bstack1lllll1l1ll_opy_():
        return
    bstack1lll11ll11_opy_ = bstack1111l11l_opy_(bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪⅿ"), bstack11l1ll1_opy_ (u"ࠨࠩↀ"), status, reason, bstack11l1ll1_opy_ (u"ࠩࠪↁ"), bstack11l1ll1_opy_ (u"ࠪࠫↂ"))
    driver.execute_script(bstack1lll11ll11_opy_)
@measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
def bstack11111l11l_opy_(page, status, reason=bstack11l1ll1_opy_ (u"ࠫࠬↃ")):
    try:
        if page is None:
            return
        bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
        if bstack11lll111l_opy_.bstack1lllll1l1ll_opy_():
            return
        bstack1lll11ll11_opy_ = bstack1111l11l_opy_(bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨↄ"), bstack11l1ll1_opy_ (u"࠭ࠧↅ"), status, reason, bstack11l1ll1_opy_ (u"ࠧࠨↆ"), bstack11l1ll1_opy_ (u"ࠨࠩↇ"))
        page.evaluate(bstack11l1ll1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥↈ"), bstack1lll11ll11_opy_)
    except Exception as e:
        print(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣ↉"), e)
def bstack1111l11l_opy_(type, name, status, reason, bstack1l11l1ll1l_opy_, bstack11ll1l1l11_opy_):
    bstack1l1111lll1_opy_ = {
        bstack11l1ll1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ↊"): type,
        bstack11l1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ↋"): {}
    }
    if type == bstack11l1ll1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ↌"):
        bstack1l1111lll1_opy_[bstack11l1ll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ↍")][bstack11l1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ↎")] = bstack1l11l1ll1l_opy_
        bstack1l1111lll1_opy_[bstack11l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ↏")][bstack11l1ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨ←")] = json.dumps(str(bstack11ll1l1l11_opy_))
    if type == bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ↑"):
        bstack1l1111lll1_opy_[bstack11l1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ→")][bstack11l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ↓")] = name
    if type == bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ↔"):
        bstack1l1111lll1_opy_[bstack11l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ↕")][bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ↖")] = status
        if status == bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ↗") and str(reason) != bstack11l1ll1_opy_ (u"ࠦࠧ↘"):
            bstack1l1111lll1_opy_[bstack11l1ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ↙")][bstack11l1ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭↚")] = json.dumps(str(reason))
    bstack111ll11111_opy_ = bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ↛").format(json.dumps(bstack1l1111lll1_opy_))
    return bstack111ll11111_opy_
def bstack11llll11ll_opy_(url, config, logger, bstack111l1ll11_opy_=False):
    hostname = bstack11l1lll1_opy_(url)
    is_private = bstack1ll1l111_opy_(hostname)
    try:
        if is_private or bstack111l1ll11_opy_:
            file_path = bstack111l1lll111_opy_(bstack11l1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ↜"), bstack11l1ll1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ↝"), logger)
            if os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ↞")) and eval(
                    os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ↟"))):
                return
            if (bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ↠") in config and not config[bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ↡")]):
                os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ↢")] = str(True)
                bstack1lll1ll11l1l_opy_ = {bstack11l1ll1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪ↣"): hostname}
                bstack111l11l1l11_opy_(bstack11l1ll1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ↤"), bstack11l1ll1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨ↥"), bstack1lll1ll11l1l_opy_, logger)
    except Exception as e:
        pass
def bstack11lll1l1_opy_(caps, bstack1lll1ll11lll_opy_):
    if bstack11l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ↦") in caps:
        caps[bstack11l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭↧")][bstack11l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ↨")] = True
        if bstack1lll1ll11lll_opy_:
            caps[bstack11l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ↩")][bstack11l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ↪")] = bstack1lll1ll11lll_opy_
    else:
        caps[bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ↫")] = True
        if bstack1lll1ll11lll_opy_:
            caps[bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ↬")] = bstack1lll1ll11lll_opy_
def bstack1llll111ll1l_opy_(bstack11111l1ll1_opy_):
    bstack1lll1ll1l111_opy_ = bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ↭"), bstack11l1ll1_opy_ (u"ࠬ࠭↮"))
    if bstack1lll1ll1l111_opy_ == bstack11l1ll1_opy_ (u"࠭ࠧ↯") or bstack1lll1ll1l111_opy_ == bstack11l1ll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ↰"):
        threading.current_thread().testStatus = bstack11111l1ll1_opy_
    else:
        if bstack11111l1ll1_opy_ == bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ↱"):
            threading.current_thread().testStatus = bstack11111l1ll1_opy_