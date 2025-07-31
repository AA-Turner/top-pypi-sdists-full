# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
from browserstack_sdk.bstack1l1lllll11_opy_ import bstack1l111l11l1_opy_
from browserstack_sdk.bstack1111ll1l11_opy_ import RobotHandler
def bstack11ll1ll1l1_opy_(framework):
    if framework.lower() == bstack1l11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫣"):
        return bstack1l111l11l1_opy_.version()
    elif framework.lower() == bstack1l11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫤"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11l11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫥"):
        import behave
        return behave.__version__
    else:
        return bstack1l11l11_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫦")
def bstack1l11l1111l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫧"))
        framework_version.append(importlib.metadata.version(bstack1l11l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫨")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11l11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫩"))
        framework_version.append(importlib.metadata.version(bstack1l11l11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫪")))
    except:
        pass
    return {
        bstack1l11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫫"): bstack1l11l11_opy_ (u"ࠫࡤ࠭᫬").join(framework_name),
        bstack1l11l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫭"): bstack1l11l11_opy_ (u"࠭࡟ࠨ᫮").join(framework_version)
    }