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
from browserstack_sdk.bstack1ll1lll11_opy_ import bstack11111111_opy_
from browserstack_sdk.bstack11111ll1ll_opy_ import RobotHandler
def bstack1l11ll1l1_opy_(framework):
    if framework.lower() == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᴫ"):
        return bstack11111111_opy_.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᴬ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᴭ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1l11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᴮ")
def bstack1l11l111l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᴯ"))
        framework_version.append(importlib.metadata.version(bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᴰ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᴱ"))
        framework_version.append(importlib.metadata.version(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᴲ")))
    except:
        pass
    return {
        bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᴳ"): bstack11l1l11_opy_ (u"ࠧࡠࠩᴴ").join(framework_name),
        bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᴵ"): bstack11l1l11_opy_ (u"ࠩࡢࠫᴶ").join(framework_version)
    }