# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
from browserstack_sdk.bstack11llllll1l_opy_ import bstack1llll1111_opy_
from browserstack_sdk.bstack1llll1l1ll1_opy_ import RobotHandler
def bstack11l1llll11_opy_(framework):
    if framework.lower() == bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭὜"):
        return bstack1llll1111_opy_.version()
    elif framework.lower() == bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭Ὕ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1lll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ὞"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1lll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪὟ")
def bstack1l1l1l11l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬὠ"))
        framework_version.append(importlib.metadata.version(bstack1ll1lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨὡ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩὢ"))
        framework_version.append(importlib.metadata.version(bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥὣ")))
    except:
        pass
    return {
        bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬὤ"): bstack1ll1lll_opy_ (u"ࠨࡡࠪὥ").join(framework_name),
        bstack1ll1lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪὦ"): bstack1ll1lll_opy_ (u"ࠪࡣࠬὧ").join(framework_version)
    }