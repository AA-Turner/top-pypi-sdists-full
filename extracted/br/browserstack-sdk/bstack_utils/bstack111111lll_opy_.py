# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from browserstack_sdk.bstack1lll1l11l1_opy_ import bstack1l1lllllll_opy_
from browserstack_sdk.bstack1111lll1l1_opy_ import RobotHandler
def bstack111l1l11l_opy_(framework):
    if framework.lower() == bstack11ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᪥"):
        return bstack1l1lllllll_opy_.version()
    elif framework.lower() == bstack11ll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᪦"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᪧ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll1l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ᪨")
def bstack1l1l1l1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11ll1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ᪩"))
        framework_version.append(importlib.metadata.version(bstack11ll1l1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ᪪")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᪫"))
        framework_version.append(importlib.metadata.version(bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᪬")))
    except:
        pass
    return {
        bstack11ll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᪭"): bstack11ll1l1_opy_ (u"ࠬࡥࠧ᪮").join(framework_name),
        bstack11ll1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᪯"): bstack11ll1l1_opy_ (u"ࠧࡠࠩ᪰").join(framework_version)
    }