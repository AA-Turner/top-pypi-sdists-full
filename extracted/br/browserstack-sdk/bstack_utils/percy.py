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
from bstack_utils.helper import bstack11111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l11ll11_opy_ import bstack1lll1l11_opy_
class bstack1ll11111l_opy_:
  working_dir = os.getcwd()
  bstack1l11l11111_opy_ = False
  config = {}
  bstack111l1llllll_opy_ = bstack1ll111_opy_ (u"ࠫࠬᵾ")
  binary_path = bstack1ll111_opy_ (u"ࠬ࠭ᵿ")
  bstack1llllll1l1ll_opy_ = bstack1ll111_opy_ (u"࠭ࠧᶀ")
  bstack1lll111ll1_opy_ = False
  bstack1lllll111l11_opy_ = None
  bstack1llllll1111l_opy_ = {}
  bstack1llll1lllll1_opy_ = 300
  bstack1lllll11ll11_opy_ = False
  logger = None
  bstack1lllllllll1l_opy_ = False
  bstack11l1l1l1ll_opy_ = False
  percy_build_id = None
  bstack1111111111l_opy_ = bstack1ll111_opy_ (u"ࠧࠨᶁ")
  bstack1lllllllll11_opy_ = {
    bstack1ll111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᶂ") : 1,
    bstack1ll111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᶃ") : 2,
    bstack1ll111_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᶄ") : 3,
    bstack1ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᶅ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lllllll11l1_opy_(self):
    bstack1llllllll11l_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ᶆ")
    bstack1lllll111111_opy_ = sys.platform
    bstack1lllll111lll_opy_ = bstack1ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᶇ")
    if re.match(bstack1ll111_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᶈ"), bstack1lllll111111_opy_) != None:
      bstack1llllllll11l_opy_ = bstack1llllllll111_opy_ + bstack1ll111_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᶉ")
      self.bstack1111111111l_opy_ = bstack1ll111_opy_ (u"ࠩࡰࡥࡨ࠭ᶊ")
    elif re.match(bstack1ll111_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᶋ"), bstack1lllll111111_opy_) != None:
      bstack1llllllll11l_opy_ = bstack1llllllll111_opy_ + bstack1ll111_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᶌ")
      bstack1lllll111lll_opy_ = bstack1ll111_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᶍ")
      self.bstack1111111111l_opy_ = bstack1ll111_opy_ (u"࠭ࡷࡪࡰࠪᶎ")
    else:
      bstack1llllllll11l_opy_ = bstack1llllllll111_opy_ + bstack1ll111_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᶏ")
      self.bstack1111111111l_opy_ = bstack1ll111_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᶐ")
    return bstack1llllllll11l_opy_, bstack1lllll111lll_opy_
  def bstack1lllll111ll1_opy_(self):
    try:
      bstack1lllll1lll11_opy_ = [os.path.join(expanduser(bstack1ll111_opy_ (u"ࠤࢁࠦᶑ")), bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᶒ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lllll1lll11_opy_:
        if(self.bstack1lllll11l1l1_opy_(path)):
          return path
      raise bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᶓ")
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᶔ").format(e))
  def bstack1lllll11l1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lllll11l1ll_opy_(self, bstack1llllllll1ll_opy_):
    return os.path.join(bstack1llllllll1ll_opy_, self.bstack111l1llllll_opy_ + bstack1ll111_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧᶕ"))
  def bstack1llllll111ll_opy_(self, bstack1llllllll1ll_opy_, bstack1lllll11ll1l_opy_):
    if not bstack1lllll11ll1l_opy_: return
    try:
      bstack1lllll1l1l11_opy_ = self.bstack1lllll11l1ll_opy_(bstack1llllllll1ll_opy_)
      with open(bstack1lllll1l1l11_opy_, bstack1ll111_opy_ (u"ࠢࡸࠤᶖ")) as f:
        f.write(bstack1lllll11ll1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧᶗ"))
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᶘ").format(e))
  def bstack1llllll11l1l_opy_(self, bstack1llllllll1ll_opy_):
    try:
      bstack1lllll1l1l11_opy_ = self.bstack1lllll11l1ll_opy_(bstack1llllllll1ll_opy_)
      if os.path.exists(bstack1lllll1l1l11_opy_):
        with open(bstack1lllll1l1l11_opy_, bstack1ll111_opy_ (u"ࠥࡶࠧᶙ")) as f:
          bstack1lllll11ll1l_opy_ = f.read().strip()
          return bstack1lllll11ll1l_opy_ if bstack1lllll11ll1l_opy_ else None
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᶚ").format(e))
  def bstack1lllllll1lll_opy_(self, bstack1llllllll1ll_opy_, bstack1llllllll11l_opy_):
    bstack1lllll1l1ll1_opy_ = self.bstack1llllll11l1l_opy_(bstack1llllllll1ll_opy_)
    if bstack1lllll1l1ll1_opy_:
      try:
        bstack1lllll1l1111_opy_ = self.bstack1llllll11l11_opy_(bstack1lllll1l1ll1_opy_, bstack1llllllll11l_opy_)
        if not bstack1lllll1l1111_opy_:
          self.logger.debug(bstack1ll111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢᶛ"))
          return True
        self.logger.debug(bstack1ll111_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧᶜ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᶝ").format(e))
    return False
  def bstack1llllll11l11_opy_(self, bstack1lllll1l1ll1_opy_, bstack1llllllll11l_opy_):
    try:
      headers = {
        bstack1ll111_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣᶞ"): bstack1lllll1l1ll1_opy_
      }
      response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠩࡊࡉ࡙࠭ᶟ"), bstack1llllllll11l_opy_, {}, {bstack1ll111_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦᶠ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨᶡ").format(e))
  @measure(event_name=EVENTS.bstack1lllll11l11l_opy_, stage=STAGE.bstack11ll1111_opy_)
  def bstack1lllll1lll1l_opy_(self, bstack1llllllll11l_opy_, bstack1lllll111lll_opy_):
    try:
      bstack1lllll11lll1_opy_ = self.bstack1lllll111ll1_opy_()
      bstack1lllll1llll1_opy_ = os.path.join(bstack1lllll11lll1_opy_, bstack1ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨᶢ"))
      bstack1lllllll1l11_opy_ = os.path.join(bstack1lllll11lll1_opy_, bstack1lllll111lll_opy_)
      if self.bstack1lllllll1lll_opy_(bstack1lllll11lll1_opy_, bstack1llllllll11l_opy_): # if true, bstack11lllll1111_opy_ bstack1lllll11ll1l_opy_ is bstack1llllllll1l1_opy_ to bstack111lll1111l_opy_ version available (response 304)
        if os.path.exists(bstack1lllllll1l11_opy_):
          self.logger.info(bstack1ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᶣ").format(bstack1lllllll1l11_opy_))
          return bstack1lllllll1l11_opy_
        if os.path.exists(bstack1lllll1llll1_opy_):
          self.logger.info(bstack1ll111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧᶤ").format(bstack1lllll1llll1_opy_))
          return self.bstack1lllll1ll111_opy_(bstack1lllll1llll1_opy_, bstack1lllll111lll_opy_)
      self.logger.info(bstack1ll111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨᶥ").format(bstack1llllllll11l_opy_))
      response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠩࡊࡉ࡙࠭ᶦ"), bstack1llllllll11l_opy_, {}, {})
      if response.status_code == 200:
        bstack1lllll1111l1_opy_ = response.headers.get(bstack1ll111_opy_ (u"ࠥࡉ࡙ࡧࡧࠣᶧ"), bstack1ll111_opy_ (u"ࠦࠧᶨ"))
        if bstack1lllll1111l1_opy_:
          self.bstack1llllll111ll_opy_(bstack1lllll11lll1_opy_, bstack1lllll1111l1_opy_)
        with open(bstack1lllll1llll1_opy_, bstack1ll111_opy_ (u"ࠬࡽࡢࠨᶩ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll111_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦᶪ").format(bstack1lllll1llll1_opy_))
        return self.bstack1lllll1ll111_opy_(bstack1lllll1llll1_opy_, bstack1lllll111lll_opy_)
      else:
        raise(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥᶫ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤᶬ").format(e))
  def bstack1lllll1111ll_opy_(self, bstack1llllllll11l_opy_, bstack1lllll111lll_opy_):
    try:
      retry = 2
      bstack1lllllll1l11_opy_ = None
      bstack1llll1llll1l_opy_ = False
      while retry > 0:
        bstack1lllllll1l11_opy_ = self.bstack1lllll1lll1l_opy_(bstack1llllllll11l_opy_, bstack1lllll111lll_opy_)
        bstack1llll1llll1l_opy_ = self.bstack1lllll1l111l_opy_(bstack1llllllll11l_opy_, bstack1lllll111lll_opy_, bstack1lllllll1l11_opy_)
        if bstack1llll1llll1l_opy_:
          break
        retry -= 1
      return bstack1lllllll1l11_opy_, bstack1llll1llll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨᶭ").format(e))
    return bstack1lllllll1l11_opy_, False
  def bstack1lllll1l111l_opy_(self, bstack1llllllll11l_opy_, bstack1lllll111lll_opy_, bstack1lllllll1l11_opy_, bstack1llllll1ll1l_opy_ = 0):
    if bstack1llllll1ll1l_opy_ > 1:
      return False
    if bstack1lllllll1l11_opy_ == None or os.path.exists(bstack1lllllll1l11_opy_) == False:
      self.logger.warn(bstack1ll111_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣᶮ"))
      return False
    command = bstack1ll111_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᶯ").format(bstack1lllllll1l11_opy_)
    bstack1llllll1ll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1ll111_opy_ (u"ࠬࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠩᶰ") in bstack1llllll1ll11_opy_:
      return True
    else:
      self.logger.error(bstack1ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧᶱ"))
      return False
  def bstack1lllll1ll111_opy_(self, bstack1lllll1llll1_opy_, bstack1lllll111lll_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllll1llll1_opy_)
      shutil.unpack_archive(bstack1lllll1llll1_opy_, working_dir)
      bstack1lllllll1l11_opy_ = os.path.join(working_dir, bstack1lllll111lll_opy_)
      os.chmod(bstack1lllllll1l11_opy_, 0o755)
      return bstack1lllllll1l11_opy_
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᶲ"))
  def bstack1lllllll1111_opy_(self):
    try:
      bstack1llllll1l11l_opy_ = self.config.get(bstack1ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᶳ"))
      bstack1lllllll1111_opy_ = bstack1llllll1l11l_opy_ or (bstack1llllll1l11l_opy_ is None and self.bstack1l11l11111_opy_)
      if not bstack1lllllll1111_opy_ or self.config.get(bstack1ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᶴ"), None) not in bstack1lllllll1ll1_opy_:
        return False
      self.bstack1lll111ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᶵ").format(e))
  def bstack1lllll1lllll_opy_(self):
    try:
      bstack1lllll1lllll_opy_ = self.percy_capture_mode
      return bstack1lllll1lllll_opy_
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᶶ").format(e))
  def init(self, bstack1l11l11111_opy_, config, logger):
    self.bstack1l11l11111_opy_ = bstack1l11l11111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lllllll1111_opy_():
      return
    self.bstack1llllll1111l_opy_ = config.get(bstack1ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᶷ"), {})
    self.percy_capture_mode = config.get(bstack1ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᶸ"))
    try:
      bstack1llllllll11l_opy_, bstack1lllll111lll_opy_ = self.bstack1lllllll11l1_opy_()
      self.bstack111l1llllll_opy_ = bstack1lllll111lll_opy_
      bstack1lllllll1l11_opy_, bstack1llll1llll1l_opy_ = self.bstack1lllll1111ll_opy_(bstack1llllllll11l_opy_, bstack1lllll111lll_opy_)
      if bstack1llll1llll1l_opy_:
        self.binary_path = bstack1lllllll1l11_opy_
        thread = Thread(target=self.bstack1llllll1lll1_opy_)
        thread.start()
      else:
        self.bstack1lllllllll1l_opy_ = True
        self.logger.error(bstack1ll111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᶹ").format(bstack1lllllll1l11_opy_))
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᶺ").format(e))
  def bstack1llllll1llll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll111_opy_ (u"ࠩ࡯ࡳ࡬࠭ᶻ"), bstack1ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ᶼ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll111_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᶽ").format(logfile))
      self.bstack1llllll1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᶾ").format(e))
  @measure(event_name=EVENTS.bstack1lllll1ll1ll_opy_, stage=STAGE.bstack11ll1111_opy_)
  def bstack1llllll1lll1_opy_(self):
    bstack1lllll1l11ll_opy_ = self.bstack1lllll111l1l_opy_()
    if bstack1lllll1l11ll_opy_ == None:
      self.bstack1lllllllll1l_opy_ = True
      self.logger.error(bstack1ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᶿ"))
      return False
    bstack1lllll11l111_opy_ = [bstack1ll111_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣ᷀") if self.bstack1l11l11111_opy_ else bstack1ll111_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬ᷁")]
    bstack1llll1ll11l_opy_ = self.bstack1lllll1ll11l_opy_()
    if bstack1llll1ll11l_opy_ != None:
      bstack1lllll11l111_opy_.append(bstack1ll111_opy_ (u"ࠤ࠰ࡧࠥࢁࡽ᷂ࠣ").format(bstack1llll1ll11l_opy_))
    env = os.environ.copy()
    env[bstack1ll111_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣ᷃")] = bstack1lllll1l11ll_opy_
    env[bstack1ll111_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦ᷄")] = os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᷅"), bstack1ll111_opy_ (u"࠭ࠧ᷆"))
    bstack1llll1llllll_opy_ = [self.binary_path]
    self.bstack1llllll1llll_opy_()
    self.bstack1lllll111l11_opy_ = self.bstack1lllllllllll_opy_(bstack1llll1llllll_opy_ + bstack1lllll11l111_opy_, env)
    self.logger.debug(bstack1ll111_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣ᷇"))
    bstack1llllll1ll1l_opy_ = 0
    while self.bstack1lllll111l11_opy_.poll() == None:
      bstack1llllll11ll1_opy_ = self.bstack1llllll11111_opy_()
      if bstack1llllll11ll1_opy_:
        self.logger.debug(bstack1ll111_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ᷈"))
        self.bstack1lllll11ll11_opy_ = True
        return True
      bstack1llllll1ll1l_opy_ += 1
      self.logger.debug(bstack1ll111_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ᷉").format(bstack1llllll1ll1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳ᷊ࠣ").format(bstack1llllll1ll1l_opy_))
    self.bstack1lllllllll1l_opy_ = True
    return False
  def bstack1llllll11111_opy_(self, bstack1llllll1ll1l_opy_ = 0):
    if bstack1llllll1ll1l_opy_ > 10:
      return False
    try:
      bstack1llllll1l111_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫ᷋"), bstack1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭᷌"))
      bstack1lllllll1l1l_opy_ = bstack1llllll1l111_opy_ + bstack1lllllll111l_opy_
      response = requests.get(bstack1lllllll1l1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ᷍"), {}).get(bstack1ll111_opy_ (u"ࠧࡪࡦ᷎ࠪ"), None)
      return True
    except:
      self.logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ᷏"))
      return False
  def bstack1lllll111l1l_opy_(self):
    bstack11111111111_opy_ = bstack1ll111_opy_ (u"ࠩࡤࡴࡵ᷐࠭") if self.bstack1l11l11111_opy_ else bstack1ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᷑")
    bstack1lllll1l1lll_opy_ = bstack1ll111_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ᷒") if self.config.get(bstack1ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᷓ")) is None else True
    bstack11111llllll_opy_ = bstack1ll111_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢᷔ").format(self.config[bstack1ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᷕ")], bstack11111111111_opy_, bstack1lllll1l1lll_opy_)
    if self.percy_capture_mode:
      bstack11111llllll_opy_ += bstack1ll111_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥᷖ").format(self.percy_capture_mode)
    uri = bstack1lll1l11_opy_(bstack11111llllll_opy_)
    try:
      response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠩࡊࡉ࡙࠭ᷗ"), uri, {}, {bstack1ll111_opy_ (u"ࠪࡥࡺࡺࡨࠨᷘ"): (self.config[bstack1ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᷙ")], self.config[bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᷚ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lll111ll1_opy_ = data.get(bstack1ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᷛ"))
        self.percy_capture_mode = data.get(bstack1ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬᷜ"))
        os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᷝ")] = str(self.bstack1lll111ll1_opy_)
        os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᷞ")] = str(self.percy_capture_mode)
        if bstack1lllll1l1lll_opy_ == bstack1ll111_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨᷟ") and str(self.bstack1lll111ll1_opy_).lower() == bstack1ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᷠ"):
          self.bstack11l1l1l1ll_opy_ = True
        if bstack1ll111_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᷡ") in data:
          return data[bstack1ll111_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᷢ")]
        else:
          raise bstack1ll111_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧᷣ").format(data)
      else:
        raise bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣᷤ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥᷥ").format(e))
  def bstack1lllll1ll11l_opy_(self):
    bstack1llllll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨᷦ"))
    try:
      if bstack1ll111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᷧ") not in self.bstack1llllll1111l_opy_:
        self.bstack1llllll1111l_opy_[bstack1ll111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᷨ")] = 2
      with open(bstack1llllll11lll_opy_, bstack1ll111_opy_ (u"࠭ࡷࠨᷩ")) as fp:
        json.dump(self.bstack1llllll1111l_opy_, fp)
      return bstack1llllll11lll_opy_
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᷪ").format(e))
  def bstack1lllllllllll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111111111l_opy_ == bstack1ll111_opy_ (u"ࠨࡹ࡬ࡲࠬᷫ"):
        bstack1llllll111l1_opy_ = [bstack1ll111_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪᷬ"), bstack1ll111_opy_ (u"ࠪ࠳ࡨ࠭ᷭ")]
        cmd = bstack1llllll111l1_opy_ + cmd
      cmd = bstack1ll111_opy_ (u"ࠫࠥ࠭ᷮ").join(cmd)
      self.logger.debug(bstack1ll111_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤᷯ").format(cmd))
      with open(self.bstack1llllll1l1ll_opy_, bstack1ll111_opy_ (u"ࠨࡡࠣᷰ")) as bstack1lllll1ll1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lllll1ll1l1_opy_, text=True, stderr=bstack1lllll1ll1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lllllllll1l_opy_ = True
      self.logger.error(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᷱ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lllll11ll11_opy_:
        self.logger.info(bstack1ll111_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤᷲ"))
        cmd = [self.binary_path, bstack1ll111_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧᷳ")]
        self.bstack1lllllllllll_opy_(cmd)
        self.bstack1lllll11ll11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᷴ").format(cmd, e))
  def bstack1111ll1l_opy_(self):
    if not self.bstack1lll111ll1_opy_:
      return
    try:
      bstack1lllll11llll_opy_ = 0
      while not self.bstack1lllll11ll11_opy_ and bstack1lllll11llll_opy_ < self.bstack1llll1lllll1_opy_:
        if self.bstack1lllllllll1l_opy_:
          self.logger.info(bstack1ll111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤ᷵"))
          return
        time.sleep(1)
        bstack1lllll11llll_opy_ += 1
      os.environ[bstack1ll111_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ᷶")] = str(self.bstack1llllllllll1_opy_())
      self.logger.info(bstack1ll111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪ᷷ࠢ"))
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽ᷸ࠣ").format(e))
  def bstack1llllllllll1_opy_(self):
    if self.bstack1l11l11111_opy_:
      return
    try:
      bstack1lllll1l1l1l_opy_ = [platform[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ᷹࠭")].lower() for platform in self.config.get(bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ᷺ࠬ"), [])]
      bstack1ll1l11111l_opy_ = sys.maxsize
      bstack1lllll1l11l1_opy_ = bstack1ll111_opy_ (u"ࠪࠫ᷻")
      for browser in bstack1lllll1l1l1l_opy_:
        if browser in self.bstack1lllllllll11_opy_:
          bstack1lllll11111l_opy_ = self.bstack1lllllllll11_opy_[browser]
        if bstack1lllll11111l_opy_ < bstack1ll1l11111l_opy_:
          bstack1ll1l11111l_opy_ = bstack1lllll11111l_opy_
          bstack1lllll1l11l1_opy_ = browser
      return bstack1lllll1l11l1_opy_
    except Exception as e:
      self.logger.error(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᷼").format(e))
  @classmethod
  def bstack1ll1l1l1l_opy_(self):
    return os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛᷽ࠪ"), bstack1ll111_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬ᷾")).lower()
  @classmethod
  def bstack1ll11l111l_opy_(self):
    return os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈ᷿ࠫ"), bstack1ll111_opy_ (u"ࠨࠩḀ"))
  @classmethod
  def bstack1l11111l11l_opy_(cls, value):
    cls.bstack11l1l1l1ll_opy_ = value
  @classmethod
  def bstack1lllllll11ll_opy_(cls):
    return cls.bstack11l1l1l1ll_opy_
  @classmethod
  def bstack1l111111l1l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1llllll1l1l1_opy_(cls):
    return cls.percy_build_id