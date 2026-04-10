# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llll1111lll_opy_, bstack11llllll1_opy_, bstack1llll1lll_opy_, bstack111lll1l1_opy_, \
    bstack1llllll1l1ll_opy_
from bstack_utils.measure import measure
def bstack111l1lll1_opy_(bstack1ll11lll1ll1_opy_):
    for driver in bstack1ll11lll1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l1lll_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack1l111l1l1l_opy_(driver, status, reason=bstack1ll_opy_ (u"ࠨࠩ⚹")):
    global_config = Config.bstack1l111l1111_opy_()
    if global_config.bstack1lll111llll_opy_():
        return
    bstack1lll11ll_opy_ = bstack1l1lll1lll_opy_(bstack1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⚺"), bstack1ll_opy_ (u"ࠪࠫ⚻"), status, reason, bstack1ll_opy_ (u"ࠫࠬ⚼"), bstack1ll_opy_ (u"ࠬ࠭⚽"))
    driver.execute_script(bstack1lll11ll_opy_)
@measure(event_name=EVENTS.bstack1l111l1lll_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack11lllll11l_opy_(page, status, reason=bstack1ll_opy_ (u"࠭ࠧ⚾")):
    try:
        if page is None:
            return
        global_config = Config.bstack1l111l1111_opy_()
        if global_config.bstack1lll111llll_opy_():
            return
        bstack1lll11ll_opy_ = bstack1l1lll1lll_opy_(bstack1ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ⚿"), bstack1ll_opy_ (u"ࠨࠩ⛀"), status, reason, bstack1ll_opy_ (u"ࠩࠪ⛁"), bstack1ll_opy_ (u"ࠪࠫ⛂"))
        page.evaluate(bstack1ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ⛃"), bstack1lll11ll_opy_)
    except Exception as e:
        print(bstack1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥ⛄"), e)
def bstack1l1lll1lll_opy_(type, name, status, reason, bstack1llllll1l_opy_, bstack1l1l11l111_opy_):
    bstack1l1lll11ll_opy_ = {
        bstack1ll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭⛅"): type,
        bstack1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛆"): {}
    }
    if type == bstack1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⛇"):
        bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⛈")][bstack1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⛉")] = bstack1llllll1l_opy_
        bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛊")][bstack1ll_opy_ (u"ࠬࡪࡡࡵࡣࠪ⛋")] = json.dumps(str(bstack1l1l11l111_opy_))
    if type == bstack1ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⛌"):
        bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛍")][bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⛎")] = name
    if type == bstack1ll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⛏"):
        bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⛐")][bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⛑")] = status
        if status == bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⛒") and str(reason) != bstack1ll_opy_ (u"ࠨࠢ⛓"):
            bstack1l1lll11ll_opy_[bstack1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛔")][bstack1ll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⛕")] = json.dumps(str(reason))
    bstack1llll1l1l_opy_ = bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ⛖").format(json.dumps(bstack1l1lll11ll_opy_))
    return bstack1llll1l1l_opy_
def bstack1ll1l1llll_opy_(url, config, logger, bstack1l1ll1lll1_opy_=False):
    hostname = bstack11llllll1_opy_(url)
    is_private = bstack111lll1l1_opy_(hostname)
    try:
        if is_private or bstack1l1ll1lll1_opy_:
            file_path = bstack1llll1111lll_opy_(bstack1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⛗"), bstack1ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⛘"), logger)
            if os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⛙")) and eval(
                    os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⛚"))):
                return
            if (bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⛛") in config and not config[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⛜")]):
                os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⛝")] = str(True)
                bstack1ll11lll1l1l_opy_ = {bstack1ll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ⛞"): hostname}
                bstack1llllll1l1ll_opy_(bstack1ll_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⛟"), bstack1ll_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ⛠"), bstack1ll11lll1l1l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11lll11ll_opy_):
    if bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⛡") in caps:
        caps[bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⛢")][bstack1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ⛣")] = True
        if bstack1ll11lll11ll_opy_:
            caps[bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⛤")][bstack1ll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⛥")] = bstack1ll11lll11ll_opy_
    else:
        caps[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ⛦")] = True
        if bstack1ll11lll11ll_opy_:
            caps[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⛧")] = bstack1ll11lll11ll_opy_
def bstack1ll1l11l111l_opy_(bstack1lll1ll111l_opy_):
    bstack1ll11lll1l11_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ⛨"), bstack1ll_opy_ (u"ࠧࠨ⛩"))
    if bstack1ll11lll1l11_opy_ == bstack1ll_opy_ (u"ࠨࠩ⛪") or bstack1ll11lll1l11_opy_ == bstack1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⛫"):
        threading.current_thread().testStatus = bstack1lll1ll111l_opy_
    else:
        if bstack1lll1ll111l_opy_ == bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⛬"):
            threading.current_thread().testStatus = bstack1lll1ll111l_opy_