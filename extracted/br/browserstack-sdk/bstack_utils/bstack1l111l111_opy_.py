# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111llll1ll1_opy_(object):
  bstack11llll111_opy_ = os.path.join(os.path.expanduser(bstack1111_opy_ (u"ࠬࢄࠧᩨ")), bstack1111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᩩ"))
  bstack111llll1l11_opy_ = os.path.join(bstack11llll111_opy_, bstack1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧᩪ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1llll11_opy_ = None
  bstack1ll1llll_opy_ = None
  bstack11l111l11l1_opy_ = None
  bstack11l1111l111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1111_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪᩫ")):
      cls.instance = super(bstack111llll1ll1_opy_, cls).__new__(cls)
      cls.instance.bstack111llll1l1l_opy_()
    return cls.instance
  def bstack111llll1l1l_opy_(self):
    try:
      with open(self.bstack111llll1l11_opy_, bstack1111_opy_ (u"ࠩࡵࠫᩬ")) as bstack1llllllll_opy_:
        bstack111llll1lll_opy_ = bstack1llllllll_opy_.read()
        data = json.loads(bstack111llll1lll_opy_)
        if bstack1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᩭ") in data:
          self.bstack11l1111l11l_opy_(data[bstack1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᩮ")])
        if bstack1111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᩯ") in data:
          self.bstack11ll1111l_opy_(data[bstack1111_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᩰ")])
        if bstack1111_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᩱ") in data:
          self.bstack111llll11ll_opy_(data[bstack1111_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᩲ")])
    except:
      pass
  def bstack111llll11ll_opy_(self, bstack11l1111l111_opy_):
    if bstack11l1111l111_opy_ != None:
      self.bstack11l1111l111_opy_ = bstack11l1111l111_opy_
  def bstack11ll1111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1111_opy_ (u"ࠩࡶࡧࡦࡴࠧᩳ"),bstack1111_opy_ (u"ࠪࠫᩴ"))
      self.bstack1l1llll11_opy_ = scripts.get(bstack1111_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨ᩵"),bstack1111_opy_ (u"ࠬ࠭᩶"))
      self.bstack1ll1llll_opy_ = scripts.get(bstack1111_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪ᩷"),bstack1111_opy_ (u"ࠧࠨ᩸"))
      self.bstack11l111l11l1_opy_ = scripts.get(bstack1111_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭᩹"),bstack1111_opy_ (u"ࠩࠪ᩺"))
  def bstack11l1111l11l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack111llll1l11_opy_, bstack1111_opy_ (u"ࠪࡻࠬ᩻")) as file:
        json.dump({
          bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨ᩼"): self.commands_to_wrap,
          bstack1111_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸࠨ᩽"): {
            bstack1111_opy_ (u"ࠨࡳࡤࡣࡱࠦ᩾"): self.perform_scan,
            bstack1111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶ᩿ࠦ"): self.bstack1l1llll11_opy_,
            bstack1111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧ᪀"): self.bstack1ll1llll_opy_,
            bstack1111_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ᪁"): self.bstack11l111l11l1_opy_
          },
          bstack1111_opy_ (u"ࠥࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠢ᪂"): self.bstack11l1111l111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠿ࠦࡻࡾࠤ᪃").format(e))
      pass
  def bstack1ll1111111_opy_(self, command_name):
    try:
      return any(command.get(bstack1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᪄")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l111l111_opy_ = bstack111llll1ll1_opy_()