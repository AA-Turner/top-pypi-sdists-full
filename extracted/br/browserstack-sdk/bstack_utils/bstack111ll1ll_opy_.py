# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from browserstack_sdk.bstack11l1111lll_opy_ import bstack1l111l1ll_opy_
from browserstack_sdk.bstack1lll1lll1l1_opy_ import RobotHandler
def bstack1l1lllll1l_opy_(framework):
    if framework.lower() == bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⅟"):
        return bstack1l111l1ll_opy_.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪⅠ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬⅡ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧⅢ"):
        import sys
        return bstack1ll1l11_opy_ (u"ࠢࡼࡿ࠱ࡿࢂ࠴ࡻࡾࠤⅣ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack1ll1l11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩⅤ")
def bstack111l1ll1l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll1l11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫⅥ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧⅦ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨⅧ"))
        framework_version.append(importlib.metadata.version(bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤⅨ")))
    except:
        pass
    return {
        bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⅩ"): bstack1ll1l11_opy_ (u"ࠧࡠࠩⅪ").join(framework_name),
        bstack1ll1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩⅫ"): bstack1ll1l11_opy_ (u"ࠩࡢࠫⅬ").join(framework_version)
    }