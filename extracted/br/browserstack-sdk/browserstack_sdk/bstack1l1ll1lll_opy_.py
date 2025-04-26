# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1ll1111_opy_():
  def __init__(self, args, logger, bstack1111ll1lll_opy_, bstack1111lll1ll_opy_, bstack1111ll11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_
    self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def bstack1l11lll1_opy_(self, bstack1111ll1ll1_opy_, bstack11lllll1ll_opy_, bstack1111ll11l1_opy_=False):
    bstack1ll11ll11l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111ll1l1l_opy_ = manager.list()
    bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
    if bstack1111ll11l1_opy_:
      for index, platform in enumerate(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")]):
        if index == 0:
          bstack11lllll1ll_opy_[bstack1l11lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩဌ")] = self.args
        bstack1ll11ll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1ll1_opy_,
                                                    args=(bstack11lllll1ll_opy_, bstack1111ll1l1l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ")]):
        bstack1ll11ll11l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1ll1_opy_,
                                                    args=(bstack11lllll1ll_opy_, bstack1111ll1l1l_opy_)))
    i = 0
    for t in bstack1ll11ll11l_opy_:
      try:
        if bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩဎ")):
          os.environ[bstack1l11lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪဏ")] = json.dumps(self.bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭တ")][i % self.bstack1111ll11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦထ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11ll11l_opy_:
      t.join()
    return list(bstack1111ll1l1l_opy_)