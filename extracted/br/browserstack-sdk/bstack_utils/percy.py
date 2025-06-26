# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
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
from bstack_utils.helper import bstack11lll1111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11ll111l1l_opy_ import bstack111l11ll_opy_
class bstack11ll1l11ll_opy_:
  working_dir = os.getcwd()
  bstack1llll1l1l1_opy_ = False
  config = {}
  bstack11l11llll11_opy_ = bstack11ll1l1_opy_ (u"ࠧࠨᷜ")
  binary_path = bstack11ll1l1_opy_ (u"ࠨࠩᷝ")
  bstack111l111ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠩࠪᷞ")
  bstack11l1ll1111_opy_ = False
  bstack111l111l1ll_opy_ = None
  bstack1111ll11111_opy_ = {}
  bstack1111l1ll1ll_opy_ = 300
  bstack1111l1l11l1_opy_ = False
  logger = None
  bstack1111l1lll1l_opy_ = False
  bstack1lllll11l_opy_ = False
  percy_build_id = None
  bstack1111lll1111_opy_ = bstack11ll1l1_opy_ (u"ࠪࠫᷟ")
  bstack111l11111l1_opy_ = {
    bstack11ll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᷠ") : 1,
    bstack11ll1l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᷡ") : 2,
    bstack11ll1l1_opy_ (u"࠭ࡥࡥࡩࡨࠫᷢ") : 3,
    bstack11ll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᷣ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l11111ll_opy_(self):
    bstack1111l11llll_opy_ = bstack11ll1l1_opy_ (u"ࠨࠩᷤ")
    bstack1111l1ll111_opy_ = sys.platform
    bstack1111lll1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᷥ")
    if re.match(bstack11ll1l1_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᷦ"), bstack1111l1ll111_opy_) != None:
      bstack1111l11llll_opy_ = bstack11l1lll1111_opy_ + bstack11ll1l1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᷧ")
      self.bstack1111lll1111_opy_ = bstack11ll1l1_opy_ (u"ࠬࡳࡡࡤࠩᷨ")
    elif re.match(bstack11ll1l1_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᷩ"), bstack1111l1ll111_opy_) != None:
      bstack1111l11llll_opy_ = bstack11l1lll1111_opy_ + bstack11ll1l1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᷪ")
      bstack1111lll1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᷫ")
      self.bstack1111lll1111_opy_ = bstack11ll1l1_opy_ (u"ࠩࡺ࡭ࡳ࠭ᷬ")
    else:
      bstack1111l11llll_opy_ = bstack11l1lll1111_opy_ + bstack11ll1l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᷭ")
      self.bstack1111lll1111_opy_ = bstack11ll1l1_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᷮ")
    return bstack1111l11llll_opy_, bstack1111lll1l1l_opy_
  def bstack1111l1llll1_opy_(self):
    try:
      bstack1111ll1lll1_opy_ = [os.path.join(expanduser(bstack11ll1l1_opy_ (u"ࠧࢄࠢᷯ")), bstack11ll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᷰ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111ll1lll1_opy_:
        if(self.bstack1111llllll1_opy_(path)):
          return path
      raise bstack11ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᷱ")
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᷲ").format(e))
  def bstack1111llllll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l1l1l1l_opy_(self, bstack111l111llll_opy_):
    return os.path.join(bstack111l111llll_opy_, self.bstack11l11llll11_opy_ + bstack11ll1l1_opy_ (u"ࠤ࠱ࡩࡹࡧࡧࠣᷳ"))
  def bstack1111ll111ll_opy_(self, bstack111l111llll_opy_, bstack1111l1l111l_opy_):
    if not bstack1111l1l111l_opy_: return
    try:
      bstack1111llll11l_opy_ = self.bstack1111l1l1l1l_opy_(bstack111l111llll_opy_)
      with open(bstack1111llll11l_opy_, bstack11ll1l1_opy_ (u"ࠥࡻࠧᷴ")) as f:
        f.write(bstack1111l1l111l_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡘࡧࡶࡦࡦࠣࡲࡪࡽࠠࡆࡖࡤ࡫ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠣ᷵"))
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡴࡩࡧࠣࡩࡹࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ᷶").format(e))
  def bstack1111ll11lll_opy_(self, bstack111l111llll_opy_):
    try:
      bstack1111llll11l_opy_ = self.bstack1111l1l1l1l_opy_(bstack111l111llll_opy_)
      if os.path.exists(bstack1111llll11l_opy_):
        with open(bstack1111llll11l_opy_, bstack11ll1l1_opy_ (u"ࠨࡲ᷷ࠣ")) as f:
          bstack1111l1l111l_opy_ = f.read().strip()
          return bstack1111l1l111l_opy_ if bstack1111l1l111l_opy_ else None
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠ࡭ࡱࡤࡨ࡮ࡴࡧࠡࡇࡗࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿ᷸ࠥ").format(e))
  def bstack1111ll11l1l_opy_(self, bstack111l111llll_opy_, bstack1111l11llll_opy_):
    bstack111l1111111_opy_ = self.bstack1111ll11lll_opy_(bstack111l111llll_opy_)
    if bstack111l1111111_opy_:
      try:
        bstack111l1111l1l_opy_ = self.bstack1111l1ll1l1_opy_(bstack111l1111111_opy_, bstack1111l11llll_opy_)
        if not bstack111l1111l1l_opy_:
          self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡵࠣࡹࡵࠦࡴࡰࠢࡧࡥࡹ࡫ࠠࠩࡇࡗࡥ࡬ࠦࡵ࡯ࡥ࡫ࡥࡳ࡭ࡥࡥ᷹ࠫࠥ"))
          return True
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡑࡩࡼࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡥ᷺ࠣ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11ll1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡬࡯ࡳࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ᷻").format(e))
    return False
  def bstack1111l1ll1l1_opy_(self, bstack111l1111111_opy_, bstack1111l11llll_opy_):
    try:
      headers = {
        bstack11ll1l1_opy_ (u"ࠦࡎ࡬࠭ࡏࡱࡱࡩ࠲ࡓࡡࡵࡥ࡫ࠦ᷼"): bstack111l1111111_opy_
      }
      response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡍࡅࡕ᷽ࠩ"), bstack1111l11llll_opy_, {}, {bstack11ll1l1_opy_ (u"ࠨࡨࡦࡣࡧࡩࡷࡹࠢ᷾"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠿ࠦࡻࡾࠤ᷿").format(e))
  @measure(event_name=EVENTS.bstack11l1lllll11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
  def bstack1111ll1l11l_opy_(self, bstack1111l11llll_opy_, bstack1111lll1l1l_opy_):
    try:
      bstack111l1111ll1_opy_ = self.bstack1111l1llll1_opy_()
      bstack1111lll1lll_opy_ = os.path.join(bstack111l1111ll1_opy_, bstack11ll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫḀ"))
      bstack1111ll111l1_opy_ = os.path.join(bstack111l1111ll1_opy_, bstack1111lll1l1l_opy_)
      if self.bstack1111ll11l1l_opy_(bstack111l1111ll1_opy_, bstack1111l11llll_opy_): # if bstack1111ll1l1l1_opy_, bstack1l1l11ll11l_opy_ bstack1111l1l111l_opy_ is bstack1111llll1l1_opy_ to bstack11l11lllll1_opy_ version available (response 304)
        if os.path.exists(bstack1111ll111l1_opy_):
          self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦḁ").format(bstack1111ll111l1_opy_))
          return bstack1111ll111l1_opy_
        if os.path.exists(bstack1111lll1lll_opy_):
          self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣḂ").format(bstack1111lll1lll_opy_))
          return self.bstack1111ll1ll1l_opy_(bstack1111lll1lll_opy_, bstack1111lll1l1l_opy_)
      self.logger.info(bstack11ll1l1_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤḃ").format(bstack1111l11llll_opy_))
      response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡍࡅࡕࠩḄ"), bstack1111l11llll_opy_, {}, {})
      if response.status_code == 200:
        bstack1111ll11ll1_opy_ = response.headers.get(bstack11ll1l1_opy_ (u"ࠨࡅࡕࡣࡪࠦḅ"), bstack11ll1l1_opy_ (u"ࠢࠣḆ"))
        if bstack1111ll11ll1_opy_:
          self.bstack1111ll111ll_opy_(bstack111l1111ll1_opy_, bstack1111ll11ll1_opy_)
        with open(bstack1111lll1lll_opy_, bstack11ll1l1_opy_ (u"ࠨࡹࡥࠫḇ")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢḈ").format(bstack1111lll1lll_opy_))
        return self.bstack1111ll1ll1l_opy_(bstack1111lll1lll_opy_, bstack1111lll1l1l_opy_)
      else:
        raise(bstack11ll1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨḉ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧḊ").format(e))
  def bstack1111ll1l1ll_opy_(self, bstack1111l11llll_opy_, bstack1111lll1l1l_opy_):
    try:
      retry = 2
      bstack1111ll111l1_opy_ = None
      bstack1111ll1111l_opy_ = False
      while retry > 0:
        bstack1111ll111l1_opy_ = self.bstack1111ll1l11l_opy_(bstack1111l11llll_opy_, bstack1111lll1l1l_opy_)
        bstack1111ll1111l_opy_ = self.bstack1111l1lll11_opy_(bstack1111l11llll_opy_, bstack1111lll1l1l_opy_, bstack1111ll111l1_opy_)
        if bstack1111ll1111l_opy_:
          break
        retry -= 1
      return bstack1111ll111l1_opy_, bstack1111ll1111l_opy_
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤḋ").format(e))
    return bstack1111ll111l1_opy_, False
  def bstack1111l1lll11_opy_(self, bstack1111l11llll_opy_, bstack1111lll1l1l_opy_, bstack1111ll111l1_opy_, bstack1111lllllll_opy_ = 0):
    if bstack1111lllllll_opy_ > 1:
      return False
    if bstack1111ll111l1_opy_ == None or os.path.exists(bstack1111ll111l1_opy_) == False:
      self.logger.warn(bstack11ll1l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦḌ"))
      return False
    bstack111l111lll1_opy_ = bstack11ll1l1_opy_ (u"ࡲࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼ࠳ࡨࡲࡩࠡ࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭࡟࠲ࡡࡪࠫࠣḍ")
    command = bstack11ll1l1_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧḎ").format(bstack1111ll111l1_opy_)
    bstack1111lll11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l111lll1_opy_, bstack1111lll11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣḏ"))
      return False
  def bstack1111ll1ll1l_opy_(self, bstack1111lll1lll_opy_, bstack1111lll1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack1111lll1lll_opy_)
      shutil.unpack_archive(bstack1111lll1lll_opy_, working_dir)
      bstack1111ll111l1_opy_ = os.path.join(working_dir, bstack1111lll1l1l_opy_)
      os.chmod(bstack1111ll111l1_opy_, 0o755)
      return bstack1111ll111l1_opy_
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦḐ"))
  def bstack111l1111l11_opy_(self):
    try:
      bstack1111l1l1ll1_opy_ = self.config.get(bstack11ll1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪḑ"))
      bstack111l1111l11_opy_ = bstack1111l1l1ll1_opy_ or (bstack1111l1l1ll1_opy_ is None and self.bstack1llll1l1l1_opy_)
      if not bstack111l1111l11_opy_ or self.config.get(bstack11ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨḒ"), None) not in bstack11ll111111l_opy_:
        return False
      self.bstack11l1ll1111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣḓ").format(e))
  def bstack1111l1l1lll_opy_(self):
    try:
      bstack1111l1l1lll_opy_ = self.percy_capture_mode
      return bstack1111l1l1lll_opy_
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺࠢࡦࡥࡵࡺࡵࡳࡧࠣࡱࡴࡪࡥ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣḔ").format(e))
  def init(self, bstack1llll1l1l1_opy_, config, logger):
    self.bstack1llll1l1l1_opy_ = bstack1llll1l1l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111l1111l11_opy_():
      return
    self.bstack1111ll11111_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧḕ"), {})
    self.percy_capture_mode = config.get(bstack11ll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬḖ"))
    try:
      bstack1111l11llll_opy_, bstack1111lll1l1l_opy_ = self.bstack111l11111ll_opy_()
      self.bstack11l11llll11_opy_ = bstack1111lll1l1l_opy_
      bstack1111ll111l1_opy_, bstack1111ll1111l_opy_ = self.bstack1111ll1l1ll_opy_(bstack1111l11llll_opy_, bstack1111lll1l1l_opy_)
      if bstack1111ll1111l_opy_:
        self.binary_path = bstack1111ll111l1_opy_
        thread = Thread(target=self.bstack1111l1lllll_opy_)
        thread.start()
      else:
        self.bstack1111l1lll1l_opy_ = True
        self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢḗ").format(bstack1111ll111l1_opy_))
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧḘ").format(e))
  def bstack111l111111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11ll1l1_opy_ (u"ࠬࡲ࡯ࡨࠩḙ"), bstack11ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩḚ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦḛ").format(logfile))
      self.bstack111l111ll1l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤḜ").format(e))
  @measure(event_name=EVENTS.bstack11ll11111ll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
  def bstack1111l1lllll_opy_(self):
    bstack1111llll111_opy_ = self.bstack1111llll1ll_opy_()
    if bstack1111llll111_opy_ == None:
      self.bstack1111l1lll1l_opy_ = True
      self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧḝ"))
      return False
    command_args = [bstack11ll1l1_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦḞ") if self.bstack1llll1l1l1_opy_ else bstack11ll1l1_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨḟ")]
    bstack111ll111l11_opy_ = self.bstack1111l1l1111_opy_()
    if bstack111ll111l11_opy_ != None:
      command_args.append(bstack11ll1l1_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦḠ").format(bstack111ll111l11_opy_))
    env = os.environ.copy()
    env[bstack11ll1l1_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦḡ")] = bstack1111llll111_opy_
    env[bstack11ll1l1_opy_ (u"ࠢࡕࡊࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠢḢ")] = os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ḣ"), bstack11ll1l1_opy_ (u"ࠩࠪḤ"))
    bstack111l111l1l1_opy_ = [self.binary_path]
    self.bstack111l111111l_opy_()
    self.bstack111l111l1ll_opy_ = self.bstack1111ll11l11_opy_(bstack111l111l1l1_opy_ + command_args, env)
    self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠦḥ"))
    bstack1111lllllll_opy_ = 0
    while self.bstack111l111l1ll_opy_.poll() == None:
      bstack111l111ll11_opy_ = self.bstack1111lll1l11_opy_()
      if bstack111l111ll11_opy_:
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲࠢḦ"))
        self.bstack1111l1l11l1_opy_ = True
        return True
      bstack1111lllllll_opy_ += 1
      self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡗ࡫ࡴࡳࡻࠣ࠱ࠥࢁࡽࠣḧ").format(bstack1111lllllll_opy_))
      time.sleep(2)
    self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡇࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡻࡾࠢࡤࡸࡹ࡫࡭ࡱࡶࡶࠦḨ").format(bstack1111lllllll_opy_))
    self.bstack1111l1lll1l_opy_ = True
    return False
  def bstack1111lll1l11_opy_(self, bstack1111lllllll_opy_ = 0):
    if bstack1111lllllll_opy_ > 10:
      return False
    try:
      bstack1111ll1l111_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡓࡆࡔ࡙ࡉࡗࡥࡁࡅࡆࡕࡉࡘ࡙ࠧḩ"), bstack11ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡮ࡲࡧࡦࡲࡨࡰࡵࡷ࠾࠺࠹࠳࠹ࠩḪ"))
      bstack111l111l11l_opy_ = bstack1111ll1l111_opy_ + bstack11l1ll1lll1_opy_
      response = requests.get(bstack111l111l11l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨḫ"), {}).get(bstack11ll1l1_opy_ (u"ࠪ࡭ࡩ࠭Ḭ"), None)
      return True
    except:
      self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡪࡨࡥࡱࡺࡨࠡࡥ࡫ࡩࡨࡱࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤḭ"))
      return False
  def bstack1111llll1ll_opy_(self):
    bstack1111lll111l_opy_ = bstack11ll1l1_opy_ (u"ࠬࡧࡰࡱࠩḮ") if self.bstack1llll1l1l1_opy_ else bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨḯ")
    bstack111l111l111_opy_ = bstack11ll1l1_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥḰ") if self.config.get(bstack11ll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧḱ")) is None else True
    bstack11ll11lll11_opy_ = bstack11ll1l1_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠧࡲࡨࡶࡨࡿ࠽ࡼࡿࠥḲ").format(self.config[bstack11ll1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨḳ")], bstack1111lll111l_opy_, bstack111l111l111_opy_)
    if self.percy_capture_mode:
      bstack11ll11lll11_opy_ += bstack11ll1l1_opy_ (u"ࠦࠫࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࡀࡿࢂࠨḴ").format(self.percy_capture_mode)
    uri = bstack111l11ll_opy_(bstack11ll11lll11_opy_)
    try:
      response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡍࡅࡕࠩḵ"), uri, {}, {bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫḶ"): (self.config[bstack11ll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩḷ")], self.config[bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫḸ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l1ll1111_opy_ = data.get(bstack11ll1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪḹ"))
        self.percy_capture_mode = data.get(bstack11ll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥࠨḺ"))
        os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩḻ")] = str(self.bstack11l1ll1111_opy_)
        os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩḼ")] = str(self.percy_capture_mode)
        if bstack111l111l111_opy_ == bstack11ll1l1_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤḽ") and str(self.bstack11l1ll1111_opy_).lower() == bstack11ll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧḾ"):
          self.bstack1lllll11l_opy_ = True
        if bstack11ll1l1_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢḿ") in data:
          return data[bstack11ll1l1_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣṀ")]
        else:
          raise bstack11ll1l1_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪṁ").format(data)
      else:
        raise bstack11ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦṂ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨṃ").format(e))
  def bstack1111l1l1111_opy_(self):
    bstack1111lll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤṄ"))
    try:
      if bstack11ll1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨṅ") not in self.bstack1111ll11111_opy_:
        self.bstack1111ll11111_opy_[bstack11ll1l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩṆ")] = 2
      with open(bstack1111lll11ll_opy_, bstack11ll1l1_opy_ (u"ࠩࡺࠫṇ")) as fp:
        json.dump(self.bstack1111ll11111_opy_, fp)
      return bstack1111lll11ll_opy_
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥṈ").format(e))
  def bstack1111ll11l11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111lll1111_opy_ == bstack11ll1l1_opy_ (u"ࠫࡼ࡯࡮ࠨṉ"):
        bstack1111l11lll1_opy_ = [bstack11ll1l1_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭Ṋ"), bstack11ll1l1_opy_ (u"࠭࠯ࡤࠩṋ")]
        cmd = bstack1111l11lll1_opy_ + cmd
      cmd = bstack11ll1l1_opy_ (u"ࠧࠡࠩṌ").join(cmd)
      self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧṍ").format(cmd))
      with open(self.bstack111l111ll1l_opy_, bstack11ll1l1_opy_ (u"ࠤࡤࠦṎ")) as bstack1111ll1llll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111ll1llll_opy_, text=True, stderr=bstack1111ll1llll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l1lll1l_opy_ = True
      self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧṏ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l1l11l1_opy_:
        self.logger.info(bstack11ll1l1_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧṐ"))
        cmd = [self.binary_path, bstack11ll1l1_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣṑ")]
        self.bstack1111ll11l11_opy_(cmd)
        self.bstack1111l1l11l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨṒ").format(cmd, e))
  def bstack1l1l1l1111_opy_(self):
    if not self.bstack11l1ll1111_opy_:
      return
    try:
      bstack1111lllll11_opy_ = 0
      while not self.bstack1111l1l11l1_opy_ and bstack1111lllll11_opy_ < self.bstack1111l1ll1ll_opy_:
        if self.bstack1111l1lll1l_opy_:
          self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧṓ"))
          return
        time.sleep(1)
        bstack1111lllll11_opy_ += 1
      os.environ[bstack11ll1l1_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧṔ")] = str(self.bstack1111l1ll11l_opy_())
      self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥṕ"))
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦṖ").format(e))
  def bstack1111l1ll11l_opy_(self):
    if self.bstack1llll1l1l1_opy_:
      return
    try:
      bstack1111ll1ll11_opy_ = [platform[bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩṗ")].lower() for platform in self.config.get(bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨṘ"), [])]
      bstack111l1111lll_opy_ = sys.maxsize
      bstack1111l1l1l11_opy_ = bstack11ll1l1_opy_ (u"࠭ࠧṙ")
      for browser in bstack1111ll1ll11_opy_:
        if browser in self.bstack111l11111l1_opy_:
          bstack1111lllll1l_opy_ = self.bstack111l11111l1_opy_[browser]
        if bstack1111lllll1l_opy_ < bstack111l1111lll_opy_:
          bstack111l1111lll_opy_ = bstack1111lllll1l_opy_
          bstack1111l1l1l11_opy_ = browser
      return bstack1111l1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack11ll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣṚ").format(e))
  @classmethod
  def bstack1l1ll1l11_opy_(self):
    return os.getenv(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ṛ"), bstack11ll1l1_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨṜ")).lower()
  @classmethod
  def bstack1ll1ll11ll_opy_(self):
    return os.getenv(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧṝ"), bstack11ll1l1_opy_ (u"ࠫࠬṞ"))
  @classmethod
  def bstack1l1l1l1lll1_opy_(cls, value):
    cls.bstack1lllll11l_opy_ = value
  @classmethod
  def bstack1111lll1ll1_opy_(cls):
    return cls.bstack1lllll11l_opy_
  @classmethod
  def bstack1l1l1l1l11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l1l11ll_opy_(cls):
    return cls.percy_build_id