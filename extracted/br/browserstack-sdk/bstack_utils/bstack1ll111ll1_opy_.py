# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from browserstack_sdk.bstack1111l11ll_opy_ import bstack11111ll1l_opy_
from browserstack_sdk.bstack111l11l1l1_opy_ import RobotHandler
def bstack1l1ll1l1ll_opy_(framework):
    if framework.lower() == bstack1l1l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫱"):
        return bstack11111ll1l_opy_.version()
    elif framework.lower() == bstack1l1l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫲"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫳"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1ll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫴")
def bstack1ll1l111l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1l1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫵"))
        framework_version.append(importlib.metadata.version(bstack1l1l1ll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫶")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫷"))
        framework_version.append(importlib.metadata.version(bstack1l1l1ll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫸")))
    except:
        pass
    return {
        bstack1l1l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫹"): bstack1l1l1ll_opy_ (u"ࠫࡤ࠭᫺").join(framework_name),
        bstack1l1l1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫻"): bstack1l1l1ll_opy_ (u"࠭࡟ࠨ᫼").join(framework_version)
    }