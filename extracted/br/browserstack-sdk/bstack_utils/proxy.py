# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l11lll1_opy_
bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
def bstack11111ll1111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111l1ll11_opy_(bstack11111ll11l1_opy_, bstack11111l1llll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111ll11l1_opy_):
        with open(bstack11111ll11l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111ll1111_opy_(bstack11111ll11l1_opy_):
        pac = get_pac(url=bstack11111ll11l1_opy_)
    else:
        raise Exception(bstack11l1111_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ẻ").format(bstack11111ll11l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1111_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣẼ"), 80))
        bstack11111ll111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111ll111l_opy_ = bstack11l1111_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩẽ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111l1llll_opy_, bstack11111ll111l_opy_)
    return proxy_url
def bstack1lll1lllll_opy_(config):
    return bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬẾ") in config or bstack11l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧế") in config
def bstack1llll11111_opy_(config):
    if not bstack1lll1lllll_opy_(config):
        return
    if config.get(bstack11l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧỀ")):
        return config.get(bstack11l1111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨề"))
    if config.get(bstack11l1111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪỂ")):
        return config.get(bstack11l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫể"))
def bstack1ll1l1l1l_opy_(config, bstack11111l1llll_opy_):
    proxy = bstack1llll11111_opy_(config)
    proxies = {}
    if config.get(bstack11l1111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫỄ")) or config.get(bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ễ")):
        if proxy.endswith(bstack11l1111_opy_ (u"ࠪ࠲ࡵࡧࡣࠨỆ")):
            proxies = bstack111ll1l1_opy_(proxy, bstack11111l1llll_opy_)
        else:
            proxies = {
                bstack11l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪệ"): proxy
            }
    bstack1l1l11l1ll_opy_.bstack1ll1lll111_opy_(bstack11l1111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬỈ"), proxies)
    return proxies
def bstack111ll1l1_opy_(bstack11111ll11l1_opy_, bstack11111l1llll_opy_):
    proxies = {}
    global bstack11111l1ll1l_opy_
    if bstack11l1111_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩỉ") in globals():
        return bstack11111l1ll1l_opy_
    try:
        proxy = bstack11111l1ll11_opy_(bstack11111ll11l1_opy_, bstack11111l1llll_opy_)
        if bstack11l1111_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢỊ") in proxy:
            proxies = {}
        elif bstack11l1111_opy_ (u"ࠣࡊࡗࡘࡕࠨị") in proxy or bstack11l1111_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣỌ") in proxy or bstack11l1111_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤọ") in proxy:
            bstack11111l1lll1_opy_ = proxy.split(bstack11l1111_opy_ (u"ࠦࠥࠨỎ"))
            if bstack11l1111_opy_ (u"ࠧࡀ࠯࠰ࠤỏ") in bstack11l1111_opy_ (u"ࠨࠢỐ").join(bstack11111l1lll1_opy_[1:]):
                proxies = {
                    bstack11l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ố"): bstack11l1111_opy_ (u"ࠣࠤỒ").join(bstack11111l1lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨồ"): str(bstack11111l1lll1_opy_[0]).lower() + bstack11l1111_opy_ (u"ࠥ࠾࠴࠵ࠢỔ") + bstack11l1111_opy_ (u"ࠦࠧổ").join(bstack11111l1lll1_opy_[1:])
                }
        elif bstack11l1111_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦỖ") in proxy:
            bstack11111l1lll1_opy_ = proxy.split(bstack11l1111_opy_ (u"ࠨࠠࠣỗ"))
            if bstack11l1111_opy_ (u"ࠢ࠻࠱࠲ࠦỘ") in bstack11l1111_opy_ (u"ࠣࠤộ").join(bstack11111l1lll1_opy_[1:]):
                proxies = {
                    bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨỚ"): bstack11l1111_opy_ (u"ࠥࠦớ").join(bstack11111l1lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪỜ"): bstack11l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨờ") + bstack11l1111_opy_ (u"ࠨࠢỞ").join(bstack11111l1lll1_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ở"): proxy
            }
    except Exception as e:
        print(bstack11l1111_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧỠ"), bstack1111l11lll1_opy_.format(bstack11111ll11l1_opy_, str(e)))
    bstack11111l1ll1l_opy_ = proxies
    return proxies