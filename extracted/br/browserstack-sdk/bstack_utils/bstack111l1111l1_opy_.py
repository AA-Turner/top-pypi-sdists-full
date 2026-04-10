# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
from browserstack_sdk.bstack1lll11l1_opy_ import bstack1l11ll1l11_opy_
from browserstack_sdk.bstack1lll1l1l1l1_opy_ import RobotHandler
def bstack1ll1lll11l_opy_(framework):
    if framework.lower() == bstack1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧⅣ"):
        return bstack1l11ll1l11_opy_.version()
    elif framework.lower() == bstack1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧⅤ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩⅥ"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫⅦ"):
        import sys
        return bstack1ll_opy_ (u"ࠦࢀࢃ࠮ࡼࡿ࠱ࡿࢂࠨⅧ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack1ll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭Ⅸ")
def bstack11l1l1llll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨⅩ"))
        framework_version.append(importlib.metadata.version(bstack1ll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤⅪ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬⅫ"))
        framework_version.append(importlib.metadata.version(bstack1ll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨⅬ")))
    except:
        pass
    return {
        bstack1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨⅭ"): bstack1ll_opy_ (u"ࠫࡤ࠭Ⅾ").join(framework_name),
        bstack1ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭Ⅿ"): bstack1ll_opy_ (u"࠭࡟ࠨⅰ").join(framework_version)
    }