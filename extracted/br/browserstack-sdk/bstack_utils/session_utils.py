# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll1111l1_opy_, bstack111l1lllll_opy_, bstack11llll11l_opy_, bstack1111ll1lll_opy_, \
    bstack11l11111ll1_opy_
from bstack_utils.measure import measure
def bstack1l1l1lll_opy_(bstack1lll1ll1lll1_opy_):
    for driver in bstack1lll1ll1lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack111lll11_opy_(driver, status, reason=bstack1ll111_opy_ (u"ࠩࠪỌ")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ọ"), bstack1ll111_opy_ (u"ࠫࠬỎ"), status, reason, bstack1ll111_opy_ (u"ࠬ࠭ỏ"), bstack1ll111_opy_ (u"࠭ࠧỐ"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack1llll1l1_opy_(page, status, reason=bstack1ll111_opy_ (u"ࠧࠨố")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫỒ"), bstack1ll111_opy_ (u"ࠩࠪồ"), status, reason, bstack1ll111_opy_ (u"ࠪࠫỔ"), bstack1ll111_opy_ (u"ࠫࠬổ"))
        page.evaluate(bstack1ll111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨỖ"), executor_string)
    except Exception as e:
        print(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦỗ"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1lll1llll_opy_, bstack1ll1l1l11_opy_):
    bstack11lll1111l_opy_ = {
        bstack1ll111_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧỘ"): type,
        bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫộ"): {}
    }
    if type == bstack1ll111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫỚ"):
        bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ớ")][bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪỜ")] = bstack1lll1llll_opy_
        bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨờ")][bstack1ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫỞ")] = json.dumps(str(bstack1ll1l1l11_opy_))
    if type == bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨở"):
        bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫỠ")][bstack1ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧỡ")] = name
    if type == bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ợ"):
        bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧợ")][bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬỤ")] = status
        if status == bstack1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ụ") and str(reason) != bstack1ll111_opy_ (u"ࠢࠣỦ"):
            bstack11lll1111l_opy_[bstack1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫủ")][bstack1ll111_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩỨ")] = json.dumps(str(reason))
    bstack111l111l11_opy_ = bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨứ").format(json.dumps(bstack11lll1111l_opy_))
    return bstack111l111l11_opy_
def bstack1l11l1llll_opy_(url, config, logger, bstack1l1l1ll1l_opy_=False):
    hostname = bstack111l1lllll_opy_(url)
    is_private = bstack1111ll1lll_opy_(hostname)
    try:
        if is_private or bstack1l1l1ll1l_opy_:
            file_path = bstack111ll1111l1_opy_(bstack1ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫỪ"), bstack1ll111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫừ"), logger)
            if os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫỬ")) and eval(
                    os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬử"))):
                return
            if (bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬỮ") in config and not config[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ữ")]):
                os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨỰ")] = str(True)
                bstack1lll1ll1l1ll_opy_ = {bstack1ll111_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ự"): hostname}
                bstack11l11111ll1_opy_(bstack1ll111_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫỲ"), bstack1ll111_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫỳ"), bstack1lll1ll1l1ll_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1lll1ll1ll1l_opy_):
    if bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨỴ") in caps:
        caps[bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩỵ")][bstack1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨỶ")] = True
        if bstack1lll1ll1ll1l_opy_:
            caps[bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫỷ")][bstack1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ỹ")] = bstack1lll1ll1ll1l_opy_
    else:
        caps[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪỹ")] = True
        if bstack1lll1ll1ll1l_opy_:
            caps[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧỺ")] = bstack1lll1ll1ll1l_opy_
def bstack1llll11l1lll_opy_(bstack1111111111_opy_):
    bstack1lll1ll1ll11_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫỻ"), bstack1ll111_opy_ (u"ࠨࠩỼ"))
    if bstack1lll1ll1ll11_opy_ == bstack1ll111_opy_ (u"ࠩࠪỽ") or bstack1lll1ll1ll11_opy_ == bstack1ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫỾ"):
        threading.current_thread().testStatus = bstack1111111111_opy_
    else:
        if bstack1111111111_opy_ == bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫỿ"):
            threading.current_thread().testStatus = bstack1111111111_opy_