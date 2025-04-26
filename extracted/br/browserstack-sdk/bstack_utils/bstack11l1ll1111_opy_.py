# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from browserstack_sdk.bstack1ll1lll11l_opy_ import bstack1ll11l11ll_opy_
from browserstack_sdk.bstack111ll11lll_opy_ import RobotHandler
def bstack1l1ll11l1_opy_(framework):
    if framework.lower() == bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᦛ"):
        return bstack1ll11l11ll_opy_.version()
    elif framework.lower() == bstack1l11lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᦜ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11lll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᦝ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11lll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᦞ")
def bstack11l1ll11l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᦟ"))
        framework_version.append(importlib.metadata.version(bstack1l11lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᦠ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᦡ"))
        framework_version.append(importlib.metadata.version(bstack1l11lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᦢ")))
    except:
        pass
    return {
        bstack1l11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᦣ"): bstack1l11lll_opy_ (u"ࠬࡥࠧᦤ").join(framework_name),
        bstack1l11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᦥ"): bstack1l11lll_opy_ (u"ࠧࡠࠩᦦ").join(framework_version)
    }