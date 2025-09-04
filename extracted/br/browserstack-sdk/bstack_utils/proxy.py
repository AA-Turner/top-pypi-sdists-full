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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l111ll_opy_
bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
def bstack111111111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111111l1_opy_(bstack11111111l11_opy_, bstack1111111l111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111111l11_opy_):
        with open(bstack11111111l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111111111ll_opy_(bstack11111111l11_opy_):
        pac = get_pac(url=bstack11111111l11_opy_)
    else:
        raise Exception(bstack1111l1l_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩἼ").format(bstack11111111l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111l1l_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦἽ"), 80))
        bstack11111111lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111111lll_opy_ = bstack1111l1l_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬἾ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111111l111_opy_, bstack11111111lll_opy_)
    return proxy_url
def bstack1llll111_opy_(config):
    return bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨἿ") in config or bstack1111l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪὀ") in config
def bstack1l11l11ll_opy_(config):
    if not bstack1llll111_opy_(config):
        return
    if config.get(bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪὁ")):
        return config.get(bstack1111l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὂ"))
    if config.get(bstack1111l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ὃ")):
        return config.get(bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ"))
def bstack11l1l111ll_opy_(config, bstack1111111l111_opy_):
    proxy = bstack1l11l11ll_opy_(config)
    proxies = {}
    if config.get(bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧὅ")) or config.get(bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ὆")):
        if proxy.endswith(bstack1111l1l_opy_ (u"࠭࠮ࡱࡣࡦࠫ὇")):
            proxies = bstack111ll11l1_opy_(proxy, bstack1111111l111_opy_)
        else:
            proxies = {
                bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὀ"): proxy
            }
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨὉ"), proxies)
    return proxies
def bstack111ll11l1_opy_(bstack11111111l11_opy_, bstack1111111l111_opy_):
    proxies = {}
    global bstack11111111ll1_opy_
    if bstack1111l1l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬὊ") in globals():
        return bstack11111111ll1_opy_
    try:
        proxy = bstack111111111l1_opy_(bstack11111111l11_opy_, bstack1111111l111_opy_)
        if bstack1111l1l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥὋ") in proxy:
            proxies = {}
        elif bstack1111l1l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤὌ") in proxy or bstack1111l1l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦὍ") in proxy or bstack1111l1l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ὎") in proxy:
            bstack11111111l1l_opy_ = proxy.split(bstack1111l1l_opy_ (u"ࠢࠡࠤ὏"))
            if bstack1111l1l_opy_ (u"ࠣ࠼࠲࠳ࠧὐ") in bstack1111l1l_opy_ (u"ࠤࠥὑ").join(bstack11111111l1l_opy_[1:]):
                proxies = {
                    bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὒ"): bstack1111l1l_opy_ (u"ࠦࠧὓ").join(bstack11111111l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὔ"): str(bstack11111111l1l_opy_[0]).lower() + bstack1111l1l_opy_ (u"ࠨ࠺࠰࠱ࠥὕ") + bstack1111l1l_opy_ (u"ࠢࠣὖ").join(bstack11111111l1l_opy_[1:])
                }
        elif bstack1111l1l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢὗ") in proxy:
            bstack11111111l1l_opy_ = proxy.split(bstack1111l1l_opy_ (u"ࠤࠣࠦ὘"))
            if bstack1111l1l_opy_ (u"ࠥ࠾࠴࠵ࠢὙ") in bstack1111l1l_opy_ (u"ࠦࠧ὚").join(bstack11111111l1l_opy_[1:]):
                proxies = {
                    bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫὛ"): bstack1111l1l_opy_ (u"ࠨࠢ὜").join(bstack11111111l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ὕ"): bstack1111l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ὞") + bstack1111l1l_opy_ (u"ࠤࠥὟ").join(bstack11111111l1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1111l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩὠ"): proxy
            }
    except Exception as e:
        print(bstack1111l1l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣὡ"), bstack111l1l111ll_opy_.format(bstack11111111l11_opy_, str(e)))
    bstack11111111ll1_opy_ = proxies
    return proxies