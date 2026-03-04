# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111l1lll11_opy_, bstack1l1lllll_opy_, bstack1lll111ll_opy_, bstack1lll1l1ll_opy_, \
    bstack11111l1l1l1_opy_
from bstack_utils.measure import measure
def bstack1l1ll111ll_opy_(bstack1lll111lllll_opy_):
    for driver in bstack1lll111lllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
def bstack111ll1l1_opy_(driver, status, reason=bstack1lll1l_opy_ (u"ࠩࠪ⎜")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⎝"), bstack1lll1l_opy_ (u"ࠫࠬ⎞"), status, reason, bstack1lll1l_opy_ (u"ࠬ࠭⎟"), bstack1lll1l_opy_ (u"࠭ࠧ⎠"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11l1l11l1l_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
def bstack111l1111l_opy_(page, status, reason=bstack1lll1l_opy_ (u"ࠧࠨ⎡")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⎢"), bstack1lll1l_opy_ (u"ࠩࠪ⎣"), status, reason, bstack1lll1l_opy_ (u"ࠪࠫ⎤"), bstack1lll1l_opy_ (u"ࠫࠬ⎥"))
        page.evaluate(bstack1lll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⎦"), executor_string)
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦ⎧"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1l1lll1l1l_opy_, bstack1l1lll1ll1_opy_):
    bstack1lllll111_opy_ = {
        bstack1lll1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ⎨"): type,
        bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⎩"): {}
    }
    if type == bstack1lll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⎪"):
        bstack1lllll111_opy_[bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⎫")][bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⎬")] = bstack1l1lll1l1l_opy_
        bstack1lllll111_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ⎭")][bstack1lll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ⎮")] = json.dumps(str(bstack1l1lll1ll1_opy_))
    if type == bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⎯"):
        bstack1lllll111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⎰")][bstack1lll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⎱")] = name
    if type == bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⎲"):
        bstack1lllll111_opy_[bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⎳")][bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⎴")] = status
        if status == bstack1lll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⎵") and str(reason) != bstack1lll1l_opy_ (u"ࠢࠣ⎶"):
            bstack1lllll111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⎷")][bstack1lll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ⎸")] = json.dumps(str(reason))
    bstack1ll1111l_opy_ = bstack1lll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ⎹").format(json.dumps(bstack1lllll111_opy_))
    return bstack1ll1111l_opy_
def bstack1l1ll111_opy_(url, config, logger, bstack1ll1lll1l1_opy_=False):
    hostname = bstack1l1lllll_opy_(url)
    is_private = bstack1lll1l1ll_opy_(hostname)
    try:
        if is_private or bstack1ll1lll1l1_opy_:
            file_path = bstack1111l1lll11_opy_(bstack1lll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⎺"), bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⎻"), logger)
            if os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⎼")) and eval(
                    os.environ.get(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ⎽"))):
                return
            if (bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⎾") in config and not config[bstack1lll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⎿")]):
                os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ⏀")] = str(True)
                bstack1lll11l11111_opy_ = {bstack1lll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭⏁"): hostname}
                bstack11111l1l1l1_opy_(bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫ⏂"), bstack1lll1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ⏃"), bstack1lll11l11111_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l1ll11_opy_(caps, bstack1lll11l1111l_opy_):
    if bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⏄") in caps:
        caps[bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⏅")][bstack1lll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ⏆")] = True
        if bstack1lll11l1111l_opy_:
            caps[bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⏇")][bstack1lll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⏈")] = bstack1lll11l1111l_opy_
    else:
        caps[bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ⏉")] = True
        if bstack1lll11l1111l_opy_:
            caps[bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⏊")] = bstack1lll11l1111l_opy_
def bstack1lll1l111l1l_opy_(bstack1lllllllll1_opy_):
    bstack1lll111llll1_opy_ = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ⏋"), bstack1lll1l_opy_ (u"ࠨࠩ⏌"))
    if bstack1lll111llll1_opy_ == bstack1lll1l_opy_ (u"ࠩࠪ⏍") or bstack1lll111llll1_opy_ == bstack1lll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⏎"):
        threading.current_thread().testStatus = bstack1lllllllll1_opy_
    else:
        if bstack1lllllllll1_opy_ == bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⏏"):
            threading.current_thread().testStatus = bstack1lllllllll1_opy_