# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l111ll_opy_, bstack111llll11_opy_, bstack11l1lll111_opy_, bstack1lll1111l1_opy_,
                                    bstack11ll1l11lll_opy_, bstack11ll1ll1lll_opy_, bstack11ll1l1ll1l_opy_, bstack11ll1ll1111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll11111ll_opy_, bstack1l11ll1ll1_opy_
from bstack_utils.proxy import bstack1ll111111l_opy_, bstack1l1lll11_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11lll1_opy_
from browserstack_sdk._version import __version__
bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
logger = bstack1l11lll1_opy_.get_logger(__name__, bstack1l11lll1_opy_.bstack1ll1lllllll_opy_())
def bstack11lll1ll111_opy_(config):
    return config[bstack11lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᦮")]
def bstack11llll11ll1_opy_(config):
    return config[bstack11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᦯")]
def bstack1l1ll11l1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11ll11111ll_opy_(obj):
    values = []
    bstack11ll11ll1l1_opy_ = re.compile(bstack11lll_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᦰ"), re.I)
    for key in obj.keys():
        if bstack11ll11ll1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11lll11l_opy_(config):
    tags = []
    tags.extend(bstack11ll11111ll_opy_(os.environ))
    tags.extend(bstack11ll11111ll_opy_(config))
    return tags
def bstack11l1ll1l1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1lll1lll_opy_(bstack11l11lll1l1_opy_):
    if not bstack11l11lll1l1_opy_:
        return bstack11lll_opy_ (u"ࠫࠬᦱ")
    return bstack11lll_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᦲ").format(bstack11l11lll1l1_opy_.name, bstack11l11lll1l1_opy_.email)
def bstack11lll1l1lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1111_opy_ = repo.common_dir
        info = {
            bstack11lll_opy_ (u"ࠨࡳࡩࡣࠥᦳ"): repo.head.commit.hexsha,
            bstack11lll_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᦴ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lll_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᦵ"): repo.active_branch.name,
            bstack11lll_opy_ (u"ࠤࡷࡥ࡬ࠨᦶ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᦷ"): bstack11l1lll1lll_opy_(repo.head.commit.committer),
            bstack11lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᦸ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᦹ"): bstack11l1lll1lll_opy_(repo.head.commit.author),
            bstack11lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᦺ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᦻ"): repo.head.commit.message,
            bstack11lll_opy_ (u"ࠣࡴࡲࡳࡹࠨᦼ"): repo.git.rev_parse(bstack11lll_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᦽ")),
            bstack11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᦾ"): bstack11l1lll1111_opy_,
            bstack11lll_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᦿ"): subprocess.check_output([bstack11lll_opy_ (u"ࠧ࡭ࡩࡵࠤᧀ"), bstack11lll_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᧁ"), bstack11lll_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᧂ")]).strip().decode(
                bstack11lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᧃ")),
            bstack11lll_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᧄ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᧅ"): repo.git.rev_list(
                bstack11lll_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᧆ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1ll11ll1_opy_ = []
        for remote in remotes:
            bstack11l1lll111l_opy_ = {
                bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᧇ"): remote.name,
                bstack11lll_opy_ (u"ࠨࡵࡳ࡮ࠥᧈ"): remote.url,
            }
            bstack11l1ll11ll1_opy_.append(bstack11l1lll111l_opy_)
        bstack11l1ll1l11l_opy_ = {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᧉ"): bstack11lll_opy_ (u"ࠣࡩ࡬ࡸࠧ᧊"),
            **info,
            bstack11lll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥ᧋"): bstack11l1ll11ll1_opy_
        }
        bstack11l1ll1l11l_opy_ = bstack11l1l11l1l1_opy_(bstack11l1ll1l11l_opy_)
        return bstack11l1ll1l11l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ᧌").format(err))
        return {}
def bstack11l1l11l1l1_opy_(bstack11l1ll1l11l_opy_):
    bstack11l11llll1l_opy_ = bstack11l1l1ll111_opy_(bstack11l1ll1l11l_opy_)
    if bstack11l11llll1l_opy_ and bstack11l11llll1l_opy_ > bstack11ll1l11lll_opy_:
        bstack11ll111l11l_opy_ = bstack11l11llll1l_opy_ - bstack11ll1l11lll_opy_
        bstack11l1l1l1lll_opy_ = bstack11l1ll11l11_opy_(bstack11l1ll1l11l_opy_[bstack11lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᧍")], bstack11ll111l11l_opy_)
        bstack11l1ll1l11l_opy_[bstack11lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᧎")] = bstack11l1l1l1lll_opy_
        logger.info(bstack11lll_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ᧏")
                    .format(bstack11l1l1ll111_opy_(bstack11l1ll1l11l_opy_) / 1024))
    return bstack11l1ll1l11l_opy_
def bstack11l1l1ll111_opy_(bstack111llll1l_opy_):
    try:
        if bstack111llll1l_opy_:
            bstack11l1l1l1l11_opy_ = json.dumps(bstack111llll1l_opy_)
            bstack11l1ll11111_opy_ = sys.getsizeof(bstack11l1l1l1l11_opy_)
            return bstack11l1ll11111_opy_
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢ᧐").format(e))
    return -1
def bstack11l1ll11l11_opy_(field, bstack11l1l111l1l_opy_):
    try:
        bstack11l11lll1ll_opy_ = len(bytes(bstack11ll1ll1lll_opy_, bstack11lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᧑")))
        bstack11l1l1111ll_opy_ = bytes(field, bstack11lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᧒"))
        bstack11l1l11ll11_opy_ = len(bstack11l1l1111ll_opy_)
        bstack11ll11ll11l_opy_ = ceil(bstack11l1l11ll11_opy_ - bstack11l1l111l1l_opy_ - bstack11l11lll1ll_opy_)
        if bstack11ll11ll11l_opy_ > 0:
            bstack11l1l11l111_opy_ = bstack11l1l1111ll_opy_[:bstack11ll11ll11l_opy_].decode(bstack11lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧓"), errors=bstack11lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ᧔")) + bstack11ll1ll1lll_opy_
            return bstack11l1l11l111_opy_
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ᧕").format(e))
    return field
def bstack11lllll11_opy_():
    env = os.environ
    if (bstack11lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᧖") in env and len(env[bstack11lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᧗")]) > 0) or (
            bstack11lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᧘") in env and len(env[bstack11lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᧙")]) > 0):
        return {
            bstack11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧚"): bstack11lll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ᧛"),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᧜"): env.get(bstack11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᧝")),
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧞"): env.get(bstack11lll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ᧟")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧠"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᧡"))
        }
    if env.get(bstack11lll_opy_ (u"ࠦࡈࡏࠢ᧢")) == bstack11lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᧣") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ᧤"))):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧥"): bstack11lll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ᧦"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧧"): env.get(bstack11lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᧨")),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧩"): env.get(bstack11lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ᧪")),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧫"): env.get(bstack11lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ᧬"))
        }
    if env.get(bstack11lll_opy_ (u"ࠣࡅࡌࠦ᧭")) == bstack11lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧮") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ᧯"))):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧰"): bstack11lll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᧱"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧲"): env.get(bstack11lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ᧳")),
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧴"): env.get(bstack11lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᧵")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧶"): env.get(bstack11lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᧷"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡉࠣ᧸")) == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧹") and env.get(bstack11lll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ᧺")) == bstack11lll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᧻"):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧼"): bstack11lll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ᧽"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧾"): None,
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧿"): None,
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨀ"): None
        }
    if env.get(bstack11lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᨁ")) and env.get(bstack11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᨂ")):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨃ"): bstack11lll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᨄ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨅ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᨆ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨇ"): None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨈ"): env.get(bstack11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᨉ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧᨊ")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨋ") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᨌ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨍ"): bstack11lll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᨎ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨏ"): env.get(bstack11lll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᨐ")),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨑ"): None,
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨒ"): env.get(bstack11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨓ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡉࠣᨔ")) == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᨕ") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᨖ"))):
        return {
            bstack11lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᨗ"): bstack11lll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩᨘࠧ"),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨙ"): env.get(bstack11lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᨚ")),
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨛ"): env.get(bstack11lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᨜")),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᨝"): env.get(bstack11lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦ᨞"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧ᨟")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨠ") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᨡ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨢ"): bstack11lll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨᨣ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨤ"): env.get(bstack11lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᨥ")),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨦ"): env.get(bstack11lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᨧ")),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨨ"): env.get(bstack11lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᨩ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠨࡃࡊࠤᨪ")) == bstack11lll_opy_ (u"ࠢࡵࡴࡸࡩࠧᨫ") and bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᨬ"))):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨭ"): bstack11lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᨮ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨯ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᨰ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨱ"): env.get(bstack11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᨲ")) or env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᨳ")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨴ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨵ"))
        }
    if bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᨶ"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨷ"): bstack11lll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᨸ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨹ"): bstack11lll_opy_ (u"ࠣࡽࢀࡿࢂࠨᨺ").format(env.get(bstack11lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᨻ")), env.get(bstack11lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᨼ"))),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨽ"): env.get(bstack11lll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᨾ")),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨿ"): env.get(bstack11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩀ"))
        }
    if bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᩁ"))):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩂ"): bstack11lll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᩃ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩄ"): bstack11lll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᩅ").format(env.get(bstack11lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᩆ")), env.get(bstack11lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᩇ")), env.get(bstack11lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᩈ")), env.get(bstack11lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᩉ"))),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩊ"): env.get(bstack11lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᩋ")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩌ"): env.get(bstack11lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᩍ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᩎ")) and env.get(bstack11lll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᩏ")):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩐ"): bstack11lll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᩑ"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩒ"): bstack11lll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᩓ").format(env.get(bstack11lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᩔ")), env.get(bstack11lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᩕ")), env.get(bstack11lll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᩖ"))),
            bstack11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩗ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᩘ")),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩙ"): env.get(bstack11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩚ"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩛ")), env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᩜ")), env.get(bstack11lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᩝ"))]):
        return {
            bstack11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩞ"): bstack11lll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥ᩟"),
            bstack11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲ᩠ࠢ"): env.get(bstack11lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᩡ")),
            bstack11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩢ"): env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᩣ")),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩤ"): env.get(bstack11lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩥ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᩦ")):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩧ"): bstack11lll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᩨ"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩩ"): env.get(bstack11lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᩪ")),
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩫ"): env.get(bstack11lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᩬ")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩭ"): env.get(bstack11lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᩮ"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᩯ")) or env.get(bstack11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᩰ")):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩱ"): bstack11lll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᩲ"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩳ"): env.get(bstack11lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᩴ")),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᩵"): bstack11lll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧ᩶") if env.get(bstack11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᩷")) else None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᩸"): env.get(bstack11lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᩹"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᩺")), env.get(bstack11lll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩻")), env.get(bstack11lll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩼"))]):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩽"): bstack11lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧ᩾"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᩿ࠥ"): None,
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪀"): env.get(bstack11lll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨ᪁")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᪂"): env.get(bstack11lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᪃"))
        }
    if env.get(bstack11lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ᪄")):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪅"): bstack11lll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥ᪆"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪇"): env.get(bstack11lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᪈")),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪉"): bstack11lll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ᪊").format(env.get(bstack11lll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ᪋"))) if env.get(bstack11lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ᪌")) else None,
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪍"): env.get(bstack11lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪎"))
        }
    if bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ᪏"))):
        return {
            bstack11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪐"): bstack11lll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ᪑"),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪒"): env.get(bstack11lll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ᪓")),
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪔"): env.get(bstack11lll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ᪕")),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪖"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᪗"))
        }
    if bstack1l11lll11l_opy_(env.get(bstack11lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ᪘"))):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪙"): bstack11lll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢ᪚"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪛"): bstack11lll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤ᪜").format(env.get(bstack11lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭᪝")), env.get(bstack11lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧ᪞")), env.get(bstack11lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫ᪟"))),
            bstack11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): env.get(bstack11lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣ᪡")),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪢"): env.get(bstack11lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣ᪣"))
        }
    if env.get(bstack11lll_opy_ (u"ࠤࡆࡍࠧ᪤")) == bstack11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪥") and env.get(bstack11lll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦ᪦")) == bstack11lll_opy_ (u"ࠧ࠷ࠢᪧ"):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪨"): bstack11lll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ᪩"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪪"): bstack11lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ᪫").format(env.get(bstack11lll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ᪬"))),
            bstack11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪭"): None,
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪮"): None,
        }
    if env.get(bstack11lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᪯")):
        return {
            bstack11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪰"): bstack11lll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ᪱"),
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪲"): None,
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪳"): env.get(bstack11lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ᪴")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᪵ࠦ"): env.get(bstack11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᪶ࠧ"))
        }
    if any([env.get(bstack11lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇ᪷ࠥ")), env.get(bstack11lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌ᪸ࠣ")), env.get(bstack11lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋ᪹ࠢ")), env.get(bstack11lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐ᪺ࠦ"))]):
        return {
            bstack11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪻"): bstack11lll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ᪼"),
            bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪽"): None,
            bstack11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪾"): env.get(bstack11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᪿ")) or None,
            bstack11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᫀࠣ"): env.get(bstack11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᫁"), 0)
        }
    if env.get(bstack11lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᫂")):
        return {
            bstack11lll_opy_ (u"ࠧࡴࡡ࡮ࡧ᫃ࠥ"): bstack11lll_opy_ (u"ࠨࡇࡰࡅࡇ᫄ࠦ"),
            bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫅"): None,
            bstack11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫆"): env.get(bstack11lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫇")),
            bstack11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫈"): env.get(bstack11lll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ᫉"))
        }
    if env.get(bstack11lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆ᫊ࠥ")):
        return {
            bstack11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫋"): bstack11lll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᫌ"),
            bstack11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᫍ"): env.get(bstack11lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᫎ")),
            bstack11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫏"): env.get(bstack11lll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ᫐")),
            bstack11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫑"): env.get(bstack11lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᫒"))
        }
    return {bstack11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫓"): None}
def get_host_info():
    return {
        bstack11lll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥ᫔"): platform.node(),
        bstack11lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ᫕"): platform.system(),
        bstack11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᫖"): platform.machine(),
        bstack11lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᫗"): platform.version(),
        bstack11lll_opy_ (u"ࠧࡧࡲࡤࡪࠥ᫘"): platform.architecture()[0]
    }
def bstack1lll11ll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1lll1l11_opy_():
    if bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᫙")):
        return bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫚")
    return bstack11lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ᫛")
def bstack11l1llll11l_opy_(driver):
    info = {
        bstack11lll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᫜"): driver.capabilities,
        bstack11lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ᫝"): driver.session_id,
        bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᫞"): driver.capabilities.get(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᫟"), None),
        bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫠"): driver.capabilities.get(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫡"), None),
        bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᫢"): driver.capabilities.get(bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᫣"), None),
        bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᫤"):driver.capabilities.get(bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫥"), None),
    }
    if bstack11l1lll1l11_opy_() == bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᫦"):
        if bstack1ll1ll11ll_opy_():
            info[bstack11lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᫧")] = bstack11lll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫨")
        elif driver.capabilities.get(bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫩"), {}).get(bstack11lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᫪"), False):
            info[bstack11lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫫")] = bstack11lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᫬")
        else:
            info[bstack11lll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᫭")] = bstack11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫮")
    return info
def bstack1ll1ll11ll_opy_():
    if bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫯")):
        return True
    if bstack1l11lll11l_opy_(os.environ.get(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᫰"), None)):
        return True
    return False
def bstack1lll1ll11l_opy_(bstack11l1l11llll_opy_, url, data, config):
    headers = config.get(bstack11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᫱"), None)
    proxies = bstack1ll111111l_opy_(config, url)
    auth = config.get(bstack11lll_opy_ (u"ࠪࡥࡺࡺࡨࠨ᫲"), None)
    response = requests.request(
            bstack11l1l11llll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll111l1ll_opy_(bstack1l1l1lll11_opy_, size):
    bstack1l11ll1l_opy_ = []
    while len(bstack1l1l1lll11_opy_) > size:
        bstack1lll111l_opy_ = bstack1l1l1lll11_opy_[:size]
        bstack1l11ll1l_opy_.append(bstack1lll111l_opy_)
        bstack1l1l1lll11_opy_ = bstack1l1l1lll11_opy_[size:]
    bstack1l11ll1l_opy_.append(bstack1l1l1lll11_opy_)
    return bstack1l11ll1l_opy_
def bstack11l11ll1ll1_opy_(message, bstack11l1l1l1ll1_opy_=False):
    os.write(1, bytes(message, bstack11lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᫳")))
    os.write(1, bytes(bstack11lll_opy_ (u"ࠬࡢ࡮ࠨ᫴"), bstack11lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᫵")))
    if bstack11l1l1l1ll1_opy_:
        with open(bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᫶") + os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᫷")] + bstack11lll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᫸"), bstack11lll_opy_ (u"ࠪࡥࠬ᫹")) as f:
            f.write(message + bstack11lll_opy_ (u"ࠫࡡࡴࠧ᫺"))
def bstack1l1lllll1l1_opy_():
    return os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᫻")].lower() == bstack11lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᫼")
def bstack11llll11_opy_(bstack11ll1111l1l_opy_):
    return bstack11lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭᫽").format(bstack11ll1l111ll_opy_, bstack11ll1111l1l_opy_)
def bstack11ll11l1ll_opy_():
    return bstack111l1l1ll1_opy_().replace(tzinfo=None).isoformat() + bstack11lll_opy_ (u"ࠨ࡜ࠪ᫾")
def bstack11l1l1ll1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lll_opy_ (u"ࠩ࡝ࠫ᫿"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lll_opy_ (u"ࠪ࡞ࠬᬀ")))).total_seconds() * 1000
def bstack11l1lll1l1l_opy_(timestamp):
    return bstack11l1lll1ll1_opy_(timestamp).isoformat() + bstack11lll_opy_ (u"ࠫ࡟࠭ᬁ")
def bstack11l1lll11l1_opy_(bstack11ll111l111_opy_):
    date_format = bstack11lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᬂ")
    bstack11l1l11111l_opy_ = datetime.datetime.strptime(bstack11ll111l111_opy_, date_format)
    return bstack11l1l11111l_opy_.isoformat() + bstack11lll_opy_ (u"࡚࠭ࠨᬃ")
def bstack11l11lllll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬄ")
    else:
        return bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᬅ")
def bstack1l11lll11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᬆ")
def bstack11l1l111lll_opy_(val):
    return val.__str__().lower() == bstack11lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᬇ")
def bstack111l11l1ll_opy_(bstack11l11lll111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11lll111_opy_ as e:
                print(bstack11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᬈ").format(func.__name__, bstack11l11lll111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l11l11l_opy_(bstack11l1ll1l111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1ll1l111_opy_(cls, *args, **kwargs)
            except bstack11l11lll111_opy_ as e:
                print(bstack11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᬉ").format(bstack11l1ll1l111_opy_.__name__, bstack11l11lll111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l11l11l_opy_
    else:
        return decorator
def bstack1l111l1ll1_opy_(bstack1111ll1ll1_opy_):
    if os.getenv(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᬊ")) is not None:
        return bstack1l11lll11l_opy_(os.getenv(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᬋ")))
    if bstack11lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬌ") in bstack1111ll1ll1_opy_ and bstack11l1l111lll_opy_(bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬍ")]):
        return False
    if bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬎ") in bstack1111ll1ll1_opy_ and bstack11l1l111lll_opy_(bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬏ")]):
        return False
    return True
def bstack1l1111l111_opy_():
    try:
        from pytest_bdd import reporting
        bstack11ll111llll_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᬐ"), None)
        return bstack11ll111llll_opy_ is None or bstack11ll111llll_opy_ == bstack11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᬑ")
    except Exception as e:
        return False
def bstack11l1lllll_opy_(hub_url, CONFIG):
    if bstack1lll1l1l11_opy_() <= version.parse(bstack11lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᬒ")):
        if hub_url:
            return bstack11lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᬓ") + hub_url + bstack11lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᬔ")
        return bstack11l1lll111_opy_
    if hub_url:
        return bstack11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᬕ") + hub_url + bstack11lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᬖ")
    return bstack1lll1111l1_opy_
def bstack11ll11l1ll1_opy_():
    return isinstance(os.getenv(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᬗ")), str)
def bstack1l1l1l1111_opy_(url):
    return urlparse(url).hostname
def bstack11l11ll1l1_opy_(hostname):
    for bstack111ll1l11_opy_ in bstack111llll11_opy_:
        regex = re.compile(bstack111ll1l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1lllll1l_opy_(bstack11l1l1llll1_opy_, file_name, logger):
    bstack111l1111l_opy_ = os.path.join(os.path.expanduser(bstack11lll_opy_ (u"࠭ࡾࠨᬘ")), bstack11l1l1llll1_opy_)
    try:
        if not os.path.exists(bstack111l1111l_opy_):
            os.makedirs(bstack111l1111l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lll_opy_ (u"ࠧࡿࠩᬙ")), bstack11l1l1llll1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lll_opy_ (u"ࠨࡹࠪᬚ")):
                pass
            with open(file_path, bstack11lll_opy_ (u"ࠤࡺ࠯ࠧᬛ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll11111ll_opy_.format(str(e)))
def bstack11l1l1l11ll_opy_(file_name, key, value, logger):
    file_path = bstack11l1lllll1l_opy_(bstack11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬜ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11111lll_opy_ = json.load(open(file_path, bstack11lll_opy_ (u"ࠫࡷࡨࠧᬝ")))
        else:
            bstack1l11111lll_opy_ = {}
        bstack1l11111lll_opy_[key] = value
        with open(file_path, bstack11lll_opy_ (u"ࠧࡽࠫࠣᬞ")) as outfile:
            json.dump(bstack1l11111lll_opy_, outfile)
def bstack11ll11l11_opy_(file_name, logger):
    file_path = bstack11l1lllll1l_opy_(bstack11lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᬟ"), file_name, logger)
    bstack1l11111lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lll_opy_ (u"ࠧࡳࠩᬠ")) as bstack11ll1ll1l_opy_:
            bstack1l11111lll_opy_ = json.load(bstack11ll1ll1l_opy_)
    return bstack1l11111lll_opy_
def bstack11ll1l1ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᬡ") + file_path + bstack11lll_opy_ (u"ࠩࠣࠫᬢ") + str(e))
def bstack1lll1l1l11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᬣ")
def bstack111l11l1l_opy_(config):
    if bstack11lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᬤ") in config:
        del (config[bstack11lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᬥ")])
        return False
    if bstack1lll1l1l11_opy_() < version.parse(bstack11lll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᬦ")):
        return False
    if bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᬧ")):
        return True
    if bstack11lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᬨ") in config and config[bstack11lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᬩ")] is False:
        return False
    else:
        return True
def bstack1ll1ll1lll_opy_(args_list, bstack11l1ll11lll_opy_):
    index = -1
    for value in bstack11l1ll11lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l11111l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l11111l1_opy_ = bstack11l11111l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᬪ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬫ"), exception=exception)
    def bstack1111l1llll_opy_(self):
        if self.result != bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᬬ"):
            return None
        if isinstance(self.exception_type, str) and bstack11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᬭ") in self.exception_type:
            return bstack11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᬮ")
        return bstack11lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᬯ")
    def bstack11ll11l1lll_opy_(self):
        if self.result != bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬰ"):
            return None
        if self.bstack11l11111l1_opy_:
            return self.bstack11l11111l1_opy_
        return bstack11ll111l1ll_opy_(self.exception)
def bstack11ll111l1ll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11l1111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll11ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll1ll1_opy_(config, logger):
    try:
        import playwright
        bstack11l11llllll_opy_ = playwright.__file__
        bstack11l1l1111l1_opy_ = os.path.split(bstack11l11llllll_opy_)
        bstack11l1l1lll11_opy_ = bstack11l1l1111l1_opy_[0] + bstack11lll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ᬱ")
        os.environ[bstack11lll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᬲ")] = bstack1l1lll11_opy_(config)
        with open(bstack11l1l1lll11_opy_, bstack11lll_opy_ (u"ࠬࡸࠧᬳ")) as f:
            bstack1l1l11ll_opy_ = f.read()
            bstack11l1ll1ll1l_opy_ = bstack11lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸ᬴ࠬ")
            bstack11l1lllllll_opy_ = bstack1l1l11ll_opy_.find(bstack11l1ll1ll1l_opy_)
            if bstack11l1lllllll_opy_ == -1:
              process = subprocess.Popen(bstack11lll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᬵ"), shell=True, cwd=bstack11l1l1111l1_opy_[0])
              process.wait()
              bstack11l1ll1llll_opy_ = bstack11lll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᬶ")
              bstack11ll11l1l1l_opy_ = bstack11lll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᬷ")
              bstack11l11ll1lll_opy_ = bstack1l1l11ll_opy_.replace(bstack11l1ll1llll_opy_, bstack11ll11l1l1l_opy_)
              with open(bstack11l1l1lll11_opy_, bstack11lll_opy_ (u"ࠪࡻࠬᬸ")) as f:
                f.write(bstack11l11ll1lll_opy_)
    except Exception as e:
        logger.error(bstack1l11ll1ll1_opy_.format(str(e)))
def bstack111111lll_opy_():
  try:
    bstack11l1llllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᬹ"))
    bstack11l1ll1lll1_opy_ = []
    if os.path.exists(bstack11l1llllll1_opy_):
      with open(bstack11l1llllll1_opy_) as f:
        bstack11l1ll1lll1_opy_ = json.load(f)
      os.remove(bstack11l1llllll1_opy_)
    return bstack11l1ll1lll1_opy_
  except:
    pass
  return []
def bstack1lll1l1l_opy_(bstack1ll11l11ll_opy_):
  try:
    bstack11l1ll1lll1_opy_ = []
    bstack11l1llllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᬺ"))
    if os.path.exists(bstack11l1llllll1_opy_):
      with open(bstack11l1llllll1_opy_) as f:
        bstack11l1ll1lll1_opy_ = json.load(f)
    bstack11l1ll1lll1_opy_.append(bstack1ll11l11ll_opy_)
    with open(bstack11l1llllll1_opy_, bstack11lll_opy_ (u"࠭ࡷࠨᬻ")) as f:
        json.dump(bstack11l1ll1lll1_opy_, f)
  except:
    pass
def bstack1l1ll11ll_opy_(logger, bstack11ll111111l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᬼ"), bstack11lll_opy_ (u"ࠨࠩᬽ"))
    if test_name == bstack11lll_opy_ (u"ࠩࠪᬾ"):
        test_name = threading.current_thread().__dict__.get(bstack11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᬿ"), bstack11lll_opy_ (u"ࠫࠬᭀ"))
    bstack11l1l1l1l1l_opy_ = bstack11lll_opy_ (u"ࠬ࠲ࠠࠨᭁ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll111111l_opy_:
        bstack1111l111l_opy_ = os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᭂ"), bstack11lll_opy_ (u"ࠧ࠱ࠩᭃ"))
        bstack111l1lll_opy_ = {bstack11lll_opy_ (u"ࠨࡰࡤࡱࡪ᭄࠭"): test_name, bstack11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᭅ"): bstack11l1l1l1l1l_opy_, bstack11lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᭆ"): bstack1111l111l_opy_}
        bstack11l1llll1l1_opy_ = []
        bstack11l1ll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᭇ"))
        if os.path.exists(bstack11l1ll1l1l1_opy_):
            with open(bstack11l1ll1l1l1_opy_) as f:
                bstack11l1llll1l1_opy_ = json.load(f)
        bstack11l1llll1l1_opy_.append(bstack111l1lll_opy_)
        with open(bstack11l1ll1l1l1_opy_, bstack11lll_opy_ (u"ࠬࡽࠧᭈ")) as f:
            json.dump(bstack11l1llll1l1_opy_, f)
    else:
        bstack111l1lll_opy_ = {bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᭉ"): test_name, bstack11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᭊ"): bstack11l1l1l1l1l_opy_, bstack11lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᭋ"): str(multiprocessing.current_process().name)}
        if bstack11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᭌ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack111l1lll_opy_)
  except Exception as e:
      logger.warn(bstack11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᭍").format(e))
def bstack1ll111ll1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1llll111_opy_ = []
    bstack111l1lll_opy_ = {bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭎"): test_name, bstack11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᭏"): error_message, bstack11lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᭐"): index}
    bstack11l1ll111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᭑"))
    if os.path.exists(bstack11l1ll111ll_opy_):
        with open(bstack11l1ll111ll_opy_) as f:
            bstack11l1llll111_opy_ = json.load(f)
    bstack11l1llll111_opy_.append(bstack111l1lll_opy_)
    with open(bstack11l1ll111ll_opy_, bstack11lll_opy_ (u"ࠨࡹࠪ᭒")) as f:
        json.dump(bstack11l1llll111_opy_, f)
  except Exception as e:
    logger.warn(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᭓").format(e))
def bstack1ll111l1l_opy_(bstack1ll1l1lll_opy_, name, logger):
  try:
    bstack111l1lll_opy_ = {bstack11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᭔"): name, bstack11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᭕"): bstack1ll1l1lll_opy_, bstack11lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᭖"): str(threading.current_thread()._name)}
    return bstack111l1lll_opy_
  except Exception as e:
    logger.warn(bstack11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ᭗").format(e))
  return
def bstack11l1l1ll11l_opy_():
    return platform.system() == bstack11lll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨ᭘")
def bstack11lll111ll_opy_(bstack11ll1111ll1_opy_, config, logger):
    bstack11ll11l1l11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll1111ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ᭙").format(e))
    return bstack11ll11l1l11_opy_
def bstack11l1l111l11_opy_(bstack11l1ll1111l_opy_, bstack11l1ll1ll11_opy_):
    bstack11l1l1ll1ll_opy_ = version.parse(bstack11l1ll1111l_opy_)
    bstack11l1ll11l1l_opy_ = version.parse(bstack11l1ll1ll11_opy_)
    if bstack11l1l1ll1ll_opy_ > bstack11l1ll11l1l_opy_:
        return 1
    elif bstack11l1l1ll1ll_opy_ < bstack11l1ll11l1l_opy_:
        return -1
    else:
        return 0
def bstack111l1l1ll1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1lll1ll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll11111l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll1ll1l_opy_(options, framework, bstack1l11lll1l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11lll_opy_ (u"ࠩࡪࡩࡹ࠭᭚"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11ll1lll_opy_ = caps.get(bstack11lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭛"))
    bstack11l1l1l11l1_opy_ = True
    bstack11ll1l111_opy_ = os.environ[bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᭜")]
    if bstack11l1l111lll_opy_(caps.get(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ᭝"))) or bstack11l1l111lll_opy_(caps.get(bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭᭞"))):
        bstack11l1l1l11l1_opy_ = False
    if bstack111l11l1l_opy_({bstack11lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ᭟"): bstack11l1l1l11l1_opy_}):
        bstack1l11ll1lll_opy_ = bstack1l11ll1lll_opy_ or {}
        bstack1l11ll1lll_opy_[bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭠")] = bstack11ll11111l1_opy_(framework)
        bstack1l11ll1lll_opy_[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭡")] = bstack1l1lllll1l1_opy_()
        bstack1l11ll1lll_opy_[bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭢")] = bstack11ll1l111_opy_
        bstack1l11ll1lll_opy_[bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭣")] = bstack1l11lll1l_opy_
        if getattr(options, bstack11lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᭤"), None):
            options.set_capability(bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᭥"), bstack1l11ll1lll_opy_)
        else:
            options[bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᭦")] = bstack1l11ll1lll_opy_
    else:
        if getattr(options, bstack11lll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᭧"), None):
            options.set_capability(bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭨"), bstack11ll11111l1_opy_(framework))
            options.set_capability(bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭩"), bstack1l1lllll1l1_opy_())
            options.set_capability(bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭪"), bstack11ll1l111_opy_)
            options.set_capability(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭫"), bstack1l11lll1l_opy_)
        else:
            options[bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑ᭬ࠧ")] = bstack11ll11111l1_opy_(framework)
            options[bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭭")] = bstack1l1lllll1l1_opy_()
            options[bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭮")] = bstack11ll1l111_opy_
            options[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭯")] = bstack1l11lll1l_opy_
    return options
def bstack11l1l11lll1_opy_(bstack11l1l1lllll_opy_, framework):
    bstack1l11lll1l_opy_ = bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ᭰"))
    if bstack11l1l1lllll_opy_ and len(bstack11l1l1lllll_opy_.split(bstack11lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭱"))) > 1:
        ws_url = bstack11l1l1lllll_opy_.split(bstack11lll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᭲"))[0]
        if bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ᭳") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11ll1111lll_opy_ = json.loads(urllib.parse.unquote(bstack11l1l1lllll_opy_.split(bstack11lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭴"))[1]))
            bstack11ll1111lll_opy_ = bstack11ll1111lll_opy_ or {}
            bstack11ll1l111_opy_ = os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᭵")]
            bstack11ll1111lll_opy_[bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭶")] = str(framework) + str(__version__)
            bstack11ll1111lll_opy_[bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭷")] = bstack1l1lllll1l1_opy_()
            bstack11ll1111lll_opy_[bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭸")] = bstack11ll1l111_opy_
            bstack11ll1111lll_opy_[bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭹")] = bstack1l11lll1l_opy_
            bstack11l1l1lllll_opy_ = bstack11l1l1lllll_opy_.split(bstack11lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᭺"))[0] + bstack11lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭻") + urllib.parse.quote(json.dumps(bstack11ll1111lll_opy_))
    return bstack11l1l1lllll_opy_
def bstack11lll11ll1_opy_():
    global bstack11ll111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11ll111l_opy_ = BrowserType.connect
    return bstack11ll111l_opy_
def bstack1l1llll1_opy_(framework_name):
    global bstack11ll1l1ll1_opy_
    bstack11ll1l1ll1_opy_ = framework_name
    return framework_name
def bstack11lll1ll1_opy_(self, *args, **kwargs):
    global bstack11ll111l_opy_
    try:
        global bstack11ll1l1ll1_opy_
        if bstack11lll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ᭼") in kwargs:
            kwargs[bstack11lll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭᭽")] = bstack11l1l11lll1_opy_(
                kwargs.get(bstack11lll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᭾"), None),
                bstack11ll1l1ll1_opy_
            )
    except Exception as e:
        logger.error(bstack11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ᭿").format(str(e)))
    return bstack11ll111l_opy_(self, *args, **kwargs)
def bstack11ll111lll1_opy_(bstack11l1l11ll1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll111111l_opy_(bstack11l1l11ll1l_opy_, bstack11lll_opy_ (u"ࠧࠨᮀ"))
        if proxies and proxies.get(bstack11lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᮁ")):
            parsed_url = urlparse(proxies.get(bstack11lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᮂ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᮃ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᮄ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᮅ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᮆ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1l11l11l_opy_(bstack11l1l11ll1l_opy_):
    bstack11l1l111ll1_opy_ = {
        bstack11ll1ll1111_opy_[bstack11ll11l11ll_opy_]: bstack11l1l11ll1l_opy_[bstack11ll11l11ll_opy_]
        for bstack11ll11l11ll_opy_ in bstack11l1l11ll1l_opy_
        if bstack11ll11l11ll_opy_ in bstack11ll1ll1111_opy_
    }
    bstack11l1l111ll1_opy_[bstack11lll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᮇ")] = bstack11ll111lll1_opy_(bstack11l1l11ll1l_opy_, bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᮈ")))
    bstack11l1lll11ll_opy_ = [element.lower() for element in bstack11ll1l1ll1l_opy_]
    bstack11l1l1l111l_opy_(bstack11l1l111ll1_opy_, bstack11l1lll11ll_opy_)
    return bstack11l1l111ll1_opy_
def bstack11l1l1l111l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11lll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᮉ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l1l1l111l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l1l1l111l_opy_(item, keys)
def bstack1ll111l1ll1_opy_():
    bstack11ll11l111l_opy_ = [os.environ.get(bstack11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥᮊ")), os.path.join(os.path.expanduser(bstack11lll_opy_ (u"ࠤࢁࠦᮋ")), bstack11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᮌ")), os.path.join(bstack11lll_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩᮍ"), bstack11lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᮎ"))]
    for path in bstack11ll11l111l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᮏ") + str(path) + bstack11lll_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥᮐ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11lll_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧᮑ") + str(path) + bstack11lll_opy_ (u"ࠤࠪࠦᮒ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᮓ") + str(path) + bstack11lll_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤᮔ"))
            else:
                logger.debug(bstack11lll_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢᮕ") + str(path) + bstack11lll_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥᮖ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11lll_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧᮗ") + str(path) + bstack11lll_opy_ (u"ࠣࠩ࠱ࠦᮘ"))
            return path
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢᮙ") + str(e) + bstack11lll_opy_ (u"ࠥࠦᮚ"))
    logger.debug(bstack11lll_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣᮛ"))
    return None
@measure(event_name=EVENTS.bstack11ll1llll11_opy_, stage=STAGE.bstack11l111ll_opy_)
def bstack1lllll1lll1_opy_(binary_path, bstack1lllll11ll1_opy_, bs_config):
    logger.debug(bstack11lll_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦᮜ").format(binary_path))
    bstack11ll11ll111_opy_ = bstack11lll_opy_ (u"࠭ࠧᮝ")
    bstack11l1l111111_opy_ = {
        bstack11lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮞ"): __version__,
        bstack11lll_opy_ (u"ࠣࡱࡶࠦᮟ"): platform.system(),
        bstack11lll_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥᮠ"): platform.machine(),
        bstack11lll_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᮡ"): bstack11lll_opy_ (u"ࠫ࠵࠭ᮢ"),
        bstack11lll_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦᮣ"): bstack11lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᮤ")
    }
    bstack11l1l1lll1l_opy_(bstack11l1l111111_opy_)
    try:
        if binary_path:
            bstack11l1l111111_opy_[bstack11lll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮥ")] = subprocess.check_output([binary_path, bstack11lll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᮦ")]).strip().decode(bstack11lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᮧ"))
        response = requests.request(
            bstack11lll_opy_ (u"ࠪࡋࡊ࡚ࠧᮨ"),
            url=bstack11llll11_opy_(bstack11ll1l1lll1_opy_),
            headers=None,
            auth=(bs_config[bstack11lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᮩ")], bs_config[bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᮪")]),
            json=None,
            params=bstack11l1l111111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11lll_opy_ (u"࠭ࡵࡳ࡮᮫ࠪ") in data.keys() and bstack11lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᮬ") in data.keys():
            logger.debug(bstack11lll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤᮭ").format(bstack11l1l111111_opy_[bstack11lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮮ")]))
            if bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭ᮯ") in os.environ:
                logger.debug(bstack11lll_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦ᮰"))
                data[bstack11lll_opy_ (u"ࠬࡻࡲ࡭ࠩ᮱")] = os.environ[bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩ᮲")]
            bstack11ll1111111_opy_ = bstack11l1l1l1111_opy_(data[bstack11lll_opy_ (u"ࠧࡶࡴ࡯ࠫ᮳")], bstack1lllll11ll1_opy_)
            bstack11ll11ll111_opy_ = os.path.join(bstack1lllll11ll1_opy_, bstack11ll1111111_opy_)
            os.chmod(bstack11ll11ll111_opy_, 0o777) # bstack11ll11l11l1_opy_ permission
            return bstack11ll11ll111_opy_
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣ᮴").format(e))
    return binary_path
def bstack11l1l1lll1l_opy_(bstack11l1l111111_opy_):
    try:
        if bstack11lll_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨ᮵") not in bstack11l1l111111_opy_[bstack11lll_opy_ (u"ࠪࡳࡸ࠭᮶")].lower():
            return
        if os.path.exists(bstack11lll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨ᮷")):
            with open(bstack11lll_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ᮸"), bstack11lll_opy_ (u"ࠨࡲࠣ᮹")) as f:
                bstack11l1l11l1ll_opy_ = {}
                for line in f:
                    if bstack11lll_opy_ (u"ࠢ࠾ࠤᮺ") in line:
                        key, value = line.rstrip().split(bstack11lll_opy_ (u"ࠣ࠿ࠥᮻ"), 1)
                        bstack11l1l11l1ll_opy_[key] = value.strip(bstack11lll_opy_ (u"ࠩࠥࡠࠬ࠭ᮼ"))
                bstack11l1l111111_opy_[bstack11lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪᮽ")] = bstack11l1l11l1ll_opy_.get(bstack11lll_opy_ (u"ࠦࡎࡊࠢᮾ"), bstack11lll_opy_ (u"ࠧࠨᮿ"))
        elif os.path.exists(bstack11lll_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᯀ")):
            bstack11l1l111111_opy_[bstack11lll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᯁ")] = bstack11lll_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨᯂ")
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦᯃ") + e)
@measure(event_name=EVENTS.bstack11ll1ll1ll1_opy_, stage=STAGE.bstack11l111ll_opy_)
def bstack11l1l1l1111_opy_(bstack11ll111ll11_opy_, bstack11ll111ll1l_opy_):
    logger.debug(bstack11lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧᯄ") + str(bstack11ll111ll11_opy_) + bstack11lll_opy_ (u"ࠦࠧᯅ"))
    zip_path = os.path.join(bstack11ll111ll1l_opy_, bstack11lll_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦᯆ"))
    bstack11ll1111111_opy_ = bstack11lll_opy_ (u"࠭ࠧᯇ")
    with requests.get(bstack11ll111ll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11lll_opy_ (u"ࠢࡸࡤࠥᯈ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11lll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥᯉ"))
    with zipfile.ZipFile(zip_path, bstack11lll_opy_ (u"ࠩࡵࠫᯊ")) as zip_ref:
        bstack11l1ll111l1_opy_ = zip_ref.namelist()
        if len(bstack11l1ll111l1_opy_) > 0:
            bstack11ll1111111_opy_ = bstack11l1ll111l1_opy_[0] # bstack11ll1111l11_opy_ bstack11ll1l11ll1_opy_ will be bstack11ll111l1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11ll111ll1l_opy_)
        logger.debug(bstack11lll_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤᯋ") + str(bstack11ll111ll1l_opy_) + bstack11lll_opy_ (u"ࠦࠬࠨᯌ"))
    os.remove(zip_path)
    return bstack11ll1111111_opy_
def get_cli_dir():
    bstack11l1lllll11_opy_ = bstack1ll111l1ll1_opy_()
    if bstack11l1lllll11_opy_:
        bstack1lllll11ll1_opy_ = os.path.join(bstack11l1lllll11_opy_, bstack11lll_opy_ (u"ࠧࡩ࡬ࡪࠤᯍ"))
        if not os.path.exists(bstack1lllll11ll1_opy_):
            os.makedirs(bstack1lllll11ll1_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll11ll1_opy_
    else:
        raise FileNotFoundError(bstack11lll_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤᯎ"))
def bstack1lll11lll11_opy_(bstack1lllll11ll1_opy_):
    bstack11lll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦᯏ")
    bstack11l1llll1ll_opy_ = [
        os.path.join(bstack1lllll11ll1_opy_, f)
        for f in os.listdir(bstack1lllll11ll1_opy_)
        if os.path.isfile(os.path.join(bstack1lllll11ll1_opy_, f)) and f.startswith(bstack11lll_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤᯐ"))
    ]
    if len(bstack11l1llll1ll_opy_) > 0:
        return max(bstack11l1llll1ll_opy_, key=os.path.getmtime) # get bstack11l11llll11_opy_ binary
    return bstack11lll_opy_ (u"ࠤࠥᯑ")
def bstack1ll1l11l111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l11l111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d