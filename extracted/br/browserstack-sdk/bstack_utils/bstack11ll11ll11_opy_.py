# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllll1l11l1_opy_, bstack1l111l1l1l_opy_, bstack11ll1l11l_opy_, bstack111l1llll1_opy_, \
    bstack1llll1llll11_opy_
from bstack_utils.measure import measure
def bstack111l1l1l1l_opy_(bstack1ll11llll111_opy_):
    for driver in bstack1ll11llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111ll1ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
def bstack111ll1l1_opy_(driver, status, reason=bstack11ll11_opy_ (u"ࠬ࠭⚶")):
    global_config = Config.bstack111llll11_opy_()
    if global_config.bstack1ll1ll1111l_opy_():
        return
    bstack1111l11lll_opy_ = bstack1l1l1l11l_opy_(bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⚷"), bstack11ll11_opy_ (u"ࠧࠨ⚸"), status, reason, bstack11ll11_opy_ (u"ࠨࠩ⚹"), bstack11ll11_opy_ (u"ࠩࠪ⚺"))
    driver.execute_script(bstack1111l11lll_opy_)
@measure(event_name=EVENTS.bstack11111ll1ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
def bstack11l1l11lll_opy_(page, status, reason=bstack11ll11_opy_ (u"ࠪࠫ⚻")):
    try:
        if page is None:
            return
        global_config = Config.bstack111llll11_opy_()
        if global_config.bstack1ll1ll1111l_opy_():
            return
        bstack1111l11lll_opy_ = bstack1l1l1l11l_opy_(bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⚼"), bstack11ll11_opy_ (u"ࠬ࠭⚽"), status, reason, bstack11ll11_opy_ (u"࠭ࠧ⚾"), bstack11ll11_opy_ (u"ࠧࠨ⚿"))
        page.evaluate(bstack11ll11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⛀"), bstack1111l11lll_opy_)
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ⛁"), e)
def bstack1l1l1l11l_opy_(type, name, status, reason, bstack111111l11_opy_, bstack1ll11111ll_opy_):
    bstack11l1l1l1l1_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ⛂"): type,
        bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛃"): {}
    }
    if type == bstack11ll11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⛄"):
        bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⛅")][bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⛆")] = bstack111111l11_opy_
        bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⛇")][bstack11ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧ⛈")] = json.dumps(str(bstack1ll11111ll_opy_))
    if type == bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⛉"):
        bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛊")][bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⛋")] = name
    if type == bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⛌"):
        bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛍")][bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⛎")] = status
        if status == bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⛏") and str(reason) != bstack11ll11_opy_ (u"ࠥࠦ⛐"):
            bstack11l1l1l1l1_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⛑")][bstack11ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⛒")] = json.dumps(str(reason))
    bstack11l11111l_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ⛓").format(json.dumps(bstack11l1l1l1l1_opy_))
    return bstack11l11111l_opy_
def bstack111l1llll_opy_(url, config, logger, bstack1l1111lll1_opy_=False):
    hostname = bstack1l111l1l1l_opy_(url)
    is_private = bstack111l1llll1_opy_(hostname)
    try:
        if is_private or bstack1l1111lll1_opy_:
            file_path = bstack1lllll1l11l1_opy_(bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⛔"), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⛕"), logger)
            if os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⛖")) and eval(
                    os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ⛗"))):
                return
            if (bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⛘") in config and not config[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⛙")]):
                os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⛚")] = str(True)
                bstack1ll11llll11l_opy_ = {bstack11ll11_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ⛛"): hostname}
                bstack1llll1llll11_opy_(bstack11ll11_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⛜"), bstack11ll11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ⛝"), bstack1ll11llll11l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11llll1l1_opy_):
    if bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⛞") in caps:
        caps[bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⛟")][bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ⛠")] = True
        if bstack1ll11llll1l1_opy_:
            caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⛡")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⛢")] = bstack1ll11llll1l1_opy_
    else:
        caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭⛣")] = True
        if bstack1ll11llll1l1_opy_:
            caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⛤")] = bstack1ll11llll1l1_opy_
def bstack1ll1l11l1l11_opy_(bstack1lll1l1lll1_opy_):
    bstack1ll11llll1ll_opy_ = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⛥"), bstack11ll11_opy_ (u"ࠫࠬ⛦"))
    if bstack1ll11llll1ll_opy_ == bstack11ll11_opy_ (u"ࠬ࠭⛧") or bstack1ll11llll1ll_opy_ == bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⛨"):
        threading.current_thread().testStatus = bstack1lll1l1lll1_opy_
    else:
        if bstack1lll1l1lll1_opy_ == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⛩"):
            threading.current_thread().testStatus = bstack1lll1l1lll1_opy_