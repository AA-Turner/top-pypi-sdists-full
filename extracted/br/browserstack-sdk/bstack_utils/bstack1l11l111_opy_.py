# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from browserstack_sdk.bstack111l1ll11l_opy_ import bstack1llll11ll_opy_
from browserstack_sdk.bstack1llll11l111_opy_ import RobotHandler
def bstack1llllll11_opy_(framework):
    if framework.lower() == bstack11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧὖ"):
        return bstack1llll11ll_opy_.version()
    elif framework.lower() == bstack11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧὗ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ὘"):
        import behave
        return behave.__version__
    else:
        return bstack11lll1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫὙ")
def bstack11l1ll1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11lll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭὚"))
        framework_version.append(importlib.metadata.version(bstack11lll1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢὛ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ὜"))
        framework_version.append(importlib.metadata.version(bstack11lll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦὝ")))
    except:
        pass
    return {
        bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭὞"): bstack11lll1_opy_ (u"ࠩࡢࠫὟ").join(framework_name),
        bstack11lll1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫὠ"): bstack11lll1_opy_ (u"ࠫࡤ࠭ὡ").join(framework_version)
    }