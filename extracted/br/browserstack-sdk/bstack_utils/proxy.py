# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l1l11l_opy_
bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
def bstack1111111lll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111111llll_opy_(bstack111111l1l11_opy_, bstack111111l11l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111111l1l11_opy_):
        with open(bstack111111l1l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111111lll1_opy_(bstack111111l1l11_opy_):
        pac = get_pac(url=bstack111111l1l11_opy_)
    else:
        raise Exception(bstack1l11l11_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩἼ").format(bstack111111l1l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11l11_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦἽ"), 80))
        bstack111111l1111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111111l1111_opy_ = bstack1l11l11_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬἾ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111111l11l1_opy_, bstack111111l1111_opy_)
    return proxy_url
def bstack1l111l11_opy_(config):
    return bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨἿ") in config or bstack1l11l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪὀ") in config
def bstack1l1111l1_opy_(config):
    if not bstack1l111l11_opy_(config):
        return
    if config.get(bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪὁ")):
        return config.get(bstack1l11l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὂ"))
    if config.get(bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ὃ")):
        return config.get(bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ"))
def bstack1lll1lll1_opy_(config, bstack111111l11l1_opy_):
    proxy = bstack1l1111l1_opy_(config)
    proxies = {}
    if config.get(bstack1l11l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧὅ")) or config.get(bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ὆")):
        if proxy.endswith(bstack1l11l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ὇")):
            proxies = bstack111l1lll1_opy_(proxy, bstack111111l11l1_opy_)
        else:
            proxies = {
                bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὀ"): proxy
            }
    bstack11l11llll_opy_.bstack11l11ll1_opy_(bstack1l11l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨὉ"), proxies)
    return proxies
def bstack111l1lll1_opy_(bstack111111l1l11_opy_, bstack111111l11l1_opy_):
    proxies = {}
    global bstack111111l11ll_opy_
    if bstack1l11l11_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬὊ") in globals():
        return bstack111111l11ll_opy_
    try:
        proxy = bstack1111111llll_opy_(bstack111111l1l11_opy_, bstack111111l11l1_opy_)
        if bstack1l11l11_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥὋ") in proxy:
            proxies = {}
        elif bstack1l11l11_opy_ (u"ࠦࡍ࡚ࡔࡑࠤὌ") in proxy or bstack1l11l11_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦὍ") in proxy or bstack1l11l11_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ὎") in proxy:
            bstack111111l111l_opy_ = proxy.split(bstack1l11l11_opy_ (u"ࠢࠡࠤ὏"))
            if bstack1l11l11_opy_ (u"ࠣ࠼࠲࠳ࠧὐ") in bstack1l11l11_opy_ (u"ࠤࠥὑ").join(bstack111111l111l_opy_[1:]):
                proxies = {
                    bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὒ"): bstack1l11l11_opy_ (u"ࠦࠧὓ").join(bstack111111l111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὔ"): str(bstack111111l111l_opy_[0]).lower() + bstack1l11l11_opy_ (u"ࠨ࠺࠰࠱ࠥὕ") + bstack1l11l11_opy_ (u"ࠢࠣὖ").join(bstack111111l111l_opy_[1:])
                }
        elif bstack1l11l11_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢὗ") in proxy:
            bstack111111l111l_opy_ = proxy.split(bstack1l11l11_opy_ (u"ࠤࠣࠦ὘"))
            if bstack1l11l11_opy_ (u"ࠥ࠾࠴࠵ࠢὙ") in bstack1l11l11_opy_ (u"ࠦࠧ὚").join(bstack111111l111l_opy_[1:]):
                proxies = {
                    bstack1l11l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὛ"): bstack1l11l11_opy_ (u"ࠨࠢ὜").join(bstack111111l111l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὕ"): bstack1l11l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ὞") + bstack1l11l11_opy_ (u"ࠤࠥὟ").join(bstack111111l111l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὠ"): proxy
            }
    except Exception as e:
        print(bstack1l11l11_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣὡ"), bstack111l1l1l11l_opy_.format(bstack111111l1l11_opy_, str(e)))
    bstack111111l11ll_opy_ = proxies
    return proxies