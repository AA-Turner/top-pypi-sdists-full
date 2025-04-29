# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from browserstack_sdk.bstack11l1111ll_opy_ import bstack1lll1111l_opy_
from browserstack_sdk.bstack111l11ll1l_opy_ import RobotHandler
def bstack1llll11l1l_opy_(framework):
    if framework.lower() == bstack1llllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦝ"):
        return bstack1lll1111l_opy_.version()
    elif framework.lower() == bstack1llllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᦞ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1llllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᦟ"):
        import behave
        return behave.__version__
    else:
        return bstack1llllll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᦠ")
def bstack1llll1111_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1llllll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᦡ"))
        framework_version.append(importlib.metadata.version(bstack1llllll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᦢ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1llllll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᦣ"))
        framework_version.append(importlib.metadata.version(bstack1llllll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᦤ")))
    except:
        pass
    return {
        bstack1llllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᦥ"): bstack1llllll_opy_ (u"ࠧࡠࠩᦦ").join(framework_name),
        bstack1llllll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᦧ"): bstack1llllll_opy_ (u"ࠩࡢࠫᦨ").join(framework_version)
    }