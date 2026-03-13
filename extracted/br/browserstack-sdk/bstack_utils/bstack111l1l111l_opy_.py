# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from browserstack_sdk.bstack1ll11l1ll_opy_ import bstack11l11llll1_opy_
from browserstack_sdk.bstack1llllll1l11_opy_ import RobotHandler
def bstack1lll11111l_opy_(framework):
    if framework.lower() == bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩἋ"):
        return bstack11l11llll1_opy_.version()
    elif framework.lower() == bstack1111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩἌ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫἍ"):
        import behave
        return behave.__version__
    else:
        return bstack1111l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭Ἆ")
def bstack1111l1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨἏ"))
        framework_version.append(importlib.metadata.version(bstack1111l_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤἐ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬἑ"))
        framework_version.append(importlib.metadata.version(bstack1111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨἒ")))
    except:
        pass
    return {
        bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨἓ"): bstack1111l_opy_ (u"ࠫࡤ࠭ἔ").join(framework_name),
        bstack1111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ἕ"): bstack1111l_opy_ (u"࠭࡟ࠨ἖").join(framework_version)
    }