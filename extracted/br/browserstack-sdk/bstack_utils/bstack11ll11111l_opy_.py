# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from browserstack_sdk.bstack11l1llll1l_opy_ import bstack1ll11l1lll_opy_
from browserstack_sdk.bstack1lll1lll111_opy_ import RobotHandler
def bstack1ll1ll111_opy_(framework):
    if framework.lower() == bstack1l111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫⅼ"):
        return bstack1ll11l1lll_opy_.version()
    elif framework.lower() == bstack1l111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫⅽ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ⅾ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack1l111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨⅿ"):
        import sys
        return bstack1l111l_opy_ (u"ࠣࡽࢀ࠲ࢀࢃ࠮ࡼࡿࠥↀ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack1l111l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪↁ")
def bstack1ll11l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l111l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬↂ"))
        framework_version.append(importlib.metadata.version(bstack1l111l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨↃ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩↄ"))
        framework_version.append(importlib.metadata.version(bstack1l111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥↅ")))
    except:
        pass
    return {
        bstack1l111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬↆ"): bstack1l111l_opy_ (u"ࠨࡡࠪↇ").join(framework_name),
        bstack1l111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪↈ"): bstack1l111l_opy_ (u"ࠪࡣࠬ↉").join(framework_version)
    }