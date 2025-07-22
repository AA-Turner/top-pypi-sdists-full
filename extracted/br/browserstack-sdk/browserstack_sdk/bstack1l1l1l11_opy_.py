# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l1l111l1_opy_():
  def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_, bstack11111l11l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
    self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    self.bstack11111l11l1_opy_ = bstack11111l11l1_opy_
  def bstack1llll11ll1_opy_(self, bstack1111l1ll1l_opy_, bstack1l1l1l11ll_opy_, bstack11111l111l_opy_=False):
    bstack11ll1l111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l11l1l_opy_ = manager.list()
    bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
    if bstack11111l111l_opy_:
      for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")]):
        if index == 0:
          bstack1l1l1l11ll_opy_[bstack111l111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧႁ")] = self.args
        bstack11ll1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1ll1l_opy_,
                                                    args=(bstack1l1l1l11ll_opy_, bstack1111l11l1l_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႂ")]):
        bstack11ll1l111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l1ll1l_opy_,
                                                    args=(bstack1l1l1l11ll_opy_, bstack1111l11l1l_opy_)))
    i = 0
    for t in bstack11ll1l111l_opy_:
      try:
        if bstack1ll1ll11_opy_.get_property(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧႃ")):
          os.environ[bstack111l111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨႄ")] = json.dumps(self.bstack11111l1ll1_opy_[bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႅ")][i % self.bstack11111l11l1_opy_])
      except Exception as e:
        self.logger.debug(bstack111l111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤႆ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll1l111l_opy_:
      t.join()
    return list(bstack1111l11l1l_opy_)