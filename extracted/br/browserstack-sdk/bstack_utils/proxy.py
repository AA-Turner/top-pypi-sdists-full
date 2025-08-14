# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l1ll11_opy_
bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
def bstack111111l111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111l11ll_opy_(bstack111111l11l1_opy_, bstack111111l1ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111111l11l1_opy_):
        with open(bstack111111l11l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111111l111l_opy_(bstack111111l11l1_opy_):
        pac = get_pac(url=bstack111111l11l1_opy_)
    else:
        raise Exception(bstack1l1l1ll_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩὊ").format(bstack111111l11l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l1ll_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦὋ"), 80))
        bstack111111l1l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111111l1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬὌ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111111l1ll1_opy_, bstack111111l1l11_opy_)
    return proxy_url
def bstack1l11l1ll1_opy_(config):
    return bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨὍ") in config or bstack1l1l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ὎") in config
def bstack11l111ll1l_opy_(config):
    if not bstack1l11l1ll1_opy_(config):
        return
    if config.get(bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ὏")):
        return config.get(bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὐ"))
    if config.get(bstack1l1l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ὑ")):
        return config.get(bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὒ"))
def bstack1lll1ll1_opy_(config, bstack111111l1ll1_opy_):
    proxy = bstack11l111ll1l_opy_(config)
    proxies = {}
    if config.get(bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧὓ")) or config.get(bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩὔ")):
        if proxy.endswith(bstack1l1l1ll_opy_ (u"࠭࠮ࡱࡣࡦࠫὕ")):
            proxies = bstack11ll111l1_opy_(proxy, bstack111111l1ll1_opy_)
        else:
            proxies = {
                bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ὖ"): proxy
            }
    bstack1l1l1111l1_opy_.bstack1l1ll11111_opy_(bstack1l1l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨὗ"), proxies)
    return proxies
def bstack11ll111l1_opy_(bstack111111l11l1_opy_, bstack111111l1ll1_opy_):
    proxies = {}
    global bstack111111l1111_opy_
    if bstack1l1l1ll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬ὘") in globals():
        return bstack111111l1111_opy_
    try:
        proxy = bstack111111l11ll_opy_(bstack111111l11l1_opy_, bstack111111l1ll1_opy_)
        if bstack1l1l1ll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥὙ") in proxy:
            proxies = {}
        elif bstack1l1l1ll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤ὚") in proxy or bstack1l1l1ll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦὛ") in proxy or bstack1l1l1ll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ὜") in proxy:
            bstack111111l1l1l_opy_ = proxy.split(bstack1l1l1ll_opy_ (u"ࠢࠡࠤὝ"))
            if bstack1l1l1ll_opy_ (u"ࠣ࠼࠲࠳ࠧ὞") in bstack1l1l1ll_opy_ (u"ࠤࠥὟ").join(bstack111111l1l1l_opy_[1:]):
                proxies = {
                    bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὠ"): bstack1l1l1ll_opy_ (u"ࠦࠧὡ").join(bstack111111l1l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὢ"): str(bstack111111l1l1l_opy_[0]).lower() + bstack1l1l1ll_opy_ (u"ࠨ࠺࠰࠱ࠥὣ") + bstack1l1l1ll_opy_ (u"ࠢࠣὤ").join(bstack111111l1l1l_opy_[1:])
                }
        elif bstack1l1l1ll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢὥ") in proxy:
            bstack111111l1l1l_opy_ = proxy.split(bstack1l1l1ll_opy_ (u"ࠤࠣࠦὦ"))
            if bstack1l1l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢὧ") in bstack1l1l1ll_opy_ (u"ࠦࠧὨ").join(bstack111111l1l1l_opy_[1:]):
                proxies = {
                    bstack1l1l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὩ"): bstack1l1l1ll_opy_ (u"ࠨࠢὪ").join(bstack111111l1l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὣ"): bstack1l1l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤὬ") + bstack1l1l1ll_opy_ (u"ࠤࠥὭ").join(bstack111111l1l1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὮ"): proxy
            }
    except Exception as e:
        print(bstack1l1l1ll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣὯ"), bstack111l1l1ll11_opy_.format(bstack111111l11l1_opy_, str(e)))
    bstack111111l1111_opy_ = proxies
    return proxies