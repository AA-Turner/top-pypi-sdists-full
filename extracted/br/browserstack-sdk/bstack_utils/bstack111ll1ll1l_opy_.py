# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from browserstack_sdk.bstack11l111ll11_opy_ import bstack111l1lll1l_opy_
from browserstack_sdk.bstack1lllll11lll_opy_ import RobotHandler
def bstack1l1111111_opy_(framework):
    if framework.lower() == bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫὡ"):
        return bstack111l1lll1l_opy_.version()
    elif framework.lower() == bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫὢ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ὣ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨὤ")
def bstack1111ll11l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪὥ"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦὦ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧὧ"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣὨ")))
    except:
        pass
    return {
        bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪὩ"): bstack1l1_opy_ (u"࠭࡟ࠨὪ").join(framework_name),
        bstack1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨὫ"): bstack1l1_opy_ (u"ࠨࡡࠪὬ").join(framework_version)
    }