# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from browserstack_sdk.bstack1l11ll1111_opy_ import bstack11l111l11l_opy_
from browserstack_sdk.bstack1111l1111l_opy_ import RobotHandler
def bstack11l1ll11l1_opy_(framework):
    if framework.lower() == bstack11l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᰵ"):
        return bstack11l111l11l_opy_.version()
    elif framework.lower() == bstack11l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᰶ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1ll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ᰷࠭"):
        import behave
        return behave.__version__
    else:
        return bstack11l1ll1_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨ᰸")
def bstack11111l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1ll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ᰹"))
        framework_version.append(importlib.metadata.version(bstack11l1ll1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᰺")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ᰻"))
        framework_version.append(importlib.metadata.version(bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᰼")))
    except:
        pass
    return {
        bstack11l1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᰽"): bstack11l1ll1_opy_ (u"࠭࡟ࠨ᰾").join(framework_name),
        bstack11l1ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᰿"): bstack11l1ll1_opy_ (u"ࠨࡡࠪ᱀").join(framework_version)
    }