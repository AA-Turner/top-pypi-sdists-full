# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111lll1l11_opy_, bstack11l111l11_opy_, bstack1lll11lll1_opy_, bstack11l11llll_opy_, \
    bstack1111ll11lll_opy_
from bstack_utils.measure import measure
def bstack111lll1l11_opy_(bstack1lll111lll11_opy_):
    for driver in bstack1lll111lll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack1l1lllll1l_opy_(driver, status, reason=bstack1111_opy_ (u"ࠪࠫ⎝")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⎞"), bstack1111_opy_ (u"ࠬ࠭⎟"), status, reason, bstack1111_opy_ (u"࠭ࠧ⎠"), bstack1111_opy_ (u"ࠧࠨ⎡"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11ll1ll11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
def bstack11lllll111_opy_(page, status, reason=bstack1111_opy_ (u"ࠨࠩ⎢")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⎣"), bstack1111_opy_ (u"ࠪࠫ⎤"), status, reason, bstack1111_opy_ (u"ࠫࠬ⎥"), bstack1111_opy_ (u"ࠬ࠭⎦"))
        page.evaluate(bstack1111_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⎧"), executor_string)
    except Exception as e:
        print(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧ⎨"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1l1l11l11_opy_, bstack1l11l1111l_opy_):
    bstack1111ll1l1_opy_ = {
        bstack1111_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ⎩"): type,
        bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⎪"): {}
    }
    if type == bstack1111_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⎫"):
        bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⎬")][bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⎭")] = bstack1l1l11l11_opy_
        bstack1111ll1l1_opy_[bstack1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⎮")][bstack1111_opy_ (u"ࠧࡥࡣࡷࡥࠬ⎯")] = json.dumps(str(bstack1l11l1111l_opy_))
    if type == bstack1111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⎰"):
        bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⎱")][bstack1111_opy_ (u"ࠪࡲࡦࡳࡥࠨ⎲")] = name
    if type == bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⎳"):
        bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ⎴")][bstack1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⎵")] = status
        if status == bstack1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⎶") and str(reason) != bstack1111_opy_ (u"ࠣࠤ⎷"):
            bstack1111ll1l1_opy_[bstack1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⎸")][bstack1111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ⎹")] = json.dumps(str(reason))
    bstack1l1ll1ll1_opy_ = bstack1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ⎺").format(json.dumps(bstack1111ll1l1_opy_))
    return bstack1l1ll1ll1_opy_
def bstack1l11l1l1ll_opy_(url, config, logger, bstack11lllll1l_opy_=False):
    hostname = bstack11l111l11_opy_(url)
    is_private = bstack11l11llll_opy_(hostname)
    try:
        if is_private or bstack11lllll1l_opy_:
            file_path = bstack1111lll1l11_opy_(bstack1111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⎻"), bstack1111_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⎼"), logger)
            if os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬ⎽")) and eval(
                    os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭⎾"))):
                return
            if (bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⎿") in config and not config[bstack1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⏀")]):
                os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ⏁")] = str(True)
                bstack1lll111llll1_opy_ = {bstack1111_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ⏂"): hostname}
                bstack1111ll11lll_opy_(bstack1111_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ⏃"), bstack1111_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬ⏄"), bstack1lll111llll1_opy_, logger)
    except Exception as e:
        pass
def bstack11ll11l11_opy_(caps, bstack1lll111lll1l_opy_):
    if bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⏅") in caps:
        caps[bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⏆")][bstack1111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩ⏇")] = True
        if bstack1lll111lll1l_opy_:
            caps[bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⏈")][bstack1111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⏉")] = bstack1lll111lll1l_opy_
    else:
        caps[bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫ⏊")] = True
        if bstack1lll111lll1l_opy_:
            caps[bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⏋")] = bstack1lll111lll1l_opy_
def bstack1lll11lllll1_opy_(bstack1lllllll1l1_opy_):
    bstack1lll111lllll_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ⏌"), bstack1111_opy_ (u"ࠩࠪ⏍"))
    if bstack1lll111lllll_opy_ == bstack1111_opy_ (u"ࠪࠫ⏎") or bstack1lll111lllll_opy_ == bstack1111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⏏"):
        threading.current_thread().testStatus = bstack1lllllll1l1_opy_
    else:
        if bstack1lllllll1l1_opy_ == bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⏐"):
            threading.current_thread().testStatus = bstack1lllllll1l1_opy_