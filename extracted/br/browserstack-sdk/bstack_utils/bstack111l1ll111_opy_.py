# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from browserstack_sdk.bstack1ll111lll1_opy_ import bstack1l1l111l11_opy_
from browserstack_sdk.bstack11111llll1_opy_ import RobotHandler
def bstack11l1l11lll_opy_(framework):
    if framework.lower() == bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᴨ"):
        return bstack1l1l111l11_opy_.version()
    elif framework.lower() == bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᴩ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫᴪ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll111_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭ᴫ")
def bstack1ll1l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11ll111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᴬ"))
        framework_version.append(importlib.metadata.version(bstack11ll111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᴭ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᴮ"))
        framework_version.append(importlib.metadata.version(bstack11ll111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᴯ")))
    except:
        pass
    return {
        bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨᴰ"): bstack11ll111_opy_ (u"ࠫࡤ࠭ᴱ").join(framework_name),
        bstack11ll111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᴲ"): bstack11ll111_opy_ (u"࠭࡟ࠨᴳ").join(framework_version)
    }