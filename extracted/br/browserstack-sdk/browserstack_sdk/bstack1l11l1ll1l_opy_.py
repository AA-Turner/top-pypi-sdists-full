# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11111lll_opy_():
  def __init__(self, args, logger, bstack1111ll11ll_opy_, bstack11111lllll_opy_, bstack11111l1l11_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
    self.bstack11111lllll_opy_ = bstack11111lllll_opy_
    self.bstack11111l1l11_opy_ = bstack11111l1l11_opy_
  def bstack1ll1ll11l_opy_(self, bstack1111l11l1l_opy_, bstack1l1l11lll_opy_, bstack11111l1l1l_opy_=False):
    bstack11l1lllll1_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111ll1ll_opy_ = manager.list()
    bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
    if bstack11111l1l1l_opy_:
      for index, platform in enumerate(self.bstack1111ll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ၇")]):
        if index == 0:
          bstack1l1l11lll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭၈")] = self.args
        bstack11l1lllll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11l1l_opy_,
                                                    args=(bstack1l1l11lll_opy_, bstack11111ll1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ၉")]):
        bstack11l1lllll1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111l11l1l_opy_,
                                                    args=(bstack1l1l11lll_opy_, bstack11111ll1ll_opy_)))
    i = 0
    for t in bstack11l1lllll1_opy_:
      try:
        if bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭၊")):
          os.environ[bstack1l1l1l1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ။")] = json.dumps(self.bstack1111ll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ၌")][i % self.bstack11111l1l11_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣ၍").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1lllll1_opy_:
      t.join()
    return list(bstack11111ll1ll_opy_)