# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
from browserstack_sdk.bstack1111l1ll_opy_ import bstack1l11l1lll1_opy_
from browserstack_sdk.bstack111l11ll11_opy_ import RobotHandler
def bstack11l11l1l11_opy_(framework):
    if framework.lower() == bstack11l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᫤"):
        return bstack1l11l1lll1_opy_.version()
    elif framework.lower() == bstack11l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ᫥"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ᫦"):
        import behave
        return behave.__version__
    else:
        return bstack11l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ᫧")
def bstack1lll11l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ᫨"))
        framework_version.append(importlib.metadata.version(bstack11l1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ᫩")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᫪"))
        framework_version.append(importlib.metadata.version(bstack11l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᫫")))
    except:
        pass
    return {
        bstack11l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᫬"): bstack11l1_opy_ (u"ࠬࡥࠧ᫭").join(framework_name),
        bstack11l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ᫮"): bstack11l1_opy_ (u"ࠧࡠࠩ᫯").join(framework_version)
    }