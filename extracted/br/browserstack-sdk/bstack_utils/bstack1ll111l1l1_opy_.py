# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111l11llll_opy_, bstack11ll1lll11_opy_, bstack11ll11l11_opy_, bstack1ll11lll_opy_, \
    bstack1111llll11l_opy_
from bstack_utils.measure import measure
def bstack11ll1l1l11_opy_(bstack1lll11l1lll1_opy_):
    for driver in bstack1lll11l1lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1ll1l1l1_opy_(driver, status, reason=bstack11l11_opy_ (u"ࠫࠬ≪")):
    bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
    if bstack11l1l1111_opy_.bstack1llll11l11l_opy_():
        return
    bstack11111lll1_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ≫"), bstack11l11_opy_ (u"࠭ࠧ≬"), status, reason, bstack11l11_opy_ (u"ࠧࠨ≭"), bstack11l11_opy_ (u"ࠨࠩ≮"))
    driver.execute_script(bstack11111lll1_opy_)
@measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1l11lll11l_opy_(page, status, reason=bstack11l11_opy_ (u"ࠩࠪ≯")):
    try:
        if page is None:
            return
        bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
        if bstack11l1l1111_opy_.bstack1llll11l11l_opy_():
            return
        bstack11111lll1_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭≰"), bstack11l11_opy_ (u"ࠫࠬ≱"), status, reason, bstack11l11_opy_ (u"ࠬ࠭≲"), bstack11l11_opy_ (u"࠭ࠧ≳"))
        page.evaluate(bstack11l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ≴"), bstack11111lll1_opy_)
    except Exception as e:
        print(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨ≵"), e)
def bstack1lll1l1l1l_opy_(type, name, status, reason, bstack111lll1ll_opy_, bstack1l11lll1l_opy_):
    bstack1lll1l11_opy_ = {
        bstack11l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ≶"): type,
        bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭≷"): {}
    }
    if type == bstack11l11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭≸"):
        bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ≹")][bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ≺")] = bstack111lll1ll_opy_
        bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ≻")][bstack11l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭≼")] = json.dumps(str(bstack1l11lll1l_opy_))
    if type == bstack11l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ≽"):
        bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭≾")][bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ≿")] = name
    if type == bstack11l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ⊀"):
        bstack1lll1l11_opy_[bstack11l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⊁")][bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⊂")] = status
        if status == bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⊃") and str(reason) != bstack11l11_opy_ (u"ࠤࠥ⊄"):
            bstack1lll1l11_opy_[bstack11l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⊅")][bstack11l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ⊆")] = json.dumps(str(reason))
    bstack1l1l111111_opy_ = bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ⊇").format(json.dumps(bstack1lll1l11_opy_))
    return bstack1l1l111111_opy_
def bstack1ll111ll1_opy_(url, config, logger, bstack1llllll11_opy_=False):
    hostname = bstack11ll1lll11_opy_(url)
    is_private = bstack1ll11lll_opy_(hostname)
    try:
        if is_private or bstack1llllll11_opy_:
            file_path = bstack1111l11llll_opy_(bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⊈"), bstack11l11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭⊉"), logger)
            if os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭⊊")) and eval(
                    os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⊋"))):
                return
            if (bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⊌") in config and not config[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⊍")]):
                os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⊎")] = str(True)
                bstack1lll11l1ll11_opy_ = {bstack11l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ⊏"): hostname}
                bstack1111llll11l_opy_(bstack11l11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭⊐"), bstack11l11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭⊑"), bstack1lll11l1ll11_opy_, logger)
    except Exception as e:
        pass
def bstack1l1111l111_opy_(caps, bstack1lll11l1llll_opy_):
    if bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⊒") in caps:
        caps[bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⊓")][bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ⊔")] = True
        if bstack1lll11l1llll_opy_:
            caps[bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⊕")][bstack11l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⊖")] = bstack1lll11l1llll_opy_
    else:
        caps[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ⊗")] = True
        if bstack1lll11l1llll_opy_:
            caps[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⊘")] = bstack1lll11l1llll_opy_
def bstack1lll1l1l1l11_opy_(bstack11111l1l11_opy_):
    bstack1lll11l1ll1l_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⊙"), bstack11l11_opy_ (u"ࠪࠫ⊚"))
    if bstack1lll11l1ll1l_opy_ == bstack11l11_opy_ (u"ࠫࠬ⊛") or bstack1lll11l1ll1l_opy_ == bstack11l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⊜"):
        threading.current_thread().testStatus = bstack11111l1l11_opy_
    else:
        if bstack11111l1l11_opy_ == bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⊝"):
            threading.current_thread().testStatus = bstack11111l1l11_opy_