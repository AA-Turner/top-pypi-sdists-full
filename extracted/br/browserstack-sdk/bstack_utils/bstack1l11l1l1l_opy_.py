# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll1ll1111_opy_ import bstack11ll1l1lll1_opy_
from bstack_utils.constants import bstack11ll11l1l11_opy_, bstack11llll111_opy_
from bstack_utils.bstack1ll1ll1l_opy_ import bstack1lllll1l11_opy_
from bstack_utils import bstack1111ll111_opy_
bstack11l1ll11l1l_opy_ = 10
class bstack1111ll1l1_opy_:
    def __init__(self, bstack1l11lll11l_opy_, config, bstack11l1lll111l_opy_=0):
        self.bstack11l1lll1l1l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1lll11l1_opy_ = bstack111lll_opy_ (u"ࠨࡻࡾ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣᩍ").format(bstack11ll11l1l11_opy_)
        self.bstack11l1ll11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣᩎ").format(os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᩏ"))))
        self.bstack11l1ll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣᩐ").format(os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᩑ"))))
        self.bstack11l1ll1lll1_opy_ = 2
        self.bstack1l11lll11l_opy_ = bstack1l11lll11l_opy_
        self.config = config
        self.logger = bstack1111ll111_opy_.get_logger(__name__, bstack11llll111_opy_)
        self.bstack11l1lll111l_opy_ = bstack11l1lll111l_opy_
        self.bstack11l1ll1l1ll_opy_ = False
        self.bstack11l1ll11l11_opy_ = not (
                            os.environ.get(bstack111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥᩒ")) and
                            os.environ.get(bstack111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣᩓ")) and
                            os.environ.get(bstack111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣᩔ"))
                        )
        if bstack1lllll1l11_opy_.bstack11l1ll1l1l1_opy_(config):
            self.bstack11l1ll1lll1_opy_ = bstack1lllll1l11_opy_.bstack11l1lll1111_opy_(config, self.bstack11l1lll111l_opy_)
            self.bstack11l1ll1ll11_opy_()
    def bstack11l1ll11lll_opy_(self):
        return bstack111lll_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨᩕ").format(self.config.get(bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᩖ")), os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᩗ")))
    def bstack11l1lll1ll1_opy_(self):
        try:
            if self.bstack11l1ll11l11_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1ll1ll1l_opy_, bstack111lll_opy_ (u"ࠥࡶࠧᩘ")) as f:
                        bstack11l1lll1lll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1lll1lll_opy_ = set()
                bstack11l1ll1l11l_opy_ = bstack11l1lll1lll_opy_ - self.bstack11l1lll1l1l_opy_
                if not bstack11l1ll1l11l_opy_:
                    return
                self.bstack11l1lll1l1l_opy_.update(bstack11l1ll1l11l_opy_)
                data = {bstack111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤᩙ"): list(self.bstack11l1lll1l1l_opy_), bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣᩚ"): self.config.get(bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᩛ")), bstack111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧᩜ"): os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᩝ")), bstack111lll_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢᩞ"): self.config.get(bstack111lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᩟"))}
            response = bstack11ll1l1lll1_opy_.bstack11l1ll1l111_opy_(self.bstack11l1lll11l1_opy_, data)
            if response.get(bstack111lll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶ᩠ࠦ")) == 200:
                self.logger.debug(bstack111lll_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᩡ").format(data))
            else:
                self.logger.debug(bstack111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᩢ").format(response))
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᩣ").format(e))
    def bstack11l1lll1l11_opy_(self):
        if self.bstack11l1ll11l11_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1ll1ll1l_opy_, bstack111lll_opy_ (u"ࠣࡴࠥᩤ")) as f:
                        bstack11l1ll111ll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1ll111ll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧᩥ").format(failed_count))
                if failed_count >= self.bstack11l1ll1lll1_opy_:
                    self.logger.info(bstack111lll_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᩦ").format(failed_count, self.bstack11l1ll1lll1_opy_))
                    self.bstack11l1ll1llll_opy_(failed_count)
                    self.bstack11l1ll1l1ll_opy_ = True
            return
        try:
            response = bstack11ll1l1lll1_opy_.bstack11l1lll1l11_opy_(bstack111lll_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣᩧ").format(self.bstack11l1lll11l1_opy_, self.config.get(bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᩨ")), os.environ.get(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᩩ")), self.config.get(bstack111lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᩪ"))))
            if response.get(bstack111lll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᩫ")) == 200:
                failed_count = response.get(bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧᩬ"), 0)
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᩭ").format(failed_count))
                if failed_count >= self.bstack11l1ll1lll1_opy_:
                    self.logger.info(bstack111lll_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᩮ").format(failed_count, self.bstack11l1ll1lll1_opy_))
                    self.bstack11l1ll1llll_opy_(failed_count)
                    self.bstack11l1ll1l1ll_opy_ = True
            else:
                self.logger.error(bstack111lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᩯ").format(response))
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢᩰ").format(e))
    def bstack11l1ll1llll_opy_(self, failed_count):
        with open(self.bstack11l1ll11ll1_opy_, bstack111lll_opy_ (u"ࠢࡸࠤᩱ")) as f:
            f.write(bstack111lll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨᩲ").format(datetime.now()))
            f.write(bstack111lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨᩳ").format(failed_count))
        self.logger.debug(bstack111lll_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦᩴ").format(self.bstack11l1ll11ll1_opy_))
    def bstack11l1ll1ll11_opy_(self):
        def bstack11l1lll11ll_opy_():
            while not self.bstack11l1ll1l1ll_opy_:
                time.sleep(bstack11l1ll11l1l_opy_)
                self.bstack11l1lll1ll1_opy_()
                self.bstack11l1lll1l11_opy_()
        bstack11l1llll111_opy_ = threading.Thread(target=bstack11l1lll11ll_opy_, daemon=True)
        bstack11l1llll111_opy_.start()