# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import json
from bstack_utils.bstack11lll1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1l111ll_opy_(object):
  bstack11l1llll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll1_opy_ (u"ࠧࡿࠩᜆ")), bstack1l1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᜇ"))
  bstack11ll1l11111_opy_ = os.path.join(bstack11l1llll11_opy_, bstack1l1ll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᜈ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1l111_opy_ = None
  bstack1ll11l1ll1_opy_ = None
  bstack11lll11l11l_opy_ = None
  bstack11ll1l11ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1ll1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᜉ")):
      cls.instance = super(bstack11ll1l111ll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1l111l1_opy_()
    return cls.instance
  def bstack11ll1l111l1_opy_(self):
    try:
      with open(self.bstack11ll1l11111_opy_, bstack1l1ll1_opy_ (u"ࠫࡷ࠭ᜊ")) as bstack1l1l1ll111_opy_:
        bstack11ll1l1111l_opy_ = bstack1l1l1ll111_opy_.read()
        data = json.loads(bstack11ll1l1111l_opy_)
        if bstack1l1ll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᜋ") in data:
          self.bstack11lll11l1l1_opy_(data[bstack1l1ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᜌ")])
        if bstack1l1ll1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᜍ") in data:
          self.bstack1l11lll111_opy_(data[bstack1l1ll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᜎ")])
        if bstack1l1ll1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜏ") in data:
          self.bstack11ll11lllll_opy_(data[bstack1l1ll1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜐ")])
    except:
      pass
  def bstack11ll11lllll_opy_(self, bstack11ll1l11ll1_opy_):
    if bstack11ll1l11ll1_opy_ != None:
      self.bstack11ll1l11ll1_opy_ = bstack11ll1l11ll1_opy_
  def bstack1l11lll111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᜑ"),bstack1l1ll1_opy_ (u"ࠬ࠭ᜒ"))
      self.bstack11l1l111_opy_ = scripts.get(bstack1l1ll1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᜓ"),bstack1l1ll1_opy_ (u"ࠧࠨ᜔"))
      self.bstack1ll11l1ll1_opy_ = scripts.get(bstack1l1ll1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽ᜕ࠬ"),bstack1l1ll1_opy_ (u"ࠩࠪ᜖"))
      self.bstack11lll11l11l_opy_ = scripts.get(bstack1l1ll1_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ᜗"),bstack1l1ll1_opy_ (u"ࠫࠬ᜘"))
  def bstack11lll11l1l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1l11111_opy_, bstack1l1ll1_opy_ (u"ࠬࡽࠧ᜙")) as file:
        json.dump({
          bstack1l1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣ᜚"): self.commands_to_wrap,
          bstack1l1ll1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ᜛"): {
            bstack1l1ll1_opy_ (u"ࠣࡵࡦࡥࡳࠨ᜜"): self.perform_scan,
            bstack1l1ll1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ᜝"): self.bstack11l1l111_opy_,
            bstack1l1ll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ᜞"): self.bstack1ll11l1ll1_opy_,
            bstack1l1ll1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᜟ"): self.bstack11lll11l11l_opy_
          },
          bstack1l1ll1_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᜠ"): self.bstack11ll1l11ll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᜡ").format(e))
      pass
  def bstack11l11lll_opy_(self, bstack1ll111l111l_opy_):
    try:
      return any(command.get(bstack1l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᜢ")) == bstack1ll111l111l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1ll1l1l1l_opy_ = bstack11ll1l111ll_opy_()