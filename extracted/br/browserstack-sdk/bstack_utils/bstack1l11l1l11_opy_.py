# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from browserstack_sdk.bstack11ll1l1l1l_opy_ import bstack1l11l11l1l_opy_
from browserstack_sdk.bstack1111llllll_opy_ import RobotHandler
def bstack1l1111l1_opy_(framework):
    if framework.lower() == bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᫺"):
        return bstack1l11l11l1l_opy_.version()
    elif framework.lower() == bstack1ll11ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ᫻"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll11ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭᫼"):
        import behave
        return behave.__version__
    else:
        return bstack1ll11ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨ᫽")
def bstack11ll1l1l11_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1ll11ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ᫾"))
        framework_version.append(importlib.metadata.version(bstack1ll11ll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᫿")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᬀ"))
        framework_version.append(importlib.metadata.version(bstack1ll11ll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᬁ")))
    except:
        pass
    return {
        bstack1ll11ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᬂ"): bstack1ll11ll_opy_ (u"࠭࡟ࠨᬃ").join(framework_name),
        bstack1ll11ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᬄ"): bstack1ll11ll_opy_ (u"ࠨࡡࠪᬅ").join(framework_version)
    }