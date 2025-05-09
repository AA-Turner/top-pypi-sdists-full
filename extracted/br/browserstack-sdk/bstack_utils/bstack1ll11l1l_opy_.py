# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from browserstack_sdk.bstack1l1l1ll1ll_opy_ import bstack1ll11l11_opy_
from browserstack_sdk.bstack111l1lll11_opy_ import RobotHandler
def bstack111111ll_opy_(framework):
    if framework.lower() == bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᦢ"):
        return bstack1ll11l11_opy_.version()
    elif framework.lower() == bstack11lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᦣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᦤ"):
        import behave
        return behave.__version__
    else:
        return bstack11lll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᦥ")
def bstack1l1l1111l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᦦ"))
        framework_version.append(importlib.metadata.version(bstack11lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᦧ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᦨ"))
        framework_version.append(importlib.metadata.version(bstack11lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᦩ")))
    except:
        pass
    return {
        bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᦪ"): bstack11lll_opy_ (u"ࠬࡥࠧᦫ").join(framework_name),
        bstack11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᦬"): bstack11lll_opy_ (u"ࠧࡠࠩ᦭").join(framework_version)
    }