# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll11l111l11_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1lll1l11_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll111llllll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡪࡵࡢࡺࡦࡲࡩࡥࡡࡸࡶࡱࠦࡵࡳ࡮ࡳࡥࡷࡹࡥࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁ࠿ࠦࡻࡾࠤ⧁").format(type(e).__name__, e))
        return False
def bstack1ll11l1111ll_opy_(bstack1ll11l111l1l_opy_, bstack1ll11l111ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll11l111l1l_opy_):
        with open(bstack1ll11l111l1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll111llllll_opy_(bstack1ll11l111l1l_opy_):
        pac = get_pac(url=bstack1ll11l111l1l_opy_)
    else:
        raise Exception(bstack1l1llll_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ⧂").format(bstack1ll11l111l1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1llll_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥ⧃"), 80))
        bstack1ll11l11111l_opy_ = s.getsockname()[0]
        s.close()
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡰࡴࡩࡡ࡭ࠢ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠤࡸࡵࡣ࡬ࡧࡷࠤࡵࡸ࡯ࡣࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦ⧄").format(type(e).__name__, e))
        bstack1ll11l11111l_opy_ = bstack1l1llll_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬ⧅")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll11l111ll1_opy_, bstack1ll11l11111l_opy_)
    return proxy_url
def bstack11ll1l1ll1_opy_(config):
    return bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⧆") in config or bstack1l1llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⧇") in config
def bstack1l111ll111_opy_(config):
    if not bstack11ll1l1ll1_opy_(config):
        return
    if config.get(bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⧈")):
        return config.get(bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⧉"))
    if config.get(bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⧊")):
        return config.get(bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⧋"))
def bstack1ll11l111l1_opy_(config, bstack1ll11l111ll1_opy_):
    proxy = bstack1l111ll111_opy_(config)
    proxies = {}
    if config.get(bstack1l1llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⧌")) or config.get(bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⧍")):
        if proxy.endswith(bstack1l1llll_opy_ (u"࠭࠮ࡱࡣࡦࠫ⧎")):
            proxies = bstack1ll1ll1111l_opy_(proxy, bstack1ll11l111ll1_opy_)
        else:
            proxies = {
                bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⧏"): proxy
            }
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⧐"), proxies)
    return proxies
def bstack1ll1ll1111l_opy_(bstack1ll11l111l1l_opy_, bstack1ll11l111ll1_opy_):
    proxies = {}
    global bstack1ll11l111111_opy_
    if bstack1l1llll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬ⧑") in globals():
        return bstack1ll11l111111_opy_
    try:
        proxy = bstack1ll11l1111ll_opy_(bstack1ll11l111l1l_opy_, bstack1ll11l111ll1_opy_)
        if bstack1l1llll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥ⧒") in proxy:
            proxies = {}
        elif bstack1l1llll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤ⧓") in proxy or bstack1l1llll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦ⧔") in proxy or bstack1l1llll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧ⧕") in proxy:
            bstack1ll11l1111l1_opy_ = proxy.split(bstack1l1llll_opy_ (u"ࠢࠡࠤ⧖"))
            if bstack1l1llll_opy_ (u"ࠣ࠼࠲࠳ࠧ⧗") in bstack1l1llll_opy_ (u"ࠤࠥ⧘").join(bstack1ll11l1111l1_opy_[1:]):
                proxies = {
                    bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⧙"): bstack1l1llll_opy_ (u"ࠦࠧ⧚").join(bstack1ll11l1111l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⧛"): str(bstack1ll11l1111l1_opy_[0]).lower() + bstack1l1llll_opy_ (u"ࠨ࠺࠰࠱ࠥ⧜") + bstack1l1llll_opy_ (u"ࠢࠣ⧝").join(bstack1ll11l1111l1_opy_[1:])
                }
        elif bstack1l1llll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢ⧞") in proxy:
            bstack1ll11l1111l1_opy_ = proxy.split(bstack1l1llll_opy_ (u"ࠤࠣࠦ⧟"))
            if bstack1l1llll_opy_ (u"ࠥ࠾࠴࠵ࠢ⧠") in bstack1l1llll_opy_ (u"ࠦࠧ⧡").join(bstack1ll11l1111l1_opy_[1:]):
                proxies = {
                    bstack1l1llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⧢"): bstack1l1llll_opy_ (u"ࠨࠢ⧣").join(bstack1ll11l1111l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⧤"): bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⧥") + bstack1l1llll_opy_ (u"ࠤࠥ⧦").join(bstack1ll11l1111l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⧧"): proxy
            }
    except Exception as e:
        print(bstack1l1llll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ⧨"), bstack1ll11l111l11_opy_.format(bstack1ll11l111l1l_opy_, str(e)))
    bstack1ll11l111111_opy_ = proxies
    return proxies