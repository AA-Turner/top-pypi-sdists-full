# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1ll1l11_opy_
bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
def bstack11111l1l1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111l1ll1l_opy_(bstack11111l1ll11_opy_, bstack11111l1lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111l1ll11_opy_):
        with open(bstack11111l1ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111l1l1l1_opy_(bstack11111l1ll11_opy_):
        pac = get_pac(url=bstack11111l1ll11_opy_)
    else:
        raise Exception(bstackl_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫỀ").format(bstack11111l1ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstackl_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨề"), 80))
        bstack11111l1llll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111l1llll_opy_ = bstackl_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧỂ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111l1lll1_opy_, bstack11111l1llll_opy_)
    return proxy_url
def bstack1lllll1l11_opy_(config):
    return bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪể") in config or bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬỄ") in config
def bstack1l1ll1l1ll_opy_(config):
    if not bstack1lllll1l11_opy_(config):
        return
    if config.get(bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬễ")):
        return config.get(bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ệ"))
    if config.get(bstackl_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨệ")):
        return config.get(bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩỈ"))
def bstack111l11ll1_opy_(config, bstack11111l1lll1_opy_):
    proxy = bstack1l1ll1l1ll_opy_(config)
    proxies = {}
    if config.get(bstackl_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩỉ")) or config.get(bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫỊ")):
        if proxy.endswith(bstackl_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ị")):
            proxies = bstack111llllll_opy_(proxy, bstack11111l1lll1_opy_)
        else:
            proxies = {
                bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨỌ"): proxy
            }
    bstack1l1llll1l1_opy_.bstack1l1ll1lll1_opy_(bstackl_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪọ"), proxies)
    return proxies
def bstack111llllll_opy_(bstack11111l1ll11_opy_, bstack11111l1lll1_opy_):
    proxies = {}
    global bstack11111l1l11l_opy_
    if bstackl_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧỎ") in globals():
        return bstack11111l1l11l_opy_
    try:
        proxy = bstack11111l1ll1l_opy_(bstack11111l1ll11_opy_, bstack11111l1lll1_opy_)
        if bstackl_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧỏ") in proxy:
            proxies = {}
        elif bstackl_opy_ (u"ࠨࡈࡕࡖࡓࠦỐ") in proxy or bstackl_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨố") in proxy or bstackl_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢỒ") in proxy:
            bstack11111l1l1ll_opy_ = proxy.split(bstackl_opy_ (u"ࠤࠣࠦồ"))
            if bstackl_opy_ (u"ࠥ࠾࠴࠵ࠢỔ") in bstackl_opy_ (u"ࠦࠧổ").join(bstack11111l1l1ll_opy_[1:]):
                proxies = {
                    bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫỖ"): bstackl_opy_ (u"ࠨࠢỗ").join(bstack11111l1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ộ"): str(bstack11111l1l1ll_opy_[0]).lower() + bstackl_opy_ (u"ࠣ࠼࠲࠳ࠧộ") + bstackl_opy_ (u"ࠤࠥỚ").join(bstack11111l1l1ll_opy_[1:])
                }
        elif bstackl_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤớ") in proxy:
            bstack11111l1l1ll_opy_ = proxy.split(bstackl_opy_ (u"ࠦࠥࠨỜ"))
            if bstackl_opy_ (u"ࠧࡀ࠯࠰ࠤờ") in bstackl_opy_ (u"ࠨࠢỞ").join(bstack11111l1l1ll_opy_[1:]):
                proxies = {
                    bstackl_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ở"): bstackl_opy_ (u"ࠣࠤỠ").join(bstack11111l1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨỡ"): bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦỢ") + bstackl_opy_ (u"ࠦࠧợ").join(bstack11111l1l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstackl_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫỤ"): proxy
            }
    except Exception as e:
        print(bstackl_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥụ"), bstack111l1ll1l11_opy_.format(bstack11111l1ll11_opy_, str(e)))
    bstack11111l1l11l_opy_ = proxies
    return proxies