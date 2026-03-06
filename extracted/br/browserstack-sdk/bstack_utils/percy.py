# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from bstack_utils.helper import bstack1llll1l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l11lll1l_opy_ import bstack1l1ll1l1ll_opy_
class bstack1l111llll1_opy_:
  working_dir = os.getcwd()
  bstack11l1ll1lll_opy_ = False
  config = {}
  bstack1111lll111l_opy_ = bstack1111_opy_ (u"ࠬ࠭≏")
  binary_path = bstack1111_opy_ (u"࠭ࠧ≐")
  bstack1llll1l1l111_opy_ = bstack1111_opy_ (u"ࠧࠨ≑")
  bstack1l1l1ll1ll_opy_ = False
  bstack1llll1l11l1l_opy_ = None
  bstack1llll111ll1l_opy_ = {}
  bstack1lll1lll11l1_opy_ = 300
  bstack1llll1111l1l_opy_ = False
  logger = None
  bstack1lll1ll1l1l1_opy_ = False
  bstack11111111_opy_ = False
  percy_build_id = None
  bstack1llll1l11l11_opy_ = bstack1111_opy_ (u"ࠨࠩ≒")
  bstack1lll1ll1l11l_opy_ = {
    bstack1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ≓") : 1,
    bstack1111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ≔") : 2,
    bstack1111_opy_ (u"ࠫࡪࡪࡧࡦࠩ≕") : 3,
    bstack1111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ≖") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll1lll1l11_opy_(self):
    bstack1llll1l111l1_opy_ = bstack1111_opy_ (u"࠭ࠧ≗")
    bstack1llll1111111_opy_ = sys.platform
    bstack1lll1ll1llll_opy_ = bstack1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭≘")
    if re.match(bstack1111_opy_ (u"ࠣࡦࡤࡶࡼ࡯࡮ࡽ࡯ࡤࡧࠥࡵࡳࠣ≙"), bstack1llll1111111_opy_) != None:
      bstack1llll1l111l1_opy_ = bstack111ll1l111l_opy_ + bstack1111_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡲࡷࡽ࠴ࡺࡪࡲࠥ≚")
      self.bstack1llll1l11l11_opy_ = bstack1111_opy_ (u"ࠪࡱࡦࡩࠧ≛")
    elif re.match(bstack1111_opy_ (u"ࠦࡲࡹࡷࡪࡰࡿࡱࡸࡿࡳࡽ࡯࡬ࡲ࡬ࡽࡼࡤࡻࡪࡻ࡮ࡴࡼࡣࡥࡦࡻ࡮ࡴࡼࡸ࡫ࡱࡧࡪࢂࡥ࡮ࡥࡿࡻ࡮ࡴ࠳࠳ࠤ≜"), bstack1llll1111111_opy_) != None:
      bstack1llll1l111l1_opy_ = bstack111ll1l111l_opy_ + bstack1111_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡽࡩ࡯࠰ࡽ࡭ࡵࠨ≝")
      bstack1lll1ll1llll_opy_ = bstack1111_opy_ (u"ࠨࡰࡦࡴࡦࡽ࠳࡫ࡸࡦࠤ≞")
      self.bstack1llll1l11l11_opy_ = bstack1111_opy_ (u"ࠧࡸ࡫ࡱࠫ≟")
    else:
      bstack1llll1l111l1_opy_ = bstack111ll1l111l_opy_ + bstack1111_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮࡮࡬ࡲࡺࡾ࠮ࡻ࡫ࡳࠦ≠")
      self.bstack1llll1l11l11_opy_ = bstack1111_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ≡")
    return bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_
  def bstack1llll111lll1_opy_(self):
    try:
      bstack1lll1lllll1l_opy_ = [os.path.join(expanduser(bstack1111_opy_ (u"ࠥࢂࠧ≢")), bstack1111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ≣")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1lllll1l_opy_:
        if(self.bstack1llll11111l1_opy_(path)):
          return path
      raise bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤ≤")
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠱ࠥࢁࡽࠣ≥").format(e))
  def bstack1llll11111l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll11l1111_opy_(self, bstack1llll1l11lll_opy_):
    return os.path.join(bstack1llll1l11lll_opy_, self.bstack1111lll111l_opy_ + bstack1111_opy_ (u"ࠢ࠯ࡧࡷࡥ࡬ࠨ≦"))
  def bstack1llll11l1ll1_opy_(self, bstack1llll1l11lll_opy_, bstack1llll111l111_opy_):
    if not bstack1llll111l111_opy_: return
    try:
      bstack1llll11lll1l_opy_ = self.bstack1llll11l1111_opy_(bstack1llll1l11lll_opy_)
      with open(bstack1llll11lll1l_opy_, bstack1111_opy_ (u"ࠣࡹࠥ≧")) as f:
        f.write(bstack1llll111l111_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠤࡖࡥࡻ࡫ࡤࠡࡰࡨࡻࠥࡋࡔࡢࡩࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠨ≨"))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡹ࡮ࡥࠡࡧࡷࡥ࡬࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ≩").format(e))
  def bstack1llll111l11l_opy_(self, bstack1llll1l11lll_opy_):
    try:
      bstack1llll11lll1l_opy_ = self.bstack1llll11l1111_opy_(bstack1llll1l11lll_opy_)
      if os.path.exists(bstack1llll11lll1l_opy_):
        with open(bstack1llll11lll1l_opy_, bstack1111_opy_ (u"ࠦࡷࠨ≪")) as f:
          bstack1llll111l111_opy_ = f.read().strip()
          return bstack1llll111l111_opy_ if bstack1llll111l111_opy_ else None
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡅࡕࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ≫").format(e))
  def bstack1lll1lll11ll_opy_(self, bstack1llll1l11lll_opy_, bstack1llll1l111l1_opy_):
    bstack1llll11ll1l1_opy_ = self.bstack1llll111l11l_opy_(bstack1llll1l11lll_opy_)
    if bstack1llll11ll1l1_opy_:
      try:
        bstack1llll111ll11_opy_ = self.bstack1lll1lll1l1l_opy_(bstack1llll11ll1l1_opy_, bstack1llll1l111l1_opy_)
        if not bstack1llll111ll11_opy_:
          self.logger.debug(bstack1111_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯ࡳࠡࡷࡳࠤࡹࡵࠠࡥࡣࡷࡩࠥ࠮ࡅࡕࡣࡪࠤࡺࡴࡣࡩࡣࡱ࡫ࡪࡪࠩࠣ≬"))
          return True
        self.logger.debug(bstack1111_opy_ (u"ࠢࡏࡧࡺࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡵࡱࡦࡤࡸࡪࠨ≭"))
        return False
      except Exception as e:
        self.logger.warn(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡴࡸࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢ≮").format(e))
    return False
  def bstack1lll1lll1l1l_opy_(self, bstack1llll11ll1l1_opy_, bstack1llll1l111l1_opy_):
    try:
      headers = {
        bstack1111_opy_ (u"ࠤࡌࡪ࠲ࡔ࡯࡯ࡧ࠰ࡑࡦࡺࡣࡩࠤ≯"): bstack1llll11ll1l1_opy_
      }
      response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠪࡋࡊ࡚ࠧ≰"), bstack1llll1l111l1_opy_, {}, {bstack1111_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧ≱"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡸࡴࡩࡧࡴࡦࡵ࠽ࠤࢀࢃࠢ≲").format(e))
  @measure(event_name=EVENTS.bstack111ll1l11ll_opy_, stage=STAGE.bstack111l1lllll_opy_)
  def bstack1lll1llll111_opy_(self, bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_):
    try:
      bstack1lll1llll11l_opy_ = self.bstack1llll111lll1_opy_()
      bstack1llll11l1l11_opy_ = os.path.join(bstack1lll1llll11l_opy_, bstack1111_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩ≳"))
      bstack1lll1ll1ll1l_opy_ = os.path.join(bstack1lll1llll11l_opy_, bstack1lll1ll1llll_opy_)
      if self.bstack1lll1lll11ll_opy_(bstack1lll1llll11l_opy_, bstack1llll1l111l1_opy_): # if true, bstack1l11111l1ll_opy_ bstack1llll111l111_opy_ is bstack1lll1llllll1_opy_ to bstack111l11l11ll_opy_ version available (response 304)
        if os.path.exists(bstack1lll1ll1ll1l_opy_):
          self.logger.info(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤ≴").format(bstack1lll1ll1ll1l_opy_))
          return bstack1lll1ll1ll1l_opy_
        if os.path.exists(bstack1llll11l1l11_opy_):
          self.logger.info(bstack1111_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨ≵").format(bstack1llll11l1l11_opy_))
          return self.bstack1lll1llll1ll_opy_(bstack1llll11l1l11_opy_, bstack1lll1ll1llll_opy_)
      self.logger.info(bstack1111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢ≶").format(bstack1llll1l111l1_opy_))
      response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠪࡋࡊ࡚ࠧ≷"), bstack1llll1l111l1_opy_, {}, {})
      if response.status_code == 200:
        bstack1lll1ll1lll1_opy_ = response.headers.get(bstack1111_opy_ (u"ࠦࡊ࡚ࡡࡨࠤ≸"), bstack1111_opy_ (u"ࠧࠨ≹"))
        if bstack1lll1ll1lll1_opy_:
          self.bstack1llll11l1ll1_opy_(bstack1lll1llll11l_opy_, bstack1lll1ll1lll1_opy_)
        with open(bstack1llll11l1l11_opy_, bstack1111_opy_ (u"࠭ࡷࡣࠩ≺")) as file:
          file.write(response.content)
        self.logger.info(bstack1111_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࢁࠧ≻").format(bstack1llll11l1l11_opy_))
        return self.bstack1lll1llll1ll_opy_(bstack1llll11l1l11_opy_, bstack1lll1ll1llll_opy_)
      else:
        raise(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࢀࠦ≼").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥ≽").format(e))
  def bstack1llll11l11ll_opy_(self, bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_):
    try:
      retry = 2
      bstack1lll1ll1ll1l_opy_ = None
      bstack1llll11l11l1_opy_ = False
      while retry > 0:
        bstack1lll1ll1ll1l_opy_ = self.bstack1lll1llll111_opy_(bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_)
        bstack1llll11l11l1_opy_ = self.bstack1llll11111ll_opy_(bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_, bstack1lll1ll1ll1l_opy_)
        if bstack1llll11l11l1_opy_:
          break
        retry -= 1
      return bstack1lll1ll1ll1l_opy_, bstack1llll11l11l1_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢ≾").format(e))
    return bstack1lll1ll1ll1l_opy_, False
  def bstack1llll11111ll_opy_(self, bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_, bstack1lll1ll1ll1l_opy_, bstack1lll1ll1ll11_opy_ = 0):
    if bstack1lll1ll1ll11_opy_ > 1:
      return False
    if bstack1lll1ll1ll1l_opy_ == None or os.path.exists(bstack1lll1ll1ll1l_opy_) == False:
      self.logger.warn(bstack1111_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤ≿"))
      return False
    command = bstack1111_opy_ (u"ࠬࢁࡽࠡ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫ⊀").format(bstack1lll1ll1ll1l_opy_)
    bstack1llll11ll1ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1111_opy_ (u"࠭ࡀࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫ࠪ⊁") in bstack1llll11ll1ll_opy_:
      return True
    else:
      self.logger.error(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨ⊂"))
      return False
  def bstack1lll1llll1ll_opy_(self, bstack1llll11l1l11_opy_, bstack1lll1ll1llll_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll11l1l11_opy_)
      shutil.unpack_archive(bstack1llll11l1l11_opy_, working_dir)
      bstack1lll1ll1ll1l_opy_ = os.path.join(working_dir, bstack1lll1ll1llll_opy_)
      os.chmod(bstack1lll1ll1ll1l_opy_, 0o755)
      return bstack1lll1ll1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤ⊃"))
  def bstack1llll1l111ll_opy_(self):
    try:
      bstack1llll11l111l_opy_ = self.config.get(bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⊄"))
      bstack1llll1l111ll_opy_ = bstack1llll11l111l_opy_ or (bstack1llll11l111l_opy_ is None and self.bstack11l1ll1lll_opy_)
      if not bstack1llll1l111ll_opy_ or self.config.get(bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⊅"), None) not in bstack111l1lll111_opy_:
        return False
      self.bstack1l1l1ll1ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⊆").format(e))
  def bstack1lll1lllllll_opy_(self):
    try:
      bstack1lll1lllllll_opy_ = self.percy_capture_mode
      return bstack1lll1lllllll_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠠࡤࡣࡳࡸࡺࡸࡥࠡ࡯ࡲࡨࡪ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⊇").format(e))
  def init(self, bstack11l1ll1lll_opy_, config, logger):
    self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1l111ll_opy_():
      return
    self.bstack1llll111ll1l_opy_ = config.get(bstack1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬ⊈"), {})
    self.percy_capture_mode = config.get(bstack1111_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪ⊉"))
    try:
      bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_ = self.bstack1lll1lll1l11_opy_()
      self.bstack1111lll111l_opy_ = bstack1lll1ll1llll_opy_
      bstack1lll1ll1ll1l_opy_, bstack1llll11l11l1_opy_ = self.bstack1llll11l11ll_opy_(bstack1llll1l111l1_opy_, bstack1lll1ll1llll_opy_)
      if bstack1llll11l11l1_opy_:
        self.binary_path = bstack1lll1ll1ll1l_opy_
        thread = Thread(target=self.bstack1llll111llll_opy_)
        thread.start()
      else:
        self.bstack1lll1ll1l1l1_opy_ = True
        self.logger.error(bstack1111_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧ⊊").format(bstack1lll1ll1ll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⊋").format(e))
  def bstack1llll1l11111_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1111_opy_ (u"ࠪࡰࡴ࡭ࠧ⊌"), bstack1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧ⊍"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1111_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤ⊎").format(logfile))
      self.bstack1llll1l1l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ⊏").format(e))
  @measure(event_name=EVENTS.bstack111ll11ll11_opy_, stage=STAGE.bstack111l1lllll_opy_)
  def bstack1llll111llll_opy_(self):
    bstack1lll1lll1lll_opy_ = self.bstack1llll11ll111_opy_()
    if bstack1lll1lll1lll_opy_ == None:
      self.bstack1lll1ll1l1l1_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥ⊐"))
      return False
    bstack1llll11l1lll_opy_ = [bstack1111_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤ⊑") if self.bstack11l1ll1lll_opy_ else bstack1111_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭⊒")]
    bstack1lllll1l1ll_opy_ = self.bstack1llll111l1ll_opy_()
    if bstack1lllll1l1ll_opy_ != None:
      bstack1llll11l1lll_opy_.append(bstack1111_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤ⊓").format(bstack1lllll1l1ll_opy_))
    env = os.environ.copy()
    env[bstack1111_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤ⊔")] = bstack1lll1lll1lll_opy_
    env[bstack1111_opy_ (u"࡚ࠧࡈࡠࡄࡘࡍࡑࡊ࡟ࡖࡗࡌࡈࠧ⊕")] = os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⊖"), bstack1111_opy_ (u"ࠧࠨ⊗"))
    bstack1llll111l1l1_opy_ = [self.binary_path]
    self.bstack1llll1l11111_opy_()
    self.bstack1llll1l11l1l_opy_ = self.bstack1llll11lll11_opy_(bstack1llll111l1l1_opy_ + bstack1llll11l1lll_opy_, env)
    self.logger.debug(bstack1111_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤ⊘"))
    bstack1lll1ll1ll11_opy_ = 0
    while self.bstack1llll1l11l1l_opy_.poll() == None:
      bstack1llll111111l_opy_ = self.bstack1llll11l1l1l_opy_()
      if bstack1llll111111l_opy_:
        self.logger.debug(bstack1111_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧ⊙"))
        self.bstack1llll1111l1l_opy_ = True
        return True
      bstack1lll1ll1ll11_opy_ += 1
      self.logger.debug(bstack1111_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨ⊚").format(bstack1lll1ll1ll11_opy_))
      time.sleep(2)
    self.logger.error(bstack1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤ⊛").format(bstack1lll1ll1ll11_opy_))
    self.bstack1lll1ll1l1l1_opy_ = True
    return False
  def bstack1llll11l1l1l_opy_(self, bstack1lll1ll1ll11_opy_ = 0):
    if bstack1lll1ll1ll11_opy_ > 10:
      return False
    try:
      bstack1llll1l11ll1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬ⊜"), bstack1111_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧ⊝"))
      bstack1llll1111ll1_opy_ = bstack1llll1l11ll1_opy_ + bstack111ll11l111_opy_
      response = requests.get(bstack1llll1111ll1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࠭⊞"), {}).get(bstack1111_opy_ (u"ࠨ࡫ࡧࠫ⊟"), None)
      return True
    except:
      self.logger.debug(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡨࡦࡣ࡯ࡸ࡭ࠦࡣࡩࡧࡦ࡯ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ⊠"))
      return False
  def bstack1llll11ll111_opy_(self):
    bstack1llll1l1111l_opy_ = bstack1111_opy_ (u"ࠪࡥࡵࡶࠧ⊡") if self.bstack11l1ll1lll_opy_ else bstack1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⊢")
    bstack1llll11ll11l_opy_ = bstack1111_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣ⊣") if self.config.get(bstack1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⊤")) is None else True
    bstack111llll11l1_opy_ = bstack1111_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠬࡰࡦࡴࡦࡽࡂࢁࡽࠣ⊥").format(self.config[bstack1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⊦")], bstack1llll1l1111l_opy_, bstack1llll11ll11l_opy_)
    if self.percy_capture_mode:
      bstack111llll11l1_opy_ += bstack1111_opy_ (u"ࠤࠩࡴࡪࡸࡣࡺࡡࡦࡥࡵࡺࡵࡳࡧࡢࡱࡴࡪࡥ࠾ࡽࢀࠦ⊧").format(self.percy_capture_mode)
    uri = bstack1l1ll1l1ll_opy_(bstack111llll11l1_opy_)
    try:
      response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠪࡋࡊ࡚ࠧ⊨"), uri, {}, {bstack1111_opy_ (u"ࠫࡦࡻࡴࡩࠩ⊩"): (self.config[bstack1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ⊪")], self.config[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ⊫")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1l1ll1ll_opy_ = data.get(bstack1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⊬"))
        self.percy_capture_mode = data.get(bstack1111_opy_ (u"ࠨࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪ࠭⊭"))
        os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧ⊮")] = str(self.bstack1l1l1ll1ll_opy_)
        os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧ⊯")] = str(self.percy_capture_mode)
        if bstack1llll11ll11l_opy_ == bstack1111_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ⊰") and str(self.bstack1l1l1ll1ll_opy_).lower() == bstack1111_opy_ (u"ࠧࡺࡲࡶࡧࠥ⊱"):
          self.bstack11111111_opy_ = True
        if bstack1111_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ⊲") in data:
          return data[bstack1111_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ⊳")]
        else:
          raise bstack1111_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨ⊴").format(data)
      else:
        raise bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤ⊵").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦ⊶").format(e))
  def bstack1llll111l1ll_opy_(self):
    bstack1lll1lllll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢ⊷"))
    try:
      if bstack1111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭⊸") not in self.bstack1llll111ll1l_opy_:
        self.bstack1llll111ll1l_opy_[bstack1111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ⊹")] = 2
      with open(bstack1lll1lllll11_opy_, bstack1111_opy_ (u"ࠧࡸࠩ⊺")) as fp:
        json.dump(self.bstack1llll111ll1l_opy_, fp)
      return bstack1lll1lllll11_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⊻").format(e))
  def bstack1llll11lll11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1l11l11_opy_ == bstack1111_opy_ (u"ࠩࡺ࡭ࡳ࠭⊼"):
        bstack1llll1111l11_opy_ = [bstack1111_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫ⊽"), bstack1111_opy_ (u"ࠫ࠴ࡩࠧ⊾")]
        cmd = bstack1llll1111l11_opy_ + cmd
      cmd = bstack1111_opy_ (u"ࠬࠦࠧ⊿").join(cmd)
      self.logger.debug(bstack1111_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥ⋀").format(cmd))
      with open(self.bstack1llll1l1l111_opy_, bstack1111_opy_ (u"ࠢࡢࠤ⋁")) as bstack1llll1111lll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll1111lll_opy_, text=True, stderr=bstack1llll1111lll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1ll1l1l1_opy_ = True
      self.logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ⋂").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1111l1l_opy_:
        self.logger.info(bstack1111_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥ⋃"))
        cmd = [self.binary_path, bstack1111_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨ⋄")]
        self.bstack1llll11lll11_opy_(cmd)
        self.bstack1llll1111l1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ⋅").format(cmd, e))
  def bstack111l1l11_opy_(self):
    if not self.bstack1l1l1ll1ll_opy_:
      return
    try:
      bstack1llll11llll1_opy_ = 0
      while not self.bstack1llll1111l1l_opy_ and bstack1llll11llll1_opy_ < self.bstack1lll1lll11l1_opy_:
        if self.bstack1lll1ll1l1l1_opy_:
          self.logger.info(bstack1111_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥ⋆"))
          return
        time.sleep(1)
        bstack1llll11llll1_opy_ += 1
      os.environ[bstack1111_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬ⋇")] = str(self.bstack1lll1llll1l1_opy_())
      self.logger.info(bstack1111_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣ⋈"))
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⋉").format(e))
  def bstack1lll1llll1l1_opy_(self):
    if self.bstack11l1ll1lll_opy_:
      return
    try:
      bstack1lll1lll1111_opy_ = [platform[bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ⋊")].lower() for platform in self.config.get(bstack1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⋋"), [])]
      bstack1ll1l1l11ll_opy_ = sys.maxsize
      bstack1lll1ll1l1ll_opy_ = bstack1111_opy_ (u"ࠫࠬ⋌")
      for browser in bstack1lll1lll1111_opy_:
        if browser in self.bstack1lll1ll1l11l_opy_:
          bstack1lll1lll1ll1_opy_ = self.bstack1lll1ll1l11l_opy_[browser]
        if bstack1lll1lll1ll1_opy_ < bstack1ll1l1l11ll_opy_:
          bstack1ll1l1l11ll_opy_ = bstack1lll1lll1ll1_opy_
          bstack1lll1ll1l1ll_opy_ = browser
      return bstack1lll1ll1l1ll_opy_
    except Exception as e:
      self.logger.error(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⋍").format(e))
  @classmethod
  def bstack1lll1l1l_opy_(self):
    return os.getenv(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ⋎"), bstack1111_opy_ (u"ࠧࡇࡣ࡯ࡷࡪ࠭⋏")).lower()
  @classmethod
  def bstack11l1l1lll1_opy_(self):
    return os.getenv(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬ⋐"), bstack1111_opy_ (u"ࠩࠪ⋑"))
  @classmethod
  def bstack1l1111lll1l_opy_(cls, value):
    cls.bstack11111111_opy_ = value
  @classmethod
  def bstack1llll11lllll_opy_(cls):
    return cls.bstack11111111_opy_
  @classmethod
  def bstack1l1111l11l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1lll1lll111l_opy_(cls):
    return cls.percy_build_id