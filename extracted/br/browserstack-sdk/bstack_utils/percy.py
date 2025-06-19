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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l1ll1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l111l1_opy_ import bstack11l1l111_opy_
class bstack11l1ll1l11_opy_:
  working_dir = os.getcwd()
  bstack1111l1lll_opy_ = False
  config = {}
  bstack11l1l11ll1l_opy_ = bstack111lll_opy_ (u"ࠨࠩᶐ")
  binary_path = bstack111lll_opy_ (u"ࠩࠪᶑ")
  bstack111l1l11ll1_opy_ = bstack111lll_opy_ (u"ࠪࠫᶒ")
  bstack1l1ll1ll1_opy_ = False
  bstack111ll111111_opy_ = None
  bstack111l1l11lll_opy_ = {}
  bstack111l1l1ll11_opy_ = 300
  bstack111ll11111l_opy_ = False
  logger = None
  bstack111l11l111l_opy_ = False
  bstack11lll1lll1_opy_ = False
  percy_build_id = None
  bstack111l1ll1l1l_opy_ = bstack111lll_opy_ (u"ࠫࠬᶓ")
  bstack111l1lll111_opy_ = {
    bstack111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᶔ") : 1,
    bstack111lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᶕ") : 2,
    bstack111lll_opy_ (u"ࠧࡦࡦࡪࡩࠬᶖ") : 3,
    bstack111lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᶗ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l1ll11ll_opy_(self):
    bstack111l11ll111_opy_ = bstack111lll_opy_ (u"ࠩࠪᶘ")
    bstack111ll111ll1_opy_ = sys.platform
    bstack111l1111lll_opy_ = bstack111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᶙ")
    if re.match(bstack111lll_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᶚ"), bstack111ll111ll1_opy_) != None:
      bstack111l11ll111_opy_ = bstack11l1lllllll_opy_ + bstack111lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᶛ")
      self.bstack111l1ll1l1l_opy_ = bstack111lll_opy_ (u"࠭࡭ࡢࡥࠪᶜ")
    elif re.match(bstack111lll_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᶝ"), bstack111ll111ll1_opy_) != None:
      bstack111l11ll111_opy_ = bstack11l1lllllll_opy_ + bstack111lll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᶞ")
      bstack111l1111lll_opy_ = bstack111lll_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᶟ")
      self.bstack111l1ll1l1l_opy_ = bstack111lll_opy_ (u"ࠪࡻ࡮ࡴࠧᶠ")
    else:
      bstack111l11ll111_opy_ = bstack11l1lllllll_opy_ + bstack111lll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᶡ")
      self.bstack111l1ll1l1l_opy_ = bstack111lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᶢ")
    return bstack111l11ll111_opy_, bstack111l1111lll_opy_
  def bstack111l1lll1l1_opy_(self):
    try:
      bstack111l11l11l1_opy_ = [os.path.join(expanduser(bstack111lll_opy_ (u"ࠨࡾࠣᶣ")), bstack111lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᶤ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l11l11l1_opy_:
        if(self.bstack111l1l1l1l1_opy_(path)):
          return path
      raise bstack111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᶥ")
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᶦ").format(e))
  def bstack111l1l1l1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111l1ll1l11_opy_(self, bstack111l11lllll_opy_):
    return os.path.join(bstack111l11lllll_opy_, self.bstack11l1l11ll1l_opy_ + bstack111lll_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤᶧ"))
  def bstack111l11llll1_opy_(self, bstack111l11lllll_opy_, bstack111l111l11l_opy_):
    if not bstack111l111l11l_opy_: return
    try:
      bstack111l1llllll_opy_ = self.bstack111l1ll1l11_opy_(bstack111l11lllll_opy_)
      with open(bstack111l1llllll_opy_, bstack111lll_opy_ (u"ࠦࡼࠨᶨ")) as f:
        f.write(bstack111l111l11l_opy_)
        self.logger.debug(bstack111lll_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤᶩ"))
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᶪ").format(e))
  def bstack111l1l11l1l_opy_(self, bstack111l11lllll_opy_):
    try:
      bstack111l1llllll_opy_ = self.bstack111l1ll1l11_opy_(bstack111l11lllll_opy_)
      if os.path.exists(bstack111l1llllll_opy_):
        with open(bstack111l1llllll_opy_, bstack111lll_opy_ (u"ࠢࡳࠤᶫ")) as f:
          bstack111l111l11l_opy_ = f.read().strip()
          return bstack111l111l11l_opy_ if bstack111l111l11l_opy_ else None
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᶬ").format(e))
  def bstack111l1l1111l_opy_(self, bstack111l11lllll_opy_, bstack111l11ll111_opy_):
    bstack111l1l1ll1l_opy_ = self.bstack111l1l11l1l_opy_(bstack111l11lllll_opy_)
    if bstack111l1l1ll1l_opy_:
      try:
        bstack111l111llll_opy_ = self.bstack111l1ll1111_opy_(bstack111l1l1ll1l_opy_, bstack111l11ll111_opy_)
        if not bstack111l111llll_opy_:
          self.logger.debug(bstack111lll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦᶭ"))
          return True
        self.logger.debug(bstack111lll_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤᶮ"))
        return False
      except Exception as e:
        self.logger.warn(bstack111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᶯ").format(e))
    return False
  def bstack111l1ll1111_opy_(self, bstack111l1l1ll1l_opy_, bstack111l11ll111_opy_):
    try:
      headers = {
        bstack111lll_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧᶰ"): bstack111l1l1ll1l_opy_
      }
      response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"࠭ࡇࡆࡖࠪᶱ"), bstack111l11ll111_opy_, {}, {bstack111lll_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᶲ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥᶳ").format(e))
  @measure(event_name=EVENTS.bstack11ll111l111_opy_, stage=STAGE.bstack111ll11l1_opy_)
  def bstack111l111ll11_opy_(self, bstack111l11ll111_opy_, bstack111l1111lll_opy_):
    try:
      bstack111l11lll1l_opy_ = self.bstack111l1lll1l1_opy_()
      bstack111ll1111ll_opy_ = os.path.join(bstack111l11lll1l_opy_, bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᶴ"))
      bstack111l1l11111_opy_ = os.path.join(bstack111l11lll1l_opy_, bstack111l1111lll_opy_)
      if self.bstack111l1l1111l_opy_(bstack111l11lll1l_opy_, bstack111l11ll111_opy_): # if bstack111l1lllll1_opy_, bstack1l1l1ll1lll_opy_ bstack111l111l11l_opy_ is bstack111l1l1l111_opy_ to bstack11l1l11l111_opy_ version available (response 304)
        if os.path.exists(bstack111l1l11111_opy_):
          self.logger.info(bstack111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᶵ").format(bstack111l1l11111_opy_))
          return bstack111l1l11111_opy_
        if os.path.exists(bstack111ll1111ll_opy_):
          self.logger.info(bstack111lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᶶ").format(bstack111ll1111ll_opy_))
          return self.bstack111l11lll11_opy_(bstack111ll1111ll_opy_, bstack111l1111lll_opy_)
      self.logger.info(bstack111lll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᶷ").format(bstack111l11ll111_opy_))
      response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"࠭ࡇࡆࡖࠪᶸ"), bstack111l11ll111_opy_, {}, {})
      if response.status_code == 200:
        bstack111l111l1ll_opy_ = response.headers.get(bstack111lll_opy_ (u"ࠢࡆࡖࡤ࡫ࠧᶹ"), bstack111lll_opy_ (u"ࠣࠤᶺ"))
        if bstack111l111l1ll_opy_:
          self.bstack111l11llll1_opy_(bstack111l11lll1l_opy_, bstack111l111l1ll_opy_)
        with open(bstack111ll1111ll_opy_, bstack111lll_opy_ (u"ࠩࡺࡦࠬᶻ")) as file:
          file.write(response.content)
        self.logger.info(bstack111lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᶼ").format(bstack111ll1111ll_opy_))
        return self.bstack111l11lll11_opy_(bstack111ll1111ll_opy_, bstack111l1111lll_opy_)
      else:
        raise(bstack111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᶽ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᶾ").format(e))
  def bstack111ll111l1l_opy_(self, bstack111l11ll111_opy_, bstack111l1111lll_opy_):
    try:
      retry = 2
      bstack111l1l11111_opy_ = None
      bstack111l11l1lll_opy_ = False
      while retry > 0:
        bstack111l1l11111_opy_ = self.bstack111l111ll11_opy_(bstack111l11ll111_opy_, bstack111l1111lll_opy_)
        bstack111l11l1lll_opy_ = self.bstack111l1l1l11l_opy_(bstack111l11ll111_opy_, bstack111l1111lll_opy_, bstack111l1l11111_opy_)
        if bstack111l11l1lll_opy_:
          break
        retry -= 1
      return bstack111l1l11111_opy_, bstack111l11l1lll_opy_
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᶿ").format(e))
    return bstack111l1l11111_opy_, False
  def bstack111l1l1l11l_opy_(self, bstack111l11ll111_opy_, bstack111l1111lll_opy_, bstack111l1l11111_opy_, bstack111l1llll1l_opy_ = 0):
    if bstack111l1llll1l_opy_ > 1:
      return False
    if bstack111l1l11111_opy_ == None or os.path.exists(bstack111l1l11111_opy_) == False:
      self.logger.warn(bstack111lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ᷀"))
      return False
    bstack111l11l1l11_opy_ = bstack111lll_opy_ (u"ࡳࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࡠ࠳ࡢࡤࠬࠤ᷁")
    command = bstack111lll_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᷂").format(bstack111l1l11111_opy_)
    bstack111l1lll11l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l11l1l11_opy_, bstack111l1lll11l_opy_) != None:
      return True
    else:
      self.logger.error(bstack111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤ᷃"))
      return False
  def bstack111l11lll11_opy_(self, bstack111ll1111ll_opy_, bstack111l1111lll_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1111ll_opy_)
      shutil.unpack_archive(bstack111ll1111ll_opy_, working_dir)
      bstack111l1l11111_opy_ = os.path.join(working_dir, bstack111l1111lll_opy_)
      os.chmod(bstack111l1l11111_opy_, 0o755)
      return bstack111l1l11111_opy_
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧ᷄"))
  def bstack111l1lll1ll_opy_(self):
    try:
      bstack111l11ll1ll_opy_ = self.config.get(bstack111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᷅"))
      bstack111l1lll1ll_opy_ = bstack111l11ll1ll_opy_ or (bstack111l11ll1ll_opy_ is None and self.bstack1111l1lll_opy_)
      if not bstack111l1lll1ll_opy_ or self.config.get(bstack111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᷆"), None) not in bstack11ll11111l1_opy_:
        return False
      self.bstack1l1ll1ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᷇").format(e))
  def bstack111ll111l11_opy_(self):
    try:
      bstack111ll111l11_opy_ = self.percy_capture_mode
      return bstack111ll111l11_opy_
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᷈").format(e))
  def init(self, bstack1111l1lll_opy_, config, logger):
    self.bstack1111l1lll_opy_ = bstack1111l1lll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111l1lll1ll_opy_():
      return
    self.bstack111l1l11lll_opy_ = config.get(bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᷉"), {})
    self.percy_capture_mode = config.get(bstack111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ᷊࠭"))
    try:
      bstack111l11ll111_opy_, bstack111l1111lll_opy_ = self.bstack111l1ll11ll_opy_()
      self.bstack11l1l11ll1l_opy_ = bstack111l1111lll_opy_
      bstack111l1l11111_opy_, bstack111l11l1lll_opy_ = self.bstack111ll111l1l_opy_(bstack111l11ll111_opy_, bstack111l1111lll_opy_)
      if bstack111l11l1lll_opy_:
        self.binary_path = bstack111l1l11111_opy_
        thread = Thread(target=self.bstack111l1l111l1_opy_)
        thread.start()
      else:
        self.bstack111l11l111l_opy_ = True
        self.logger.error(bstack111lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣ᷋").format(bstack111l1l11111_opy_))
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᷌").format(e))
  def bstack111l11l1ll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111lll_opy_ (u"࠭࡬ࡰࡩࠪ᷍"), bstack111lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩ᷎ࠪ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111lll_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁ᷏ࠧ").format(logfile))
      self.bstack111l1l11ll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿ᷐ࠥ").format(e))
  @measure(event_name=EVENTS.bstack11ll1111ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
  def bstack111l1l111l1_opy_(self):
    bstack111l1ll1ll1_opy_ = self.bstack111l1l111ll_opy_()
    if bstack111l1ll1ll1_opy_ == None:
      self.bstack111l11l111l_opy_ = True
      self.logger.error(bstack111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨ᷑"))
      return False
    command_args = [bstack111lll_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧ᷒") if self.bstack1111l1lll_opy_ else bstack111lll_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩᷓ")]
    bstack111ll1l1lll_opy_ = self.bstack111l11l1l1l_opy_()
    if bstack111ll1l1lll_opy_ != None:
      command_args.append(bstack111lll_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧᷔ").format(bstack111ll1l1lll_opy_))
    env = os.environ.copy()
    env[bstack111lll_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧᷕ")] = bstack111l1ll1ll1_opy_
    env[bstack111lll_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣᷖ")] = os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᷗ"), bstack111lll_opy_ (u"ࠪࠫᷘ"))
    bstack111ll1111l1_opy_ = [self.binary_path]
    self.bstack111l11l1ll1_opy_()
    self.bstack111ll111111_opy_ = self.bstack111l111l1l1_opy_(bstack111ll1111l1_opy_ + command_args, env)
    self.logger.debug(bstack111lll_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧᷙ"))
    bstack111l1llll1l_opy_ = 0
    while self.bstack111ll111111_opy_.poll() == None:
      bstack111l1111l1l_opy_ = self.bstack111l1111ll1_opy_()
      if bstack111l1111l1l_opy_:
        self.logger.debug(bstack111lll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣᷚ"))
        self.bstack111ll11111l_opy_ = True
        return True
      bstack111l1llll1l_opy_ += 1
      self.logger.debug(bstack111lll_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤᷛ").format(bstack111l1llll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack111lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧᷜ").format(bstack111l1llll1l_opy_))
    self.bstack111l11l111l_opy_ = True
    return False
  def bstack111l1111ll1_opy_(self, bstack111l1llll1l_opy_ = 0):
    if bstack111l1llll1l_opy_ > 10:
      return False
    try:
      bstack111l11ll1l1_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨᷝ"), bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪᷞ"))
      bstack111l111l111_opy_ = bstack111l11ll1l1_opy_ + bstack11ll1111l1l_opy_
      response = requests.get(bstack111l111l111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩᷟ"), {}).get(bstack111lll_opy_ (u"ࠫ࡮ࡪࠧᷠ"), None)
      return True
    except:
      self.logger.debug(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᷡ"))
      return False
  def bstack111l1l111ll_opy_(self):
    bstack111l1ll1lll_opy_ = bstack111lll_opy_ (u"࠭ࡡࡱࡲࠪᷢ") if self.bstack1111l1lll_opy_ else bstack111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᷣ")
    bstack111l1ll11l1_opy_ = bstack111lll_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦᷤ") if self.config.get(bstack111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᷥ")) is None else True
    bstack11ll1ll11l1_opy_ = bstack111lll_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀࠦᷦ").format(self.config[bstack111lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᷧ")], bstack111l1ll1lll_opy_, bstack111l1ll11l1_opy_)
    if self.percy_capture_mode:
      bstack11ll1ll11l1_opy_ += bstack111lll_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃࠢᷨ").format(self.percy_capture_mode)
    uri = bstack11l1l111_opy_(bstack11ll1ll11l1_opy_)
    try:
      response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"࠭ࡇࡆࡖࠪᷩ"), uri, {}, {bstack111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᷪ"): (self.config[bstack111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᷫ")], self.config[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᷬ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1ll1ll1_opy_ = data.get(bstack111lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᷭ"))
        self.percy_capture_mode = data.get(bstack111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦࠩᷮ"))
        os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᷯ")] = str(self.bstack1l1ll1ll1_opy_)
        os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᷰ")] = str(self.percy_capture_mode)
        if bstack111l1ll11l1_opy_ == bstack111lll_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥᷱ") and str(self.bstack1l1ll1ll1_opy_).lower() == bstack111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᷲ"):
          self.bstack11lll1lll1_opy_ = True
        if bstack111lll_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᷳ") in data:
          return data[bstack111lll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᷴ")]
        else:
          raise bstack111lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫ᷵").format(data)
      else:
        raise bstack111lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧ᷶").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺ᷷ࠢ").format(e))
  def bstack111l11l1l1l_opy_(self):
    bstack111l1l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰ᷸ࠥ"))
    try:
      if bstack111lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯᷹ࠩ") not in self.bstack111l1l11lll_opy_:
        self.bstack111l1l11lll_opy_[bstack111lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰ᷺ࠪ")] = 2
      with open(bstack111l1l1l1ll_opy_, bstack111lll_opy_ (u"ࠪࡻࠬ᷻")) as fp:
        json.dump(self.bstack111l1l11lll_opy_, fp)
      return bstack111l1l1l1ll_opy_
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᷼").format(e))
  def bstack111l111l1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111l1ll1l1l_opy_ == bstack111lll_opy_ (u"ࠬࡽࡩ࡯᷽ࠩ"):
        bstack111l1l1llll_opy_ = [bstack111lll_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧ᷾"), bstack111lll_opy_ (u"ࠧ࠰ࡥ᷿ࠪ")]
        cmd = bstack111l1l1llll_opy_ + cmd
      cmd = bstack111lll_opy_ (u"ࠨࠢࠪḀ").join(cmd)
      self.logger.debug(bstack111lll_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨḁ").format(cmd))
      with open(self.bstack111l1l11ll1_opy_, bstack111lll_opy_ (u"ࠥࡥࠧḂ")) as bstack111l111ll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l111ll1l_opy_, text=True, stderr=bstack111l111ll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l11l111l_opy_ = True
      self.logger.error(bstack111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨḃ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll11111l_opy_:
        self.logger.info(bstack111lll_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨḄ"))
        cmd = [self.binary_path, bstack111lll_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤḅ")]
        self.bstack111l111l1l1_opy_(cmd)
        self.bstack111ll11111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢḆ").format(cmd, e))
  def bstack11l1111l1_opy_(self):
    if not self.bstack1l1ll1ll1_opy_:
      return
    try:
      bstack111l11l11ll_opy_ = 0
      while not self.bstack111ll11111l_opy_ and bstack111l11l11ll_opy_ < self.bstack111l1l1ll11_opy_:
        if self.bstack111l11l111l_opy_:
          self.logger.info(bstack111lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨḇ"))
          return
        time.sleep(1)
        bstack111l11l11ll_opy_ += 1
      os.environ[bstack111lll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨḈ")] = str(self.bstack111l1ll111l_opy_())
      self.logger.info(bstack111lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦḉ"))
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧḊ").format(e))
  def bstack111l1ll111l_opy_(self):
    if self.bstack1111l1lll_opy_:
      return
    try:
      bstack111l11l1111_opy_ = [platform[bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪḋ")].lower() for platform in self.config.get(bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩḌ"), [])]
      bstack111l111lll1_opy_ = sys.maxsize
      bstack111l1l11l11_opy_ = bstack111lll_opy_ (u"ࠧࠨḍ")
      for browser in bstack111l11l1111_opy_:
        if browser in self.bstack111l1lll111_opy_:
          bstack111l1llll11_opy_ = self.bstack111l1lll111_opy_[browser]
        if bstack111l1llll11_opy_ < bstack111l111lll1_opy_:
          bstack111l111lll1_opy_ = bstack111l1llll11_opy_
          bstack111l1l11l11_opy_ = browser
      return bstack111l1l11l11_opy_
    except Exception as e:
      self.logger.error(bstack111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤḎ").format(e))
  @classmethod
  def bstack11l1ll11l1_opy_(self):
    return os.getenv(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧḏ"), bstack111lll_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩḐ")).lower()
  @classmethod
  def bstack1ll111ll11_opy_(self):
    return os.getenv(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨḑ"), bstack111lll_opy_ (u"ࠬ࠭Ḓ"))
  @classmethod
  def bstack1l1ll11l111_opy_(cls, value):
    cls.bstack11lll1lll1_opy_ = value
  @classmethod
  def bstack111l1l1lll1_opy_(cls):
    return cls.bstack11lll1lll1_opy_
  @classmethod
  def bstack1l1ll111l11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111l11ll11l_opy_(cls):
    return cls.percy_build_id