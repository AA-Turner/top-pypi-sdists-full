# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from browserstack_sdk.bstack11l1lll1l_opy_ import bstack1ll11l1ll1_opy_
from browserstack_sdk.bstack111ll1l111_opy_ import RobotHandler
def bstack1111l1l1_opy_(framework):
    if framework.lower() == bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᦢ"):
        return bstack1ll11l1ll1_opy_.version()
    elif framework.lower() == bstack1l1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᦣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᦤ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1lll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᦥ")
def bstack1l111l1lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᦦ"))
        framework_version.append(importlib.metadata.version(bstack1l1lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᦧ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᦨ"))
        framework_version.append(importlib.metadata.version(bstack1l1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᦩ")))
    except:
        pass
    return {
        bstack1l1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᦪ"): bstack1l1lll_opy_ (u"ࠬࡥࠧᦫ").join(framework_name),
        bstack1l1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᦬"): bstack1l1lll_opy_ (u"ࠧࡠࠩ᦭").join(framework_version)
    }