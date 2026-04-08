# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llllllll1ll_opy_, bstack11l1l111ll_opy_, bstack1llll11111_opy_, bstack1ll1lll1_opy_, \
    bstack1lllllll1l1l_opy_
from bstack_utils.measure import measure
def bstack1l111l1l1_opy_(bstack1ll11llll11l_opy_):
    for driver in bstack1ll11llll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llllll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
def bstack11ll1l11ll_opy_(driver, status, reason=bstack111l_opy_ (u"ࠫࠬ⚵")):
    global_config = Config.bstack1lll111ll_opy_()
    if global_config.bstack1ll1l1l1l11_opy_():
        return
    bstack111l1l111_opy_ = bstack1111llll1l_opy_(bstack111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ⚶"), bstack111l_opy_ (u"࠭ࠧ⚷"), status, reason, bstack111l_opy_ (u"ࠧࠨ⚸"), bstack111l_opy_ (u"ࠨࠩ⚹"))
    driver.execute_script(bstack111l1l111_opy_)
@measure(event_name=EVENTS.bstack11llllll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
def bstack111ll111l_opy_(page, status, reason=bstack111l_opy_ (u"ࠩࠪ⚺")):
    try:
        if page is None:
            return
        global_config = Config.bstack1lll111ll_opy_()
        if global_config.bstack1ll1l1l1l11_opy_():
            return
        bstack111l1l111_opy_ = bstack1111llll1l_opy_(bstack111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⚻"), bstack111l_opy_ (u"ࠫࠬ⚼"), status, reason, bstack111l_opy_ (u"ࠬ࠭⚽"), bstack111l_opy_ (u"࠭ࠧ⚾"))
        page.evaluate(bstack111l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ⚿"), bstack111l1l111_opy_)
    except Exception as e:
        print(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨ⛀"), e)
def bstack1111llll1l_opy_(type, name, status, reason, bstack111l1ll1ll_opy_, bstack1lll1lllll_opy_):
    bstack11ll1lll_opy_ = {
        bstack111l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ⛁"): type,
        bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⛂"): {}
    }
    if type == bstack111l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭⛃"):
        bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ⛄")][bstack111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⛅")] = bstack111l1ll1ll_opy_
        bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⛆")][bstack111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭⛇")] = json.dumps(str(bstack1lll1lllll_opy_))
    if type == bstack111l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⛈"):
        bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⛉")][bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⛊")] = name
    if type == bstack111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ⛋"):
        bstack11ll1lll_opy_[bstack111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⛌")][bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⛍")] = status
        if status == bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⛎") and str(reason) != bstack111l_opy_ (u"ࠤࠥ⛏"):
            bstack11ll1lll_opy_[bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⛐")][bstack111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ⛑")] = json.dumps(str(reason))
    bstack1ll11ll11l_opy_ = bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ⛒").format(json.dumps(bstack11ll1lll_opy_))
    return bstack1ll11ll11l_opy_
def bstack1l1111l1ll_opy_(url, config, logger, bstack1l1lll1ll1_opy_=False):
    hostname = bstack11l1l111ll_opy_(url)
    is_private = bstack1ll1lll1_opy_(hostname)
    try:
        if is_private or bstack1l1lll1ll1_opy_:
            file_path = bstack1llllllll1ll_opy_(bstack111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⛓"), bstack111l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭⛔"), logger)
            if os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭⛕")) and eval(
                    os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⛖"))):
                return
            if (bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⛗") in config and not config[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⛘")]):
                os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⛙")] = str(True)
                bstack1ll11llll1ll_opy_ = {bstack111l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨ⛚"): hostname}
                bstack1lllllll1l1l_opy_(bstack111l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭⛛"), bstack111l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭⛜"), bstack1ll11llll1ll_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll11lllll11_opy_):
    if bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⛝") in caps:
        caps[bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⛞")][bstack111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ⛟")] = True
        if bstack1ll11lllll11_opy_:
            caps[bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⛠")][bstack111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⛡")] = bstack1ll11lllll11_opy_
    else:
        caps[bstack111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ⛢")] = True
        if bstack1ll11lllll11_opy_:
            caps[bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⛣")] = bstack1ll11lllll11_opy_
def bstack1ll1l11l1lll_opy_(bstack1lll11lllll_opy_):
    bstack1ll11llll1l1_opy_ = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⛤"), bstack111l_opy_ (u"ࠪࠫ⛥"))
    if bstack1ll11llll1l1_opy_ == bstack111l_opy_ (u"ࠫࠬ⛦") or bstack1ll11llll1l1_opy_ == bstack111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⛧"):
        threading.current_thread().testStatus = bstack1lll11lllll_opy_
    else:
        if bstack1lll11lllll_opy_ == bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⛨"):
            threading.current_thread().testStatus = bstack1lll11lllll_opy_