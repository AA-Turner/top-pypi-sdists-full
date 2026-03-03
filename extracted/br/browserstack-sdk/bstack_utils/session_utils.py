# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l1l1lll1_opy_, bstack1lllll1111_opy_, bstack1lll11l111_opy_, bstack11lll1111l_opy_, \
    bstack1111lll1ll1_opy_
from bstack_utils.measure import measure
def bstack1l11l11lll_opy_(bstack1lll11llll1l_opy_):
    for driver in bstack1lll11llll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack1l11l1ll11_opy_(driver, status, reason=bstack11ll111_opy_ (u"ࠬ࠭≲")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ≳"), bstack11ll111_opy_ (u"ࠧࠨ≴"), status, reason, bstack11ll111_opy_ (u"ࠨࠩ≵"), bstack11ll111_opy_ (u"ࠩࠪ≶"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack111l1l1lll_opy_(page, status, reason=bstack11ll111_opy_ (u"ࠪࠫ≷")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ≸"), bstack11ll111_opy_ (u"ࠬ࠭≹"), status, reason, bstack11ll111_opy_ (u"࠭ࠧ≺"), bstack11ll111_opy_ (u"ࠧࠨ≻"))
        page.evaluate(bstack11ll111_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ≼"), executor_string)
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢ≽"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1l11l1llll_opy_, bstack11111l11_opy_):
    bstack1ll11lll11_opy_ = {
        bstack11ll111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ≾"): type,
        bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ≿"): {}
    }
    if type == bstack11ll111_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⊀"):
        bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ⊁")][bstack11ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⊂")] = bstack1l11l1llll_opy_
        bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ⊃")][bstack11ll111_opy_ (u"ࠩࡧࡥࡹࡧࠧ⊄")] = json.dumps(str(bstack11111l11_opy_))
    if type == bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⊅"):
        bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⊆")][bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⊇")] = name
    if type == bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⊈"):
        bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⊉")][bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⊊")] = status
        if status == bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⊋") and str(reason) != bstack11ll111_opy_ (u"ࠥࠦ⊌"):
            bstack1ll11lll11_opy_[bstack11ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⊍")][bstack11ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⊎")] = json.dumps(str(reason))
    bstack11ll1l1l_opy_ = bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ⊏").format(json.dumps(bstack1ll11lll11_opy_))
    return bstack11ll1l1l_opy_
def bstack111l11l111_opy_(url, config, logger, bstack11ll111l1l_opy_=False):
    hostname = bstack1lllll1111_opy_(url)
    is_private = bstack11lll1111l_opy_(hostname)
    try:
        if is_private or bstack11ll111l1l_opy_:
            file_path = bstack111l1l1lll1_opy_(bstack11ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⊐"), bstack11ll111_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⊑"), logger)
            if os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⊒")) and eval(
                    os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨ⊓"))):
                return
            if (bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⊔") in config and not config[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⊕")]):
                os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⊖")] = str(True)
                bstack1lll11llllll_opy_ = {bstack11ll111_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ⊗"): hostname}
                bstack1111lll1ll1_opy_(bstack11ll111_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧ⊘"), bstack11ll111_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ⊙"), bstack1lll11llllll_opy_, logger)
    except Exception as e:
        pass
def bstack1l1111l1l_opy_(caps, bstack1lll11llll11_opy_):
    if bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⊚") in caps:
        caps[bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ⊛")][bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ⊜")] = True
        if bstack1lll11llll11_opy_:
            caps[bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⊝")][bstack11ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⊞")] = bstack1lll11llll11_opy_
    else:
        caps[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭⊟")] = True
        if bstack1lll11llll11_opy_:
            caps[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⊠")] = bstack1lll11llll11_opy_
def bstack1lll1ll11l1l_opy_(bstack111111lll1_opy_):
    bstack1lll11lllll1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⊡"), bstack11ll111_opy_ (u"ࠫࠬ⊢"))
    if bstack1lll11lllll1_opy_ == bstack11ll111_opy_ (u"ࠬ࠭⊣") or bstack1lll11lllll1_opy_ == bstack11ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⊤"):
        threading.current_thread().testStatus = bstack111111lll1_opy_
    else:
        if bstack111111lll1_opy_ == bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⊥"):
            threading.current_thread().testStatus = bstack111111lll1_opy_