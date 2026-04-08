# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
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
from bstack_utils.helper import bstack11111l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11ll1ll1l1_opy_ import bstack1l11llllll_opy_
class bstack11llll1l1_opy_:
  working_dir = os.getcwd()
  bstack1l1ll111_opy_ = False
  config = {}
  bstack1llll1l11111_opy_ = bstack111l_opy_ (u"࠭ࠧ╧")
  binary_path = bstack111l_opy_ (u"ࠧࠨ╨")
  bstack1ll1lllll11l_opy_ = bstack111l_opy_ (u"ࠨࠩ╩")
  bstack11l111l1l_opy_ = False
  bstack1ll1ll1l1ll1_opy_ = None
  bstack1ll1ll1llll1_opy_ = {}
  bstack1ll1ll1l11l1_opy_ = 300
  bstack1lll111111l1_opy_ = False
  logger = None
  bstack1ll1lll1l11l_opy_ = False
  bstack111l1l1ll1_opy_ = False
  percy_build_id = None
  bstack1ll1lll1l111_opy_ = bstack111l_opy_ (u"ࠩࠪ╪")
  bstack1ll1lll11l1l_opy_ = {
    bstack111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ╫") : 1,
    bstack111l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ╬") : 2,
    bstack111l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ╭") : 3,
    bstack111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭╮") : 4
  }
  def __init__(self) -> None: pass
  def bstack1ll1ll1lll11_opy_(self):
    bstack1ll1ll1l1l1l_opy_ = bstack111l_opy_ (u"ࠧࠨ╯")
    bstack1ll1ll1l1l11_opy_ = sys.platform
    bstack1ll1lllll1ll_opy_ = bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ╰")
    if re.match(bstack111l_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤ╱"), bstack1ll1ll1l1l11_opy_) != None:
      bstack1ll1ll1l1l1l_opy_ = bstack11111l11lll_opy_ + bstack111l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦ╲")
      self.bstack1ll1lll1l111_opy_ = bstack111l_opy_ (u"ࠫࡲࡧࡣࠨ╳")
    elif re.match(bstack111l_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥ╴"), bstack1ll1ll1l1l11_opy_) != None:
      bstack1ll1ll1l1l1l_opy_ = bstack11111l11lll_opy_ + bstack111l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢ╵")
      bstack1ll1lllll1ll_opy_ = bstack111l_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥ╶")
      self.bstack1ll1lll1l111_opy_ = bstack111l_opy_ (u"ࠨࡹ࡬ࡲࠬ╷")
    else:
      bstack1ll1ll1l1l1l_opy_ = bstack11111l11lll_opy_ + bstack111l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧ╸")
      self.bstack1ll1lll1l111_opy_ = bstack111l_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ╹")
    return bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_
  def bstack1ll1llll11l1_opy_(self):
    try:
      bstack1ll1lll1111l_opy_ = [os.path.join(expanduser(bstack111l_opy_ (u"ࠦࢃࠨ╺")), bstack111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ╻")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1ll1lll1111l_opy_:
        if(self.bstack1ll1ll1ll111_opy_(path)):
          return path
      raise bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥ╼")
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤ╽").format(e))
  def bstack1ll1ll1ll111_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1ll1llll111l_opy_(self, bstack1ll1lll11lll_opy_):
    return os.path.join(bstack1ll1lll11lll_opy_, self.bstack1llll1l11111_opy_ + bstack111l_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢ╾"))
  def bstack1ll1ll11l11l_opy_(self, bstack1ll1lll11lll_opy_, bstack1ll1ll11ll1l_opy_):
    if not bstack1ll1ll11ll1l_opy_: return
    try:
      bstack1lll11111l11_opy_ = self.bstack1ll1llll111l_opy_(bstack1ll1lll11lll_opy_)
      with open(bstack1lll11111l11_opy_, bstack111l_opy_ (u"ࠤࡺࠦ╿")) as f:
        f.write(bstack1ll1ll11ll1l_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢ▀"))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ▁").format(e))
  def bstack1ll1ll11l1l1_opy_(self, bstack1ll1lll11lll_opy_):
    try:
      bstack1lll11111l11_opy_ = self.bstack1ll1llll111l_opy_(bstack1ll1lll11lll_opy_)
      if os.path.exists(bstack1lll11111l11_opy_):
        with open(bstack1lll11111l11_opy_, bstack111l_opy_ (u"ࠧࡸࠢ▂")) as f:
          bstack1ll1ll11ll1l_opy_ = f.read().strip()
          return bstack1ll1ll11ll1l_opy_ if bstack1ll1ll11ll1l_opy_ else None
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ▃").format(e))
  def bstack1ll1ll111lll_opy_(self, bstack1ll1lll11lll_opy_, bstack1ll1ll1l1l1l_opy_):
    bstack1ll1ll1l1lll_opy_ = self.bstack1ll1ll11l1l1_opy_(bstack1ll1lll11lll_opy_)
    if bstack1ll1ll1l1lll_opy_:
      try:
        bstack1ll1llll11ll_opy_ = self.bstack1ll1lll1l1ll_opy_(bstack1ll1ll1l1lll_opy_, bstack1ll1ll1l1l1l_opy_)
        if not bstack1ll1llll11ll_opy_:
          self.logger.debug(bstack111l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤ▄"))
          return True
        self.logger.debug(bstack111l_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢ▅"))
        return False
      except Exception as e:
        self.logger.warn(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ▆").format(e))
    return False
  def bstack1ll1lll1l1ll_opy_(self, bstack1ll1ll1l1lll_opy_, bstack1ll1ll1l1l1l_opy_):
    try:
      headers = {
        bstack111l_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥ▇"): bstack1ll1ll1l1lll_opy_
      }
      response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠫࡌࡋࡔࠨ█"), bstack1ll1ll1l1l1l_opy_, {}, {bstack111l_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ▉"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣ▊").format(e))
  @measure(event_name=EVENTS.bstack11111ll1ll1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
  def bstack1ll1ll1l111l_opy_(self, bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_):
    try:
      bstack1ll1ll11llll_opy_ = self.bstack1ll1llll11l1_opy_()
      bstack1ll1llllll11_opy_ = os.path.join(bstack1ll1ll11llll_opy_, bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪ▋"))
      bstack1ll1ll11ll11_opy_ = os.path.join(bstack1ll1ll11llll_opy_, bstack1ll1lllll1ll_opy_)
      if self.bstack1ll1ll111lll_opy_(bstack1ll1ll11llll_opy_, bstack1ll1ll1l1l1l_opy_): # if true, bstack11l1l111l1l_opy_ bstack1ll1ll11ll1l_opy_ is bstack1ll1ll1ll1ll_opy_ to bstack1llllll11l1l_opy_ version available (response 304)
        if os.path.exists(bstack1ll1ll11ll11_opy_):
          self.logger.info(bstack111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ▌").format(bstack1ll1ll11ll11_opy_))
          return bstack1ll1ll11ll11_opy_
        if os.path.exists(bstack1ll1llllll11_opy_):
          self.logger.info(bstack111l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢ▍").format(bstack1ll1llllll11_opy_))
          return self.bstack1ll1lllllll1_opy_(bstack1ll1llllll11_opy_, bstack1ll1lllll1ll_opy_)
      self.logger.info(bstack111l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣ▎").format(bstack1ll1ll1l1l1l_opy_))
      response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠫࡌࡋࡔࠨ▏"), bstack1ll1ll1l1l1l_opy_, {}, {})
      if response.status_code == 200:
        bstack1ll1lllll1l1_opy_ = response.headers.get(bstack111l_opy_ (u"ࠧࡋࡔࡢࡩࠥ▐"), bstack111l_opy_ (u"ࠨࠢ░"))
        if bstack1ll1lllll1l1_opy_:
          self.bstack1ll1ll11l11l_opy_(bstack1ll1ll11llll_opy_, bstack1ll1lllll1l1_opy_)
        with open(bstack1ll1llllll11_opy_, bstack111l_opy_ (u"ࠧࡸࡤࠪ▒")) as file:
          file.write(response.content)
        self.logger.info(bstack111l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨ▓").format(bstack1ll1llllll11_opy_))
        return self.bstack1ll1lllllll1_opy_(bstack1ll1llllll11_opy_, bstack1ll1lllll1ll_opy_)
      else:
        raise(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧ▔").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ▕").format(e))
  def bstack1ll1lll11111_opy_(self, bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_):
    try:
      retry = 2
      bstack1ll1ll11ll11_opy_ = None
      bstack1ll1ll1lll1l_opy_ = False
      while retry > 0:
        bstack1ll1ll11ll11_opy_ = self.bstack1ll1ll1l111l_opy_(bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_)
        bstack1ll1ll1lll1l_opy_ = self.bstack1ll1lll1llll_opy_(bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_, bstack1ll1ll11ll11_opy_)
        if bstack1ll1ll1lll1l_opy_:
          break
        retry -= 1
      return bstack1ll1ll11ll11_opy_, bstack1ll1ll1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣ▖").format(e))
    return bstack1ll1ll11ll11_opy_, False
  def bstack1ll1lll1llll_opy_(self, bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_, bstack1ll1ll11ll11_opy_, bstack1ll1llll1111_opy_ = 0):
    if bstack1ll1llll1111_opy_ > 1:
      return False
    if bstack1ll1ll11ll11_opy_ == None or os.path.exists(bstack1ll1ll11ll11_opy_) == False:
      self.logger.warn(bstack111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ▗"))
      return False
    command = bstack111l_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ▘").format(bstack1ll1ll11ll11_opy_)
    bstack1ll1lllll111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack111l_opy_ (u"ࠧࡁࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬ࠫ▙") in bstack1ll1lllll111_opy_:
      return True
    else:
      self.logger.error(bstack111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢ▚"))
      return False
  def bstack1ll1lllllll1_opy_(self, bstack1ll1llllll11_opy_, bstack1ll1lllll1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack1ll1llllll11_opy_)
      shutil.unpack_archive(bstack1ll1llllll11_opy_, working_dir)
      bstack1ll1ll11ll11_opy_ = os.path.join(working_dir, bstack1ll1lllll1ll_opy_)
      os.chmod(bstack1ll1ll11ll11_opy_, 0o755)
      return bstack1ll1ll11ll11_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥ▛"))
  def bstack1lll11111111_opy_(self):
    try:
      bstack1ll1ll11l1ll_opy_ = self.config.get(bstack111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ▜"))
      bstack1lll11111111_opy_ = bstack1ll1ll11l1ll_opy_ or (bstack1ll1ll11l1ll_opy_ is None and self.bstack1l1ll111_opy_)
      if not bstack1lll11111111_opy_ or self.config.get(bstack111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ▝"), None) not in bstack11111lll11l_opy_:
        return False
      self.bstack11l111l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ▞").format(e))
  def bstack1ll1ll111ll1_opy_(self):
    try:
      bstack1ll1ll111ll1_opy_ = self.percy_capture_mode
      return bstack1ll1ll111ll1_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ▟").format(e))
  def init(self, bstack1l1ll111_opy_, config, logger):
    self.bstack1l1ll111_opy_ = bstack1l1ll111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll11111111_opy_():
      return
    self.bstack1ll1ll1llll1_opy_ = config.get(bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭■"), {})
    self.percy_capture_mode = config.get(bstack111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ□"))
    try:
      bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_ = self.bstack1ll1ll1lll11_opy_()
      self.bstack1llll1l11111_opy_ = bstack1ll1lllll1ll_opy_
      bstack1ll1ll11ll11_opy_, bstack1ll1ll1lll1l_opy_ = self.bstack1ll1lll11111_opy_(bstack1ll1ll1l1l1l_opy_, bstack1ll1lllll1ll_opy_)
      if bstack1ll1ll1lll1l_opy_:
        self.binary_path = bstack1ll1ll11ll11_opy_
        thread = Thread(target=self.bstack1ll1lll1ll11_opy_)
        thread.start()
      else:
        self.bstack1ll1lll1l11l_opy_ = True
        self.logger.error(bstack111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨ▢").format(bstack1ll1ll11ll11_opy_))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ▣").format(e))
  def bstack1ll1llll1ll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l_opy_ (u"ࠫࡱࡵࡧࠨ▤"), bstack111l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨ▥"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥ▦").format(logfile))
      self.bstack1ll1lllll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ▧").format(e))
  @measure(event_name=EVENTS.bstack11111ll1l11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
  def bstack1ll1lll1ll11_opy_(self):
    bstack1ll1lll1l1l1_opy_ = self.bstack1ll1lll1ll1l_opy_()
    if bstack1ll1lll1l1l1_opy_ == None:
      self.bstack1ll1lll1l11l_opy_ = True
      self.logger.error(bstack111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦ▨"))
      return False
    bstack1ll1llllllll_opy_ = [bstack111l_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥ▩") if self.bstack1l1ll111_opy_ else bstack111l_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧ▪")]
    bstack1ll1l1l1111_opy_ = self.bstack1ll1lll111l1_opy_()
    if bstack1ll1l1l1111_opy_ != None:
      bstack1ll1llllllll_opy_.append(bstack111l_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥ▫").format(bstack1ll1l1l1111_opy_))
    env = os.environ.copy()
    env[bstack111l_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥ▬")] = bstack1ll1lll1l1l1_opy_
    env[bstack111l_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨ▭")] = os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ▮"), bstack111l_opy_ (u"ࠨࠩ▯"))
    bstack1ll1llll1l1l_opy_ = [self.binary_path]
    self.bstack1ll1llll1ll1_opy_()
    self.bstack1ll1ll1l1ll1_opy_ = self.bstack1ll1lll1lll1_opy_(bstack1ll1llll1l1l_opy_ + bstack1ll1llllllll_opy_, env)
    self.logger.debug(bstack111l_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥ▰"))
    bstack1ll1llll1111_opy_ = 0
    while self.bstack1ll1ll1l1ll1_opy_.poll() == None:
      bstack1ll1lll11ll1_opy_ = self.bstack1ll1ll11l111_opy_()
      if bstack1ll1lll11ll1_opy_:
        self.logger.debug(bstack111l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨ▱"))
        self.bstack1lll111111l1_opy_ = True
        return True
      bstack1ll1llll1111_opy_ += 1
      self.logger.debug(bstack111l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢ▲").format(bstack1ll1llll1111_opy_))
      time.sleep(2)
    self.logger.error(bstack111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥ△").format(bstack1ll1llll1111_opy_))
    self.bstack1ll1lll1l11l_opy_ = True
    return False
  def bstack1ll1ll11l111_opy_(self, bstack1ll1llll1111_opy_ = 0):
    if bstack1ll1llll1111_opy_ > 10:
      return False
    try:
      bstack1ll1ll1ll11l_opy_ = os.environ.get(bstack111l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭▴"), bstack111l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨ▵"))
      bstack1ll1ll11lll1_opy_ = bstack1ll1ll1ll11l_opy_ + bstack11111l1l1ll_opy_
      response = requests.get(bstack1ll1ll11lll1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧ▶"), {}).get(bstack111l_opy_ (u"ࠩ࡬ࡨࠬ▷"), None)
      return True
    except:
      self.logger.debug(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣ▸"))
      return False
  def bstack1ll1lll1ll1l_opy_(self):
    bstack1lll11111l1l_opy_ = bstack111l_opy_ (u"ࠫࡦࡶࡰࠨ▹") if self.bstack1l1ll111_opy_ else bstack111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ►")
    bstack1lll1111111l_opy_ = bstack111l_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤ▻") if self.config.get(bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭▼")) is None else True
    bstack1111l11llll_opy_ = bstack111l_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤ▽").format(self.config[bstack111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ▾")], bstack1lll11111l1l_opy_, bstack1lll1111111l_opy_)
    if self.percy_capture_mode:
      bstack1111l11llll_opy_ += bstack111l_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧ▿").format(self.percy_capture_mode)
    uri = bstack1l11llllll_opy_(bstack1111l11llll_opy_)
    try:
      response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠫࡌࡋࡔࠨ◀"), uri, {}, {bstack111l_opy_ (u"ࠬࡧࡵࡵࡪࠪ◁"): (self.config[bstack111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ◂")], self.config[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ◃")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l111l1l_opy_ = data.get(bstack111l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ◄"))
        self.percy_capture_mode = data.get(bstack111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧ◅"))
        os.environ[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ◆")] = str(self.bstack11l111l1l_opy_)
        os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ◇")] = str(self.percy_capture_mode)
        if bstack1lll1111111l_opy_ == bstack111l_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣ◈") and str(self.bstack11l111l1l_opy_).lower() == bstack111l_opy_ (u"ࠨࡴࡳࡷࡨࠦ◉"):
          self.bstack111l1l1ll1_opy_ = True
        if bstack111l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ◊") in data:
          return data[bstack111l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ○")]
        else:
          raise bstack111l_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩ◌").format(data)
      else:
        raise bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥ◍").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧ◎").format(e))
  def bstack1ll1lll111l1_opy_(self):
    bstack1ll1ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack111l_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣ●"))
    try:
      if bstack111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ◐") not in self.bstack1ll1ll1llll1_opy_:
        self.bstack1ll1ll1llll1_opy_[bstack111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ◑")] = 2
      with open(bstack1ll1ll1l1111_opy_, bstack111l_opy_ (u"ࠨࡹࠪ◒")) as fp:
        json.dump(self.bstack1ll1ll1llll1_opy_, fp)
      return bstack1ll1ll1l1111_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ◓").format(e))
  def bstack1ll1lll1lll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1ll1lll1l111_opy_ == bstack111l_opy_ (u"ࠪࡻ࡮ࡴࠧ◔"):
        bstack1ll1lll11l11_opy_ = [bstack111l_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬ◕"), bstack111l_opy_ (u"ࠬ࠵ࡣࠨ◖")]
        cmd = bstack1ll1lll11l11_opy_ + cmd
      cmd = bstack111l_opy_ (u"࠭ࠠࠨ◗").join(cmd)
      self.logger.debug(bstack111l_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦ◘").format(cmd))
      with open(self.bstack1ll1lllll11l_opy_, bstack111l_opy_ (u"ࠣࡣࠥ◙")) as bstack1ll1ll1l11ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1ll1ll1l11ll_opy_, text=True, stderr=bstack1ll1ll1l11ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1ll1lll1l11l_opy_ = True
      self.logger.error(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ◚").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll111111l1_opy_:
        self.logger.info(bstack111l_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦ◛"))
        cmd = [self.binary_path, bstack111l_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢ◜")]
        self.bstack1ll1lll1lll1_opy_(cmd)
        self.bstack1lll111111l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ◝").format(cmd, e))
  def bstack1llllll111_opy_(self):
    if not self.bstack11l111l1l_opy_:
      return
    try:
      bstack1ll1ll1lllll_opy_ = 0
      while not self.bstack1lll111111l1_opy_ and bstack1ll1ll1lllll_opy_ < self.bstack1ll1ll1l11l1_opy_:
        if self.bstack1ll1lll1l11l_opy_:
          self.logger.info(bstack111l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦ◞"))
          return
        time.sleep(1)
        bstack1ll1ll1lllll_opy_ += 1
      os.environ[bstack111l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭◟")] = str(self.bstack1ll1lll111ll_opy_())
      self.logger.info(bstack111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤ◠"))
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ◡").format(e))
  def bstack1ll1lll111ll_opy_(self):
    if self.bstack1l1ll111_opy_:
      return
    try:
      bstack1ll1llll1l11_opy_ = [platform[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ◢")].lower() for platform in self.config.get(bstack111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ◣"), [])]
      bstack1l11llll111_opy_ = sys.maxsize
      bstack1lll111111ll_opy_ = bstack111l_opy_ (u"ࠬ࠭◤")
      for browser in bstack1ll1llll1l11_opy_:
        if browser in self.bstack1ll1lll11l1l_opy_:
          bstack1ll1ll1ll1l1_opy_ = self.bstack1ll1lll11l1l_opy_[browser]
        if bstack1ll1ll1ll1l1_opy_ < bstack1l11llll111_opy_:
          bstack1l11llll111_opy_ = bstack1ll1ll1ll1l1_opy_
          bstack1lll111111ll_opy_ = browser
      return bstack1lll111111ll_opy_
    except Exception as e:
      self.logger.error(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ◥").format(e))
  @classmethod
  def bstack11l1111l1_opy_(self):
    return os.getenv(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ◦"), bstack111l_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧ◧")).lower()
  @classmethod
  def bstack11ll1ll1_opy_(self):
    return os.getenv(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭◨"), bstack111l_opy_ (u"ࠪࠫ◩"))
  @classmethod
  def bstack11l1l1llll1_opy_(cls, value):
    cls.bstack111l1l1ll1_opy_ = value
  @classmethod
  def bstack1ll1llllll1l_opy_(cls):
    return cls.bstack111l1l1ll1_opy_
  @classmethod
  def bstack11l1l1ll11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1ll1llll1lll_opy_(cls):
    return cls.percy_build_id