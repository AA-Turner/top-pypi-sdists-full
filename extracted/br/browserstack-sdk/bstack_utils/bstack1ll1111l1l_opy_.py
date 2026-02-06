# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l11lll11l_opy_(object):
  bstack1111l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠬࢄࠧᢌ")), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᢍ"))
  bstack11l11llll11_opy_ = os.path.join(bstack1111l11ll_opy_, bstack11lllll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᢎ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1l1l1ll_opy_ = None
  bstack111lll1l1_opy_ = None
  bstack11l1l1l11l1_opy_ = None
  bstack11l1l1l111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11lllll_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᢏ")):
      cls.instance = super(bstack11l11lll11l_opy_, cls).__new__(cls)
      cls.instance.bstack11l11lll1ll_opy_()
    return cls.instance
  def bstack11l11lll1ll_opy_(self):
    try:
      with open(self.bstack11l11llll11_opy_, bstack11lllll_opy_ (u"ࠩࡵࠫᢐ")) as bstack1111ll1l1_opy_:
        bstack11l11lll111_opy_ = bstack1111ll1l1_opy_.read()
        data = json.loads(bstack11l11lll111_opy_)
        if bstack11lllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᢑ") in data:
          self.bstack11l1ll111l1_opy_(data[bstack11lllll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᢒ")])
        if bstack11lllll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᢓ") in data:
          self.bstack1l11l11ll1_opy_(data[bstack11lllll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᢔ")])
        if bstack11lllll_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᢕ") in data:
          self.bstack11l11lll1l1_opy_(data[bstack11lllll_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᢖ")])
    except:
      pass
  def bstack11l11lll1l1_opy_(self, bstack11l1l1l111l_opy_):
    if bstack11l1l1l111l_opy_ != None:
      self.bstack11l1l1l111l_opy_ = bstack11l1l1l111l_opy_
  def bstack1l11l11ll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11lllll_opy_ (u"ࠩࡶࡧࡦࡴࠧᢗ"),bstack11lllll_opy_ (u"ࠪࠫᢘ"))
      self.bstack11l1l1l1ll_opy_ = scripts.get(bstack11lllll_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᢙ"),bstack11lllll_opy_ (u"ࠬ࠭ᢚ"))
      self.bstack111lll1l1_opy_ = scripts.get(bstack11lllll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᢛ"),bstack11lllll_opy_ (u"ࠧࠨᢜ"))
      self.bstack11l1l1l11l1_opy_ = scripts.get(bstack11lllll_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᢝ"),bstack11lllll_opy_ (u"ࠩࠪᢞ"))
  def bstack11l1ll111l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l11llll11_opy_, bstack11lllll_opy_ (u"ࠪࡻࠬᢟ")) as file:
        json.dump({
          bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨᢠ"): self.commands_to_wrap,
          bstack11lllll_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨᢡ"): {
            bstack11lllll_opy_ (u"ࠨࡳࡤࡣࡱࠦᢢ"): self.perform_scan,
            bstack11lllll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᢣ"): self.bstack11l1l1l1ll_opy_,
            bstack11lllll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᢤ"): self.bstack111lll1l1_opy_,
            bstack11lllll_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᢥ"): self.bstack11l1l1l11l1_opy_
          },
          bstack11lllll_opy_ (u"ࠥࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠢᢦ"): self.bstack11l1l1l111l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠿ࠦࡻࡾࠤᢧ").format(e))
      pass
  def bstack1ll111ll_opy_(self, command_name):
    try:
      return any(command.get(bstack11lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢨ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1ll1111l1l_opy_ = bstack11l11lll11l_opy_()