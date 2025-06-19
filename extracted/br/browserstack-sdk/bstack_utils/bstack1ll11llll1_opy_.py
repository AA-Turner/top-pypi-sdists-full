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
from browserstack_sdk.bstack1l1l1lllll_opy_ import bstack1llll1l111_opy_
from browserstack_sdk.bstack111l11ll1l_opy_ import RobotHandler
def bstack11l111ll1l_opy_(framework):
    if framework.lower() == bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᩵"):
        return bstack1llll1l111_opy_.version()
    elif framework.lower() == bstack111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᩶"):
        return RobotHandler.version()
    elif framework.lower() == bstack111lll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭᩷"):
        import behave
        return behave.__version__
    else:
        return bstack111lll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨ᩸")
def bstack1l11ll1lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ᩹"))
        framework_version.append(importlib.metadata.version(bstack111lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᩺")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ᩻"))
        framework_version.append(importlib.metadata.version(bstack111lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᩼")))
    except:
        pass
    return {
        bstack111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᩽"): bstack111lll_opy_ (u"࠭࡟ࠨ᩾").join(framework_name),
        bstack111lll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᩿"): bstack111lll_opy_ (u"ࠨࡡࠪ᪀").join(framework_version)
    }