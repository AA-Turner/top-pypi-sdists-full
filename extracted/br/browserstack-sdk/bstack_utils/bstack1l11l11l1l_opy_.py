# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111llll1lll_opy_(object):
  bstack111l11llll_opy_ = os.path.join(os.path.expanduser(bstack1lll1l_opy_ (u"ࠫࢃ࠭ᩧ")), bstack1lll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᩨ"))
  bstack111llll1ll1_opy_ = os.path.join(bstack111l11llll_opy_, bstack1lll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᩩ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll1lllll1_opy_ = None
  bstack11l1l1llll_opy_ = None
  bstack11l1111l111_opy_ = None
  bstack11l111ll111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1lll1l_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᩪ")):
      cls.instance = super(bstack111llll1lll_opy_, cls).__new__(cls)
      cls.instance.bstack111lllll111_opy_()
    return cls.instance
  def bstack111lllll111_opy_(self):
    try:
      with open(self.bstack111llll1ll1_opy_, bstack1lll1l_opy_ (u"ࠨࡴࠪᩫ")) as bstack111ll1l111_opy_:
        bstack111lllll11l_opy_ = bstack111ll1l111_opy_.read()
        data = json.loads(bstack111lllll11l_opy_)
        if bstack1lll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᩬ") in data:
          self.bstack11l1111ll11_opy_(data[bstack1lll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᩭ")])
        if bstack1lll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᩮ") in data:
          self.bstack11l1l1lll_opy_(data[bstack1lll1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᩯ")])
        if bstack1lll1l_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᩰ") in data:
          self.bstack111llll1l1l_opy_(data[bstack1lll1l_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᩱ")])
    except:
      pass
  def bstack111llll1l1l_opy_(self, bstack11l111ll111_opy_):
    if bstack11l111ll111_opy_ != None:
      self.bstack11l111ll111_opy_ = bstack11l111ll111_opy_
  def bstack11l1l1lll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1lll1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᩲ"),bstack1lll1l_opy_ (u"ࠩࠪᩳ"))
      self.bstack1ll1lllll1_opy_ = scripts.get(bstack1lll1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᩴ"),bstack1lll1l_opy_ (u"ࠫࠬ᩵"))
      self.bstack11l1l1llll_opy_ = scripts.get(bstack1lll1l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩ᩶"),bstack1lll1l_opy_ (u"࠭ࠧ᩷"))
      self.bstack11l1111l111_opy_ = scripts.get(bstack1lll1l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬ᩸"),bstack1lll1l_opy_ (u"ࠨࠩ᩹"))
  def bstack11l1111ll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack111llll1ll1_opy_, bstack1lll1l_opy_ (u"ࠩࡺࠫ᩺")) as file:
        json.dump({
          bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧ᩻"): self.commands_to_wrap,
          bstack1lll1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧ᩼"): {
            bstack1lll1l_opy_ (u"ࠧࡹࡣࡢࡰࠥ᩽"): self.perform_scan,
            bstack1lll1l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥ᩾"): self.bstack1ll1lllll1_opy_,
            bstack1lll1l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼ᩿ࠦ"): self.bstack11l1l1llll_opy_,
            bstack1lll1l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨ᪀"): self.bstack11l1111l111_opy_
          },
          bstack1lll1l_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨ᪁"): self.bstack11l111ll111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1lll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣ᪂").format(e))
      pass
  def bstack11ll1l111l_opy_(self, command_name):
    try:
      return any(command.get(bstack1lll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᪃")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l11l1l_opy_ = bstack111llll1lll_opy_()