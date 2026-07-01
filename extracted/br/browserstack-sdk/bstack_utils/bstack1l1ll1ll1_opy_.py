# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllll1111l1_opy_, bstack11l1ll1l11_opy_, bstack11llll11_opy_, bstack1lllll11ll1_opy_, \
    bstack1llll1l1l1l1_opy_
from bstack_utils.measure import measure
def bstack1111l1111l_opy_(bstack1ll111111l1l_opy_):
    for driver in bstack1ll111111l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111llll111_opy_, stage=STAGE.SINGLE)
def bstack1l1lll1ll1l_opy_(driver, status, reason=bstack1l1llll_opy_ (u"ࠧࠨ⪯")):
    global_config = Config.bstack1lll1l11_opy_()
    if global_config.bstack11l11l1l_opy_():
        return
    bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⪰"), bstack1l1llll_opy_ (u"ࠩࠪ⪱"), status, reason, bstack1l1llll_opy_ (u"ࠪࠫ⪲"), bstack1l1llll_opy_ (u"ࠫࠬ⪳"))
    driver.execute_script(bstack1l1lll11l_opy_)
@measure(event_name=EVENTS.bstack111llll111_opy_, stage=STAGE.SINGLE)
def bstack1lll1111l1l_opy_(page, status, reason=bstack1l1llll_opy_ (u"ࠬ࠭⪴")):
    try:
        if page is None:
            return
        global_config = Config.bstack1lll1l11_opy_()
        if global_config.bstack11l11l1l_opy_():
            return
        bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⪵"), bstack1l1llll_opy_ (u"ࠧࠨ⪶"), status, reason, bstack1l1llll_opy_ (u"ࠨࠩ⪷"), bstack1l1llll_opy_ (u"ࠩࠪ⪸"))
        page.evaluate(bstack1l1llll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⪹"), bstack1l1lll11l_opy_)
    except Exception as e:
        print(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤ⪺"), e)
def bstack1lll111ll_opy_(type, name, status, reason, bstack11l1l11l_opy_, bstack1l11ll11_opy_):
    bstack11111ll1l1_opy_ = {
        bstack1l1llll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ⪻"): type,
        bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⪼"): {}
    }
    if type == bstack1l1llll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ⪽"):
        bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⪾")][bstack1l1llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⪿")] = bstack11l1l11l_opy_
        bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⫀")][bstack1l1llll_opy_ (u"ࠫࡩࡧࡴࡢࠩ⫁")] = json.dumps(str(bstack1l11ll11_opy_))
    if type == bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⫂"):
        bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⫃")][bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⫄")] = name
    if type == bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⫅"):
        bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⫆")][bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⫇")] = status
        if status == bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⫈") and str(reason) != bstack1l1llll_opy_ (u"ࠧࠨ⫉"):
            bstack11111ll1l1_opy_[bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⫊")][bstack1l1llll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ⫋")] = json.dumps(str(reason))
    bstack1lll111111_opy_ = bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭⫌").format(json.dumps(bstack11111ll1l1_opy_))
    return bstack1lll111111_opy_
def bstack1l1l1llll1l_opy_(url, config, logger, bstack1lll1l1l11_opy_=False):
    hostname = bstack11l1ll1l11_opy_(url)
    is_private = bstack1lllll11ll1_opy_(hostname)
    try:
        if is_private or bstack1lll1l1l11_opy_:
            file_path = bstack1lllll1111l1_opy_(bstack1l1llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⫍"), bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ⫎"), logger)
            if os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ⫏")) and eval(
                    os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⫐"))):
                return
            if (bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⫑") in config and not config[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⫒")]):
                os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭⫓")] = str(True)
                bstack1ll1111111ll_opy_ = {bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ⫔"): hostname}
                bstack1llll1l1l1l1_opy_(bstack1l1llll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ⫕"), bstack1l1llll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ⫖"), bstack1ll1111111ll_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1111111l1_opy_):
    if bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⫗") in caps:
        caps[bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⫘")][bstack1l1llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭⫙")] = True
        if bstack1ll1111111l1_opy_:
            caps[bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⫚")][bstack1l1llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⫛")] = bstack1ll1111111l1_opy_
    else:
        caps[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ⫝̸")] = True
        if bstack1ll1111111l1_opy_:
            caps[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⫝")] = bstack1ll1111111l1_opy_
def bstack1ll111ll111l_opy_(bstack1111llll_opy_):
    bstack1ll111111l11_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⫞"), bstack1l1llll_opy_ (u"࠭ࠧ⫟"))
    if bstack1ll111111l11_opy_ == bstack1l1llll_opy_ (u"ࠧࠨ⫠") or bstack1ll111111l11_opy_ == bstack1l1llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⫡"):
        threading.current_thread().testStatus = bstack1111llll_opy_
    else:
        if bstack1111llll_opy_ == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⫢"):
            threading.current_thread().testStatus = bstack1111llll_opy_