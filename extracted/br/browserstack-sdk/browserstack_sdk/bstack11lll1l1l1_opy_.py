# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111l1ll111_opy_():
  def __init__(self, args, logger, bstack1llll1l1lll_opy_, bstack1lllll11l1l_opy_, bstack1llll111ll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1l1lll_opy_ = bstack1llll1l1lll_opy_
    self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
  def bstack111ll1l11_opy_(self, bstack1lllll1l111_opy_, bstack1111111l1_opy_, bstack1llll111lll_opy_=False):
    bstack111l11ll11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll11llll_opy_ = manager.list()
    bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
    if bstack1llll111lll_opy_:
      for index, platform in enumerate(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄪ")]):
        if index == 0:
          bstack1111111l1_opy_[bstack1l1111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᄫ")] = self.args
        bstack111l11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lllll1l111_opy_,
                                                    args=(bstack1111111l1_opy_, bstack1llll11llll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᄬ")]):
        bstack111l11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lllll1l111_opy_,
                                                    args=(bstack1111111l1_opy_, bstack1llll11llll_opy_)))
    i = 0
    for t in bstack111l11ll11_opy_:
      try:
        if bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᄭ")):
          os.environ[bstack1l1111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪᄮ")] = json.dumps(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄯ")][i % self.bstack1llll111ll1_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦᄰ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111l11ll11_opy_:
      t.join()
    return list(bstack1llll11llll_opy_)