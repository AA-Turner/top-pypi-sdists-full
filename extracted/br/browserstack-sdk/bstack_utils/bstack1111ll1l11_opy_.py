# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from browserstack_sdk.bstack111lll1l_opy_ import bstack1l1l1ll1l_opy_
from browserstack_sdk.bstack1lll1ll1lll_opy_ import RobotHandler
def bstack1l111l1111_opy_(framework):
    if framework.lower() == bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫↃ"):
        return bstack1l1l1ll1l_opy_.version()
    elif framework.lower() == bstack1l1111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫↄ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ↅ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack1l1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨↆ"):
        import sys
        return bstack1l1111l_opy_ (u"ࠣࡽࢀ࠲ࢀࢃ࠮ࡼࡿࠥↇ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack1l1111l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪↈ")
def bstack11ll1l11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ↉"))
        framework_version.append(importlib.metadata.version(bstack1l1111l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨ↊")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ↋"))
        framework_version.append(importlib.metadata.version(bstack1l1111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ↌")))
    except:
        pass
    return {
        bstack1l1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ↍"): bstack1l1111l_opy_ (u"ࠨࡡࠪ↎").join(framework_name),
        bstack1l1111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ↏"): bstack1l1111l_opy_ (u"ࠪࡣࠬ←").join(framework_version)
    }