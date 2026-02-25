# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111l111ll11_opy_, bstack11l1l111ll_opy_, bstack11llll11l1_opy_, bstack1111l1l1_opy_, \
    bstack1111lllllll_opy_
from bstack_utils.measure import measure
def bstack1llll1l1_opy_(bstack1lll1l111111_opy_):
    for driver in bstack1lll1l111111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1111l1l11_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack11lll1l11l_opy_(driver, status, reason=bstack11l1l11_opy_ (u"ࠨࠩ≵")):
    global_config = Config.get_instance()
    if global_config.should_skip_session_status():
        return
    executor_string = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ≶"), bstack11l1l11_opy_ (u"ࠪࠫ≷"), status, reason, bstack11l1l11_opy_ (u"ࠫࠬ≸"), bstack11l1l11_opy_ (u"ࠬ࠭≹"))
    driver.execute_script(executor_string)
@measure(event_name=EVENTS.bstack1111l1l11_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1l111l11l1_opy_(page, status, reason=bstack11l1l11_opy_ (u"࠭ࠧ≺")):
    try:
        if page is None:
            return
        global_config = Config.get_instance()
        if global_config.should_skip_session_status():
            return
        executor_string = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ≻"), bstack11l1l11_opy_ (u"ࠨࠩ≼"), status, reason, bstack11l1l11_opy_ (u"ࠩࠪ≽"), bstack11l1l11_opy_ (u"ࠪࠫ≾"))
        page.evaluate(bstack11l1l11_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ≿"), executor_string)
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥ⊀"), e)
def browserstack_executor_helper(type, name, status, reason, bstack1ll1llll_opy_, bstack1lll11l1_opy_):
    bstack1l1lll1l1_opy_ = {
        bstack11l1l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭⊁"): type,
        bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⊂"): {}
    }
    if type == bstack11l1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⊃"):
        bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ⊄")][bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⊅")] = bstack1ll1llll_opy_
        bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⊆")][bstack11l1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪ⊇")] = json.dumps(str(bstack1lll11l1_opy_))
    if type == bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⊈"):
        bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⊉")][bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⊊")] = name
    if type == bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⊋"):
        bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭⊌")][bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⊍")] = status
        if status == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⊎") and str(reason) != bstack11l1l11_opy_ (u"ࠨࠢ⊏"):
            bstack1l1lll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ⊐")][bstack11l1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⊑")] = json.dumps(str(reason))
    bstack11l11lll1_opy_ = bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ⊒").format(json.dumps(bstack1l1lll1l1_opy_))
    return bstack11l11lll1_opy_
def bstack11llll1ll1_opy_(url, config, logger, bstack1ll1l1lll1_opy_=False):
    hostname = bstack11l1l111ll_opy_(url)
    is_private = bstack1111l1l1_opy_(hostname)
    try:
        if is_private or bstack1ll1l1lll1_opy_:
            file_path = bstack111l111ll11_opy_(bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⊓"), bstack11l1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⊔"), logger)
            if os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪ⊕")) and eval(
                    os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫ⊖"))):
                return
            if (bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⊗") in config and not config[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⊘")]):
                os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧ⊙")] = str(True)
                bstack1lll11llll1l_opy_ = {bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ⊚"): hostname}
                bstack1111lllllll_opy_(bstack11l1l11_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ⊛"), bstack11l1l11_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪ⊜"), bstack1lll11llll1l_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l11111l_opy_(caps, bstack1lll11lllll1_opy_):
    if bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⊝") in caps:
        caps[bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ⊞")][bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧ⊟")] = True
        if bstack1lll11lllll1_opy_:
            caps[bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⊠")][bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⊡")] = bstack1lll11lllll1_opy_
    else:
        caps[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩ⊢")] = True
        if bstack1lll11lllll1_opy_:
            caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⊣")] = bstack1lll11lllll1_opy_
def bstack1lll1l1ll11l_opy_(bstack1111111l1l_opy_):
    bstack1lll11llllll_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ⊤"), bstack11l1l11_opy_ (u"ࠧࠨ⊥"))
    if bstack1lll11llllll_opy_ == bstack11l1l11_opy_ (u"ࠨࠩ⊦") or bstack1lll11llllll_opy_ == bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⊧"):
        threading.current_thread().testStatus = bstack1111111l1l_opy_
    else:
        if bstack1111111l1l_opy_ == bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⊨"):
            threading.current_thread().testStatus = bstack1111111l1l_opy_