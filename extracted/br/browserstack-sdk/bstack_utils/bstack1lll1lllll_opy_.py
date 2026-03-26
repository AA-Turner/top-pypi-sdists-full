# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111l1ll11ll_opy_ import bstack111l1ll11l1_opy_
from bstack_utils.constants import bstack111l11l11ll_opy_, bstack1l1111ll_opy_
from bstack_utils.bstack1lll111ll_opy_ import bstack1l111111l1_opy_
from bstack_utils import logger_utils
bstack1111ll1ll11_opy_ = 10
class bstack1l1l11l11_opy_:
    def __init__(self, bstack1ll11ll1l_opy_, config, bstack1111lll11l1_opy_=0):
        self.bstack1111ll1lll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1111lll1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧὕ").format(bstack111l11l11ll_opy_)
        self.bstack1111ll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣὖ").format(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ὗ"))))
        self.bstack1111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ὘").format(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨὙ"))))
        self.bstack1111ll1l11l_opy_ = 2
        self.bstack1ll11ll1l_opy_ = bstack1ll11ll1l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l1111ll_opy_)
        self.bstack1111lll11l1_opy_ = bstack1111lll11l1_opy_
        self.bstack1111lll1l11_opy_ = False
        self.bstack1111lll1l1l_opy_ = not (
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ὚")) and
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣὛ")) and
                            os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ὜"))
                        )
        if bstack1l111111l1_opy_.bstack1111ll11l1l_opy_(config):
            self.bstack1111ll1l11l_opy_ = bstack1l111111l1_opy_.bstack1111ll1l111_opy_(config, self.bstack1111lll11l1_opy_)
            self.bstack1111lll1111_opy_()
    def bstack1111llll111_opy_(self):
        return bstack1ll1lll_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨὝ").format(self.config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ὞")), os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨὟ")))
    def bstack1111ll11ll1_opy_(self):
        try:
            if self.bstack1111lll1l1l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111lll1lll_opy_, bstack1ll1lll_opy_ (u"ࠥࡶࠧὠ")) as f:
                        bstack1111ll11lll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111ll11lll_opy_ = set()
                bstack1111ll1llll_opy_ = bstack1111ll11lll_opy_ - self.bstack1111ll1lll1_opy_
                if not bstack1111ll1llll_opy_:
                    return
                self.bstack1111ll1lll1_opy_.update(bstack1111ll1llll_opy_)
                data = {bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤὡ"): list(self.bstack1111ll1lll1_opy_), bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣὢ"): self.config.get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩὣ")), bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧὤ"): os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧὥ")), bstack1ll1lll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢὦ"): self.config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨὧ"))}
            response = bstack111l1ll11l1_opy_.bstack1111lll111l_opy_(self.bstack1111lll1ll1_opy_, data)
            if response.get(bstack1ll1lll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦὨ")) == 200:
                self.logger.debug(bstack1ll1lll_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧὩ").format(data))
            else:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥὪ").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢὫ").format(e))
    def bstack1111ll1ll1l_opy_(self):
        if self.bstack1111lll1l1l_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111lll1lll_opy_, bstack1ll1lll_opy_ (u"ࠣࡴࠥὬ")) as f:
                        bstack1111llll1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111llll1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧὭ").format(failed_count))
                if failed_count >= self.bstack1111ll1l11l_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦὮ").format(failed_count, self.bstack1111ll1l11l_opy_))
                    self.bstack1111llll11l_opy_(failed_count)
                    self.bstack1111lll1l11_opy_ = True
            return
        try:
            response = bstack111l1ll11l1_opy_.bstack1111ll1ll1l_opy_(bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣὯ").format(self.bstack1111lll1ll1_opy_, self.config.get(bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨὰ")), os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬά")), self.config.get(bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬὲ"))))
            if response.get(bstack1ll1lll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣέ")) == 200:
                failed_count = response.get(bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧὴ"), 0)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧή").format(failed_count))
                if failed_count >= self.bstack1111ll1l11l_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦὶ").format(failed_count, self.bstack1111ll1l11l_opy_))
                    self.bstack1111llll11l_opy_(failed_count)
                    self.bstack1111lll1l11_opy_ = True
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤί").format(response))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢὸ").format(e))
    def bstack1111llll11l_opy_(self, failed_count):
        with open(self.bstack1111ll1l1l1_opy_, bstack1ll1lll_opy_ (u"ࠢࡸࠤό")) as f:
            f.write(bstack1ll1lll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨὺ").format(datetime.now()))
            f.write(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨύ").format(failed_count))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦὼ").format(self.bstack1111ll1l1l1_opy_))
    def bstack1111lll1111_opy_(self):
        def bstack1111ll1l1ll_opy_():
            while not self.bstack1111lll1l11_opy_:
                time.sleep(bstack1111ll1ll11_opy_)
                self.bstack1111ll11ll1_opy_()
                self.bstack1111ll1ll1l_opy_()
        bstack1111lll11ll_opy_ = threading.Thread(target=bstack1111ll1l1ll_opy_, daemon=True)
        bstack1111lll11ll_opy_.start()