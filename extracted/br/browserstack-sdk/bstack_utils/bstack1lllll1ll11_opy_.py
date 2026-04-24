# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
from browserstack_sdk.bstack111ll11l_opy_ import bstack1ll1l1lll1_opy_
from browserstack_sdk.bstack1lll11ll1ll_opy_ import RobotHandler
def bstack1ll11l111_opy_(framework):
    if framework.lower() == bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩↁ"):
        return bstack1ll1l1lll1_opy_.version()
    elif framework.lower() == bstack111ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩↂ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫↃ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack111ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ↄ"):
        import sys
        return bstack111ll11_opy_ (u"ࠨࡻࡾ࠰ࡾࢁ࠳ࢁࡽࠣↅ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack111ll11_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨↆ")
def bstack11l1lll11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111ll11_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪↇ"))
        framework_version.append(importlib.metadata.version(bstack111ll11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦↈ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ↉"))
        framework_version.append(importlib.metadata.version(bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ↊")))
    except:
        pass
    return {
        bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ↋"): bstack111ll11_opy_ (u"࠭࡟ࠨ↌").join(framework_name),
        bstack111ll11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ↍"): bstack111ll11_opy_ (u"ࠨࡡࠪ↎").join(framework_version)
    }