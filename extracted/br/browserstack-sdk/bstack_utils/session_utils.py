# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111111l111l_opy_, bstack1l11111l1l_opy_, bstack1l11lll1_opy_, bstack1l111lllll_opy_, \
    bstack1111l11llll_opy_
from bstack_utils.measure import measure
def bstack11l1l111l_opy_(bstack1ll1lll111ll_opy_):
    for driver in bstack1ll1lll111ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l111l111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1ll1lll1l_opy_(driver, status, reason=bstack1ll1lll_opy_ (u"ࠧࠨⓎ")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫⓏ"), bstack1ll1lll_opy_ (u"ࠩࠪⓐ"), status, reason, bstack1ll1lll_opy_ (u"ࠪࠫⓑ"), bstack1ll1lll_opy_ (u"ࠫࠬⓒ"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack11l111l111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
def bstack1ll1l1lll1_opy_(page, status, reason=bstack1ll1lll_opy_ (u"ࠬ࠭ⓓ")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩⓔ"), bstack1ll1lll_opy_ (u"ࠧࠨⓕ"), status, reason, bstack1ll1lll_opy_ (u"ࠨࠩⓖ"), bstack1ll1lll_opy_ (u"ࠩࠪⓗ"))
        page.evaluate(bstack1ll1lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦⓘ"), executor_string)
    except Exception as e:
        print(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤⓙ"), e)
def browserstack_executor_helper(type, name, status, reason, bstack11l111l1l1_opy_, bstack111llll111_opy_):
    bstack1ll1lll111_opy_ = {
        bstack1ll1lll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬⓚ"): type,
        bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⓛ"): {}
    }
    if type == bstack1ll1lll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩⓜ"):
        bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫⓝ")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨⓞ")] = bstack11l111l1l1_opy_
        bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ⓟ")][bstack1ll1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩⓠ")] = json.dumps(str(bstack111llll111_opy_))
    if type == bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⓡ"):
        bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⓢ")][bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⓣ")] = name
    if type == bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫⓤ"):
        bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬⓥ")][bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪⓦ")] = status
        if status == bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫⓧ") and str(reason) != bstack1ll1lll_opy_ (u"ࠧࠨⓨ"):
            bstack1ll1lll111_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩⓩ")][bstack1ll1lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ⓪")] = json.dumps(str(reason))
    bstack11l111llll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭⓫").format(json.dumps(bstack1ll1lll111_opy_))
    return bstack11l111llll_opy_
def bstack11l1ll1111_opy_(url, config, logger, bstack11l1lllll1_opy_=False):
    hostname = bstack1l11111l1l_opy_(url)
    is_private = bstack1l111lllll_opy_(hostname)
    try:
        if is_private or bstack11l1lllll1_opy_:
            file_path = bstack111111l111l_opy_(bstack1ll1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⓬"), bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ⓭"), logger)
            if os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩ⓮")) and eval(
                    os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⓯"))):
                return
            if (bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⓰") in config and not config[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⓱")]):
                os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭⓲")] = str(True)
                bstack1ll1lll11l1l_opy_ = {bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ⓳"): hostname}
                bstack1111l11llll_opy_(bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩ⓴"), bstack1ll1lll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩ⓵"), bstack1ll1lll11l1l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1ll1lll11l11_opy_):
    if bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⓶") in caps:
        caps[bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⓷")][bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭⓸")] = True
        if bstack1ll1lll11l11_opy_:
            caps[bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⓹")][bstack1ll1lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⓺")] = bstack1ll1lll11l11_opy_
    else:
        caps[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ⓻")] = True
        if bstack1ll1lll11l11_opy_:
            caps[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⓼")] = bstack1ll1lll11l11_opy_
def bstack1lll111111l1_opy_(bstack1llll111l11_opy_):
    bstack1ll1lll111l1_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⓽"), bstack1ll1lll_opy_ (u"࠭ࠧ⓾"))
    if bstack1ll1lll111l1_opy_ == bstack1ll1lll_opy_ (u"ࠧࠨ⓿") or bstack1ll1lll111l1_opy_ == bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ─"):
        threading.current_thread().testStatus = bstack1llll111l11_opy_
    else:
        if bstack1llll111l11_opy_ == bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ━"):
            threading.current_thread().testStatus = bstack1llll111l11_opy_