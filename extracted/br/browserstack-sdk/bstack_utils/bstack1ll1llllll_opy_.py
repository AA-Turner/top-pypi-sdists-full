# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from browserstack_sdk.bstack11llll11ll_opy_ import bstack1lll1l111l_opy_
from browserstack_sdk.bstack1lll1ll11l1_opy_ import RobotHandler
def bstack11l1lllll1_opy_(framework):
    if framework.lower() == bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᾎ"):
        return bstack1lll1l111l_opy_.version()
    elif framework.lower() == bstack1ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᾏ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᾐ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᾑ")
def bstack1l1lll11ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᾒ"))
        framework_version.append(importlib.metadata.version(bstack1ll11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᾓ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᾔ"))
        framework_version.append(importlib.metadata.version(bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᾕ")))
    except:
        pass
    return {
        bstack1ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᾖ"): bstack1ll11_opy_ (u"ࠩࡢࠫᾗ").join(framework_name),
        bstack1ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᾘ"): bstack1ll11_opy_ (u"ࠫࡤ࠭ᾙ").join(framework_version)
    }