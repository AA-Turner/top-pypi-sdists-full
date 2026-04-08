# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from browserstack_sdk.bstack1l1l1lllll_opy_ import bstack111l111ll_opy_
from browserstack_sdk.bstack1lll1l1llll_opy_ import RobotHandler
def bstack111111l1l1_opy_(framework):
    if framework.lower() == bstack111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⅟"):
        return bstack111l111ll_opy_.version()
    elif framework.lower() == bstack111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪⅠ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬⅡ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧⅢ"):
        import sys
        return bstack111l_opy_ (u"ࠢࡼࡿ࠱ࡿࢂ࠴ࡻࡾࠤⅣ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack111l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩⅤ")
def bstack1l111l11l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫⅥ"))
        framework_version.append(importlib.metadata.version(bstack111l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧⅦ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨⅧ"))
        framework_version.append(importlib.metadata.version(bstack111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤⅨ")))
    except:
        pass
    return {
        bstack111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⅩ"): bstack111l_opy_ (u"ࠧࡠࠩⅪ").join(framework_name),
        bstack111l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩⅫ"): bstack111l_opy_ (u"ࠩࡢࠫⅬ").join(framework_version)
    }