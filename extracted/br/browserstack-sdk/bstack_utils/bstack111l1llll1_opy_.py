# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.bstack1l1l111l_opy_ import bstack1l11l11111_opy_
from browserstack_sdk.bstack1111111l1l_opy_ import RobotHandler
def bstack1ll11l1111_opy_(framework):
    if framework.lower() == bstack1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧṓ"):
        return bstack1l11l11111_opy_.version()
    elif framework.lower() == bstack1111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧṔ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩṕ"):
        import behave
        return behave.__version__
    else:
        return bstack1111_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫṖ")
def bstack1ll11l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ṗ"))
        framework_version.append(importlib.metadata.version(bstack1111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢṘ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪṙ"))
        framework_version.append(importlib.metadata.version(bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦṚ")))
    except:
        pass
    return {
        bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ṛ"): bstack1111_opy_ (u"ࠩࡢࠫṜ").join(framework_name),
        bstack1111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫṝ"): bstack1111_opy_ (u"ࠫࡤ࠭Ṟ").join(framework_version)
    }