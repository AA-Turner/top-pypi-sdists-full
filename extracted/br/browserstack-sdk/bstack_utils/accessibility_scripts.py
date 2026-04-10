# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l1l1111_opy_(object):
  bstack1lllll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠨࢀࠪᵦ")), bstack1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᵧ"))
  bstack1111l11l1ll_opy_ = os.path.join(bstack1lllll11ll_opy_, bstack1ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪᵨ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111ll11l11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ᵩ")):
      cls.instance = super(bstack1111l1l1111_opy_, cls).__new__(cls)
      cls.instance.bstack1111l11llll_opy_()
    return cls.instance
  def bstack1111l11llll_opy_(self):
    try:
      with open(self.bstack1111l11l1ll_opy_, bstack1ll_opy_ (u"ࠬࡸࠧᵪ")) as bstack11lll11l_opy_:
        bstack1111l11ll1l_opy_ = bstack11lll11l_opy_.read()
        data = json.loads(bstack1111l11ll1l_opy_)
        if bstack1ll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᵫ") in data:
          self.bstack1l1l1l1l111_opy_(data[bstack1ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᵬ")])
        if bstack1ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧᵭ") in data:
          self.bstack1111l11ll11_opy_(data[bstack1ll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࡗࡳࡗࡻ࡮ࠨᵮ")])
        if bstack1ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᵯ") in data:
          self.bstack11lll1l1_opy_(data[bstack1ll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᵰ")])
        if bstack1ll_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵱ") in data:
          self.bstack1111l11lll1_opy_(data[bstack1ll_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵲ")])
    except:
      pass
  def bstack1111l11lll1_opy_(self, bstack1111ll11l11_opy_):
    if bstack1111ll11l11_opy_ != None:
      self.bstack1111ll11l11_opy_ = bstack1111ll11l11_opy_
  def bstack11lll1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll_opy_ (u"ࠧࡴࡥࡤࡲࠬᵳ"),bstack1ll_opy_ (u"ࠨࠩᵴ"))
      self.get_results = scripts.get(bstack1ll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᵵ"),bstack1ll_opy_ (u"ࠪࠫᵶ"))
      self.get_results_summary = scripts.get(bstack1ll_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᵷ"),bstack1ll_opy_ (u"ࠬ࠭ᵸ"))
      self.save_test_results = scripts.get(bstack1ll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᵹ"),bstack1ll_opy_ (u"ࠧࠨᵺ"))
  def bstack1l1l1l1l111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l11ll11_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l11l1ll_opy_, bstack1ll_opy_ (u"ࠨࡹࠪᵻ")) as file:
        json.dump({
          bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᵼ"): self.commands_to_wrap,
          bstack1ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠤᵽ"): self.scripts_to_run,
          bstack1ll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᵾ"): {
            bstack1ll_opy_ (u"ࠧࡹࡣࡢࡰࠥᵿ"): self.perform_scan,
            bstack1ll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᶀ"): self.get_results,
            bstack1ll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᶁ"): self.get_results_summary,
            bstack1ll_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᶂ"): self.save_test_results
          },
          bstack1ll_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨᶃ"): self.bstack1111ll11l11_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᶄ").format(e))
      pass
  def bstack1l1llllll_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᶅ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l1l1111_opy_()