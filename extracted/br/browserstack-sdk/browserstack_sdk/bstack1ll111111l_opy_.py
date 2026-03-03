# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll11llll1_opy_():
  def __init__(self, args, logger, bstack1llll111l1l_opy_, bstack1llll11ll1l_opy_, bstack1lll1lll111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
    self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
    self.bstack1lll1lll111_opy_ = bstack1lll1lll111_opy_
  def bstack1111llll_opy_(self, bstack1llll1lll1l_opy_, bstack1ll111l1l1_opy_, bstack1lll1ll1lll_opy_=False):
    bstack11ll111l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll1llll1_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll1ll1lll_opy_:
      for index, platform in enumerate(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆂ")]):
        if index == 0:
          bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᆃ")] = self.args
        bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1lll1l_opy_,
                                                    args=(bstack1ll111l1l1_opy_, bstack1llll1llll1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᆄ")]):
        bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1lll1l_opy_,
                                                    args=(bstack1ll111l1l1_opy_, bstack1llll1llll1_opy_)))
    i = 0
    for t in bstack11ll111l_opy_:
      try:
        if global_config.get_property(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᆅ")):
          os.environ[bstack11ll111_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧᆆ")] = json.dumps(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᆇ")][i % self.bstack1lll1lll111_opy_])
      except Exception as e:
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣᆈ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11ll111l_opy_:
      t.join()
    return list(bstack1llll1llll1_opy_)