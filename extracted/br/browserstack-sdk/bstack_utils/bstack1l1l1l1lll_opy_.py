# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1ll1llll1lll_opy_(object):
  bstack111l1ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠫࢃ࠭∲")), bstack1ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ∳"))
  bstack1ll1llll1ll1_opy_ = os.path.join(bstack111l1ll11_opy_, bstack1ll111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭∴"))
  commands_to_wrap = None
  perform_scan = None
  bstack111111l1_opy_ = None
  bstack111ll1111l_opy_ = None
  bstack1lll1111lll1_opy_ = None
  bstack1lll11ll111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll111_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩ∵")):
      cls.instance = super(bstack1ll1llll1lll_opy_, cls).__new__(cls)
      cls.instance.bstack1ll1lllll111_opy_()
    return cls.instance
  def bstack1ll1lllll111_opy_(self):
    try:
      with open(self.bstack1ll1llll1ll1_opy_, bstack1ll111_opy_ (u"ࠨࡴࠪ∶")) as bstack111l1l1l1l_opy_:
        bstack1ll1llll1l1l_opy_ = bstack111l1l1l1l_opy_.read()
        data = json.loads(bstack1ll1llll1l1l_opy_)
        if bstack1ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ∷") in data:
          self.bstack1lll11lll1ll_opy_(data[bstack1ll111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ∸")])
        if bstack1ll111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ∹") in data:
          self.bstack1lllll1l1_opy_(data[bstack1ll111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭∺")])
        if bstack1ll111_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ∻") in data:
          self.bstack1lll11l1lll1_opy_(data[bstack1ll111_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ∼")])
    except:
      pass
  def bstack1lll11l1lll1_opy_(self, bstack1lll11ll111l_opy_):
    if bstack1lll11ll111l_opy_ != None:
      self.bstack1lll11ll111l_opy_ = bstack1lll11ll111l_opy_
  def bstack1lllll1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll111_opy_ (u"ࠨࡵࡦࡥࡳ࠭∽"),bstack1ll111_opy_ (u"ࠩࠪ∾"))
      self.bstack111111l1_opy_ = scripts.get(bstack1ll111_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧ∿"),bstack1ll111_opy_ (u"ࠫࠬ≀"))
      self.bstack111ll1111l_opy_ = scripts.get(bstack1ll111_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩ≁"),bstack1ll111_opy_ (u"࠭ࠧ≂"))
      self.bstack1lll1111lll1_opy_ = scripts.get(bstack1ll111_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬ≃"),bstack1ll111_opy_ (u"ࠨࠩ≄"))
  def bstack1lll11lll1ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack1ll1llll1ll1_opy_, bstack1ll111_opy_ (u"ࠩࡺࠫ≅")) as file:
        json.dump({
          bstack1ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧ≆"): self.commands_to_wrap,
          bstack1ll111_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧ≇"): {
            bstack1ll111_opy_ (u"ࠧࡹࡣࡢࡰࠥ≈"): self.perform_scan,
            bstack1ll111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥ≉"): self.bstack111111l1_opy_,
            bstack1ll111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦ≊"): self.bstack111ll1111l_opy_,
            bstack1ll111_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨ≋"): self.bstack1lll1111lll1_opy_
          },
          bstack1ll111_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨ≌"): self.bstack1lll11ll111l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣ≍").format(e))
      pass
  def bstack1ll1l1111_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ≎")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l1l1l1lll_opy_ = bstack1ll1llll1lll_opy_()