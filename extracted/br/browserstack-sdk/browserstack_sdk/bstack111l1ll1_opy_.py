# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1l1l1_opy_():
  def __init__(self, args, logger, bstack11111lll1l_opy_, bstack11111ll1ll_opy_, bstack11111l11l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111lll1l_opy_ = bstack11111lll1l_opy_
    self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    self.bstack11111l11l1_opy_ = bstack11111l11l1_opy_
  def bstack11ll111ll1_opy_(self, bstack1111l1llll_opy_, bstack11l1ll1l11_opy_, bstack11111l111l_opy_=False):
    bstack11ll11l11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l111l1_opy_ = manager.list()
    bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
    if bstack11111l111l_opy_:
      for index, platform in enumerate(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႇ")]):
        if index == 0:
          bstack11l1ll1l11_opy_[bstack1111lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧႈ")] = self.args
        bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1llll_opy_,
                                                    args=(bstack11l1ll1l11_opy_, bstack1111l111l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႉ")]):
        bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1llll_opy_,
                                                    args=(bstack11l1ll1l11_opy_, bstack1111l111l1_opy_)))
    i = 0
    for t in bstack11ll11l11_opy_:
      try:
        if bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧႊ")):
          os.environ[bstack1111lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨႋ")] = json.dumps(self.bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႌ")][i % self.bstack11111l11l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤႍ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll11l11_opy_:
      t.join()
    return list(bstack1111l111l1_opy_)