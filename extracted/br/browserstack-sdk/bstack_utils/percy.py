# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
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
from bstack_utils.helper import bstack111l11l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111l111l_opy_ import bstack11l1l1ll11_opy_
class bstack111llll11_opy_:
  working_dir = os.getcwd()
  bstack1ll11ll11_opy_ = False
  config = {}
  bstack111ll11l11l_opy_ = bstack11l1ll1_opy_ (u"ࠨࠩ‰")
  binary_path = bstack11l1ll1_opy_ (u"ࠩࠪ‱")
  bstack1llllll1llll_opy_ = bstack11l1ll1_opy_ (u"ࠪࠫ′")
  bstack1ll1lll11l_opy_ = False
  bstack1llllll11ll1_opy_ = None
  bstack1llllll111l1_opy_ = {}
  bstack1lllll1l1ll1_opy_ = 300
  bstack1lllll11ll1l_opy_ = False
  logger = None
  bstack1llllll1lll1_opy_ = False
  bstack1111l1ll1_opy_ = False
  percy_build_id = None
  bstack1llll1ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠫࠬ″")
  bstack1lllll11l11l_opy_ = {
    bstack11l1ll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ‴") : 1,
    bstack11l1ll1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ‵") : 2,
    bstack11l1ll1_opy_ (u"ࠧࡦࡦࡪࡩࠬ‶") : 3,
    bstack11l1ll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ‷") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lllll1ll1ll_opy_(self):
    bstack1llll1lll111_opy_ = bstack11l1ll1_opy_ (u"ࠩࠪ‸")
    bstack1lllll1l1111_opy_ = sys.platform
    bstack1llllll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ‹")
    if re.match(bstack11l1ll1_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦ›"), bstack1lllll1l1111_opy_) != None:
      bstack1llll1lll111_opy_ = bstack11l111ll1l1_opy_ + bstack11l1ll1_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨ※")
      self.bstack1llll1ll1l11_opy_ = bstack11l1ll1_opy_ (u"࠭࡭ࡢࡥࠪ‼")
    elif re.match(bstack11l1ll1_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧ‽"), bstack1lllll1l1111_opy_) != None:
      bstack1llll1lll111_opy_ = bstack11l111ll1l1_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤ‾")
      bstack1llllll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧ‿")
      self.bstack1llll1ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠪࡻ࡮ࡴࠧ⁀")
    else:
      bstack1llll1lll111_opy_ = bstack11l111ll1l1_opy_ + bstack11l1ll1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢ⁁")
      self.bstack1llll1ll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫ⁂")
    return bstack1llll1lll111_opy_, bstack1llllll1111l_opy_
  def bstack1llll1ll1lll_opy_(self):
    try:
      bstack1llll1ll11ll_opy_ = [os.path.join(expanduser(bstack11l1ll1_opy_ (u"ࠨࡾࠣ⁃")), bstack11l1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⁄")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll1ll11ll_opy_:
        if(self.bstack1lllll1llll1_opy_(path)):
          return path
      raise bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧ⁅")
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦ⁆").format(e))
  def bstack1lllll1llll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lllll11l1ll_opy_(self, bstack1lllll11l111_opy_):
    return os.path.join(bstack1lllll11l111_opy_, self.bstack111ll11l11l_opy_ + bstack11l1ll1_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤ⁇"))
  def bstack1llll1lll11l_opy_(self, bstack1lllll11l111_opy_, bstack1lllll1lll11_opy_):
    if not bstack1lllll1lll11_opy_: return
    try:
      bstack1lllll11111l_opy_ = self.bstack1lllll11l1ll_opy_(bstack1lllll11l111_opy_)
      with open(bstack1lllll11111l_opy_, bstack11l1ll1_opy_ (u"ࠦࡼࠨ⁈")) as f:
        f.write(bstack1lllll1lll11_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤ⁉"))
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ⁊").format(e))
  def bstack1lllll11lll1_opy_(self, bstack1lllll11l111_opy_):
    try:
      bstack1lllll11111l_opy_ = self.bstack1lllll11l1ll_opy_(bstack1lllll11l111_opy_)
      if os.path.exists(bstack1lllll11111l_opy_):
        with open(bstack1lllll11111l_opy_, bstack11l1ll1_opy_ (u"ࠢࡳࠤ⁋")) as f:
          bstack1lllll1lll11_opy_ = f.read().strip()
          return bstack1lllll1lll11_opy_ if bstack1lllll1lll11_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ⁌").format(e))
  def bstack1lllll1ll111_opy_(self, bstack1lllll11l111_opy_, bstack1llll1lll111_opy_):
    bstack1lllll1l11l1_opy_ = self.bstack1lllll11lll1_opy_(bstack1lllll11l111_opy_)
    if bstack1lllll1l11l1_opy_:
      try:
        bstack1llll1lll1l1_opy_ = self.bstack1lllll1l1lll_opy_(bstack1lllll1l11l1_opy_, bstack1llll1lll111_opy_)
        if not bstack1llll1lll1l1_opy_:
          self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦ⁍"))
          return True
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤ⁎"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥ⁏").format(e))
    return False
  def bstack1lllll1l1lll_opy_(self, bstack1lllll1l11l1_opy_, bstack1llll1lll111_opy_):
    try:
      headers = {
        bstack11l1ll1_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧ⁐"): bstack1lllll1l11l1_opy_
      }
      response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"࠭ࡇࡆࡖࠪ⁑"), bstack1llll1lll111_opy_, {}, {bstack11l1ll1_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣ⁒"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥ⁓").format(e))
  @measure(event_name=EVENTS.bstack11l11l11l1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
  def bstack1llll1lll1ll_opy_(self, bstack1llll1lll111_opy_, bstack1llllll1111l_opy_):
    try:
      bstack1lllll1ll11l_opy_ = self.bstack1llll1ll1lll_opy_()
      bstack1lllll1l111l_opy_ = os.path.join(bstack1lllll1ll11l_opy_, bstack11l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬ⁔"))
      bstack1lllll1l1l11_opy_ = os.path.join(bstack1lllll1ll11l_opy_, bstack1llllll1111l_opy_)
      if self.bstack1lllll1ll111_opy_(bstack1lllll1ll11l_opy_, bstack1llll1lll111_opy_): # if bstack1lllll11l1l1_opy_, bstack1l111llll1l_opy_ bstack1lllll1lll11_opy_ is bstack1llllll1l111_opy_ to bstack111l11l11l1_opy_ version available (response 304)
        if os.path.exists(bstack1lllll1l1l11_opy_):
          self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ⁕").format(bstack1lllll1l1l11_opy_))
          return bstack1lllll1l1l11_opy_
        if os.path.exists(bstack1lllll1l111l_opy_):
          self.logger.info(bstack11l1ll1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤ⁖").format(bstack1lllll1l111l_opy_))
          return self.bstack1lllll1111ll_opy_(bstack1lllll1l111l_opy_, bstack1llllll1111l_opy_)
      self.logger.info(bstack11l1ll1_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥ⁗").format(bstack1llll1lll111_opy_))
      response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"࠭ࡇࡆࡖࠪ⁘"), bstack1llll1lll111_opy_, {}, {})
      if response.status_code == 200:
        bstack1lllllll1l11_opy_ = response.headers.get(bstack11l1ll1_opy_ (u"ࠢࡆࡖࡤ࡫ࠧ⁙"), bstack11l1ll1_opy_ (u"ࠣࠤ⁚"))
        if bstack1lllllll1l11_opy_:
          self.bstack1llll1lll11l_opy_(bstack1lllll1ll11l_opy_, bstack1lllllll1l11_opy_)
        with open(bstack1lllll1l111l_opy_, bstack11l1ll1_opy_ (u"ࠩࡺࡦࠬ⁛")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣ⁜").format(bstack1lllll1l111l_opy_))
        return self.bstack1lllll1111ll_opy_(bstack1lllll1l111l_opy_, bstack1llllll1111l_opy_)
      else:
        raise(bstack11l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢ⁝").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨ⁞").format(e))
  def bstack1lllll111l1l_opy_(self, bstack1llll1lll111_opy_, bstack1llllll1111l_opy_):
    try:
      retry = 2
      bstack1lllll1l1l11_opy_ = None
      bstack1lllll1lll1l_opy_ = False
      while retry > 0:
        bstack1lllll1l1l11_opy_ = self.bstack1llll1lll1ll_opy_(bstack1llll1lll111_opy_, bstack1llllll1111l_opy_)
        bstack1lllll1lll1l_opy_ = self.bstack1llllll1ll11_opy_(bstack1llll1lll111_opy_, bstack1llllll1111l_opy_, bstack1lllll1l1l11_opy_)
        if bstack1lllll1lll1l_opy_:
          break
        retry -= 1
      return bstack1lllll1l1l11_opy_, bstack1lllll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥ ").format(e))
    return bstack1lllll1l1l11_opy_, False
  def bstack1llllll1ll11_opy_(self, bstack1llll1lll111_opy_, bstack1llllll1111l_opy_, bstack1lllll1l1l11_opy_, bstack1llllll1l1l1_opy_ = 0):
    if bstack1llllll1l1l1_opy_ > 1:
      return False
    if bstack1lllll1l1l11_opy_ == None or os.path.exists(bstack1lllll1l1l11_opy_) == False:
      self.logger.warn(bstack11l1ll1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧ⁠"))
      return False
    command = bstack11l1ll1_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧ⁡").format(bstack1lllll1l1l11_opy_)
    bstack1lllll111lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack11l1ll1_opy_ (u"ࠩࡃࡴࡪࡸࡣࡺ࠱ࡦࡰ࡮࠭⁢") in bstack1lllll111lll_opy_:
      return True
    else:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤ⁣"))
      return False
  def bstack1lllll1111ll_opy_(self, bstack1lllll1l111l_opy_, bstack1llllll1111l_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllll1l111l_opy_)
      shutil.unpack_archive(bstack1lllll1l111l_opy_, working_dir)
      bstack1lllll1l1l11_opy_ = os.path.join(working_dir, bstack1llllll1111l_opy_)
      os.chmod(bstack1lllll1l1l11_opy_, 0o755)
      return bstack1lllll1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧ⁤"))
  def bstack1llllll11111_opy_(self):
    try:
      bstack1llll1llll11_opy_ = self.config.get(bstack11l1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⁥"))
      bstack1llllll11111_opy_ = bstack1llll1llll11_opy_ or (bstack1llll1llll11_opy_ is None and self.bstack1ll11ll11_opy_)
      if not bstack1llllll11111_opy_ or self.config.get(bstack11l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⁦"), None) not in bstack11l111lllll_opy_:
        return False
      self.bstack1ll1lll11l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⁧").format(e))
  def bstack1llllll11l11_opy_(self):
    try:
      bstack1llllll11l11_opy_ = self.percy_capture_mode
      return bstack1llllll11l11_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⁨").format(e))
  def init(self, bstack1ll11ll11_opy_, config, logger):
    self.bstack1ll11ll11_opy_ = bstack1ll11ll11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llllll11111_opy_():
      return
    self.bstack1llllll111l1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⁩"), {})
    self.percy_capture_mode = config.get(bstack11l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭⁪"))
    try:
      bstack1llll1lll111_opy_, bstack1llllll1111l_opy_ = self.bstack1lllll1ll1ll_opy_()
      self.bstack111ll11l11l_opy_ = bstack1llllll1111l_opy_
      bstack1lllll1l1l11_opy_, bstack1lllll1lll1l_opy_ = self.bstack1lllll111l1l_opy_(bstack1llll1lll111_opy_, bstack1llllll1111l_opy_)
      if bstack1lllll1lll1l_opy_:
        self.binary_path = bstack1lllll1l1l11_opy_
        thread = Thread(target=self.bstack1lllll1l1l1l_opy_)
        thread.start()
      else:
        self.bstack1llllll1lll1_opy_ = True
        self.logger.error(bstack11l1ll1_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣ⁫").format(bstack1lllll1l1l11_opy_))
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⁬").format(e))
  def bstack1llllll1l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1ll1_opy_ (u"࠭࡬ࡰࡩࠪ⁭"), bstack11l1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪ⁮"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧ⁯").format(logfile))
      self.bstack1llllll1llll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⁰").format(e))
  @measure(event_name=EVENTS.bstack11l111l11l1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
  def bstack1lllll1l1l1l_opy_(self):
    bstack1lllllll111l_opy_ = self.bstack1lllllll11l1_opy_()
    if bstack1lllllll111l_opy_ == None:
      self.bstack1llllll1lll1_opy_ = True
      self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨⁱ"))
      return False
    bstack1llll1ll1l1l_opy_ = [bstack11l1ll1_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧ⁲") if self.bstack1ll11ll11_opy_ else bstack11l1ll1_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩ⁳")]
    bstack1111l111lll_opy_ = self.bstack1llll1llll1l_opy_()
    if bstack1111l111lll_opy_ != None:
      bstack1llll1ll1l1l_opy_.append(bstack11l1ll1_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧ⁴").format(bstack1111l111lll_opy_))
    env = os.environ.copy()
    env[bstack11l1ll1_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧ⁵")] = bstack1lllllll111l_opy_
    env[bstack11l1ll1_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣ⁶")] = os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⁷"), bstack11l1ll1_opy_ (u"ࠪࠫ⁸"))
    bstack1lllll1l11ll_opy_ = [self.binary_path]
    self.bstack1llllll1l11l_opy_()
    self.bstack1llllll11ll1_opy_ = self.bstack1lllll1lllll_opy_(bstack1lllll1l11ll_opy_ + bstack1llll1ll1l1l_opy_, env)
    self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧ⁹"))
    bstack1llllll1l1l1_opy_ = 0
    while self.bstack1llllll11ll1_opy_.poll() == None:
      bstack1lllll11ll11_opy_ = self.bstack1llllll111ll_opy_()
      if bstack1lllll11ll11_opy_:
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣ⁺"))
        self.bstack1lllll11ll1l_opy_ = True
        return True
      bstack1llllll1l1l1_opy_ += 1
      self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤ⁻").format(bstack1llllll1l1l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧ⁼").format(bstack1llllll1l1l1_opy_))
    self.bstack1llllll1lll1_opy_ = True
    return False
  def bstack1llllll111ll_opy_(self, bstack1llllll1l1l1_opy_ = 0):
    if bstack1llllll1l1l1_opy_ > 10:
      return False
    try:
      bstack1llllll1ll1l_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨ⁽"), bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪ⁾"))
      bstack1llllll11l1l_opy_ = bstack1llllll1ll1l_opy_ + bstack11l1111111l_opy_
      response = requests.get(bstack1llllll11l1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࠩⁿ"), {}).get(bstack11l1ll1_opy_ (u"ࠫ࡮ࡪࠧ₀"), None)
      return True
    except:
      self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ₁"))
      return False
  def bstack1lllllll11l1_opy_(self):
    bstack1llllll11lll_opy_ = bstack11l1ll1_opy_ (u"࠭ࡡࡱࡲࠪ₂") if self.bstack1ll11ll11_opy_ else bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ₃")
    bstack1lllll111ll1_opy_ = bstack11l1ll1_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ₄") if self.config.get(bstack11l1ll1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ₅")) is None else True
    bstack11l11lllll1_opy_ = bstack11l1ll1_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀࠦ₆").format(self.config[bstack11l1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ₇")], bstack1llllll11lll_opy_, bstack1lllll111ll1_opy_)
    if self.percy_capture_mode:
      bstack11l11lllll1_opy_ += bstack11l1ll1_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃࠢ₈").format(self.percy_capture_mode)
    uri = bstack11l1l1ll11_opy_(bstack11l11lllll1_opy_)
    try:
      response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"࠭ࡇࡆࡖࠪ₉"), uri, {}, {bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ₊"): (self.config[bstack11l1ll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ₋")], self.config[bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ₌")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1ll1lll11l_opy_ = data.get(bstack11l1ll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ₍"))
        self.percy_capture_mode = data.get(bstack11l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦࠩ₎"))
        os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪ₏")] = str(self.bstack1ll1lll11l_opy_)
        os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪₐ")] = str(self.percy_capture_mode)
        if bstack1lllll111ll1_opy_ == bstack11l1ll1_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦࠥₑ") and str(self.bstack1ll1lll11l_opy_).lower() == bstack11l1ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨₒ"):
          self.bstack1111l1ll1_opy_ = True
        if bstack11l1ll1_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣₓ") in data:
          return data[bstack11l1ll1_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤₔ")]
        else:
          raise bstack11l1ll1_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫₕ").format(data)
      else:
        raise bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧₖ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢₗ").format(e))
  def bstack1llll1llll1l_opy_(self):
    bstack1lllll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥₘ"))
    try:
      if bstack11l1ll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩₙ") not in self.bstack1llllll111l1_opy_:
        self.bstack1llllll111l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪₚ")] = 2
      with open(bstack1lllll1111l1_opy_, bstack11l1ll1_opy_ (u"ࠪࡻࠬₛ")) as fp:
        json.dump(self.bstack1llllll111l1_opy_, fp)
      return bstack1lllll1111l1_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦₜ").format(e))
  def bstack1lllll1lllll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1ll1l11_opy_ == bstack11l1ll1_opy_ (u"ࠬࡽࡩ࡯ࠩ₝"):
        bstack1lllll111111_opy_ = [bstack11l1ll1_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧ₞"), bstack11l1ll1_opy_ (u"ࠧ࠰ࡥࠪ₟")]
        cmd = bstack1lllll111111_opy_ + cmd
      cmd = bstack11l1ll1_opy_ (u"ࠨࠢࠪ₠").join(cmd)
      self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨ₡").format(cmd))
      with open(self.bstack1llllll1llll_opy_, bstack11l1ll1_opy_ (u"ࠥࡥࠧ₢")) as bstack1lllll11llll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lllll11llll_opy_, text=True, stderr=bstack1lllll11llll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llllll1lll1_opy_ = True
      self.logger.error(bstack11l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ₣").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lllll11ll1l_opy_:
        self.logger.info(bstack11l1ll1_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨ₤"))
        cmd = [self.binary_path, bstack11l1ll1_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤ₥")]
        self.bstack1lllll1lllll_opy_(cmd)
        self.bstack1lllll11ll1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ₦").format(cmd, e))
  def bstack1111ll11_opy_(self):
    if not self.bstack1ll1lll11l_opy_:
      return
    try:
      bstack1llllll1l1ll_opy_ = 0
      while not self.bstack1lllll11ll1l_opy_ and bstack1llllll1l1ll_opy_ < self.bstack1lllll1l1ll1_opy_:
        if self.bstack1llllll1lll1_opy_:
          self.logger.info(bstack11l1ll1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨ₧"))
          return
        time.sleep(1)
        bstack1llllll1l1ll_opy_ += 1
      os.environ[bstack11l1ll1_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ₨")] = str(self.bstack1llll1ll1ll1_opy_())
      self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦ₩"))
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ₪").format(e))
  def bstack1llll1ll1ll1_opy_(self):
    if self.bstack1ll11ll11_opy_:
      return
    try:
      bstack1llll1lllll1_opy_ = [platform[bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ₫")].lower() for platform in self.config.get(bstack11l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ€"), [])]
      bstack1lllllll11ll_opy_ = sys.maxsize
      bstack1lllllll1111_opy_ = bstack11l1ll1_opy_ (u"ࠧࠨ₭")
      for browser in bstack1llll1lllll1_opy_:
        if browser in self.bstack1lllll11l11l_opy_:
          bstack1lllll1ll1l1_opy_ = self.bstack1lllll11l11l_opy_[browser]
        if bstack1lllll1ll1l1_opy_ < bstack1lllllll11ll_opy_:
          bstack1lllllll11ll_opy_ = bstack1lllll1ll1l1_opy_
          bstack1lllllll1111_opy_ = browser
      return bstack1lllllll1111_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ₮").format(e))
  @classmethod
  def bstack1l11l111l_opy_(self):
    return os.getenv(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧ₯"), bstack11l1ll1_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩ₰")).lower()
  @classmethod
  def bstack1l111l11_opy_(self):
    return os.getenv(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ₱"), bstack11l1ll1_opy_ (u"ࠬ࠭₲"))
  @classmethod
  def bstack1l11l11ll1l_opy_(cls, value):
    cls.bstack1111l1ll1_opy_ = value
  @classmethod
  def bstack1lllll111l11_opy_(cls):
    return cls.bstack1111l1ll1_opy_
  @classmethod
  def bstack1l11l1l11l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1llll1llllll_opy_(cls):
    return cls.percy_build_id