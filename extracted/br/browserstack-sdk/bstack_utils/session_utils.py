# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111ll11l11_opy_, bstack111l1lll1_opy_, bstack111ll1ll_opy_, bstack1l11ll1ll1_opy_, \
    bstack11111ll111l_opy_
from bstack_utils.measure import measure
def bstack1111l111l1_opy_(bstack1ll1llll111l_opy_):
    for driver in bstack1ll1llll111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1llll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack11111l11_opy_(driver, status, reason=bstack11lll1_opy_ (u"ࠪࠫ⒧")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack11lll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⒨"), bstack11lll1_opy_ (u"ࠬ࠭⒩"), status, reason, bstack11lll1_opy_ (u"࠭ࠧ⒪"), bstack11lll1_opy_ (u"ࠧࠨ⒫"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11l1llll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
def bstack1ll11ll1ll_opy_(page, status, reason=bstack11lll1_opy_ (u"ࠨࠩ⒬")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack11lll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⒭"), bstack11lll1_opy_ (u"ࠪࠫ⒮"), status, reason, bstack11lll1_opy_ (u"ࠫࠬ⒯"), bstack11lll1_opy_ (u"ࠬ࠭⒰"))
        page.evaluate(bstack11lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⒱"), executor_string)
    except Exception as e:
        print(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ⒲"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1l111111ll_opy_, bstack1ll111ll_opy_):
    bstack11l1ll111l_opy_ = {
        bstack11lll1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ⒳"): type,
        bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⒴"): {}
    }
    if type == bstack11lll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⒵"):
        bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧⒶ")][bstack11lll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫⒷ")] = bstack1l111111ll_opy_
        bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⒸ")][bstack11lll1_opy_ (u"ࠧࡥࡣࡷࡥࠬⒹ")] = json.dumps(str(bstack1ll111ll_opy_))
    if type == bstack11lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩⒺ"):
        bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬⒻ")][bstack11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨⒼ")] = name
    if type == bstack11lll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧⒽ"):
        bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨⒾ")][bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ⓙ")] = status
        if status == bstack11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧⓀ") and str(reason) != bstack11lll1_opy_ (u"ࠣࠤⓁ"):
            bstack11l1ll111l_opy_[bstack11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬⓂ")][bstack11lll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪⓃ")] = json.dumps(str(reason))
    bstack1l1ll11l_opy_ = bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩⓄ").format(json.dumps(bstack11l1ll111l_opy_))
    return bstack1l1ll11l_opy_
def bstack11lll1l1_opy_(url, config, logger, bstack1ll1l1ll11_opy_=False):
    hostname = bstack111l1lll1_opy_(url)
    is_private = bstack1l11ll1ll1_opy_(hostname)
    try:
        if is_private or bstack1ll1l1ll11_opy_:
            file_path = bstack1111ll11l11_opy_(bstack11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬⓅ"), bstack11lll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬⓆ"), logger)
            if os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬⓇ")) and eval(
                    os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭Ⓢ"))):
                return
            if (bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ⓣ") in config and not config[bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧⓊ")]):
                os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩⓋ")] = str(True)
                bstack1ll1lll1lll1_opy_ = {bstack11lll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧⓌ"): hostname}
                bstack11111ll111l_opy_(bstack11lll1_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬⓍ"), bstack11lll1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬⓎ"), bstack1ll1lll1lll1_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1llll1111_opy_):
    if bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩⓏ") in caps:
        caps[bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪⓐ")][bstack11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩⓑ")] = True
        if bstack1ll1llll1111_opy_:
            caps[bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬⓒ")][bstack11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧⓓ")] = bstack1ll1llll1111_opy_
    else:
        caps[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫⓔ")] = True
        if bstack1ll1llll1111_opy_:
            caps[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨⓕ")] = bstack1ll1llll1111_opy_
def bstack1lll1111ll1l_opy_(bstack1lllll1111l_opy_):
    bstack1ll1lll1llll_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬⓖ"), bstack11lll1_opy_ (u"ࠩࠪⓗ"))
    if bstack1ll1lll1llll_opy_ == bstack11lll1_opy_ (u"ࠪࠫⓘ") or bstack1ll1lll1llll_opy_ == bstack11lll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬⓙ"):
        threading.current_thread().testStatus = bstack1lllll1111l_opy_
    else:
        if bstack1lllll1111l_opy_ == bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬⓚ"):
            threading.current_thread().testStatus = bstack1lllll1111l_opy_