# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111ll111l1_opy_, bstack1ll1l1111_opy_, bstack111l1lll11_opy_, bstack1ll1l1l11_opy_, \
    bstack1111l1ll11l_opy_
from bstack_utils.measure import measure
def bstack111ll1l11l_opy_(bstack1ll1lll1lll1_opy_):
    for driver in bstack1ll1lll1lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1111lll1l1_opy_(driver, status, reason=bstack1ll1lll_opy_ (u"ࠩࠪ⒭")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⒮"), bstack1ll1lll_opy_ (u"ࠫࠬ⒯"), status, reason, bstack1ll1lll_opy_ (u"ࠬ࠭⒰"), bstack1ll1lll_opy_ (u"࠭ࠧ⒱"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11l1ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack11ll11ll11_opy_(page, status, reason=bstack1ll1lll_opy_ (u"ࠧࠨ⒲")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⒳"), bstack1ll1lll_opy_ (u"ࠩࠪ⒴"), status, reason, bstack1ll1lll_opy_ (u"ࠪࠫ⒵"), bstack1ll1lll_opy_ (u"ࠫࠬⒶ"))
        page.evaluate(bstack1ll1lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨⒷ"), executor_string)
    except Exception as e:
        print(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦⒸ"), e)
def browserstack_executor_helper(type, name, status, reason, bstack11l1lll1l1_opy_, bstack1l11l1ll_opy_):
    bstack111ll1ll1l_opy_ = {
        bstack1ll1lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧⒹ"): type,
        bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫⒺ"): {}
    }
    if type == bstack1ll1lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫⒻ"):
        bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ⓖ")][bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪⒽ")] = bstack11l1lll1l1_opy_
        bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨⒾ")][bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫⒿ")] = json.dumps(str(bstack1l11l1ll_opy_))
    if type == bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨⓀ"):
        bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫⓁ")][bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧⓂ")] = name
    if type == bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ⓝ"):
        bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧⓄ")][bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⓅ")] = status
        if status == bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ⓠ") and str(reason) != bstack1ll1lll_opy_ (u"ࠢࠣⓇ"):
            bstack111ll1ll1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫⓈ")][bstack1ll1lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩⓉ")] = json.dumps(str(reason))
    bstack111ll111_opy_ = bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨⓊ").format(json.dumps(bstack111ll1ll1l_opy_))
    return bstack111ll111_opy_
def bstack11l11ll11_opy_(url, config, logger, bstack1l1111l1ll_opy_=False):
    hostname = bstack1ll1l1111_opy_(url)
    is_private = bstack1ll1l1l11_opy_(hostname)
    try:
        if is_private or bstack1l1111l1ll_opy_:
            file_path = bstack1111ll111l1_opy_(bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫⓋ"), bstack1ll1lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫⓌ"), logger)
            if os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫⓍ")) and eval(
                    os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬⓎ"))):
                return
            if (bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬⓏ") in config and not config[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ⓐ")]):
                os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨⓑ")] = str(True)
                bstack1ll1lll1ll11_opy_ = {bstack1ll1lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ⓒ"): hostname}
                bstack1111l1ll11l_opy_(bstack1ll1lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫⓓ"), bstack1ll1lll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫⓔ"), bstack1ll1lll1ll11_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1lll1ll1l_opy_):
    if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨⓕ") in caps:
        caps[bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩⓖ")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨⓗ")] = True
        if bstack1ll1lll1ll1l_opy_:
            caps[bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫⓘ")][bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ⓙ")] = bstack1ll1lll1ll1l_opy_
    else:
        caps[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪⓚ")] = True
        if bstack1ll1lll1ll1l_opy_:
            caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧⓛ")] = bstack1ll1lll1ll1l_opy_
def bstack1lll1111llll_opy_(bstack1llll11l11l_opy_):
    bstack1ll1lll1l1ll_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫⓜ"), bstack1ll1lll_opy_ (u"ࠨࠩⓝ"))
    if bstack1ll1lll1l1ll_opy_ == bstack1ll1lll_opy_ (u"ࠩࠪⓞ") or bstack1ll1lll1l1ll_opy_ == bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫⓟ"):
        threading.current_thread().testStatus = bstack1llll11l11l_opy_
    else:
        if bstack1llll11l11l_opy_ == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫⓠ"):
            threading.current_thread().testStatus = bstack1llll11l11l_opy_