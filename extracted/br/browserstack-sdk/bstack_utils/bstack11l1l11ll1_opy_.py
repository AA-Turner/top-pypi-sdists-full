# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from browserstack_sdk.bstack1l1llll11_opy_ import bstack11lll111l1_opy_
from browserstack_sdk.bstack1111lll11l_opy_ import RobotHandler
def bstack11l1ll11l1_opy_(framework):
    if framework.lower() == bstack11l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᮛ"):
        return bstack11lll111l1_opy_.version()
    elif framework.lower() == bstack11l1111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᮜ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᮝ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1111_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᮞ")
def bstack11ll11lll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᮟ"))
        framework_version.append(importlib.metadata.version(bstack11l1111_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᮠ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᮡ"))
        framework_version.append(importlib.metadata.version(bstack11l1111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᮢ")))
    except:
        pass
    return {
        bstack11l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᮣ"): bstack11l1111_opy_ (u"࠭࡟ࠨᮤ").join(framework_name),
        bstack11l1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮥ"): bstack11l1111_opy_ (u"ࠨࡡࠪᮦ").join(framework_version)
    }