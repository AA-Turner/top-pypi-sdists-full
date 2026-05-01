# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from browserstack_sdk.bstack1lllllll1_opy_ import bstack11l11111l_opy_
from browserstack_sdk.bstack1lll11lll1l_opy_ import RobotHandler
def bstack11lll1111l_opy_(framework):
    if framework.lower() == bstack111ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⇍"):
        return bstack11l11111l_opy_.version()
    elif framework.lower() == bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ⇎"):
        return RobotHandler.version()
    elif framework.lower() == bstack111ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ⇏"):
        import behave
        return behave.__version__
    elif framework.lower() == bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ⇐"):
        import sys
        return bstack111ll_opy_ (u"ࠧࢁࡽ࠯ࡽࢀ࠲ࢀࢃࠢ⇑").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    else:
        return bstack111ll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ⇒")
def bstack1l1111l1l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack111ll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ⇓"))
        framework_version.append(importlib.metadata.version(bstack111ll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥ⇔")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack111ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭⇕"))
        framework_version.append(importlib.metadata.version(bstack111ll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ⇖")))
    except:
        pass
    return {
        bstack111ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⇗"): bstack111ll_opy_ (u"ࠬࡥࠧ⇘").join(framework_name),
        bstack111ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ⇙"): bstack111ll_opy_ (u"ࠧࡠࠩ⇚").join(framework_version)
    }