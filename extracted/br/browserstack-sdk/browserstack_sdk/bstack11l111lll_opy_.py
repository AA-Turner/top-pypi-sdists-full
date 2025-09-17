# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1llll111_opy_():
  def __init__(self, args, logger, bstack11111l11ll_opy_, bstack11111l111l_opy_, bstack111111l1ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
    self.bstack11111l111l_opy_ = bstack11111l111l_opy_
    self.bstack111111l1ll_opy_ = bstack111111l1ll_opy_
  def bstack11l11l11ll_opy_(self, bstack1111l111ll_opy_, bstack111lllllll_opy_, bstack111111ll11_opy_=False):
    bstack11111llll_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111l11l1_opy_ = manager.list()
    bstack111lllll11_opy_ = Config.bstack1lll111l1l_opy_()
    if bstack111111ll11_opy_:
      for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႊ")]):
        if index == 0:
          bstack111lllllll_opy_[bstack1l11ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪႋ")] = self.args
        bstack11111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l111ll_opy_,
                                                    args=(bstack111lllllll_opy_, bstack11111l11l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႌ")]):
        bstack11111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l111ll_opy_,
                                                    args=(bstack111lllllll_opy_, bstack11111l11l1_opy_)))
    i = 0
    for t in bstack11111llll_opy_:
      try:
        if bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰႍࠪ")):
          os.environ[bstack1l11ll1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫႎ")] = json.dumps(self.bstack11111l11ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႏ")][i % self.bstack111111l1ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧ႐").format(str(e)))
      i += 1
      t.start()
    for t in bstack11111llll_opy_:
      t.join()
    return list(bstack11111l11l1_opy_)