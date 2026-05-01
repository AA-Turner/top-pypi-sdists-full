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
from bstack_utils.helper import bstack1ll11l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1ll1l1ll11_opy_
class bstack1l1lllll1_opy_:
  working_dir = os.getcwd()
  bstack11ll1l1lll_opy_ = False
  config = {}
  bstack1lllll11l1l1_opy_ = bstack111ll_opy_ (u"ࠫࠬ◪")
  binary_path = bstack111ll_opy_ (u"ࠬ࠭◫")
  bstack1ll1l1ll11l1_opy_ = bstack111ll_opy_ (u"࠭ࠧ◬")
  bstack1llll1llll_opy_ = False
  bstack1ll1l1lll111_opy_ = None
  bstack1ll1ll1lll11_opy_ = {}
  bstack1ll1lll1ll1l_opy_ = 300
  bstack1ll1l1llllll_opy_ = False
  logger = None
  bstack1ll1lll11l1l_opy_ = False
  bstack11l11l111l_opy_ = False
  percy_build_id = None
  bstack1ll1ll111lll_opy_ = bstack111ll_opy_ (u"ࠧࠨ◭")
  bstack1ll1ll1lll1l_opy_ = {
    bstack111ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ◮") : 1,
    bstack111ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ◯") : 2,
    bstack111ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨ◰") : 3,
    bstack111ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫ◱") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1ll11ll1l_opy_(self):
    bstack1ll1l1lll1l1_opy_ = bstack111ll_opy_ (u"ࠬ࠭◲")
    bstack1ll1lll1l111_opy_ = sys.platform
    bstack1ll1ll1111l1_opy_ = bstack111ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ◳")
    if re.match(bstack111ll_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢ◴"), bstack1ll1lll1l111_opy_) != None:
      bstack1ll1l1lll1l1_opy_ = bstack111111l1ll1_opy_ + bstack111ll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤ◵")
      self.bstack1ll1ll111lll_opy_ = bstack111ll_opy_ (u"ࠩࡰࡥࡨ࠭◶")
    elif re.match(bstack111ll_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣ◷"), bstack1ll1lll1l111_opy_) != None:
      bstack1ll1l1lll1l1_opy_ = bstack111111l1ll1_opy_ + bstack111ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧ◸")
      bstack1ll1ll1111l1_opy_ = bstack111ll_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣ◹")
      self.bstack1ll1ll111lll_opy_ = bstack111ll_opy_ (u"࠭ࡷࡪࡰࠪ◺")
    else:
      bstack1ll1l1lll1l1_opy_ = bstack111111l1ll1_opy_ + bstack111ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥ◻")
      self.bstack1ll1ll111lll_opy_ = bstack111ll_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧ◼")
    return bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_
  def bstack1ll1ll11l1ll_opy_(self):
    try:
      bstack1ll1ll11lll1_opy_ = [os.path.join(expanduser(bstack111ll_opy_ (u"ࠤࢁࠦ◽")), bstack111ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ◾")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1ll11lll1_opy_:
        if(self.bstack1ll1l1ll1l1l_opy_(path)):
          return path
      raise bstack111ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣ◿")
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢ☀").format(e))
  def bstack1ll1l1ll1l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1ll1lll1111l_opy_(self, bstack1ll1lll111l1_opy_):
    return os.path.join(bstack1ll1lll111l1_opy_, self.bstack1lllll11l1l1_opy_ + bstack111ll_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧ☁"))
  def bstack1ll1l1ll1ll1_opy_(self, bstack1ll1lll111l1_opy_, bstack1ll1l1ll1111_opy_):
    if not bstack1ll1l1ll1111_opy_: return
    try:
      bstack1ll1ll1ll111_opy_ = self.bstack1ll1lll1111l_opy_(bstack1ll1lll111l1_opy_)
      with open(bstack1ll1ll1ll111_opy_, bstack111ll_opy_ (u"ࠢࡸࠤ☂")) as f:
        f.write(bstack1ll1l1ll1111_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧ☃"))
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ☄").format(e))
  def bstack1ll1ll111ll1_opy_(self, bstack1ll1lll111l1_opy_):
    try:
      bstack1ll1ll1ll111_opy_ = self.bstack1ll1lll1111l_opy_(bstack1ll1lll111l1_opy_)
      if os.path.exists(bstack1ll1ll1ll111_opy_):
        with open(bstack1ll1ll1ll111_opy_, bstack111ll_opy_ (u"ࠥࡶࠧ★")) as f:
          bstack1ll1l1ll1111_opy_ = f.read().strip()
          return bstack1ll1l1ll1111_opy_ if bstack1ll1l1ll1111_opy_ else None
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ☆").format(e))
  def bstack1ll1lll1l1l1_opy_(self, bstack1ll1lll111l1_opy_, bstack1ll1l1lll1l1_opy_):
    bstack1ll1ll1l1ll1_opy_ = self.bstack1ll1ll111ll1_opy_(bstack1ll1lll111l1_opy_)
    if bstack1ll1ll1l1ll1_opy_:
      try:
        bstack1ll1ll1ll1l1_opy_ = self.bstack1ll1ll11l1l1_opy_(bstack1ll1ll1l1ll1_opy_, bstack1ll1l1lll1l1_opy_)
        if not bstack1ll1ll1ll1l1_opy_:
          self.logger.debug(bstack111ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢ☇"))
          return True
        self.logger.debug(bstack111ll_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧ☈"))
        return False
      except Exception as e:
        self.logger.warn(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨ☉").format(e))
    return False
  def bstack1ll1ll11l1l1_opy_(self, bstack1ll1ll1l1ll1_opy_, bstack1ll1l1lll1l1_opy_):
    try:
      headers = {
        bstack111ll_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣ☊"): bstack1ll1ll1l1ll1_opy_
      }
      response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠩࡊࡉ࡙࠭☋"), bstack1ll1l1lll1l1_opy_, {}, {bstack111ll_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ☌"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨ☍").format(e))
  @measure(event_name=EVENTS.bstack1111111l1l1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
  def bstack1ll1ll111l1l_opy_(self, bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_):
    try:
      bstack1ll1l1llll11_opy_ = self.bstack1ll1ll11l1ll_opy_()
      bstack1ll1ll1l1111_opy_ = os.path.join(bstack1ll1l1llll11_opy_, bstack111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨ☎"))
      bstack1ll1ll1111ll_opy_ = os.path.join(bstack1ll1l1llll11_opy_, bstack1ll1ll1111l1_opy_)
      if self.bstack1ll1lll1l1l1_opy_(bstack1ll1l1llll11_opy_, bstack1ll1l1lll1l1_opy_): # if true, bstack11l1lll1lll_opy_ bstack1ll1l1ll1111_opy_ is bstack1ll1lll11111_opy_ to bstack1llll1llll11_opy_ version available (response 304)
        if os.path.exists(bstack1ll1ll1111ll_opy_):
          self.logger.info(bstack111ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ☏").format(bstack1ll1ll1111ll_opy_))
          return bstack1ll1ll1111ll_opy_
        if os.path.exists(bstack1ll1ll1l1111_opy_):
          self.logger.info(bstack111ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧ☐").format(bstack1ll1ll1l1111_opy_))
          return self.bstack1ll1lll1l1ll_opy_(bstack1ll1ll1l1111_opy_, bstack1ll1ll1111l1_opy_)
      self.logger.info(bstack111ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨ☑").format(bstack1ll1l1lll1l1_opy_))
      response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠩࡊࡉ࡙࠭☒"), bstack1ll1l1lll1l1_opy_, {}, {})
      if response.status_code == 200:
        bstack1ll1ll1l11ll_opy_ = response.headers.get(bstack111ll_opy_ (u"ࠥࡉ࡙ࡧࡧࠣ☓"), bstack111ll_opy_ (u"ࠦࠧ☔"))
        if bstack1ll1ll1l11ll_opy_:
          self.bstack1ll1l1ll1ll1_opy_(bstack1ll1l1llll11_opy_, bstack1ll1ll1l11ll_opy_)
        with open(bstack1ll1ll1l1111_opy_, bstack111ll_opy_ (u"ࠬࡽࡢࠨ☕")) as file:
          file.write(response.content)
        self.logger.info(bstack111ll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦ☖").format(bstack1ll1ll1l1111_opy_))
        return self.bstack1ll1lll1l1ll_opy_(bstack1ll1ll1l1111_opy_, bstack1ll1ll1111l1_opy_)
      else:
        raise(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥ☗").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ☘").format(e))
  def bstack1ll1lll1ll11_opy_(self, bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_):
    try:
      retry = 2
      bstack1ll1ll1111ll_opy_ = None
      bstack1ll1ll111111_opy_ = False
      while retry > 0:
        bstack1ll1ll1111ll_opy_ = self.bstack1ll1ll111l1l_opy_(bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_)
        bstack1ll1ll111111_opy_ = self.bstack1ll1ll1ll11l_opy_(bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_, bstack1ll1ll1111ll_opy_)
        if bstack1ll1ll111111_opy_:
          break
        retry -= 1
      return bstack1ll1ll1111ll_opy_, bstack1ll1ll111111_opy_
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨ☙").format(e))
    return bstack1ll1ll1111ll_opy_, False
  def bstack1ll1ll1ll11l_opy_(self, bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_, bstack1ll1ll1111ll_opy_, bstack1ll1lll11l11_opy_ = 0):
    if bstack1ll1lll11l11_opy_ > 1:
      return False
    if bstack1ll1ll1111ll_opy_ == None or os.path.exists(bstack1ll1ll1111ll_opy_) == False:
      self.logger.warn(bstack111ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ☚"))
      return False
    command = bstack111ll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ☛").format(bstack1ll1ll1111ll_opy_)
    bstack1ll1ll11l11l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack111ll_opy_ (u"ࠬࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠩ☜") in bstack1ll1ll11l11l_opy_:
      return True
    else:
      self.logger.error(bstack111ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧ☝"))
      return False
  def bstack1ll1lll1l1ll_opy_(self, bstack1ll1ll1l1111_opy_, bstack1ll1ll1111l1_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1ll1l1111_opy_)
      shutil.unpack_archive(bstack1ll1ll1l1111_opy_, working_dir)
      bstack1ll1ll1111ll_opy_ = os.path.join(working_dir, bstack1ll1ll1111l1_opy_)
      os.chmod(bstack1ll1ll1111ll_opy_, 0o755)
      return bstack1ll1ll1111ll_opy_
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣ☞"))
  def bstack1ll1ll11llll_opy_(self):
    try:
      bstack1ll1l1llll1l_opy_ = self.config.get(bstack111ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ☟"))
      bstack1ll1ll11llll_opy_ = bstack1ll1l1llll1l_opy_ or (bstack1ll1l1llll1l_opy_ is None and self.bstack11ll1l1lll_opy_)
      if not bstack1ll1ll11llll_opy_ or self.config.get(bstack111ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ☠"), None) not in bstack111111ll1l1_opy_:
        return False
      self.bstack1llll1llll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ☡").format(e))
  def bstack1ll1lll111ll_opy_(self):
    try:
      bstack1ll1lll111ll_opy_ = self.percy_capture_mode
      return bstack1ll1lll111ll_opy_
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ☢").format(e))
  def init(self, bstack11ll1l1lll_opy_, config, logger):
    self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1ll1ll11llll_opy_():
      return
    self.bstack1ll1ll1lll11_opy_ = config.get(bstack111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ☣"), {})
    self.percy_capture_mode = config.get(bstack111ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ☤"))
    try:
      bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_ = self.bstack1ll1ll11ll1l_opy_()
      self.bstack1lllll11l1l1_opy_ = bstack1ll1ll1111l1_opy_
      bstack1ll1ll1111ll_opy_, bstack1ll1ll111111_opy_ = self.bstack1ll1lll1ll11_opy_(bstack1ll1l1lll1l1_opy_, bstack1ll1ll1111l1_opy_)
      if bstack1ll1ll111111_opy_:
        self.binary_path = bstack1ll1ll1111ll_opy_
        thread = Thread(target=self.bstack1ll1ll1ll1ll_opy_)
        thread.start()
      else:
        self.bstack1ll1lll11l1l_opy_ = True
        self.logger.error(bstack111ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦ☥").format(bstack1ll1ll1111ll_opy_))
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ☦").format(e))
  def bstack1ll1l1l1lll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111ll_opy_ (u"ࠩ࡯ࡳ࡬࠭☧"), bstack111ll_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭☨"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111ll_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣ☩").format(logfile))
      self.bstack1ll1l1ll11l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ☪").format(e))
  @measure(event_name=EVENTS.bstack111111l1l11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
  def bstack1ll1ll1ll1ll_opy_(self):
    bstack1ll1l1lllll1_opy_ = self.bstack1ll1ll111l11_opy_()
    if bstack1ll1l1lllll1_opy_ == None:
      self.bstack1ll1lll11l1l_opy_ = True
      self.logger.error(bstack111ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤ☫"))
      return False
    bstack1ll1l1lll11l_opy_ = [bstack111ll_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣ☬") if self.bstack11ll1l1lll_opy_ else bstack111ll_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬ☭")]
    bstack1l1l1l1lll_opy_ = self.bstack1ll1ll11111l_opy_()
    if bstack1l1l1l1lll_opy_ != None:
      bstack1ll1l1lll11l_opy_.append(bstack111ll_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣ☮").format(bstack1l1l1l1lll_opy_))
    env = os.environ.copy()
    env[bstack111ll_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣ☯")] = bstack1ll1l1lllll1_opy_
    env[bstack111ll_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦ☰")] = os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ☱"), bstack111ll_opy_ (u"࠭ࠧ☲"))
    bstack1ll1l1ll1l11_opy_ = [self.binary_path]
    self.bstack1ll1l1l1lll1_opy_()
    self.bstack1ll1l1lll111_opy_ = self.bstack1ll1l1ll111l_opy_(bstack1ll1l1ll1l11_opy_ + bstack1ll1l1lll11l_opy_, env)
    self.logger.debug(bstack111ll_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣ☳"))
    bstack1ll1lll11l11_opy_ = 0
    while self.bstack1ll1l1lll111_opy_.poll() == None:
      bstack1ll1ll1l1lll_opy_ = self.bstack1ll1l1lll1ll_opy_()
      if bstack1ll1ll1l1lll_opy_:
        self.logger.debug(bstack111ll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ☴"))
        self.bstack1ll1l1llllll_opy_ = True
        return True
      bstack1ll1lll11l11_opy_ += 1
      self.logger.debug(bstack111ll_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ☵").format(bstack1ll1lll11l11_opy_))
      time.sleep(2)
    self.logger.error(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣ☶").format(bstack1ll1lll11l11_opy_))
    self.bstack1ll1lll11l1l_opy_ = True
    return False
  def bstack1ll1l1lll1ll_opy_(self, bstack1ll1lll11l11_opy_ = 0):
    if bstack1ll1lll11l11_opy_ > 10:
      return False
    try:
      bstack1ll1ll1l11l1_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫ☷"), bstack111ll_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭☸"))
      bstack1ll1ll1l1l1l_opy_ = bstack1ll1ll1l11l1_opy_ + bstack1111111ll1l_opy_
      response = requests.get(bstack1ll1ll1l1l1l_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ☹"), {}).get(bstack111ll_opy_ (u"ࠧࡪࡦࠪ☺"), None)
      return True
    except:
      self.logger.debug(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ☻"))
      return False
  def bstack1ll1ll111l11_opy_(self):
    bstack1ll1ll11ll11_opy_ = bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭☼") if self.bstack11ll1l1lll_opy_ else bstack111ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ☽")
    bstack1ll1l1ll1lll_opy_ = bstack111ll_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ☾") if self.config.get(bstack111ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ☿")) is None else True
    bstack1111l1111l1_opy_ = bstack111ll_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢ♀").format(self.config[bstack111ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ♁")], bstack1ll1ll11ll11_opy_, bstack1ll1l1ll1lll_opy_)
    if self.percy_capture_mode:
      bstack1111l1111l1_opy_ += bstack111ll_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥ♂").format(self.percy_capture_mode)
    uri = bstack1ll1l1ll11_opy_(bstack1111l1111l1_opy_)
    try:
      response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠩࡊࡉ࡙࠭♃"), uri, {}, {bstack111ll_opy_ (u"ࠪࡥࡺࡺࡨࠨ♄"): (self.config[bstack111ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭♅")], self.config[bstack111ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ♆")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1llll1llll_opy_ = data.get(bstack111ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ♇"))
        self.percy_capture_mode = data.get(bstack111ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬ♈"))
        os.environ[bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭♉")] = str(self.bstack1llll1llll_opy_)
        os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭♊")] = str(self.percy_capture_mode)
        if bstack1ll1l1ll1lll_opy_ == bstack111ll_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨ♋") and str(self.bstack1llll1llll_opy_).lower() == bstack111ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ♌"):
          self.bstack11l11l111l_opy_ = True
        if bstack111ll_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ♍") in data:
          return data[bstack111ll_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ♎")]
        else:
          raise bstack111ll_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧ♏").format(data)
      else:
        raise bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣ♐").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥ♑").format(e))
  def bstack1ll1ll11111l_opy_(self):
    bstack1ll1lll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨ♒"))
    try:
      if bstack111ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ♓") not in self.bstack1ll1ll1lll11_opy_:
        self.bstack1ll1ll1lll11_opy_[bstack111ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭♔")] = 2
      with open(bstack1ll1lll1l11l_opy_, bstack111ll_opy_ (u"࠭ࡷࠨ♕")) as fp:
        json.dump(self.bstack1ll1ll1lll11_opy_, fp)
      return bstack1ll1lll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ♖").format(e))
  def bstack1ll1l1ll111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1ll111lll_opy_ == bstack111ll_opy_ (u"ࠨࡹ࡬ࡲࠬ♗"):
        bstack1ll1ll11l111_opy_ = [bstack111ll_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪ♘"), bstack111ll_opy_ (u"ࠪ࠳ࡨ࠭♙")]
        cmd = bstack1ll1ll11l111_opy_ + cmd
      cmd = bstack111ll_opy_ (u"ࠫࠥ࠭♚").join(cmd)
      self.logger.debug(bstack111ll_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤ♛").format(cmd))
      with open(self.bstack1ll1l1ll11l1_opy_, bstack111ll_opy_ (u"ࠨࡡࠣ♜")) as bstack1ll1l1l1llll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1ll1l1l1llll_opy_, text=True, stderr=bstack1ll1l1l1llll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1lll11l1l_opy_ = True
      self.logger.error(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ♝").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1ll1l1llllll_opy_:
        self.logger.info(bstack111ll_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤ♞"))
        cmd = [self.binary_path, bstack111ll_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧ♟")]
        self.bstack1ll1l1ll111l_opy_(cmd)
        self.bstack1ll1l1llllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ♠").format(cmd, e))
  def bstack11111ll11_opy_(self):
    if not self.bstack1llll1llll_opy_:
      return
    try:
      bstack1ll1ll1lllll_opy_ = 0
      while not self.bstack1ll1l1llllll_opy_ and bstack1ll1ll1lllll_opy_ < self.bstack1ll1lll1ll1l_opy_:
        if self.bstack1ll1lll11l1l_opy_:
          self.logger.info(bstack111ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤ♡"))
          return
        time.sleep(1)
        bstack1ll1ll1lllll_opy_ += 1
      os.environ[bstack111ll_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ♢")] = str(self.bstack1ll1lll11ll1_opy_())
      self.logger.info(bstack111ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢ♣"))
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ♤").format(e))
  def bstack1ll1lll11ll1_opy_(self):
    if self.bstack11ll1l1lll_opy_:
      return
    try:
      bstack1ll1l1ll11ll_opy_ = [platform[bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭♥")].lower() for platform in self.config.get(bstack111ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ♦"), [])]
      bstack1l1ll1l11l1_opy_ = sys.maxsize
      bstack1ll1ll1llll1_opy_ = bstack111ll_opy_ (u"ࠪࠫ♧")
      for browser in bstack1ll1l1ll11ll_opy_:
        if browser in self.bstack1ll1ll1lll1l_opy_:
          bstack1ll1ll1l1l11_opy_ = self.bstack1ll1ll1lll1l_opy_[browser]
        if bstack1ll1ll1l1l11_opy_ < bstack1l1ll1l11l1_opy_:
          bstack1l1ll1l11l1_opy_ = bstack1ll1ll1l1l11_opy_
          bstack1ll1ll1llll1_opy_ = browser
      return bstack1ll1ll1llll1_opy_
    except Exception as e:
      self.logger.error(bstack111ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ♨").format(e))
  @classmethod
  def bstack11l1111ll_opy_(self):
    return os.getenv(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪ♩"), bstack111ll_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬ♪")).lower()
  @classmethod
  def bstack111l1lll1_opy_(self):
    return os.getenv(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ♫"), bstack111ll_opy_ (u"ࠨࠩ♬"))
  @classmethod
  def bstack11ll11111l1_opy_(cls, value):
    cls.bstack11l11l111l_opy_ = value
  @classmethod
  def bstack1ll1ll1l111l_opy_(cls):
    return cls.bstack11l11l111l_opy_
  @classmethod
  def bstack11l1lllllll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1ll1lll11lll_opy_(cls):
    return cls.percy_build_id