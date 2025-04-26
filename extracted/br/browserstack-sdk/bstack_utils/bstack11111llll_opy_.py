# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1lll11l_opy_, bstack11ll1l1lll1_opy_
import tempfile
import json
bstack11l111l1l11_opy_ = os.getenv(bstack1l11lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅ᯲ࠣ"), None) or os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩ᯳ࠥ"))
bstack11l111lll11_opy_ = os.path.join(bstack1l11lll_opy_ (u"ࠤ࡯ࡳ࡬ࠨ᯴"), bstack1l11lll_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧ᯵"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l11lll_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ᯶"),
      datefmt=bstack1l11lll_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ᯷"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1lll111_opy_():
  bstack11l111l11ll_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡊࡅࡃࡗࡊࠦ᯸"), bstack1l11lll_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ᯹"))
  return logging.DEBUG if bstack11l111l11ll_opy_.lower() == bstack1l11lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᯺") else logging.INFO
def bstack1l1lll1ll1l_opy_():
  global bstack11l111l1l11_opy_
  if os.path.exists(bstack11l111l1l11_opy_):
    os.remove(bstack11l111l1l11_opy_)
  if os.path.exists(bstack11l111lll11_opy_):
    os.remove(bstack11l111lll11_opy_)
def bstack11ll1l11ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1ll1ll1_opy_(config, log_level):
  bstack11l111llll1_opy_ = log_level
  if bstack1l11lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ᯻") in config and config[bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬ᯼")] in bstack11ll1lll11l_opy_:
    bstack11l111llll1_opy_ = bstack11ll1lll11l_opy_[config[bstack1l11lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭᯽")]]
  if config.get(bstack1l11lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ᯾"), False):
    logging.getLogger().setLevel(bstack11l111llll1_opy_)
    return bstack11l111llll1_opy_
  global bstack11l111l1l11_opy_
  bstack11ll1l11ll_opy_()
  bstack11l111l111l_opy_ = logging.Formatter(
    fmt=bstack1l11lll_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩ᯿"),
    datefmt=bstack1l11lll_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬᰀ"),
  )
  bstack11l11l111ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l1l11_opy_)
  file_handler.setFormatter(bstack11l111l111l_opy_)
  bstack11l11l111ll_opy_.setFormatter(bstack11l111l111l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l11l111ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l11lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪᰁ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l11l111ll_opy_.setLevel(bstack11l111llll1_opy_)
  logging.getLogger().addHandler(bstack11l11l111ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111llll1_opy_
def bstack11l111ll11l_opy_(config):
  try:
    bstack11l11l1111l_opy_ = set(bstack11ll1l1lll1_opy_)
    bstack11l11l11l11_opy_ = bstack1l11lll_opy_ (u"ࠩࠪᰂ")
    with open(bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᰃ")) as bstack11l111ll1l1_opy_:
      bstack11l111ll1ll_opy_ = bstack11l111ll1l1_opy_.read()
      bstack11l11l11l11_opy_ = re.sub(bstack1l11lll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬᰄ"), bstack1l11lll_opy_ (u"ࠬ࠭ᰅ"), bstack11l111ll1ll_opy_, flags=re.M)
      bstack11l11l11l11_opy_ = re.sub(
        bstack1l11lll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩᰆ") + bstack1l11lll_opy_ (u"ࠧࡽࠩᰇ").join(bstack11l11l1111l_opy_) + bstack1l11lll_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭ᰈ"),
        bstack1l11lll_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᰉ"),
        bstack11l11l11l11_opy_, flags=re.M | re.I
      )
    def bstack11l11l11l1l_opy_(dic):
      bstack11l11l11111_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l11l1111l_opy_:
          bstack11l11l11111_opy_[key] = bstack1l11lll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᰊ")
        else:
          if isinstance(value, dict):
            bstack11l11l11111_opy_[key] = bstack11l11l11l1l_opy_(value)
          else:
            bstack11l11l11111_opy_[key] = value
      return bstack11l11l11111_opy_
    bstack11l11l11111_opy_ = bstack11l11l11l1l_opy_(config)
    return {
      bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᰋ"): bstack11l11l11l11_opy_,
      bstack1l11lll_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᰌ"): json.dumps(bstack11l11l11111_opy_)
    }
  except Exception as e:
    return {}
def bstack11l11l11lll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l11lll_opy_ (u"࠭࡬ࡰࡩࠪᰍ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l111l1_opy_ = os.path.join(log_dir, bstack1l11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳࠨᰎ"))
  if not os.path.exists(bstack11l11l111l1_opy_):
    bstack11l111l1l1l_opy_ = {
      bstack1l11lll_opy_ (u"ࠣ࡫ࡱ࡭ࡵࡧࡴࡩࠤᰏ"): str(inipath),
      bstack1l11lll_opy_ (u"ࠤࡵࡳࡴࡺࡰࡢࡶ࡫ࠦᰐ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᰑ")), bstack1l11lll_opy_ (u"ࠫࡼ࠭ᰒ")) as bstack11l111l1lll_opy_:
      bstack11l111l1lll_opy_.write(json.dumps(bstack11l111l1l1l_opy_))
def bstack11l111l11l1_opy_():
  try:
    bstack11l11l111l1_opy_ = os.path.join(os.getcwd(), bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡨࠩᰓ"), bstack1l11lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬᰔ"))
    if os.path.exists(bstack11l11l111l1_opy_):
      with open(bstack11l11l111l1_opy_, bstack1l11lll_opy_ (u"ࠧࡳࠩᰕ")) as bstack11l111l1lll_opy_:
        bstack11l111l1ll1_opy_ = json.load(bstack11l111l1lll_opy_)
      return bstack11l111l1ll1_opy_.get(bstack1l11lll_opy_ (u"ࠨ࡫ࡱ࡭ࡵࡧࡴࡩࠩᰖ"), bstack1l11lll_opy_ (u"ࠩࠪᰗ")), bstack11l111l1ll1_opy_.get(bstack1l11lll_opy_ (u"ࠪࡶࡴࡵࡴࡱࡣࡷ࡬ࠬᰘ"), bstack1l11lll_opy_ (u"ࠫࠬᰙ"))
  except:
    pass
  return None, None
def bstack11l111lllll_opy_():
  try:
    bstack11l11l111l1_opy_ = os.path.join(os.getcwd(), bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡨࠩᰚ"), bstack1l11lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬᰛ"))
    if os.path.exists(bstack11l11l111l1_opy_):
      os.remove(bstack11l11l111l1_opy_)
  except:
    pass
def bstack1l1l111ll_opy_(config):
  from bstack_utils.helper import bstack11lll1l1ll_opy_
  global bstack11l111l1l11_opy_
  try:
    if config.get(bstack1l11lll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᰜ"), False):
      return
    uuid = os.getenv(bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᰝ")) if os.getenv(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᰞ")) else bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧᰟ"))
    if not uuid or uuid == bstack1l11lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᰠ"):
      return
    bstack11l111lll1l_opy_ = [bstack1l11lll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᰡ"), bstack1l11lll_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᰢ"), bstack1l11lll_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᰣ"), bstack11l111l1l11_opy_, bstack11l111lll11_opy_]
    bstack11l111ll111_opy_, root_path = bstack11l111l11l1_opy_()
    if bstack11l111ll111_opy_ != None:
      bstack11l111lll1l_opy_.append(bstack11l111ll111_opy_)
    if root_path != None:
      bstack11l111lll1l_opy_.append(os.path.join(root_path, bstack1l11lll_opy_ (u"ࠨࡥࡲࡲ࡫ࡺࡥࡴࡶ࠱ࡴࡾ࠭ᰤ")))
    bstack11ll1l11ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨᰥ") + uuid + bstack1l11lll_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫᰦ"))
    with tarfile.open(output_file, bstack1l11lll_opy_ (u"ࠦࡼࡀࡧࡻࠤᰧ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l111lll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111ll11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l11l11ll1_opy_ = data.encode()
        tarinfo.size = len(bstack11l11l11ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l11l11ll1_opy_))
    bstack1l111lllll_opy_ = MultipartEncoder(
      fields= {
        bstack1l11lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᰨ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l11lll_opy_ (u"࠭ࡲࡣࠩᰩ")), bstack1l11lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬᰪ")),
        bstack1l11lll_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰫ"): uuid
      }
    )
    response = requests.post(
      bstack1l11lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦᰬ"),
      data=bstack1l111lllll_opy_,
      headers={bstack1l11lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᰭ"): bstack1l111lllll_opy_.content_type},
      auth=(config[bstack1l11lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᰮ")], config[bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᰯ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l11lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬᰰ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l11lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ᰱ") + str(e))
  finally:
    try:
      bstack1l1lll1ll1l_opy_()
      bstack11l111lllll_opy_()
    except:
      pass