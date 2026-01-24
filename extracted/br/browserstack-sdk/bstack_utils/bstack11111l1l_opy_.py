# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from browserstack_sdk.bstack111l1l1ll1_opy_ import bstack111ll1l1ll_opy_
from browserstack_sdk.bstack11111lll1l_opy_ import RobotHandler
def bstack111lll1111_opy_(framework):
    if framework.lower() == bstack1l1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᰯ"):
        return bstack111ll1l1ll_opy_.version()
    elif framework.lower() == bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᰰ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᰱ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1111_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᰲ")
def bstack1l1ll1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᰳ"))
        framework_version.append(importlib.metadata.version(bstack1l1111_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᰴ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᰵ"))
        framework_version.append(importlib.metadata.version(bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᰶ")))
    except:
        pass
    return {
        bstack1l1111_opy_ (u"࠭࡮ࡢ࡯ࡨ᰷ࠫ"): bstack1l1111_opy_ (u"ࠧࡠࠩ᰸").join(framework_name),
        bstack1l1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ᰹"): bstack1l1111_opy_ (u"ࠩࡢࠫ᰺").join(framework_version)
    }