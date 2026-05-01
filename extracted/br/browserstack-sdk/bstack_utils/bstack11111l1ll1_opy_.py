# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llll1llll1l_opy_, bstack111ll11ll_opy_, bstack1ll11l1ll1_opy_, bstack11llll11_opy_, \
    bstack1lllll11111l_opy_
from bstack_utils.measure import measure
def bstack1l111111ll_opy_(bstack1ll11ll1111l_opy_):
    for driver in bstack1ll11ll1111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1lll1lll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack11ll1l1l1_opy_(driver, status, reason=bstack111ll_opy_ (u"ࠩࠪ✸")):
    global_config = Config.bstack1l1l11ll1_opy_()
    if global_config.bstack1ll1ll1lll1_opy_():
        return
    bstack1l11l1l111_opy_ = bstack111ll111l_opy_(bstack111ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭✹"), bstack111ll_opy_ (u"ࠫࠬ✺"), status, reason, bstack111ll_opy_ (u"ࠬ࠭✻"), bstack111ll_opy_ (u"࠭ࠧ✼"))
    driver.execute_script(bstack1l11l1l111_opy_)
@measure(event_name=EVENTS.bstack1l1lll1lll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
def bstack1lllll111_opy_(page, status, reason=bstack111ll_opy_ (u"ࠧࠨ✽")):
    try:
        if page is None:
            return
        global_config = Config.bstack1l1l11ll1_opy_()
        if global_config.bstack1ll1ll1lll1_opy_():
            return
        bstack1l11l1l111_opy_ = bstack111ll111l_opy_(bstack111ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ✾"), bstack111ll_opy_ (u"ࠩࠪ✿"), status, reason, bstack111ll_opy_ (u"ࠪࠫ❀"), bstack111ll_opy_ (u"ࠫࠬ❁"))
        page.evaluate(bstack111ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ❂"), bstack1l11l1l111_opy_)
    except Exception as e:
        print(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦ❃"), e)
def bstack111ll111l_opy_(type, name, status, reason, bstack111l1l11ll_opy_, bstack1111111l1_opy_):
    bstack1l1lll1ll1_opy_ = {
        bstack111ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ❄"): type,
        bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ❅"): {}
    }
    if type == bstack111ll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ❆"):
        bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭❇")][bstack111ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ❈")] = bstack111l1l11ll_opy_
        bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ❉")][bstack111ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ❊")] = json.dumps(str(bstack1111111l1_opy_))
    if type == bstack111ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ❋"):
        bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ❌")][bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ❍")] = name
    if type == bstack111ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭❎"):
        bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ❏")][bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ❐")] = status
        if status == bstack111ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭❑") and str(reason) != bstack111ll_opy_ (u"ࠢࠣ❒"):
            bstack1l1lll1ll1_opy_[bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ❓")][bstack111ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ❔")] = json.dumps(str(reason))
    bstack111ll1llll_opy_ = bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ❕").format(json.dumps(bstack1l1lll1ll1_opy_))
    return bstack111ll1llll_opy_
def bstack1ll1l11l11_opy_(url, config, logger, bstack11l1l1ll1l_opy_=False):
    hostname = bstack111ll11ll_opy_(url)
    is_private = bstack11llll11_opy_(hostname)
    try:
        if is_private or bstack11l1l1ll1l_opy_:
            file_path = bstack1llll1llll1l_opy_(bstack111ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ❖"), bstack111ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ❗"), logger)
            if os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ❘")) and eval(
                    os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ❙"))):
                return
            if (bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ❚") in config and not config[bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭❛")]):
                os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ❜")] = str(True)
                bstack1ll11ll111l1_opy_ = {bstack111ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭❝"): hostname}
                bstack1lllll11111l_opy_(bstack111ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ❞"), bstack111ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ❟"), bstack1ll11ll111l1_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11ll11l11_opy_):
    if bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ❠") in caps:
        caps[bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ❡")][bstack111ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ❢")] = True
        if bstack1ll11ll11l11_opy_:
            caps[bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ❣")][bstack111ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭❤")] = bstack1ll11ll11l11_opy_
    else:
        caps[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ❥")] = True
        if bstack1ll11ll11l11_opy_:
            caps[bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ❦")] = bstack1ll11ll11l11_opy_
def bstack1ll11lllll1l_opy_(bstack1lll1l1l111_opy_):
    bstack1ll11ll111ll_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ❧"), bstack111ll_opy_ (u"ࠨࠩ❨"))
    if bstack1ll11ll111ll_opy_ == bstack111ll_opy_ (u"ࠩࠪ❩") or bstack1ll11ll111ll_opy_ == bstack111ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ❪"):
        threading.current_thread().testStatus = bstack1lll1l1l111_opy_
    else:
        if bstack1lll1l1l111_opy_ == bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ❫"):
            threading.current_thread().testStatus = bstack1lll1l1l111_opy_