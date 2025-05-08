# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1l1l1l1_opy_, bstack11ll1l1l1ll_opy_
import tempfile
import json
bstack11l111l1lll_opy_ = os.getenv(bstack1l1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡉࡢࡊࡎࡒࡅࠣ᯹"), None) or os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠥ᯺"))
bstack11l111llll1_opy_ = os.path.join(bstack1l1lll_opy_ (u"ࠤ࡯ࡳ࡬ࠨ᯻"), bstack1l1lll_opy_ (u"ࠪࡷࡩࡱ࠭ࡤ࡮࡬࠱ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧ᯼"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1lll_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ᯽"),
      datefmt=bstack1l1lll_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ᯾"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll11lll_opy_():
  bstack11l111ll11l_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡊࡅࡃࡗࡊࠦ᯿"), bstack1l1lll_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨᰀ"))
  return logging.DEBUG if bstack11l111ll11l_opy_.lower() == bstack1l1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᰁ") else logging.INFO
def bstack1ll111llll1_opy_():
  global bstack11l111l1lll_opy_
  if os.path.exists(bstack11l111l1lll_opy_):
    os.remove(bstack11l111l1lll_opy_)
  if os.path.exists(bstack11l111llll1_opy_):
    os.remove(bstack11l111llll1_opy_)
def bstack1l11l11l11_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l1ll11_opy_(config, log_level):
  bstack11l11l111ll_opy_ = log_level
  if bstack1l1lll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᰂ") in config and config[bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᰃ")] in bstack11ll1l1l1l1_opy_:
    bstack11l11l111ll_opy_ = bstack11ll1l1l1l1_opy_[config[bstack1l1lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᰄ")]]
  if config.get(bstack1l1lll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧᰅ"), False):
    logging.getLogger().setLevel(bstack11l11l111ll_opy_)
    return bstack11l11l111ll_opy_
  global bstack11l111l1lll_opy_
  bstack1l11l11l11_opy_()
  bstack11l111l11l1_opy_ = logging.Formatter(
    fmt=bstack1l1lll_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᰆ"),
    datefmt=bstack1l1lll_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞ࠬᰇ"),
  )
  bstack11l111ll111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l1lll_opy_)
  file_handler.setFormatter(bstack11l111l11l1_opy_)
  bstack11l111ll111_opy_.setFormatter(bstack11l111l11l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l111ll111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1lll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪᰈ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l111ll111_opy_.setLevel(bstack11l11l111ll_opy_)
  logging.getLogger().addHandler(bstack11l111ll111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l11l111ll_opy_
def bstack11l111ll1ll_opy_(config):
  try:
    bstack11l111lll1l_opy_ = set(bstack11ll1l1l1ll_opy_)
    bstack11l11l1111l_opy_ = bstack1l1lll_opy_ (u"ࠩࠪᰉ")
    with open(bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ᰊ")) as bstack11l11l111l1_opy_:
      bstack11l111l111l_opy_ = bstack11l11l111l1_opy_.read()
      bstack11l11l1111l_opy_ = re.sub(bstack1l1lll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬᰋ"), bstack1l1lll_opy_ (u"ࠬ࠭ᰌ"), bstack11l111l111l_opy_, flags=re.M)
      bstack11l11l1111l_opy_ = re.sub(
        bstack1l1lll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩᰍ") + bstack1l1lll_opy_ (u"ࠧࡽࠩᰎ").join(bstack11l111lll1l_opy_) + bstack1l1lll_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭ᰏ"),
        bstack1l1lll_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᰐ"),
        bstack11l11l1111l_opy_, flags=re.M | re.I
      )
    def bstack11l111l1l1l_opy_(dic):
      bstack11l111lllll_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l111lll1l_opy_:
          bstack11l111lllll_opy_[key] = bstack1l1lll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᰑ")
        else:
          if isinstance(value, dict):
            bstack11l111lllll_opy_[key] = bstack11l111l1l1l_opy_(value)
          else:
            bstack11l111lllll_opy_[key] = value
      return bstack11l111lllll_opy_
    bstack11l111lllll_opy_ = bstack11l111l1l1l_opy_(config)
    return {
      bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᰒ"): bstack11l11l1111l_opy_,
      bstack1l1lll_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᰓ"): json.dumps(bstack11l111lllll_opy_)
    }
  except Exception as e:
    return {}
def bstack11l111l1ll1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1lll_opy_ (u"࠭࡬ࡰࡩࠪᰔ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l11l11lll_opy_ = os.path.join(log_dir, bstack1l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳࠨᰕ"))
  if not os.path.exists(bstack11l11l11lll_opy_):
    bstack11l111l1l11_opy_ = {
      bstack1l1lll_opy_ (u"ࠣ࡫ࡱ࡭ࡵࡧࡴࡩࠤᰖ"): str(inipath),
      bstack1l1lll_opy_ (u"ࠤࡵࡳࡴࡺࡰࡢࡶ࡫ࠦᰗ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᰘ")), bstack1l1lll_opy_ (u"ࠫࡼ࠭ᰙ")) as bstack11l111ll1l1_opy_:
      bstack11l111ll1l1_opy_.write(json.dumps(bstack11l111l1l11_opy_))
def bstack11l11l11111_opy_():
  try:
    bstack11l11l11lll_opy_ = os.path.join(os.getcwd(), bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡨࠩᰚ"), bstack1l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬᰛ"))
    if os.path.exists(bstack11l11l11lll_opy_):
      with open(bstack11l11l11lll_opy_, bstack1l1lll_opy_ (u"ࠧࡳࠩᰜ")) as bstack11l111ll1l1_opy_:
        bstack11l11l11l11_opy_ = json.load(bstack11l111ll1l1_opy_)
      return bstack11l11l11l11_opy_.get(bstack1l1lll_opy_ (u"ࠨ࡫ࡱ࡭ࡵࡧࡴࡩࠩᰝ"), bstack1l1lll_opy_ (u"ࠩࠪᰞ")), bstack11l11l11l11_opy_.get(bstack1l1lll_opy_ (u"ࠪࡶࡴࡵࡴࡱࡣࡷ࡬ࠬᰟ"), bstack1l1lll_opy_ (u"ࠫࠬᰠ"))
  except:
    pass
  return None, None
def bstack11l11l11l1l_opy_():
  try:
    bstack11l11l11lll_opy_ = os.path.join(os.getcwd(), bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡨࠩᰡ"), bstack1l1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬᰢ"))
    if os.path.exists(bstack11l11l11lll_opy_):
      os.remove(bstack11l11l11lll_opy_)
  except:
    pass
def bstack11lll11111_opy_(config):
  from bstack_utils.helper import bstack11l1l1l1l_opy_
  global bstack11l111l1lll_opy_
  try:
    if config.get(bstack1l1lll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᰣ"), False):
      return
    uuid = os.getenv(bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᰤ")) if os.getenv(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᰥ")) else bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠥࡷࡩࡱࡒࡶࡰࡌࡨࠧᰦ"))
    if not uuid or uuid == bstack1l1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᰧ"):
      return
    bstack11l11l11ll1_opy_ = [bstack1l1lll_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᰨ"), bstack1l1lll_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᰩ"), bstack1l1lll_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᰪ"), bstack11l111l1lll_opy_, bstack11l111llll1_opy_]
    bstack11l111lll11_opy_, root_path = bstack11l11l11111_opy_()
    if bstack11l111lll11_opy_ != None:
      bstack11l11l11ll1_opy_.append(bstack11l111lll11_opy_)
    if root_path != None:
      bstack11l11l11ll1_opy_.append(os.path.join(root_path, bstack1l1lll_opy_ (u"ࠨࡥࡲࡲ࡫ࡺࡥࡴࡶ࠱ࡴࡾ࠭ᰫ")))
    bstack1l11l11l11_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨᰬ") + uuid + bstack1l1lll_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫᰭ"))
    with tarfile.open(output_file, bstack1l1lll_opy_ (u"ࠦࡼࡀࡧࡻࠤᰮ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l11l11ll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111ll1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111l11ll_opy_ = data.encode()
        tarinfo.size = len(bstack11l111l11ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111l11ll_opy_))
    bstack11lll111ll_opy_ = MultipartEncoder(
      fields= {
        bstack1l1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᰯ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1lll_opy_ (u"࠭ࡲࡣࠩᰰ")), bstack1l1lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬᰱ")),
        bstack1l1lll_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᰲ"): uuid
      }
    )
    response = requests.post(
      bstack1l1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦᰳ"),
      data=bstack11lll111ll_opy_,
      headers={bstack1l1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᰴ"): bstack11lll111ll_opy_.content_type},
      auth=(config[bstack1l1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᰵ")], config[bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᰶ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤ᰷ࠬ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭᰸") + str(e))
  finally:
    try:
      bstack1ll111llll1_opy_()
      bstack11l11l11l1l_opy_()
    except:
      pass