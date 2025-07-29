# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from browserstack_sdk.bstack11l11l111_opy_ import bstack11lll111l_opy_
from browserstack_sdk.bstack111l1l11l1_opy_ import RobotHandler
def bstack1ll1lll1ll_opy_(framework):
    if framework.lower() == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᫣"):
        return bstack11lll111l_opy_.version()
    elif framework.lower() == bstackl_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ᫤"):
        return RobotHandler.version()
    elif framework.lower() == bstackl_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ᫥"):
        import behave
        return behave.__version__
    else:
        return bstackl_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭᫦")
def bstack11l11llll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstackl_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᫧"))
        framework_version.append(importlib.metadata.version(bstackl_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᫨")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstackl_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᫩"))
        framework_version.append(importlib.metadata.version(bstackl_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᫪")))
    except:
        pass
    return {
        bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨ᫫"): bstackl_opy_ (u"ࠫࡤ࠭᫬").join(framework_name),
        bstackl_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭᫭"): bstackl_opy_ (u"࠭࡟ࠨ᫮").join(framework_version)
    }