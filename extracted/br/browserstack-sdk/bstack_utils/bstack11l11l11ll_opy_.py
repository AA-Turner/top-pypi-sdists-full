# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
from browserstack_sdk.bstack1ll11l11ll_opy_ import bstack11l1l11ll1_opy_
from browserstack_sdk.bstack1llll11111l_opy_ import RobotHandler
def bstack11l11l111l_opy_(framework):
    if framework.lower() == bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫⅠ"):
        return bstack11l1l11ll1_opy_.version()
    elif framework.lower() == bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫⅡ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭Ⅲ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack11ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨⅣ"):
        import sys
        return bstack11ll11_opy_ (u"ࠣࡽࢀ࠲ࢀࢃ࠮ࡼࡿࠥⅤ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack11ll11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪⅥ")
def bstack111ll1l111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬⅦ"))
        framework_version.append(importlib.metadata.version(bstack11ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨⅧ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩⅨ"))
        framework_version.append(importlib.metadata.version(bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥⅩ")))
    except:
        pass
    return {
        bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⅪ"): bstack11ll11_opy_ (u"ࠨࡡࠪⅫ").join(framework_name),
        bstack11ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪⅬ"): bstack11ll11_opy_ (u"ࠪࡣࠬⅭ").join(framework_version)
    }