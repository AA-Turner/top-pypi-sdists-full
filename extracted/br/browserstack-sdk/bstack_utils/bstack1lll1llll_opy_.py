# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from browserstack_sdk.bstack1ll1l111ll_opy_ import bstack1ll11l1l11_opy_
from browserstack_sdk.bstack1llllll11ll_opy_ import RobotHandler
def bstack1ll1llll_opy_(framework):
    if framework.lower() == bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᴠ"):
        return bstack1ll11l1l11_opy_.version()
    elif framework.lower() == bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᴡ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᴢ"):
        import behave
        return behave.__version__
    else:
        return bstack11l11_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬᴣ")
def bstack11l1l1111l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᴤ"))
        framework_version.append(importlib.metadata.version(bstack11l11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᴥ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᴦ"))
        framework_version.append(importlib.metadata.version(bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᴧ")))
    except:
        pass
    return {
        bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᴨ"): bstack11l11_opy_ (u"ࠪࡣࠬᴩ").join(framework_name),
        bstack11l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᴪ"): bstack11l11_opy_ (u"ࠬࡥࠧᴫ").join(framework_version)
    }