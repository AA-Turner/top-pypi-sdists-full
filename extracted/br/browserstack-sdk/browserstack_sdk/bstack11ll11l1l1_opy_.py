# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11ll1llll1_opy_():
  def __init__(self, args, logger, bstack1llll1lll11_opy_, bstack1llll1111l1_opy_, bstack1lll1lll111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
    self.bstack1lll1lll111_opy_ = bstack1lll1lll111_opy_
  def bstack1lllll111_opy_(self, bstack1llll11l1ll_opy_, bstack1lllll1l11_opy_, bstack1lll1lll11l_opy_=False):
    bstack11ll11111_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll11lll1_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll1lll11l_opy_:
      for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᆆ")]):
        if index == 0:
          bstack1lllll1l11_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᆇ")] = self.args
        bstack11ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11l1ll_opy_,
                                                    args=(bstack1lllll1l11_opy_, bstack1llll11lll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᆈ")]):
        bstack11ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11l1ll_opy_,
                                                    args=(bstack1lllll1l11_opy_, bstack1llll11lll1_opy_)))
    i = 0
    for t in bstack11ll11111_opy_:
      try:
        if global_config.get_property(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪᆉ")):
          os.environ[bstack11l1l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫᆊ")] = json.dumps(self.bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᆋ")][i % self.bstack1lll1lll111_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧᆌ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll11111_opy_:
      t.join()
    return list(bstack1llll11lll1_opy_)