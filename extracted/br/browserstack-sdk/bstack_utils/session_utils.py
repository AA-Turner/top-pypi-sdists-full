# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11111ll1lll_opy_, bstack11l11ll1l_opy_, bstack1l11l11l11_opy_, bstack111ll1l111_opy_, \
    bstack1111l1ll111_opy_
from bstack_utils.measure import measure
def bstack11l11l1l1_opy_(bstack1lll11111lll_opy_):
    for driver in bstack1lll11111lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1ll1111l1l_opy_(driver, status, reason=bstack1111l_opy_ (u"ࠬ࠭⑜")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack1111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⑝"), bstack1111l_opy_ (u"ࠧࠨ⑞"), status, reason, bstack1111l_opy_ (u"ࠨࠩ⑟"), bstack1111l_opy_ (u"ࠩࠪ①"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack11lll111l_opy_)
def bstack1l111l11ll_opy_(page, status, reason=bstack1111l_opy_ (u"ࠪࠫ②")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ③"), bstack1111l_opy_ (u"ࠬ࠭④"), status, reason, bstack1111l_opy_ (u"࠭ࠧ⑤"), bstack1111l_opy_ (u"ࠧࠨ⑥"))
        page.evaluate(bstack1111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⑦"), executor_string)
    except Exception as e:
        print(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ⑧"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1l1l11ll_opy_, bstack1l111111ll_opy_):
    bstack111l111111_opy_ = {
        bstack1111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ⑨"): type,
        bstack1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⑩"): {}
    }
    if type == bstack1111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⑪"):
        bstack111l111111_opy_[bstack1111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⑫")][bstack1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⑬")] = bstack1l1l11ll_opy_
        bstack111l111111_opy_[bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⑭")][bstack1111l_opy_ (u"ࠩࡧࡥࡹࡧࠧ⑮")] = json.dumps(str(bstack1l111111ll_opy_))
    if type == bstack1111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⑯"):
        bstack111l111111_opy_[bstack1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⑰")][bstack1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⑱")] = name
    if type == bstack1111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⑲"):
        bstack111l111111_opy_[bstack1111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⑳")][bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⑴")] = status
        if status == bstack1111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⑵") and str(reason) != bstack1111l_opy_ (u"ࠥࠦ⑶"):
            bstack111l111111_opy_[bstack1111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⑷")][bstack1111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⑸")] = json.dumps(str(reason))
    bstack111l1l1ll_opy_ = bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ⑹").format(json.dumps(bstack111l111111_opy_))
    return bstack111l1l1ll_opy_
def bstack1l11ll111l_opy_(url, config, logger, bstack1ll11l1111_opy_=False):
    hostname = bstack11l11ll1l_opy_(url)
    is_private = bstack111ll1l111_opy_(hostname)
    try:
        if is_private or bstack1ll11l1111_opy_:
            file_path = bstack11111ll1lll_opy_(bstack1111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⑺"), bstack1111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⑻"), logger)
            if os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⑼")) and eval(
                    os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ⑽"))):
                return
            if (bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⑾") in config and not config[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⑿")]):
                os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⒀")] = str(True)
                bstack1lll1111l11l_opy_ = {bstack1111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ⒁"): hostname}
                bstack1111l1ll111_opy_(bstack1111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⒂"), bstack1111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ⒃"), bstack1lll1111l11l_opy_, logger)
    except Exception as e:
        pass
def update_caps_for_local(caps, bstack1lll1111l1l1_opy_):
    if bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⒄") in caps:
        caps[bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⒅")][bstack1111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ⒆")] = True
        if bstack1lll1111l1l1_opy_:
            caps[bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⒇")][bstack1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⒈")] = bstack1lll1111l1l1_opy_
    else:
        caps[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭⒉")] = True
        if bstack1lll1111l1l1_opy_:
            caps[bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⒊")] = bstack1lll1111l1l1_opy_
def bstack1lll11l1l111_opy_(bstack1lllllll111_opy_):
    bstack1lll1111l111_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⒋"), bstack1111l_opy_ (u"ࠫࠬ⒌"))
    if bstack1lll1111l111_opy_ == bstack1111l_opy_ (u"ࠬ࠭⒍") or bstack1lll1111l111_opy_ == bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⒎"):
        threading.current_thread().testStatus = bstack1lllllll111_opy_
    else:
        if bstack1lllllll111_opy_ == bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⒏"):
            threading.current_thread().testStatus = bstack1lllllll111_opy_