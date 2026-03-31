# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1llllllll1ll_opy_, bstack11lllll11_opy_, bstack1l1111l111_opy_, bstack1ll1l111ll_opy_, \
    bstack1llllll1llll_opy_
from bstack_utils.measure import measure
def bstack11llllll1_opy_(bstack1ll1lll11111_opy_):
    for driver in bstack1ll1lll11111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack11l11l111l_opy_(driver, status, reason=bstack1ll11_opy_ (u"ࠪࠫⓟ")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧⓠ"), bstack1ll11_opy_ (u"ࠬ࠭ⓡ"), status, reason, bstack1ll11_opy_ (u"࠭ࠧⓢ"), bstack1ll11_opy_ (u"ࠧࠨⓣ"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack11111llll_opy_)
def bstack1ll1l11lll_opy_(page, status, reason=bstack1ll11_opy_ (u"ࠨࠩⓤ")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬⓥ"), bstack1ll11_opy_ (u"ࠪࠫⓦ"), status, reason, bstack1ll11_opy_ (u"ࠫࠬⓧ"), bstack1ll11_opy_ (u"ࠬ࠭ⓨ"))
        page.evaluate(bstack1ll11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢⓩ"), executor_string)
    except Exception as e:
        print(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ⓪"), e)
def browserstack_executor_helper(type, name, status, reason, bstack11l11ll11_opy_, bstack11ll1l1l11_opy_):
    bstack1lll111111_opy_ = {
        bstack1ll11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ⓫"): type,
        bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⓬"): {}
    }
    if type == bstack1ll11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⓭"):
        bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⓮")][bstack1ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⓯")] = bstack11l11ll11_opy_
        bstack1lll111111_opy_[bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⓰")][bstack1ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬ⓱")] = json.dumps(str(bstack11ll1l1l11_opy_))
    if type == bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⓲"):
        bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⓳")][bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⓴")] = name
    if type == bstack1ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⓵"):
        bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ⓶")][bstack1ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⓷")] = status
        if status == bstack1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⓸") and str(reason) != bstack1ll11_opy_ (u"ࠣࠤ⓹"):
            bstack1lll111111_opy_[bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⓺")][bstack1ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ⓻")] = json.dumps(str(reason))
    bstack1llll11l11_opy_ = bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ⓼").format(json.dumps(bstack1lll111111_opy_))
    return bstack1llll11l11_opy_
def bstack1111ll1l1_opy_(url, config, logger, bstack1ll11l1l1l_opy_=False):
    hostname = bstack11lllll11_opy_(url)
    is_private = bstack1ll1l111ll_opy_(hostname)
    try:
        if is_private or bstack1ll11l1l1l_opy_:
            file_path = bstack1llllllll1ll_opy_(bstack1ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⓽"), bstack1ll11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⓾"), logger)
            if os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ⓿")) and eval(
                    os.environ.get(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭─"))):
                return
            if (bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭━") in config and not config[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ│")]):
                os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ┃")] = str(True)
                bstack1ll1lll111l1_opy_ = {bstack1ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ┄"): hostname}
                bstack1llllll1llll_opy_(bstack1ll11_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ┅"), bstack1ll11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ┆"), bstack1ll1lll111l1_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1lll1111l_opy_):
    if bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ┇") in caps:
        caps[bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ┈")][bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ┉")] = True
        if bstack1ll1lll1111l_opy_:
            caps[bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ┊")][bstack1ll11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ┋")] = bstack1ll1lll1111l_opy_
    else:
        caps[bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ┌")] = True
        if bstack1ll1lll1111l_opy_:
            caps[bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ┍")] = bstack1ll1lll1111l_opy_
def bstack1lll11111lll_opy_(bstack1llll1l11l1_opy_):
    bstack1ll1lll111ll_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ┎"), bstack1ll11_opy_ (u"ࠩࠪ┏"))
    if bstack1ll1lll111ll_opy_ == bstack1ll11_opy_ (u"ࠪࠫ┐") or bstack1ll1lll111ll_opy_ == bstack1ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ┑"):
        threading.current_thread().testStatus = bstack1llll1l11l1_opy_
    else:
        if bstack1llll1l11l1_opy_ == bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ┒"):
            threading.current_thread().testStatus = bstack1llll1l11l1_opy_