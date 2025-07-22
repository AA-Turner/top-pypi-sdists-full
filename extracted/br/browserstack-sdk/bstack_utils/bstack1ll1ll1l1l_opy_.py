# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from browserstack_sdk.bstack1l1ll11ll_opy_ import bstack1l1l11l111_opy_
from browserstack_sdk.bstack111l1ll1ll_opy_ import RobotHandler
def bstack1l1111l1l1_opy_(framework):
    if framework.lower() == bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᫢"):
        return bstack1l1l11l111_opy_.version()
    elif framework.lower() == bstack111l111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ᫣"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ᫤"):
        import behave
        return behave.__version__
    else:
        return bstack111l111_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬ᫥")
def bstack11l11l1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111l111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ᫦"))
        framework_version.append(importlib.metadata.version(bstack111l111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ᫧")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ᫨"))
        framework_version.append(importlib.metadata.version(bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ᫩")))
    except:
        pass
    return {
        bstack111l111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᫪"): bstack111l111_opy_ (u"ࠪࡣࠬ᫫").join(framework_name),
        bstack111l111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᫬"): bstack111l111_opy_ (u"ࠬࡥࠧ᫭").join(framework_version)
    }