# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.bstack11l11l1ll_opy_ import bstack1ll1ll1l11_opy_
from browserstack_sdk.bstack111l1ll111_opy_ import RobotHandler
def bstack1llll11l1_opy_(framework):
    if framework.lower() == bstack1111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫱"):
        return bstack1ll1ll1l11_opy_.version()
    elif framework.lower() == bstack1111lll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫲"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111lll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫳"):
        import behave
        return behave.__version__
    else:
        return bstack1111lll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫴")
def bstack11l1l111ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1111lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫵"))
        framework_version.append(importlib.metadata.version(bstack1111lll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫶")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫷"))
        framework_version.append(importlib.metadata.version(bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫸")))
    except:
        pass
    return {
        bstack1111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫹"): bstack1111lll_opy_ (u"ࠫࡤ࠭᫺").join(framework_name),
        bstack1111lll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫻"): bstack1111lll_opy_ (u"࠭࡟ࠨ᫼").join(framework_version)
    }