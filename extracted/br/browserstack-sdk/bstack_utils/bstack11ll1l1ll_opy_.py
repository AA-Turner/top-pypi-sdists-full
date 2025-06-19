# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
from bstack_utils.bstack1111ll111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1ll1l11_opy_(object):
  bstack11lllllll_opy_ = os.path.join(os.path.expanduser(bstack111lll_opy_ (u"ࠩࢁࠫᛗ")), bstack111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᛘ"))
  bstack11ll1ll1lll_opy_ = os.path.join(bstack11lllllll_opy_, bstack111lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᛙ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11llll11l_opy_ = None
  bstack11llllll1l_opy_ = None
  bstack11ll1lllll1_opy_ = None
  bstack11lll1111ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111lll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᛚ")):
      cls.instance = super(bstack11ll1ll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1lll111_opy_()
    return cls.instance
  def bstack11ll1lll111_opy_(self):
    try:
      with open(self.bstack11ll1ll1lll_opy_, bstack111lll_opy_ (u"࠭ࡲࠨᛛ")) as bstack1l1lll1l_opy_:
        bstack11ll1ll1l1l_opy_ = bstack1l1lll1l_opy_.read()
        data = json.loads(bstack11ll1ll1l1l_opy_)
        if bstack111lll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛜ") in data:
          self.bstack11lll1lll11_opy_(data[bstack111lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᛝ")])
        if bstack111lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᛞ") in data:
          self.bstack1ll1l11l1_opy_(data[bstack111lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᛟ")])
        if bstack111lll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛠ") in data:
          self.bstack11ll1ll1ll1_opy_(data[bstack111lll_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛡ")])
    except:
      pass
  def bstack11ll1ll1ll1_opy_(self, bstack11lll1111ll_opy_):
    if bstack11lll1111ll_opy_ != None:
      self.bstack11lll1111ll_opy_ = bstack11lll1111ll_opy_
  def bstack1ll1l11l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111lll_opy_ (u"࠭ࡳࡤࡣࡱࠫᛢ"),bstack111lll_opy_ (u"ࠧࠨᛣ"))
      self.bstack11llll11l_opy_ = scripts.get(bstack111lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᛤ"),bstack111lll_opy_ (u"ࠩࠪᛥ"))
      self.bstack11llllll1l_opy_ = scripts.get(bstack111lll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᛦ"),bstack111lll_opy_ (u"ࠫࠬᛧ"))
      self.bstack11ll1lllll1_opy_ = scripts.get(bstack111lll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᛨ"),bstack111lll_opy_ (u"࠭ࠧᛩ"))
  def bstack11lll1lll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1ll1lll_opy_, bstack111lll_opy_ (u"ࠧࡸࠩᛪ")) as file:
        json.dump({
          bstack111lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ᛫"): self.commands_to_wrap,
          bstack111lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᛬"): {
            bstack111lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᛭"): self.perform_scan,
            bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᛮ"): self.bstack11llll11l_opy_,
            bstack111lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᛯ"): self.bstack11llllll1l_opy_,
            bstack111lll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᛰ"): self.bstack11ll1lllll1_opy_
          },
          bstack111lll_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦᛱ"): self.bstack11lll1111ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᛲ").format(e))
      pass
  def bstack1l1ll1lll_opy_(self, bstack1ll1l11111l_opy_):
    try:
      return any(command.get(bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛳ")) == bstack1ll1l11111l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11ll1l1ll_opy_ = bstack11ll1ll1l11_opy_()