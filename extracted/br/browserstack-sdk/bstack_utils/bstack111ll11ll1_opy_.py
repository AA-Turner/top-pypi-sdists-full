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
from browserstack_sdk.bstack1111ll111_opy_ import bstack1l11111l_opy_
from browserstack_sdk.bstack1lll1llllll_opy_ import RobotHandler
def bstack1llllllll_opy_(framework):
    if framework.lower() == bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫώ"):
        return bstack1l11111l_opy_.version()
    elif framework.lower() == bstack1ll1lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ὾"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭὿"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1lll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᾀ")
def bstack111ll1l11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᾁ"))
        framework_version.append(importlib.metadata.version(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᾂ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᾃ"))
        framework_version.append(importlib.metadata.version(bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᾄ")))
    except:
        pass
    return {
        bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᾅ"): bstack1ll1lll_opy_ (u"࠭࡟ࠨᾆ").join(framework_name),
        bstack1ll1lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᾇ"): bstack1ll1lll_opy_ (u"ࠨࡡࠪᾈ").join(framework_version)
    }