# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
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
from bstack_utils.helper import bstack1l111l1111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111l11l1_opy_ import bstack11l11l1l1l_opy_
class bstack1l11111l11_opy_:
  working_dir = os.getcwd()
  bstack1lll1lll1_opy_ = False
  config = {}
  bstack1111ll1l11l_opy_ = bstack1l1_opy_ (u"ࠩࠪ⍤")
  binary_path = bstack1l1_opy_ (u"ࠪࠫ⍥")
  bstack1lll11lllll1_opy_ = bstack1l1_opy_ (u"ࠫࠬ⍦")
  bstack11l1l11ll1_opy_ = False
  bstack1lll1l111ll1_opy_ = None
  bstack1lll1ll1l1ll_opy_ = {}
  bstack1lll1l1l1lll_opy_ = 300
  bstack1lll11llll1l_opy_ = False
  logger = None
  bstack1lll1l1ll11l_opy_ = False
  bstack111l1l1ll1_opy_ = False
  percy_build_id = None
  bstack1lll1l1llll1_opy_ = bstack1l1_opy_ (u"ࠬ࠭⍧")
  bstack1lll1ll1l111_opy_ = {
    bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭⍨") : 1,
    bstack1l1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ⍩") : 2,
    bstack1l1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭⍪") : 3,
    bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ⍫") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll1ll11l1l_opy_(self):
    bstack1lll1lll1111_opy_ = bstack1l1_opy_ (u"ࠪࠫ⍬")
    bstack1lll1ll1l1l1_opy_ = sys.platform
    bstack1lll1l1lllll_opy_ = bstack1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⍭")
    if re.match(bstack1l1_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧ⍮"), bstack1lll1ll1l1l1_opy_) != None:
      bstack1lll1lll1111_opy_ = bstack111l1l1l1l1_opy_ + bstack1l1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢ⍯")
      self.bstack1lll1l1llll1_opy_ = bstack1l1_opy_ (u"ࠧ࡮ࡣࡦࠫ⍰")
    elif re.match(bstack1l1_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨ⍱"), bstack1lll1ll1l1l1_opy_) != None:
      bstack1lll1lll1111_opy_ = bstack111l1l1l1l1_opy_ + bstack1l1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥ⍲")
      bstack1lll1l1lllll_opy_ = bstack1l1_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨ⍳")
      self.bstack1lll1l1llll1_opy_ = bstack1l1_opy_ (u"ࠫࡼ࡯࡮ࠨ⍴")
    else:
      bstack1lll1lll1111_opy_ = bstack111l1l1l1l1_opy_ + bstack1l1_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣ⍵")
      self.bstack1lll1l1llll1_opy_ = bstack1l1_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ⍶")
    return bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_
  def bstack1lll1l1l11l1_opy_(self):
    try:
      bstack1lll1l1ll1l1_opy_ = [os.path.join(expanduser(bstack1l1_opy_ (u"ࠢࡿࠤ⍷")), bstack1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⍸")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1lll1l1ll1l1_opy_:
        if(self.bstack1lll1l1l1111_opy_(path)):
          return path
      raise bstack1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ⍹")
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧ⍺").format(e))
  def bstack1lll1l1l1111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1lll1l11_opy_(self, bstack1lll1lll1ll1_opy_):
    return os.path.join(bstack1lll1lll1ll1_opy_, self.bstack1111ll1l11l_opy_ + bstack1l1_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥ⍻"))
  def bstack1lll1ll1lll1_opy_(self, bstack1lll1lll1ll1_opy_, bstack1lll1l1ll111_opy_):
    if not bstack1lll1l1ll111_opy_: return
    try:
      bstack1lll1l1l1l1l_opy_ = self.bstack1lll1lll1l11_opy_(bstack1lll1lll1ll1_opy_)
      with open(bstack1lll1l1l1l1l_opy_, bstack1l1_opy_ (u"ࠧࡽࠢ⍼")) as f:
        f.write(bstack1lll1l1ll111_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥ⍽"))
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ⍾").format(e))
  def bstack1lll1l11l111_opy_(self, bstack1lll1lll1ll1_opy_):
    try:
      bstack1lll1l1l1l1l_opy_ = self.bstack1lll1lll1l11_opy_(bstack1lll1lll1ll1_opy_)
      if os.path.exists(bstack1lll1l1l1l1l_opy_):
        with open(bstack1lll1l1l1l1l_opy_, bstack1l1_opy_ (u"ࠣࡴࠥ⍿")) as f:
          bstack1lll1l1ll111_opy_ = f.read().strip()
          return bstack1lll1l1ll111_opy_ if bstack1lll1l1ll111_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ⎀").format(e))
  def bstack1lll1ll11lll_opy_(self, bstack1lll1lll1ll1_opy_, bstack1lll1lll1111_opy_):
    bstack1lll1l1l11ll_opy_ = self.bstack1lll1l11l111_opy_(bstack1lll1lll1ll1_opy_)
    if bstack1lll1l1l11ll_opy_:
      try:
        bstack1lll1l1lll1l_opy_ = self.bstack1lll1ll1l11l_opy_(bstack1lll1l1l11ll_opy_, bstack1lll1lll1111_opy_)
        if not bstack1lll1l1lll1l_opy_:
          self.logger.debug(bstack1l1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧ⎁"))
          return True
        self.logger.debug(bstack1l1_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥ⎂"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ⎃").format(e))
    return False
  def bstack1lll1ll1l11l_opy_(self, bstack1lll1l1l11ll_opy_, bstack1lll1lll1111_opy_):
    try:
      headers = {
        bstack1l1_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨ⎄"): bstack1lll1l1l11ll_opy_
      }
      response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠧࡈࡇࡗࠫ⎅"), bstack1lll1lll1111_opy_, {}, {bstack1l1_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤ⎆"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦ⎇").format(e))
  @measure(event_name=EVENTS.bstack111l11lllll_opy_, stage=STAGE.bstack1ll1llll_opy_)
  def bstack1lll1lll1l1l_opy_(self, bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_):
    try:
      bstack1lll11lll1ll_opy_ = self.bstack1lll1l1l11l1_opy_()
      bstack1lll1ll1ll1l_opy_ = os.path.join(bstack1lll11lll1ll_opy_, bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭⎈"))
      bstack1lll11llll11_opy_ = os.path.join(bstack1lll11lll1ll_opy_, bstack1lll1l1lllll_opy_)
      if self.bstack1lll1ll11lll_opy_(bstack1lll11lll1ll_opy_, bstack1lll1lll1111_opy_): # if true, bstack11lll1l1lll_opy_ bstack1lll1l1ll111_opy_ is bstack1lll1l1lll11_opy_ to bstack1111ll11l11_opy_ version available (response 304)
        if os.path.exists(bstack1lll11llll11_opy_):
          self.logger.info(bstack1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨ⎉").format(bstack1lll11llll11_opy_))
          return bstack1lll11llll11_opy_
        if os.path.exists(bstack1lll1ll1ll1l_opy_):
          self.logger.info(bstack1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥ⎊").format(bstack1lll1ll1ll1l_opy_))
          return self.bstack1lll11ll1lll_opy_(bstack1lll1ll1ll1l_opy_, bstack1lll1l1lllll_opy_)
      self.logger.info(bstack1l1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦ⎋").format(bstack1lll1lll1111_opy_))
      response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠧࡈࡇࡗࠫ⎌"), bstack1lll1lll1111_opy_, {}, {})
      if response.status_code == 200:
        bstack1lll1l1ll1ll_opy_ = response.headers.get(bstack1l1_opy_ (u"ࠣࡇࡗࡥ࡬ࠨ⎍"), bstack1l1_opy_ (u"ࠤࠥ⎎"))
        if bstack1lll1l1ll1ll_opy_:
          self.bstack1lll1ll1lll1_opy_(bstack1lll11lll1ll_opy_, bstack1lll1l1ll1ll_opy_)
        with open(bstack1lll1ll1ll1l_opy_, bstack1l1_opy_ (u"ࠪࡻࡧ࠭⎏")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤ⎐").format(bstack1lll1ll1ll1l_opy_))
        return self.bstack1lll11ll1lll_opy_(bstack1lll1ll1ll1l_opy_, bstack1lll1l1lllll_opy_)
      else:
        raise(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣ⎑").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢ⎒").format(e))
  def bstack1lll1ll1ll11_opy_(self, bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_):
    try:
      retry = 2
      bstack1lll11llll11_opy_ = None
      bstack1lll1ll111ll_opy_ = False
      while retry > 0:
        bstack1lll11llll11_opy_ = self.bstack1lll1lll1l1l_opy_(bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_)
        bstack1lll1ll111ll_opy_ = self.bstack1lll1l111lll_opy_(bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_, bstack1lll11llll11_opy_)
        if bstack1lll1ll111ll_opy_:
          break
        retry -= 1
      return bstack1lll11llll11_opy_, bstack1lll1ll111ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦ⎓").format(e))
    return bstack1lll11llll11_opy_, False
  def bstack1lll1l111lll_opy_(self, bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_, bstack1lll11llll11_opy_, bstack1lll1l11l11l_opy_ = 0):
    if bstack1lll1l11l11l_opy_ > 1:
      return False
    if bstack1lll11llll11_opy_ == None or os.path.exists(bstack1lll11llll11_opy_) == False:
      self.logger.warn(bstack1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨ⎔"))
      return False
    command = bstack1l1_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⎕").format(bstack1lll11llll11_opy_)
    bstack1lll1ll111l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1l1_opy_ (u"ࠪࡄࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯ࠧ⎖") in bstack1lll1ll111l1_opy_:
      return True
    else:
      self.logger.error(bstack1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥ⎗"))
      return False
  def bstack1lll11ll1lll_opy_(self, bstack1lll1ll1ll1l_opy_, bstack1lll1l1lllll_opy_):
    try:
      working_dir = os.path.dirname(bstack1lll1ll1ll1l_opy_)
      shutil.unpack_archive(bstack1lll1ll1ll1l_opy_, working_dir)
      bstack1lll11llll11_opy_ = os.path.join(working_dir, bstack1lll1l1lllll_opy_)
      os.chmod(bstack1lll11llll11_opy_, 0o755)
      return bstack1lll11llll11_opy_
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ⎘"))
  def bstack1lll1ll11ll1_opy_(self):
    try:
      bstack1lll1l1l111l_opy_ = self.config.get(bstack1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⎙"))
      bstack1lll1ll11ll1_opy_ = bstack1lll1l1l111l_opy_ or (bstack1lll1l1l111l_opy_ is None and self.bstack1lll1lll1_opy_)
      if not bstack1lll1ll11ll1_opy_ or self.config.get(bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⎚"), None) not in bstack111l11l1ll1_opy_:
        return False
      self.bstack11l1l11ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⎛").format(e))
  def bstack1lll1ll11111_opy_(self):
    try:
      bstack1lll1ll11111_opy_ = self.percy_capture_mode
      return bstack1lll1ll11111_opy_
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⎜").format(e))
  def init(self, bstack1lll1lll1_opy_, config, logger):
    self.bstack1lll1lll1_opy_ = bstack1lll1lll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll1ll11ll1_opy_():
      return
    self.bstack1lll1ll1l1ll_opy_ = config.get(bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎝"), {})
    self.percy_capture_mode = config.get(bstack1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ⎞"))
    try:
      bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_ = self.bstack1lll1ll11l1l_opy_()
      self.bstack1111ll1l11l_opy_ = bstack1lll1l1lllll_opy_
      bstack1lll11llll11_opy_, bstack1lll1ll111ll_opy_ = self.bstack1lll1ll1ll11_opy_(bstack1lll1lll1111_opy_, bstack1lll1l1lllll_opy_)
      if bstack1lll1ll111ll_opy_:
        self.binary_path = bstack1lll11llll11_opy_
        thread = Thread(target=self.bstack1lll1l1l1ll1_opy_)
        thread.start()
      else:
        self.bstack1lll1l1ll11l_opy_ = True
        self.logger.error(bstack1l1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤ⎟").format(bstack1lll11llll11_opy_))
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ⎠").format(e))
  def bstack1lll1lll111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࠫ⎡"), bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫ⎢"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨ⎣").format(logfile))
      self.bstack1lll11lllll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⎤").format(e))
  @measure(event_name=EVENTS.bstack111l11l1l1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
  def bstack1lll1l1l1ll1_opy_(self):
    bstack1lll1l11llll_opy_ = self.bstack1lll1lll11ll_opy_()
    if bstack1lll1l11llll_opy_ == None:
      self.bstack1lll1l1ll11l_opy_ = True
      self.logger.error(bstack1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢ⎥"))
      return False
    bstack1lll11lll1l1_opy_ = [bstack1l1_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨ⎦") if self.bstack1lll1lll1_opy_ else bstack1l1_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪ⎧")]
    bstack1lll1ll1ll1_opy_ = self.bstack1lll1l1111l1_opy_()
    if bstack1lll1ll1ll1_opy_ != None:
      bstack1lll11lll1l1_opy_.append(bstack1l1_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨ⎨").format(bstack1lll1ll1ll1_opy_))
    env = os.environ.copy()
    env[bstack1l1_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨ⎩")] = bstack1lll1l11llll_opy_
    env[bstack1l1_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤ⎪")] = os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⎫"), bstack1l1_opy_ (u"ࠫࠬ⎬"))
    bstack1lll1l111l11_opy_ = [self.binary_path]
    self.bstack1lll1lll111l_opy_()
    self.bstack1lll1l111ll1_opy_ = self.bstack1lll1lll11l1_opy_(bstack1lll1l111l11_opy_ + bstack1lll11lll1l1_opy_, env)
    self.logger.debug(bstack1l1_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨ⎭"))
    bstack1lll1l11l11l_opy_ = 0
    while self.bstack1lll1l111ll1_opy_.poll() == None:
      bstack1lll1l11l1ll_opy_ = self.bstack1lll11lll111_opy_()
      if bstack1lll1l11l1ll_opy_:
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤ⎮"))
        self.bstack1lll11llll1l_opy_ = True
        return True
      bstack1lll1l11l11l_opy_ += 1
      self.logger.debug(bstack1l1_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥ⎯").format(bstack1lll1l11l11l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨ⎰").format(bstack1lll1l11l11l_opy_))
    self.bstack1lll1l1ll11l_opy_ = True
    return False
  def bstack1lll11lll111_opy_(self, bstack1lll1l11l11l_opy_ = 0):
    if bstack1lll1l11l11l_opy_ > 10:
      return False
    try:
      bstack1lll1ll11l11_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩ⎱"), bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫ⎲"))
      bstack1lll1l11l1l1_opy_ = bstack1lll1ll11l11_opy_ + bstack111l1111lll_opy_
      response = requests.get(bstack1lll1l11l1l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ⎳"), {}).get(bstack1l1_opy_ (u"ࠬ࡯ࡤࠨ⎴"), None)
      return True
    except:
      self.logger.debug(bstack1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ⎵"))
      return False
  def bstack1lll1lll11ll_opy_(self):
    bstack1lll1l11ll1l_opy_ = bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫ⎶") if self.bstack1lll1lll1_opy_ else bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⎷")
    bstack1lll1l1l1l11_opy_ = bstack1l1_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧ⎸") if self.config.get(bstack1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⎹")) is None else True
    bstack111ll111111_opy_ = bstack1l1_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧ⎺").format(self.config[bstack1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⎻")], bstack1lll1l11ll1l_opy_, bstack1lll1l1l1l11_opy_)
    if self.percy_capture_mode:
      bstack111ll111111_opy_ += bstack1l1_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣ⎼").format(self.percy_capture_mode)
    uri = bstack11l11l1l1l_opy_(bstack111ll111111_opy_)
    try:
      response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠧࡈࡇࡗࠫ⎽"), uri, {}, {bstack1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭⎾"): (self.config[bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ⎿")], self.config[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭⏀")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l1l11ll1_opy_ = data.get(bstack1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⏁"))
        self.percy_capture_mode = data.get(bstack1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪ⏂"))
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ⏃")] = str(self.bstack11l1l11ll1_opy_)
        os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ⏄")] = str(self.percy_capture_mode)
        if bstack1lll1l1l1l11_opy_ == bstack1l1_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ⏅") and str(self.bstack11l1l11ll1_opy_).lower() == bstack1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⏆"):
          self.bstack111l1l1ll1_opy_ = True
        if bstack1l1_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ⏇") in data:
          return data[bstack1l1_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ⏈")]
        else:
          raise bstack1l1_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ⏉").format(data)
      else:
        raise bstack1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ⏊").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ⏋").format(e))
  def bstack1lll1l1111l1_opy_(self):
    bstack1lll1ll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ⏌"))
    try:
      if bstack1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ⏍") not in self.bstack1lll1ll1l1ll_opy_:
        self.bstack1lll1ll1l1ll_opy_[bstack1l1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ⏎")] = 2
      with open(bstack1lll1ll1llll_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭⏏")) as fp:
        json.dump(self.bstack1lll1ll1l1ll_opy_, fp)
      return bstack1lll1ll1llll_opy_
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⏐").format(e))
  def bstack1lll1lll11l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lll1l1llll1_opy_ == bstack1l1_opy_ (u"࠭ࡷࡪࡰࠪ⏑"):
        bstack1lll1l11lll1_opy_ = [bstack1l1_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ⏒"), bstack1l1_opy_ (u"ࠨ࠱ࡦࠫ⏓")]
        cmd = bstack1lll1l11lll1_opy_ + cmd
      cmd = bstack1l1_opy_ (u"ࠩࠣࠫ⏔").join(cmd)
      self.logger.debug(bstack1l1_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢ⏕").format(cmd))
      with open(self.bstack1lll11lllll1_opy_, bstack1l1_opy_ (u"ࠦࡦࠨ⏖")) as bstack1lll11llllll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll11llllll_opy_, text=True, stderr=bstack1lll11llllll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1l1ll11l_opy_ = True
      self.logger.error(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ⏗").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll11llll1l_opy_:
        self.logger.info(bstack1l1_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢ⏘"))
        cmd = [self.binary_path, bstack1l1_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥ⏙")]
        self.bstack1lll1lll11l1_opy_(cmd)
        self.bstack1lll11llll1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ⏚").format(cmd, e))
  def bstack1l1l111lll_opy_(self):
    if not self.bstack11l1l11ll1_opy_:
      return
    try:
      bstack1lll1l111l1l_opy_ = 0
      while not self.bstack1lll11llll1l_opy_ and bstack1lll1l111l1l_opy_ < self.bstack1lll1l1l1lll_opy_:
        if self.bstack1lll1l1ll11l_opy_:
          self.logger.info(bstack1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢ⏛"))
          return
        time.sleep(1)
        bstack1lll1l111l1l_opy_ += 1
      os.environ[bstack1l1_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ⏜")] = str(self.bstack1lll1ll1111l_opy_())
      self.logger.info(bstack1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧ⏝"))
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⏞").format(e))
  def bstack1lll1ll1111l_opy_(self):
    if self.bstack1lll1lll1_opy_:
      return
    try:
      bstack1lll1l1111ll_opy_ = [platform[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ⏟")].lower() for platform in self.config.get(bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⏠"), [])]
      bstack1ll11l1ll11_opy_ = sys.maxsize
      bstack1lll1l111111_opy_ = bstack1l1_opy_ (u"ࠨࠩ⏡")
      for browser in bstack1lll1l1111ll_opy_:
        if browser in self.bstack1lll1ll1l111_opy_:
          bstack1lll11lll11l_opy_ = self.bstack1lll1ll1l111_opy_[browser]
        if bstack1lll11lll11l_opy_ < bstack1ll11l1ll11_opy_:
          bstack1ll11l1ll11_opy_ = bstack1lll11lll11l_opy_
          bstack1lll1l111111_opy_ = browser
      return bstack1lll1l111111_opy_
    except Exception as e:
      self.logger.error(bstack1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ⏢").format(e))
  @classmethod
  def bstack1lll1111_opy_(self):
    return os.getenv(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ⏣"), bstack1l1_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪ⏤")).lower()
  @classmethod
  def bstack1l1l11l1l_opy_(self):
    return os.getenv(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ⏥"), bstack1l1_opy_ (u"࠭ࠧ⏦"))
  @classmethod
  def bstack11llll1l1l1_opy_(cls, value):
    cls.bstack111l1l1ll1_opy_ = value
  @classmethod
  def bstack1lll1l11ll11_opy_(cls):
    return cls.bstack111l1l1ll1_opy_
  @classmethod
  def bstack11llll1lll1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1lll1l11111l_opy_(cls):
    return cls.percy_build_id