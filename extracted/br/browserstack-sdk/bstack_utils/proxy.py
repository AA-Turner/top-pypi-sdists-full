# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l1l1l1_opy_
bstack1llll11l_opy_ = Config.bstack1l11llllll_opy_()
def bstack111111l1ll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111ll111_opy_(bstack111111l1lll_opy_, bstack111111l11ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111111l1lll_opy_):
        with open(bstack111111l1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111111l1ll1_opy_(bstack111111l1lll_opy_):
        pac = get_pac(url=bstack111111l1lll_opy_)
    else:
        raise Exception(bstack1ll1ll_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩἼ").format(bstack111111l1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1ll_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦἽ"), 80))
        bstack111111l11l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111111l11l1_opy_ = bstack1ll1ll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬἾ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111111l11ll_opy_, bstack111111l11l1_opy_)
    return proxy_url
def bstack1ll11l1ll1_opy_(config):
    return bstack1ll1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨἿ") in config or bstack1ll1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪὀ") in config
def bstack11ll1l11ll_opy_(config):
    if not bstack1ll11l1ll1_opy_(config):
        return
    if config.get(bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪὁ")):
        return config.get(bstack1ll1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὂ"))
    if config.get(bstack1ll1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ὃ")):
        return config.get(bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ"))
def bstack11l1ll11l1_opy_(config, bstack111111l11ll_opy_):
    proxy = bstack11ll1l11ll_opy_(config)
    proxies = {}
    if config.get(bstack1ll1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧὅ")) or config.get(bstack1ll1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ὆")):
        if proxy.endswith(bstack1ll1ll_opy_ (u"࠭࠮ࡱࡣࡦࠫ὇")):
            proxies = bstack1ll11l1ll_opy_(proxy, bstack111111l11ll_opy_)
        else:
            proxies = {
                bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὀ"): proxy
            }
    bstack1llll11l_opy_.bstack11l1l1lll1_opy_(bstack1ll1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨὉ"), proxies)
    return proxies
def bstack1ll11l1ll_opy_(bstack111111l1lll_opy_, bstack111111l11ll_opy_):
    proxies = {}
    global bstack111111l1l1l_opy_
    if bstack1ll1ll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬὊ") in globals():
        return bstack111111l1l1l_opy_
    try:
        proxy = bstack111111ll111_opy_(bstack111111l1lll_opy_, bstack111111l11ll_opy_)
        if bstack1ll1ll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥὋ") in proxy:
            proxies = {}
        elif bstack1ll1ll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤὌ") in proxy or bstack1ll1ll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦὍ") in proxy or bstack1ll1ll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ὎") in proxy:
            bstack111111l1l11_opy_ = proxy.split(bstack1ll1ll_opy_ (u"ࠢࠡࠤ὏"))
            if bstack1ll1ll_opy_ (u"ࠣ࠼࠲࠳ࠧὐ") in bstack1ll1ll_opy_ (u"ࠤࠥὑ").join(bstack111111l1l11_opy_[1:]):
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὒ"): bstack1ll1ll_opy_ (u"ࠦࠧὓ").join(bstack111111l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὔ"): str(bstack111111l1l11_opy_[0]).lower() + bstack1ll1ll_opy_ (u"ࠨ࠺࠰࠱ࠥὕ") + bstack1ll1ll_opy_ (u"ࠢࠣὖ").join(bstack111111l1l11_opy_[1:])
                }
        elif bstack1ll1ll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢὗ") in proxy:
            bstack111111l1l11_opy_ = proxy.split(bstack1ll1ll_opy_ (u"ࠤࠣࠦ὘"))
            if bstack1ll1ll_opy_ (u"ࠥ࠾࠴࠵ࠢὙ") in bstack1ll1ll_opy_ (u"ࠦࠧ὚").join(bstack111111l1l11_opy_[1:]):
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὛ"): bstack1ll1ll_opy_ (u"ࠨࠢ὜").join(bstack111111l1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὕ"): bstack1ll1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ὞") + bstack1ll1ll_opy_ (u"ࠤࠥὟ").join(bstack111111l1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὠ"): proxy
            }
    except Exception as e:
        print(bstack1ll1ll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣὡ"), bstack111l1l1l1l1_opy_.format(bstack111111l1lll_opy_, str(e)))
    bstack111111l1l1l_opy_ = proxies
    return proxies