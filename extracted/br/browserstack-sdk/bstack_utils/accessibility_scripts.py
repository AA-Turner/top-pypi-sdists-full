# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111ll111l11_opy_(object):
  bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"࠭ࡾࠨ᭥")), bstack1ll1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᭦"))
  bstack111ll11l111_opy_ = os.path.join(bstack111l11l11_opy_, bstack1ll1lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ᭧"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack111ll1lll11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫ᭨")):
      cls.instance = super(bstack111ll111l11_opy_, cls).__new__(cls)
      cls.instance.bstack111ll111ll1_opy_()
    return cls.instance
  def bstack111ll111ll1_opy_(self):
    try:
      with open(self.bstack111ll11l111_opy_, bstack1ll1lll_opy_ (u"ࠪࡶࠬ᭩")) as bstack1lll1111ll_opy_:
        bstack111ll111lll_opy_ = bstack1lll1111ll_opy_.read()
        data = json.loads(bstack111ll111lll_opy_)
        if bstack1ll1lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭᭪") in data:
          self.bstack111ll1ll1l1_opy_(data[bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᭫")])
        if bstack1ll1lll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲ᭬ࠬ") in data:
          self.bstack111ll111l1l_opy_(data[bstack1ll1lll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳ࠭᭭")])
        if bstack1ll1lll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᭮") in data:
          self.bstack11lll1ll_opy_(data[bstack1ll1lll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᭯")])
        if bstack1ll1lll_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᭰") in data:
          self.bstack111ll1111ll_opy_(data[bstack1ll1lll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭱")])
    except:
      pass
  def bstack111ll1111ll_opy_(self, bstack111ll1lll11_opy_):
    if bstack111ll1lll11_opy_ != None:
      self.bstack111ll1lll11_opy_ = bstack111ll1lll11_opy_
  def bstack11lll1ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࠪ᭲"),bstack1ll1lll_opy_ (u"࠭ࠧ᭳"))
      self.get_results = scripts.get(bstack1ll1lll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫ᭴"),bstack1ll1lll_opy_ (u"ࠨࠩ᭵"))
      self.get_results_summary = scripts.get(bstack1ll1lll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭᭶"),bstack1ll1lll_opy_ (u"ࠪࠫ᭷"))
      self.save_test_results = scripts.get(bstack1ll1lll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩ᭸"),bstack1ll1lll_opy_ (u"ࠬ࠭᭹"))
  def bstack111ll1ll1l1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111ll111l1l_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111ll11l111_opy_, bstack1ll1lll_opy_ (u"࠭ࡷࠨ᭺")) as file:
        json.dump({
          bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤ᭻"): self.commands_to_wrap,
          bstack1ll1lll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠢ᭼"): self.scripts_to_run,
          bstack1ll1lll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᭽"): {
            bstack1ll1lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᭾"): self.perform_scan,
            bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ᭿"): self.get_results,
            bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᮀ"): self.get_results_summary,
            bstack1ll1lll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᮁ"): self.save_test_results
          },
          bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦᮂ"): self.bstack111ll1lll11_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᮃ").format(e))
      pass
  def bstack1111lll1_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᮄ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111ll111l11_opy_()