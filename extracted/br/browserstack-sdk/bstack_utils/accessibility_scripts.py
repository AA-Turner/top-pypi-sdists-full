# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l11l111_opy_(object):
  bstack1ll11l11ll_opy_ = os.path.join(os.path.expanduser(bstack111ll_opy_ (u"࠭ࡾࠨᶜ")), bstack111ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᶝ"))
  bstack1111l111l11_opy_ = os.path.join(bstack1ll11l11ll_opy_, bstack111ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᶞ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111ll1l1ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111ll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᶟ")):
      cls.instance = super(bstack1111l11l111_opy_, cls).__new__(cls)
      cls.instance.bstack1111l111lll_opy_()
    return cls.instance
  def bstack1111l111lll_opy_(self):
    try:
      with open(self.bstack1111l111l11_opy_, bstack111ll_opy_ (u"ࠪࡶࠬᶠ")) as bstack1llll11l1l_opy_:
        bstack1111l1111ll_opy_ = bstack1llll11l1l_opy_.read()
        data = json.loads(bstack1111l1111ll_opy_)
        if bstack111ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᶡ") in data:
          self.bstack1l1l1111l11_opy_(data[bstack111ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᶢ")])
        if bstack111ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬᶣ") in data:
          self.bstack1111l111l1l_opy_(data[bstack111ll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳ࠭ᶤ")])
        if bstack111ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᶥ") in data:
          self.bstack11ll111l11_opy_(data[bstack111ll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᶦ")])
        if bstack111ll_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶧ") in data:
          self.bstack1111l111ll1_opy_(data[bstack111ll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᶨ")])
    except:
      pass
  def bstack1111l111ll1_opy_(self, bstack1111ll1l1ll_opy_):
    if bstack1111ll1l1ll_opy_ != None:
      self.bstack1111ll1l1ll_opy_ = bstack1111ll1l1ll_opy_
  def bstack11ll111l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111ll_opy_ (u"ࠬࡹࡣࡢࡰࠪᶩ"),bstack111ll_opy_ (u"࠭ࠧᶪ"))
      self.get_results = scripts.get(bstack111ll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᶫ"),bstack111ll_opy_ (u"ࠨࠩᶬ"))
      self.get_results_summary = scripts.get(bstack111ll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᶭ"),bstack111ll_opy_ (u"ࠪࠫᶮ"))
      self.save_test_results = scripts.get(bstack111ll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᶯ"),bstack111ll_opy_ (u"ࠬ࠭ᶰ"))
  def bstack1l1l1111l11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l111l1l_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l111l11_opy_, bstack111ll_opy_ (u"࠭ࡷࠨᶱ")) as file:
        json.dump({
          bstack111ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤᶲ"): self.commands_to_wrap,
          bstack111ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠢᶳ"): self.scripts_to_run,
          bstack111ll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥᶴ"): {
            bstack111ll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᶵ"): self.perform_scan,
            bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᶶ"): self.get_results,
            bstack111ll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᶷ"): self.get_results_summary,
            bstack111ll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᶸ"): self.save_test_results
          },
          bstack111ll_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦᶹ"): self.bstack1111ll1l1ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᶺ").format(e))
      pass
  def bstack111l11ll1_opy_(self, command_name):
    try:
      return any(command.get(bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᶻ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l11l111_opy_()