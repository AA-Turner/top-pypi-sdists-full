# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1ll111ll_opy_, bstack11l1llllll1_opy_, bstack11l1lll1lll_opy_
import tempfile
import json
bstack111l1ll11ll_opy_ = os.getenv(bstack1l11ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧᶡ"), None) or os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢᶢ"))
bstack111l1l1ll1l_opy_ = os.path.join(bstack1l11ll1_opy_ (u"ࠨ࡬ࡰࡩࠥᶣ"), bstack1l11ll1_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᶤ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l11ll1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᶥ"),
      datefmt=bstack1l11ll1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᶦ"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11l1l1_opy_():
  bstack111l1l11ll1_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣᶧ"), bstack1l11ll1_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᶨ"))
  return logging.DEBUG if bstack111l1l11ll1_opy_.lower() == bstack1l11ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᶩ") else logging.INFO
def bstack1l1l1ll111l_opy_():
  global bstack111l1ll11ll_opy_
  if os.path.exists(bstack111l1ll11ll_opy_):
    os.remove(bstack111l1ll11ll_opy_)
  if os.path.exists(bstack111l1l1ll1l_opy_):
    os.remove(bstack111l1l1ll1l_opy_)
def bstack1l1ll11l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l1l1lll1_opy_ = log_level
  if bstack1l11ll1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᶪ") in config and config[bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᶫ")] in bstack11l1llllll1_opy_:
    bstack111l1l1lll1_opy_ = bstack11l1llllll1_opy_[config[bstack1l11ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᶬ")]]
  if config.get(bstack1l11ll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᶭ"), False):
    logging.getLogger().setLevel(bstack111l1l1lll1_opy_)
    return bstack111l1l1lll1_opy_
  global bstack111l1ll11ll_opy_
  bstack1l1ll11l1_opy_()
  bstack111l1ll1l11_opy_ = logging.Formatter(
    fmt=bstack1l11ll1_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᶮ"),
    datefmt=bstack1l11ll1_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᶯ"),
  )
  bstack111l1lll1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1ll11ll_opy_)
  file_handler.setFormatter(bstack111l1ll1l11_opy_)
  bstack111l1lll1ll_opy_.setFormatter(bstack111l1ll1l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1lll1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l11ll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᶰ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1lll1ll_opy_.setLevel(bstack111l1l1lll1_opy_)
  logging.getLogger().addHandler(bstack111l1lll1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1l1lll1_opy_
def bstack111l1ll111l_opy_(config):
  try:
    bstack111l1l1l111_opy_ = set(bstack11l1lll1lll_opy_)
    bstack111l1ll1lll_opy_ = bstack1l11ll1_opy_ (u"࠭ࠧᶱ")
    with open(bstack1l11ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᶲ")) as bstack111l1ll1l1l_opy_:
      bstack111l1ll1ll1_opy_ = bstack111l1ll1l1l_opy_.read()
      bstack111l1ll1lll_opy_ = re.sub(bstack1l11ll1_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᶳ"), bstack1l11ll1_opy_ (u"ࠩࠪᶴ"), bstack111l1ll1ll1_opy_, flags=re.M)
      bstack111l1ll1lll_opy_ = re.sub(
        bstack1l11ll1_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᶵ") + bstack1l11ll1_opy_ (u"ࠫࢁ࠭ᶶ").join(bstack111l1l1l111_opy_) + bstack1l11ll1_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᶷ"),
        bstack1l11ll1_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᶸ"),
        bstack111l1ll1lll_opy_, flags=re.M | re.I
      )
    def bstack111l1l1ll11_opy_(dic):
      bstack111l1lll11l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1l1l111_opy_:
          bstack111l1lll11l_opy_[key] = bstack1l11ll1_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᶹ")
        else:
          if isinstance(value, dict):
            bstack111l1lll11l_opy_[key] = bstack111l1l1ll11_opy_(value)
          else:
            bstack111l1lll11l_opy_[key] = value
      return bstack111l1lll11l_opy_
    bstack111l1lll11l_opy_ = bstack111l1l1ll11_opy_(config)
    return {
      bstack1l11ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᶺ"): bstack111l1ll1lll_opy_,
      bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᶻ"): json.dumps(bstack111l1lll11l_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1ll1111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠪࡰࡴ࡭ࠧᶼ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1l1l1l1_opy_ = os.path.join(log_dir, bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬᶽ"))
  if not os.path.exists(bstack111l1l1l1l1_opy_):
    bstack111l1l11l1l_opy_ = {
      bstack1l11ll1_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᶾ"): str(inipath),
      bstack1l11ll1_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᶿ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᷀")), bstack1l11ll1_opy_ (u"ࠨࡹࠪ᷁")) as bstack111l1l11lll_opy_:
      bstack111l1l11lll_opy_.write(json.dumps(bstack111l1l11l1l_opy_))
def bstack111l1lll1l1_opy_():
  try:
    bstack111l1l1l1l1_opy_ = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠩ࡯ࡳ࡬᷂࠭"), bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩ᷃"))
    if os.path.exists(bstack111l1l1l1l1_opy_):
      with open(bstack111l1l1l1l1_opy_, bstack1l11ll1_opy_ (u"ࠫࡷ࠭᷄")) as bstack111l1l11lll_opy_:
        bstack111l1lll111_opy_ = json.load(bstack111l1l11lll_opy_)
      return bstack111l1lll111_opy_.get(bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭᷅"), bstack1l11ll1_opy_ (u"࠭ࠧ᷆")), bstack111l1lll111_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩ᷇"), bstack1l11ll1_opy_ (u"ࠨࠩ᷈"))
  except:
    pass
  return None, None
def bstack111l1l1llll_opy_():
  try:
    bstack111l1l1l1l1_opy_ = os.path.join(os.getcwd(), bstack1l11ll1_opy_ (u"ࠩ࡯ࡳ࡬࠭᷉"), bstack1l11ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯᷊ࠩ"))
    if os.path.exists(bstack111l1l1l1l1_opy_):
      os.remove(bstack111l1l1l1l1_opy_)
  except:
    pass
def bstack1l1lll1l1_opy_(config):
  try:
    from bstack_utils.helper import bstack111lllll11_opy_, bstack1ll1111l1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1ll11ll_opy_
    if config.get(bstack1l11ll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭᷋"), False):
      return
    uuid = os.getenv(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᷌")) if os.getenv(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᷍")) else bstack111lllll11_opy_.get_property(bstack1l11ll1_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤ᷎"))
    if not uuid or uuid == bstack1l11ll1_opy_ (u"ࠨࡰࡸࡰࡱ᷏࠭"):
      return
    bstack111l1l1l1ll_opy_ = [bstack1l11ll1_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸ᷐ࠬ"), bstack1l11ll1_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ᷑"), bstack1l11ll1_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ᷒"), bstack111l1ll11ll_opy_, bstack111l1l1ll1l_opy_]
    bstack111l1l1l11l_opy_, root_path = bstack111l1lll1l1_opy_()
    if bstack111l1l1l11l_opy_ != None:
      bstack111l1l1l1ll_opy_.append(bstack111l1l1l11l_opy_)
    if root_path != None:
      bstack111l1l1l1ll_opy_.append(os.path.join(root_path, bstack1l11ll1_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᷓ")))
    bstack1l1ll11l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᷔ") + uuid + bstack1l11ll1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᷕ"))
    with tarfile.open(output_file, bstack1l11ll1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᷖ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1l1l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1ll111l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1l11l11_opy_ = data.encode()
        tarinfo.size = len(bstack111l1l11l11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1l11l11_opy_))
    bstack1l1ll111l1_opy_ = MultipartEncoder(
      fields= {
        bstack1l11ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧᷗ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l11ll1_opy_ (u"ࠪࡶࡧ࠭ᷘ")), bstack1l11ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᷙ")),
        bstack1l11ll1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᷚ"): uuid
      }
    )
    bstack111l1ll11l1_opy_ = bstack1ll1111l1l_opy_(cli.config, [bstack1l11ll1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦᷛ"), bstack1l11ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᷜ"), bstack1l11ll1_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣᷝ")], bstack11l1ll111ll_opy_)
    response = requests.post(
      bstack1l11ll1_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᷞ").format(bstack111l1ll11l1_opy_),
      data=bstack1l1ll111l1_opy_,
      headers={bstack1l11ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᷟ"): bstack1l1ll111l1_opy_.content_type},
      auth=(config[bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᷠ")], config[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᷡ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l11ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬᷢ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l11ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ᷣ") + str(e))
  finally:
    try:
      bstack1l1l1ll111l_opy_()
      bstack111l1l1llll_opy_()
    except:
      pass