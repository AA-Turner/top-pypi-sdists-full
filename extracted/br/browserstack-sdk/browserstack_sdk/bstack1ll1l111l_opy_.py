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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1lll1lll11_opy_():
  def __init__(self, args, logger, bstack1lllll1111l_opy_, bstack1llll1lll11_opy_, bstack1ll111ll111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll1111l_opy_ = bstack1lllll1111l_opy_
    self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    self.bstack1ll111ll111_opy_ = bstack1ll111ll111_opy_
  def bstack1ll1lll111_opy_(self, bstack1ll11ll11ll_opy_, bstack1l1l11l1l1_opy_, bstack1ll111l1lll_opy_=False):
    bstack11ll1ll1l1_opy_ = multiprocessing.get_context(bstack1l1111l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᎫ"))
    bstack1l11111lll_opy_ = []
    manager = bstack11ll1ll1l1_opy_.Manager()
    bstack1ll111llll1_opy_ = manager.list()
    global_config = Config.bstack111111l1ll_opy_()
    if bstack1ll111l1lll_opy_:
      for index, platform in enumerate(self.bstack1lllll1111l_opy_[bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꭼ")]):
        if index == 0:
          bstack1l1l11l1l1_opy_[bstack1l1111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᎭ")] = self.args
        bstack1l11111lll_opy_.append(bstack11ll1ll1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11ll11ll_opy_,
                                          args=(bstack1l1l11l1l1_opy_, bstack1ll111llll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll1111l_opy_[bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎮ")]):
        bstack1l11111lll_opy_.append(bstack11ll1ll1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11ll11ll_opy_,
                                          args=(bstack1l1l11l1l1_opy_, bstack1ll111llll1_opy_)))
    i = 0
    for t in bstack1l11111lll_opy_:
      try:
        if global_config.get_property(bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᎯ")):
          os.environ[bstack1l1111l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᎰ")] = json.dumps(self.bstack1lllll1111l_opy_[bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎱ")][i % self.bstack1ll111ll111_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᎲ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l11111lll_opy_:
      t.join()
    return list(bstack1ll111llll1_opy_)