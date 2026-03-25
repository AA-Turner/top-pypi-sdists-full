# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1lllllllllll_opy_, bstack1llll111l1_opy_, bstack1l1lll111l_opy_, bstack1l1ll1111_opy_, \
    bstack1111l1l1lll_opy_
from bstack_utils.measure import measure
def bstack11l1l1l1l_opy_(bstack1ll1lll1l1l1_opy_):
    for driver in bstack1ll1lll1l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack11l11l1l11_opy_(driver, status, reason=bstack1l1_opy_ (u"ࠧࠨ⒲")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⒳"), bstack1l1_opy_ (u"ࠩࠪ⒴"), status, reason, bstack1l1_opy_ (u"ࠪࠫ⒵"), bstack1l1_opy_ (u"ࠫࠬⒶ"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack1lll11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1ll111ll11_opy_(page, status, reason=bstack1l1_opy_ (u"ࠬ࠭Ⓑ")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩⒸ"), bstack1l1_opy_ (u"ࠧࠨⒹ"), status, reason, bstack1l1_opy_ (u"ࠨࠩⒺ"), bstack1l1_opy_ (u"ࠩࠪⒻ"))
        page.evaluate(bstack1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦⒼ"), executor_string)
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤⒽ"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1lll111l11_opy_, bstack1lll1l111_opy_):
    bstack1llll111l_opy_ = {
        bstack1l1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬⒾ"): type,
        bstack1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⒿ"): {}
    }
    if type == bstack1l1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩⓀ"):
        bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫⓁ")][bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨⓂ")] = bstack1lll111l11_opy_
        bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ⓝ")][bstack1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩⓄ")] = json.dumps(str(bstack1lll1l111_opy_))
    if type == bstack1l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ⓟ"):
        bstack1llll111l_opy_[bstack1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⓆ")][bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⓇ")] = name
    if type == bstack1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫⓈ"):
        bstack1llll111l_opy_[bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬⓉ")][bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪⓊ")] = status
        if status == bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫⓋ") and str(reason) != bstack1l1_opy_ (u"ࠧࠨⓌ"):
            bstack1llll111l_opy_[bstack1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⓍ")][bstack1l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧⓎ")] = json.dumps(str(reason))
    bstack1111llll1l_opy_ = bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭Ⓩ").format(json.dumps(bstack1llll111l_opy_))
    return bstack1111llll1l_opy_
def bstack1ll111l1_opy_(url, config, logger, bstack111ll11l1l_opy_=False):
    hostname = bstack1llll111l1_opy_(url)
    is_private = bstack1l1ll1111_opy_(hostname)
    try:
        if is_private or bstack111ll11l1l_opy_:
            file_path = bstack1lllllllllll_opy_(bstack1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩⓐ"), bstack1l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩⓑ"), logger)
            if os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩⓒ")) and eval(
                    os.environ.get(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪⓓ"))):
                return
            if (bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪⓔ") in config and not config[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫⓕ")]):
                os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ⓖ")] = str(True)
                bstack1ll1lll1ll1l_opy_ = {bstack1l1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫⓗ"): hostname}
                bstack1111l1l1lll_opy_(bstack1l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩⓘ"), bstack1l1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩⓙ"), bstack1ll1lll1ll1l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1lll1ll11_opy_):
    if bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ⓚ") in caps:
        caps[bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧⓛ")][bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ⓜ")] = True
        if bstack1ll1lll1ll11_opy_:
            caps[bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩⓝ")][bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫⓞ")] = bstack1ll1lll1ll11_opy_
    else:
        caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨⓟ")] = True
        if bstack1ll1lll1ll11_opy_:
            caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬⓠ")] = bstack1ll1lll1ll11_opy_
def bstack1lll1111ll11_opy_(bstack1lllll1l111_opy_):
    bstack1ll1lll1l1ll_opy_ = bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩⓡ"), bstack1l1_opy_ (u"࠭ࠧⓢ"))
    if bstack1ll1lll1l1ll_opy_ == bstack1l1_opy_ (u"ࠧࠨⓣ") or bstack1ll1lll1l1ll_opy_ == bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩⓤ"):
        threading.current_thread().testStatus = bstack1lllll1l111_opy_
    else:
        if bstack1lllll1l111_opy_ == bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩⓥ"):
            threading.current_thread().testStatus = bstack1lllll1l111_opy_