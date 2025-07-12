# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111llll1l1l_opy_, bstack11l11111111_opy_, bstack111llllll1l_opy_
import tempfile
import json
bstack1111l1l11l1_opy_ = os.getenv(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧḑ"), None) or os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢḒ"))
bstack1111ll111ll_opy_ = os.path.join(bstack11l1111_opy_ (u"ࠨ࡬ࡰࡩࠥḓ"), bstack11l1111_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫḔ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1111_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫḕ"),
      datefmt=bstack11l1111_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧḖ"),
      stream=sys.stdout
    )
  return logger
def bstack1l11ll11l1l_opy_():
  bstack1111ll111l1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣḗ"), bstack11l1111_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥḘ"))
  return logging.DEBUG if bstack1111ll111l1_opy_.lower() == bstack11l1111_opy_ (u"ࠧࡺࡲࡶࡧࠥḙ") else logging.INFO
def bstack1llll111ll1_opy_():
  global bstack1111l1l11l1_opy_
  if os.path.exists(bstack1111l1l11l1_opy_):
    os.remove(bstack1111l1l11l1_opy_)
  if os.path.exists(bstack1111ll111ll_opy_):
    os.remove(bstack1111ll111ll_opy_)
def bstack11ll1ll1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l11l1111_opy_(config, log_level):
  bstack1111l1ll111_opy_ = log_level
  if bstack11l1111_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨḚ") in config and config[bstack11l1111_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩḛ")] in bstack11l11111111_opy_:
    bstack1111l1ll111_opy_ = bstack11l11111111_opy_[config[bstack11l1111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪḜ")]]
  if config.get(bstack11l1111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫḝ"), False):
    logging.getLogger().setLevel(bstack1111l1ll111_opy_)
    return bstack1111l1ll111_opy_
  global bstack1111l1l11l1_opy_
  bstack11ll1ll1ll_opy_()
  bstack1111l1ll11l_opy_ = logging.Formatter(
    fmt=bstack11l1111_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭Ḟ"),
    datefmt=bstack11l1111_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩḟ"),
  )
  bstack1111l1l1l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111l1l11l1_opy_)
  file_handler.setFormatter(bstack1111l1ll11l_opy_)
  bstack1111l1l1l1l_opy_.setFormatter(bstack1111l1ll11l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111l1l1l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧḠ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111l1l1l1l_opy_.setLevel(bstack1111l1ll111_opy_)
  logging.getLogger().addHandler(bstack1111l1l1l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111l1ll111_opy_
def bstack1111ll11l11_opy_(config):
  try:
    bstack1111ll11l1l_opy_ = set(bstack111llllll1l_opy_)
    bstack1111ll11111_opy_ = bstack11l1111_opy_ (u"࠭ࠧḡ")
    with open(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪḢ")) as bstack1111l1llll1_opy_:
      bstack1111l1lll1l_opy_ = bstack1111l1llll1_opy_.read()
      bstack1111ll11111_opy_ = re.sub(bstack11l1111_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩḣ"), bstack11l1111_opy_ (u"ࠩࠪḤ"), bstack1111l1lll1l_opy_, flags=re.M)
      bstack1111ll11111_opy_ = re.sub(
        bstack11l1111_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ḥ") + bstack11l1111_opy_ (u"ࠫࢁ࠭Ḧ").join(bstack1111ll11l1l_opy_) + bstack11l1111_opy_ (u"ࠬ࠯࠮ࠫࠦࠪḧ"),
        bstack11l1111_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨḨ"),
        bstack1111ll11111_opy_, flags=re.M | re.I
      )
    def bstack1111l1l1lll_opy_(dic):
      bstack1111l1ll1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111ll11l1l_opy_:
          bstack1111l1ll1l1_opy_[key] = bstack11l1111_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫḩ")
        else:
          if isinstance(value, dict):
            bstack1111l1ll1l1_opy_[key] = bstack1111l1l1lll_opy_(value)
          else:
            bstack1111l1ll1l1_opy_[key] = value
      return bstack1111l1ll1l1_opy_
    bstack1111l1ll1l1_opy_ = bstack1111l1l1lll_opy_(config)
    return {
      bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫḪ"): bstack1111ll11111_opy_,
      bstack11l1111_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬḫ"): json.dumps(bstack1111l1ll1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack1111l11llll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11l1111_opy_ (u"ࠪࡰࡴ࡭ࠧḬ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l1l1ll1l1_opy_ = os.path.join(log_dir, bstack11l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬḭ"))
  if not os.path.exists(bstack11l1l1ll1l1_opy_):
    bstack1111l1l1l11_opy_ = {
      bstack11l1111_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨḮ"): str(inipath),
      bstack11l1111_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣḯ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11l1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭Ḱ")), bstack11l1111_opy_ (u"ࠨࡹࠪḱ")) as bstack1111l1l111l_opy_:
      bstack1111l1l111l_opy_.write(json.dumps(bstack1111l1l1l11_opy_))
def bstack1111l1lll11_opy_():
  try:
    bstack11l1l1ll1l1_opy_ = os.path.join(os.getcwd(), bstack11l1111_opy_ (u"ࠩ࡯ࡳ࡬࠭Ḳ"), bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩḳ"))
    if os.path.exists(bstack11l1l1ll1l1_opy_):
      with open(bstack11l1l1ll1l1_opy_, bstack11l1111_opy_ (u"ࠫࡷ࠭Ḵ")) as bstack1111l1l111l_opy_:
        bstack1111l1ll1ll_opy_ = json.load(bstack1111l1l111l_opy_)
      return bstack1111l1ll1ll_opy_.get(bstack11l1111_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ḵ"), bstack11l1111_opy_ (u"࠭ࠧḶ")), bstack1111l1ll1ll_opy_.get(bstack11l1111_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩḷ"), bstack11l1111_opy_ (u"ࠨࠩḸ"))
  except:
    pass
  return None, None
def bstack1111l1l11ll_opy_():
  try:
    bstack11l1l1ll1l1_opy_ = os.path.join(os.getcwd(), bstack11l1111_opy_ (u"ࠩ࡯ࡳ࡬࠭ḹ"), bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩḺ"))
    if os.path.exists(bstack11l1l1ll1l1_opy_):
      os.remove(bstack11l1l1ll1l1_opy_)
  except:
    pass
def bstack11lll11l_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1l11l1ll_opy_, bstack1l1l1l11l1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111l1l11l1_opy_
    if config.get(bstack11l1111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ḻ"), False):
      return
    uuid = os.getenv(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḼ")) if os.getenv(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫḽ")) else bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤḾ"))
    if not uuid or uuid == bstack11l1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭ḿ"):
      return
    bstack1111l1lllll_opy_ = [bstack11l1111_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬṀ"), bstack11l1111_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫṁ"), bstack11l1111_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬṂ"), bstack1111l1l11l1_opy_, bstack1111ll111ll_opy_]
    bstack1111ll1111l_opy_, root_path = bstack1111l1lll11_opy_()
    if bstack1111ll1111l_opy_ != None:
      bstack1111l1lllll_opy_.append(bstack1111ll1111l_opy_)
    if root_path != None:
      bstack1111l1lllll_opy_.append(os.path.join(root_path, bstack11l1111_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪṃ")))
    bstack11ll1ll1ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬṄ") + uuid + bstack11l1111_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨṅ"))
    with tarfile.open(output_file, bstack11l1111_opy_ (u"ࠣࡹ࠽࡫ࡿࠨṆ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111l1lllll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111ll11l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111l1l1111_opy_ = data.encode()
        tarinfo.size = len(bstack1111l1l1111_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111l1l1111_opy_))
    bstack1l111l11l_opy_ = MultipartEncoder(
      fields= {
        bstack11l1111_opy_ (u"ࠩࡧࡥࡹࡧࠧṇ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1111_opy_ (u"ࠪࡶࡧ࠭Ṉ")), bstack11l1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩṉ")),
        bstack11l1111_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧṊ"): uuid
      }
    )
    bstack1111l1l1ll1_opy_ = bstack1l1l1l11l1_opy_(cli.config, [bstack11l1111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦṋ"), bstack11l1111_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢṌ"), bstack11l1111_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣṍ")], bstack111llll1l1l_opy_)
    response = requests.post(
      bstack11l1111_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥṎ").format(bstack1111l1l1ll1_opy_),
      data=bstack1l111l11l_opy_,
      headers={bstack11l1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩṏ"): bstack1l111l11l_opy_.content_type},
      auth=(config[bstack11l1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ṑ")], config[bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨṑ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬṒ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ṓ") + str(e))
  finally:
    try:
      bstack1llll111ll1_opy_()
      bstack1111l1l11ll_opy_()
    except:
      pass