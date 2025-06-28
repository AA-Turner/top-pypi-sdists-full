# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from browserstack_sdk.bstack1l11l1l1ll_opy_ import bstack1llll111_opy_
from browserstack_sdk.bstack111l1l1l11_opy_ import RobotHandler
def bstack11l111l1_opy_(framework):
    if framework.lower() == bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᪥"):
        return bstack1llll111_opy_.version()
    elif framework.lower() == bstack1l1ll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᪦"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1ll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᪧ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1ll1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ᪨")
def bstack11ll1l1l11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ᪩"))
        framework_version.append(importlib.metadata.version(bstack1l1ll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ᪪")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1ll1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᪫"))
        framework_version.append(importlib.metadata.version(bstack1l1ll1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᪬")))
    except:
        pass
    return {
        bstack1l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᪭"): bstack1l1ll1_opy_ (u"ࠬࡥࠧ᪮").join(framework_name),
        bstack1l1ll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᪯"): bstack1l1ll1_opy_ (u"ࠧࡠࠩ᪰").join(framework_version)
    }