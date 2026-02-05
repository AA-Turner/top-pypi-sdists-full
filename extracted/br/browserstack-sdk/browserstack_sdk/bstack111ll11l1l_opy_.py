# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111llll1_opy_():
  def __init__(self, args, logger, bstack1lllll1ll1l_opy_, bstack1lllll111l1_opy_, bstack1llll111l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll1ll1l_opy_ = bstack1lllll1ll1l_opy_
    self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
  def bstack11ll11l1l_opy_(self, bstack1llll11ll1l_opy_, bstack111l1lll1l_opy_, bstack1llll111ll1_opy_=False):
    bstack111llll111_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lllll11ll1_opy_ = manager.list()
    bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
    if bstack1llll111ll1_opy_:
      for index, platform in enumerate(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄯ")]):
        if index == 0:
          bstack111l1lll1l_opy_[bstack11l1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᄰ")] = self.args
        bstack111llll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11ll1l_opy_,
                                                    args=(bstack111l1lll1l_opy_, bstack1lllll11ll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄱ")]):
        bstack111llll111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll11ll1l_opy_,
                                                    args=(bstack111l1lll1l_opy_, bstack1lllll11ll1_opy_)))
    i = 0
    for t in bstack111llll111_opy_:
      try:
        if bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᄲ")):
          os.environ[bstack11l1ll1_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᄳ")] = json.dumps(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄴ")][i % self.bstack1llll111l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᄵ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111llll111_opy_:
      t.join()
    return list(bstack1lllll11ll1_opy_)