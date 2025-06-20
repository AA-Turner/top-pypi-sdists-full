# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from browserstack_sdk.bstack1l1ll11ll1_opy_ import bstack1l111l1l_opy_
from browserstack_sdk.bstack111l111ll1_opy_ import RobotHandler
def bstack1l1111l1ll_opy_(framework):
    if framework.lower() == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᪄"):
        return bstack1l111l1l_opy_.version()
    elif framework.lower() == bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ᪅"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ᪆"):
        import behave
        return behave.__version__
    else:
        return bstack11ll11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩ᪇")
def bstack1ll1ll1lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11ll11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ᪈"))
        framework_version.append(importlib.metadata.version(bstack11ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧ᪉")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ᪊"))
        framework_version.append(importlib.metadata.version(bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᪋")))
    except:
        pass
    return {
        bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᪌"): bstack11ll11_opy_ (u"ࠧࡠࠩ᪍").join(framework_name),
        bstack11ll11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ᪎"): bstack11ll11_opy_ (u"ࠩࡢࠫ᪏").join(framework_version)
    }