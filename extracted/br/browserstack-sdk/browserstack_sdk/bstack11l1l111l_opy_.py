# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l11111ll_opy_():
  def __init__(self, args, logger, bstack11111ll1ll_opy_, bstack11111ll11l_opy_, bstack11111l111l_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
    self.bstack11111l111l_opy_ = bstack11111l111l_opy_
  def bstack1l11l1lll_opy_(self, bstack1111l11lll_opy_, bstack1l11l1l1l1_opy_, bstack11111l11l1_opy_=False):
    bstack11l1l111ll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1l111_opy_ = manager.list()
    bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
    if bstack11111l11l1_opy_:
      for index, platform in enumerate(self.bstack11111ll1ll_opy_[bstack1l1l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႇ")]):
        if index == 0:
          bstack1l11l1l1l1_opy_[bstack1l1l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧႈ")] = self.args
        bstack11l1l111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11lll_opy_,
                                                    args=(bstack1l11l1l1l1_opy_, bstack1111l1l111_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111ll1ll_opy_[bstack1l1l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႉ")]):
        bstack11l1l111ll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11lll_opy_,
                                                    args=(bstack1l11l1l1l1_opy_, bstack1111l1l111_opy_)))
    i = 0
    for t in bstack11l1l111ll_opy_:
      try:
        if bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧႊ")):
          os.environ[bstack1l1l1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨႋ")] = json.dumps(self.bstack11111ll1ll_opy_[bstack1l1l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႌ")][i % self.bstack11111l111l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤႍ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1l111ll_opy_:
      t.join()
    return list(bstack1111l1l111_opy_)