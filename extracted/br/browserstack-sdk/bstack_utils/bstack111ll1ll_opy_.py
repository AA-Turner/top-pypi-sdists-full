# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l1l1_opy_, bstack1l1l1lll1_opy_, bstack1ll11l1l1l_opy_, bstack11111l1l1_opy_, \
    bstack11l1l111111_opy_
from bstack_utils.measure import measure
def bstack1ll1lll111_opy_(bstack1111l1111l1_opy_):
    for driver in bstack1111l1111l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1lll11l1ll_opy_(driver, status, reason=bstack111lll_opy_ (u"ࠩࠪỌ")):
    bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
    if bstack1ll1l11ll_opy_.bstack1111ll1l1l_opy_():
        return
    bstack11ll1111l1_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ọ"), bstack111lll_opy_ (u"ࠫࠬỎ"), status, reason, bstack111lll_opy_ (u"ࠬ࠭ỏ"), bstack111lll_opy_ (u"࠭ࠧỐ"))
    driver.execute_script(bstack11ll1111l1_opy_)
@measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1l1ll1ll11_opy_(page, status, reason=bstack111lll_opy_ (u"ࠧࠨố")):
    try:
        if page is None:
            return
        bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
        if bstack1ll1l11ll_opy_.bstack1111ll1l1l_opy_():
            return
        bstack11ll1111l1_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫỒ"), bstack111lll_opy_ (u"ࠩࠪồ"), status, reason, bstack111lll_opy_ (u"ࠪࠫỔ"), bstack111lll_opy_ (u"ࠫࠬổ"))
        page.evaluate(bstack111lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨỖ"), bstack11ll1111l1_opy_)
    except Exception as e:
        print(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦỗ"), e)
def bstack1lll1ll11_opy_(type, name, status, reason, bstack1llllll111_opy_, bstack1ll111lll_opy_):
    bstack1lll1lll_opy_ = {
        bstack111lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧỘ"): type,
        bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫộ"): {}
    }
    if type == bstack111lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫỚ"):
        bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ớ")][bstack111lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪỜ")] = bstack1llllll111_opy_
        bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨờ")][bstack111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫỞ")] = json.dumps(str(bstack1ll111lll_opy_))
    if type == bstack111lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨở"):
        bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫỠ")][bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧỡ")] = name
    if type == bstack111lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ợ"):
        bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧợ")][bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬỤ")] = status
        if status == bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ụ") and str(reason) != bstack111lll_opy_ (u"ࠢࠣỦ"):
            bstack1lll1lll_opy_[bstack111lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫủ")][bstack111lll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩỨ")] = json.dumps(str(reason))
    bstack11l1ll1lll_opy_ = bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨứ").format(json.dumps(bstack1lll1lll_opy_))
    return bstack11l1ll1lll_opy_
def bstack11ll111l1l_opy_(url, config, logger, bstack1l1lll111_opy_=False):
    hostname = bstack1l1l1lll1_opy_(url)
    is_private = bstack11111l1l1_opy_(hostname)
    try:
        if is_private or bstack1l1lll111_opy_:
            file_path = bstack11l1l11l1l1_opy_(bstack111lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫỪ"), bstack111lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫừ"), logger)
            if os.environ.get(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫỬ")) and eval(
                    os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬử"))):
                return
            if (bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬỮ") in config and not config[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ữ")]):
                os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨỰ")] = str(True)
                bstack11111llllll_opy_ = {bstack111lll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ự"): hostname}
                bstack11l1l111111_opy_(bstack111lll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫỲ"), bstack111lll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫỳ"), bstack11111llllll_opy_, logger)
    except Exception as e:
        pass
def bstack1lll111l1l_opy_(caps, bstack1111l111111_opy_):
    if bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨỴ") in caps:
        caps[bstack111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩỵ")][bstack111lll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨỶ")] = True
        if bstack1111l111111_opy_:
            caps[bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫỷ")][bstack111lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ỹ")] = bstack1111l111111_opy_
    else:
        caps[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪỹ")] = True
        if bstack1111l111111_opy_:
            caps[bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧỺ")] = bstack1111l111111_opy_
def bstack1111ll111ll_opy_(bstack111l1l11l1_opy_):
    bstack1111l11111l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫỻ"), bstack111lll_opy_ (u"ࠨࠩỼ"))
    if bstack1111l11111l_opy_ == bstack111lll_opy_ (u"ࠩࠪỽ") or bstack1111l11111l_opy_ == bstack111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫỾ"):
        threading.current_thread().testStatus = bstack111l1l11l1_opy_
    else:
        if bstack111l1l11l1_opy_ == bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫỿ"):
            threading.current_thread().testStatus = bstack111l1l11l1_opy_