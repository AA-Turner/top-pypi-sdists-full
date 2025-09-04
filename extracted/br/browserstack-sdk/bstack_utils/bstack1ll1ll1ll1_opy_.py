# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import json
from bstack_utils.bstack11l1111l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11l1l11_opy_(object):
  bstack1lllllll1l_opy_ = os.path.join(os.path.expanduser(bstack1111l1l_opy_ (u"ࠫࢃ࠭ᝐ")), bstack1111l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᝑ"))
  bstack11ll11l1lll_opy_ = os.path.join(bstack1lllllll1l_opy_, bstack1111l1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᝒ"))
  commands_to_wrap = None
  perform_scan = None
  bstack111l11ll1_opy_ = None
  bstack111l1l111_opy_ = None
  bstack11ll1l11l1l_opy_ = None
  bstack11ll1ll1l1l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1111l1l_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᝓ")):
      cls.instance = super(bstack11ll11l1l11_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11l1l1l_opy_()
    return cls.instance
  def bstack11ll11l1l1l_opy_(self):
    try:
      with open(self.bstack11ll11l1lll_opy_, bstack1111l1l_opy_ (u"ࠨࡴࠪ᝔")) as bstack111ll1lll_opy_:
        bstack11ll11l1ll1_opy_ = bstack111ll1lll_opy_.read()
        data = json.loads(bstack11ll11l1ll1_opy_)
        if bstack1111l1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᝕") in data:
          self.bstack11ll1l1l11l_opy_(data[bstack1111l1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ᝖")])
        if bstack1111l1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ᝗") in data:
          self.bstack1l11l1ll_opy_(data[bstack1111l1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭᝘")])
        if bstack1111l1l_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᝙") in data:
          self.bstack11ll11ll111_opy_(data[bstack1111l1l_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᝚")])
    except:
      pass
  def bstack11ll11ll111_opy_(self, bstack11ll1ll1l1l_opy_):
    if bstack11ll1ll1l1l_opy_ != None:
      self.bstack11ll1ll1l1l_opy_ = bstack11ll1ll1l1l_opy_
  def bstack1l11l1ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1111l1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭᝛"),bstack1111l1l_opy_ (u"ࠩࠪ᝜"))
      self.bstack111l11ll1_opy_ = scripts.get(bstack1111l1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧ᝝"),bstack1111l1l_opy_ (u"ࠫࠬ᝞"))
      self.bstack111l1l111_opy_ = scripts.get(bstack1111l1l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩ᝟"),bstack1111l1l_opy_ (u"࠭ࠧᝠ"))
      self.bstack11ll1l11l1l_opy_ = scripts.get(bstack1111l1l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᝡ"),bstack1111l1l_opy_ (u"ࠨࠩᝢ"))
  def bstack11ll1l1l11l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11l1lll_opy_, bstack1111l1l_opy_ (u"ࠩࡺࠫᝣ")) as file:
        json.dump({
          bstack1111l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᝤ"): self.commands_to_wrap,
          bstack1111l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᝥ"): {
            bstack1111l1l_opy_ (u"ࠧࡹࡣࡢࡰࠥᝦ"): self.perform_scan,
            bstack1111l1l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᝧ"): self.bstack111l11ll1_opy_,
            bstack1111l1l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᝨ"): self.bstack111l1l111_opy_,
            bstack1111l1l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᝩ"): self.bstack11ll1l11l1l_opy_
          },
          bstack1111l1l_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨᝪ"): self.bstack11ll1ll1l1l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1111l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᝫ").format(e))
      pass
  def bstack1ll111l11_opy_(self, command_name):
    try:
      return any(command.get(bstack1111l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᝬ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1ll1ll1ll1_opy_ = bstack11ll11l1l11_opy_()