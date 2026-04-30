# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l111l11_opy_
from bstack_utils import logger_utils
global_config = Config.bstack111111l1ll_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l11l1l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l111lll1_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l11ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l11l111l_opy_):
        with open(bstack1ll1l11l111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l11l1l11_opy_(bstack1ll1l11l111l_opy_):
        pac = get_pac(url=bstack1ll1l11l111l_opy_)
    else:
        raise Exception(bstack1l1111l_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧ♁").format(bstack1ll1l11l111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1111l_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤ♂"), 80))
        bstack1ll1l11l11l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l11l11l1_opy_ = bstack1l1111l_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪ♃")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11l11ll_opy_, bstack1ll1l11l11l1_opy_)
    return proxy_url
def bstack1l1l1l1ll1_opy_(config):
    return bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭♄") in config or bstack1l1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ♅") in config
def bstack11l1ll11_opy_(config):
    if not bstack1l1l1l1ll1_opy_(config):
        return
    if config.get(bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ♆")):
        return config.get(bstack1l1111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ♇"))
    if config.get(bstack1l1111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ♈")):
        return config.get(bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ♉"))
def bstack11111ll1_opy_(config, bstack1ll1l11l11ll_opy_):
    proxy = bstack11l1ll11_opy_(config)
    proxies = {}
    if config.get(bstack1l1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ♊")) or config.get(bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ♋")):
        if proxy.endswith(bstack1l1111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ♌")):
            proxies = bstack111ll111ll_opy_(proxy, bstack1ll1l11l11ll_opy_)
        else:
            proxies = {
                bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ♍"): proxy
            }
    global_config.bstack11l11lll1l_opy_(bstack1l1111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭♎"), proxies)
    return proxies
def bstack111ll111ll_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l11ll_opy_):
    proxies = {}
    global bstack1ll1l111llll_opy_
    if bstack1l1111l_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪ♏") in globals():
        return bstack1ll1l111llll_opy_
    try:
        proxy = bstack1ll1l111lll1_opy_(bstack1ll1l11l111l_opy_, bstack1ll1l11l11ll_opy_)
        if bstack1l1111l_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣ♐") in proxy:
            proxies = {}
        elif bstack1l1111l_opy_ (u"ࠤࡋࡘ࡙ࡖࠢ♑") in proxy or bstack1l1111l_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤ♒") in proxy or bstack1l1111l_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥ♓") in proxy:
            bstack1ll1l11l1111_opy_ = proxy.split(bstack1l1111l_opy_ (u"ࠧࠦࠢ♔"))
            if bstack1l1111l_opy_ (u"ࠨ࠺࠰࠱ࠥ♕") in bstack1l1111l_opy_ (u"ࠢࠣ♖").join(bstack1ll1l11l1111_opy_[1:]):
                proxies = {
                    bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ♗"): bstack1l1111l_opy_ (u"ࠤࠥ♘").join(bstack1ll1l11l1111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ♙"): str(bstack1ll1l11l1111_opy_[0]).lower() + bstack1l1111l_opy_ (u"ࠦ࠿࠵࠯ࠣ♚") + bstack1l1111l_opy_ (u"ࠧࠨ♛").join(bstack1ll1l11l1111_opy_[1:])
                }
        elif bstack1l1111l_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧ♜") in proxy:
            bstack1ll1l11l1111_opy_ = proxy.split(bstack1l1111l_opy_ (u"ࠢࠡࠤ♝"))
            if bstack1l1111l_opy_ (u"ࠣ࠼࠲࠳ࠧ♞") in bstack1l1111l_opy_ (u"ࠤࠥ♟").join(bstack1ll1l11l1111_opy_[1:]):
                proxies = {
                    bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ♠"): bstack1l1111l_opy_ (u"ࠦࠧ♡").join(bstack1ll1l11l1111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ♢"): bstack1l1111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ♣") + bstack1l1111l_opy_ (u"ࠢࠣ♤").join(bstack1ll1l11l1111_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ♥"): proxy
            }
    except Exception as e:
        print(bstack1l1111l_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ♦"), bstack1lll1l111l11_opy_.format(bstack1ll1l11l111l_opy_, str(e)))
    bstack1ll1l111llll_opy_ = proxies
    return proxies