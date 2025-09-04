# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from browserstack_sdk.bstack1l111llll1_opy_ import bstack11l1ll1ll1_opy_
from browserstack_sdk.bstack111l11l11l_opy_ import RobotHandler
def bstack11llll11l1_opy_(framework):
    if framework.lower() == bstack1111l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ᫶"):
        return bstack11l1ll1ll1_opy_.version()
    elif framework.lower() == bstack1111l1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ᫷"):
        return RobotHandler.version()
    elif framework.lower() == bstack1111l1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ᫸"):
        import behave
        return behave.__version__
    else:
        return bstack1111l1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫ᫹")
def bstack1ll11l11l1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1111l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭᫺"))
        framework_version.append(importlib.metadata.version(bstack1111l1l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ᫻")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᫼"))
        framework_version.append(importlib.metadata.version(bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ᫽")))
    except:
        pass
    return {
        bstack1111l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᫾"): bstack1111l1l_opy_ (u"ࠩࡢࠫ᫿").join(framework_name),
        bstack1111l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᬀ"): bstack1111l1l_opy_ (u"ࠫࡤ࠭ᬁ").join(framework_version)
    }