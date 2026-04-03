# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llll1111lll_opy_, bstack11l1l1111_opy_, bstack11l11l1ll_opy_, bstack1l1l11111l_opy_, \
    bstack1llll1ll1l11_opy_
from bstack_utils.measure import measure
def bstack11111l11l1_opy_(bstack1ll11lllll1l_opy_):
    for driver in bstack1ll11lllll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1ll11l_opy_, stage=STAGE.bstack1ll11l11_opy_)
def bstack11l11lll1l_opy_(driver, status, reason=bstack1ll1l11_opy_ (u"ࠨࠩ⚲")):
    global_config = Config.bstack1lllllll1_opy_()
    if global_config.bstack1ll1lll1111_opy_():
        return
    bstack11111lll1_opy_ = bstack1l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⚳"), bstack1ll1l11_opy_ (u"ࠪࠫ⚴"), status, reason, bstack1ll1l11_opy_ (u"ࠫࠬ⚵"), bstack1ll1l11_opy_ (u"ࠬ࠭⚶"))
    driver.execute_script(bstack11111lll1_opy_)
@measure(event_name=EVENTS.bstack1ll1ll11l_opy_, stage=STAGE.bstack1ll11l11_opy_)
def bstack1l1ll1l111_opy_(page, status, reason=bstack1ll1l11_opy_ (u"࠭ࠧ⚷")):
    try:
        if page is None:
            return
        global_config = Config.bstack1lllllll1_opy_()
        if global_config.bstack1ll1lll1111_opy_():
            return
        bstack11111lll1_opy_ = bstack1l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ⚸"), bstack1ll1l11_opy_ (u"ࠨࠩ⚹"), status, reason, bstack1ll1l11_opy_ (u"ࠩࠪ⚺"), bstack1ll1l11_opy_ (u"ࠪࠫ⚻"))
        page.evaluate(bstack1ll1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ⚼"), bstack11111lll1_opy_)
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥ⚽"), e)
def bstack1l11ll111l_opy_(type, name, status, reason, bstack1lllll1lll1_opy_, bstack1l11l11ll1_opy_):
    bstack1ll1l1ll_opy_ = {
        bstack1ll1l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭⚾"): type,
        bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⚿"): {}
    }
    if type == bstack1ll1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⛀"):
        bstack1ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⛁")][bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⛂")] = bstack1lllll1lll1_opy_
        bstack1ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛃")][bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪ⛄")] = json.dumps(str(bstack1l11l11ll1_opy_))
    if type == bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⛅"):
        bstack1ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛆")][bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⛇")] = name
    if type == bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⛈"):
        bstack1ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⛉")][bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⛊")] = status
        if status == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⛋") and str(reason) != bstack1ll1l11_opy_ (u"ࠨࠢ⛌"):
            bstack1ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛍")][bstack1ll1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⛎")] = json.dumps(str(reason))
    bstack1111lll11_opy_ = bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ⛏").format(json.dumps(bstack1ll1l1ll_opy_))
    return bstack1111lll11_opy_
def bstack1lll1l111l_opy_(url, config, logger, bstack1l1llll11l_opy_=False):
    hostname = bstack11l1l1111_opy_(url)
    is_private = bstack1l1l11111l_opy_(hostname)
    try:
        if is_private or bstack1l1llll11l_opy_:
            file_path = bstack1llll1111lll_opy_(bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⛐"), bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⛑"), logger)
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⛒")) and eval(
                    os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⛓"))):
                return
            if (bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⛔") in config and not config[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⛕")]):
                os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⛖")] = str(True)
                bstack1ll11llllll1_opy_ = {bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ⛗"): hostname}
                bstack1llll1ll1l11_opy_(bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⛘"), bstack1ll1l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ⛙"), bstack1ll11llllll1_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11llll1ll_opy_):
    if bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⛚") in caps:
        caps[bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⛛")][bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ⛜")] = True
        if bstack1ll11llll1ll_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⛝")][bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⛞")] = bstack1ll11llll1ll_opy_
    else:
        caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ⛟")] = True
        if bstack1ll11llll1ll_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⛠")] = bstack1ll11llll1ll_opy_
def bstack1ll1l11ll1ll_opy_(bstack1lll1l1llll_opy_):
    bstack1ll11lllll11_opy_ = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ⛡"), bstack1ll1l11_opy_ (u"ࠧࠨ⛢"))
    if bstack1ll11lllll11_opy_ == bstack1ll1l11_opy_ (u"ࠨࠩ⛣") or bstack1ll11lllll11_opy_ == bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⛤"):
        threading.current_thread().testStatus = bstack1lll1l1llll_opy_
    else:
        if bstack1lll1l1llll_opy_ == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⛥"):
            threading.current_thread().testStatus = bstack1lll1l1llll_opy_