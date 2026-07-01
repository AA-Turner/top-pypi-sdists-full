# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
from browserstack_sdk.bstack11ll11l1l_opy_ import bstack11llll11l_opy_
from browserstack_sdk.bstack11111l11_opy_ import RobotHandler
def bstack1l1l1l1l111_opy_(framework):
    if framework.lower() == bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⒂"):
        return bstack11llll11l_opy_.version()
    elif framework.lower() == bstack1l1llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ⒃"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ⒄"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ⒅"):
        import sys
        return bstack1l1llll_opy_ (u"ࠧࢁࡽ࠯ࡽࢀ࠲ࢀࢃࠢ⒆").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack1l1llll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ⒇")
def bstack1lllll1lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1llll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ⒈"))
        framework_version.append(importlib.metadata.version(bstack1l1llll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ⒉")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭⒊"))
        framework_version.append(importlib.metadata.version(bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ⒋")))
    except:
        pass
    return {
        bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⒌"): bstack1l1llll_opy_ (u"ࠬࡥࠧ⒍").join(framework_name),
        bstack1l1llll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ⒎"): bstack1l1llll_opy_ (u"ࠧࡠࠩ⒏").join(framework_version)
    }