# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
from browserstack_sdk.bstack1111lll1l_opy_ import bstack11l11ll111_opy_
from browserstack_sdk.bstack111l1l11ll_opy_ import RobotHandler
def bstack1llllll11_opy_(framework):
    if framework.lower() == bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫜"):
        return bstack11l11ll111_opy_.version()
    elif framework.lower() == bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫝"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫞"):
        import behave
        return behave.__version__
    else:
        return bstack1l1_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫟")
def bstack1l11lll1l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫠"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫡")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫢"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫣")))
    except:
        pass
    return {
        bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫤"): bstack1l1_opy_ (u"ࠫࡤ࠭᫥").join(framework_name),
        bstack1l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫦"): bstack1l1_opy_ (u"࠭࡟ࠨ᫧").join(framework_version)
    }