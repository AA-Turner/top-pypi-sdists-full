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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l11l1l1l_opy_
bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
def bstack1lllllll1ll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llllllll111_opy_(bstack1llllllll11l_opy_, bstack1llllllll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllllll11l_opy_):
        with open(bstack1llllllll11l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllllll1ll1_opy_(bstack1llllllll11l_opy_):
        pac = get_pac(url=bstack1llllllll11l_opy_)
    else:
        raise Exception(bstack1ll11ll_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ὀ").format(bstack1llllllll11l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll11ll_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣὁ"), 80))
        bstack1lllllllll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllllllll11_opy_ = bstack1ll11ll_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩὂ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llllllll1l1_opy_, bstack1lllllllll11_opy_)
    return proxy_url
def bstack11l11lll1l_opy_(config):
    return bstack1ll11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬὃ") in config or bstack1ll11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ") in config
def bstack11l1l1ll1l_opy_(config):
    if not bstack11l11lll1l_opy_(config):
        return
    if config.get(bstack1ll11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧὅ")):
        return config.get(bstack1ll11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ὆"))
    if config.get(bstack1ll11ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ὇")):
        return config.get(bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫὈ"))
def bstack1llll11lll_opy_(config, bstack1llllllll1l1_opy_):
    proxy = bstack11l1l1ll1l_opy_(config)
    proxies = {}
    if config.get(bstack1ll11ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὉ")) or config.get(bstack1ll11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ὂ")):
        if proxy.endswith(bstack1ll11ll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨὋ")):
            proxies = bstack11ll11ll_opy_(proxy, bstack1llllllll1l1_opy_)
        else:
            proxies = {
                bstack1ll11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪὌ"): proxy
            }
    bstack1l111111l1_opy_.bstack11l111l1l_opy_(bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬὍ"), proxies)
    return proxies
def bstack11ll11ll_opy_(bstack1llllllll11l_opy_, bstack1llllllll1l1_opy_):
    proxies = {}
    global bstack1lllllll1lll_opy_
    if bstack1ll11ll_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩ὎") in globals():
        return bstack1lllllll1lll_opy_
    try:
        proxy = bstack1llllllll111_opy_(bstack1llllllll11l_opy_, bstack1llllllll1l1_opy_)
        if bstack1ll11ll_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢ὏") in proxy:
            proxies = {}
        elif bstack1ll11ll_opy_ (u"ࠣࡊࡗࡘࡕࠨὐ") in proxy or bstack1ll11ll_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣὑ") in proxy or bstack1ll11ll_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤὒ") in proxy:
            bstack1llllllll1ll_opy_ = proxy.split(bstack1ll11ll_opy_ (u"ࠦࠥࠨὓ"))
            if bstack1ll11ll_opy_ (u"ࠧࡀ࠯࠰ࠤὔ") in bstack1ll11ll_opy_ (u"ࠨࠢὕ").join(bstack1llllllll1ll_opy_[1:]):
                proxies = {
                    bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ὖ"): bstack1ll11ll_opy_ (u"ࠣࠤὗ").join(bstack1llllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ὘"): str(bstack1llllllll1ll_opy_[0]).lower() + bstack1ll11ll_opy_ (u"ࠥ࠾࠴࠵ࠢὙ") + bstack1ll11ll_opy_ (u"ࠦࠧ὚").join(bstack1llllllll1ll_opy_[1:])
                }
        elif bstack1ll11ll_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦὛ") in proxy:
            bstack1llllllll1ll_opy_ = proxy.split(bstack1ll11ll_opy_ (u"ࠨࠠࠣ὜"))
            if bstack1ll11ll_opy_ (u"ࠢ࠻࠱࠲ࠦὝ") in bstack1ll11ll_opy_ (u"ࠣࠤ὞").join(bstack1llllllll1ll_opy_[1:]):
                proxies = {
                    bstack1ll11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨὟ"): bstack1ll11ll_opy_ (u"ࠥࠦὠ").join(bstack1llllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪὡ"): bstack1ll11ll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨὢ") + bstack1ll11ll_opy_ (u"ࠨࠢὣ").join(bstack1llllllll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll11ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ὤ"): proxy
            }
    except Exception as e:
        print(bstack1ll11ll_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧὥ"), bstack111l11l1l1l_opy_.format(bstack1llllllll11l_opy_, str(e)))
    bstack1lllllll1lll_opy_ = proxies
    return proxies