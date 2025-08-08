# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
from browserstack_sdk.bstack11lllll11_opy_ import bstack1l1lll1l11_opy_
from browserstack_sdk.bstack1111ll1l1l_opy_ import RobotHandler
def bstack11ll1ll111_opy_(framework):
    if framework.lower() == bstack1ll1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫣"):
        return bstack1l1lll1l11_opy_.version()
    elif framework.lower() == bstack1ll1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫤"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫥"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1ll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫦")
def bstack11l1lll11l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫧"))
        framework_version.append(importlib.metadata.version(bstack1ll1ll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫨")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫩"))
        framework_version.append(importlib.metadata.version(bstack1ll1ll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫪")))
    except:
        pass
    return {
        bstack1ll1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫫"): bstack1ll1ll_opy_ (u"ࠫࡤ࠭᫬").join(framework_name),
        bstack1ll1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫭"): bstack1ll1ll_opy_ (u"࠭࡟ࠨ᫮").join(framework_version)
    }