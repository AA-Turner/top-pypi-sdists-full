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
from bstack_utils.constants import (bstack11ll1l1l1ll_opy_, bstack11l11lll_opy_, bstack1l111l1l1l_opy_, bstack1lll1ll1_opy_,
                                    bstack11ll1lll111_opy_, bstack11ll1l1ll1l_opy_, bstack11ll1l1lll1_opy_, bstack11ll1l111l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l11l1ll_opy_, bstack111ll1lll_opy_
from bstack_utils.proxy import bstack1llll1111l_opy_, bstack1lll1ll111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11111llll_opy_
from browserstack_sdk._version import __version__
bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
logger = bstack11111llll_opy_.get_logger(__name__, bstack11111llll_opy_.bstack1lll1lll111_opy_())
def bstack11lll1ll1l1_opy_(config):
    return config[bstack1l11lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᦧ")]
def bstack11lllll1111_opy_(config):
    return config[bstack1l11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᦨ")]
def bstack11ll1ll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1lll11l1_opy_(obj):
    values = []
    bstack11l1llll1ll_opy_ = re.compile(bstack1l11lll_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᦩ"), re.I)
    for key in obj.keys():
        if bstack11l1llll1ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll111111l_opy_(config):
    tags = []
    tags.extend(bstack11l1lll11l1_opy_(os.environ))
    tags.extend(bstack11l1lll11l1_opy_(config))
    return tags
def bstack11l1ll1l111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll111lll1_opy_(bstack11ll11ll1ll_opy_):
    if not bstack11ll11ll1ll_opy_:
        return bstack1l11lll_opy_ (u"ࠫࠬᦪ")
    return bstack1l11lll_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᦫ").format(bstack11ll11ll1ll_opy_.name, bstack11ll11ll1ll_opy_.email)
def bstack11llll1l1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1llll111_opy_ = repo.common_dir
        info = {
            bstack1l11lll_opy_ (u"ࠨࡳࡩࡣࠥ᦬"): repo.head.commit.hexsha,
            bstack1l11lll_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥ᦭"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l11lll_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣ᦮"): repo.active_branch.name,
            bstack1l11lll_opy_ (u"ࠤࡷࡥ࡬ࠨ᦯"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᦰ"): bstack11ll111lll1_opy_(repo.head.commit.committer),
            bstack1l11lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᦱ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l11lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᦲ"): bstack11ll111lll1_opy_(repo.head.commit.author),
            bstack1l11lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᦳ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l11lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᦴ"): repo.head.commit.message,
            bstack1l11lll_opy_ (u"ࠣࡴࡲࡳࡹࠨᦵ"): repo.git.rev_parse(bstack1l11lll_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᦶ")),
            bstack1l11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᦷ"): bstack11l1llll111_opy_,
            bstack1l11lll_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᦸ"): subprocess.check_output([bstack1l11lll_opy_ (u"ࠧ࡭ࡩࡵࠤᦹ"), bstack1l11lll_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᦺ"), bstack1l11lll_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᦻ")]).strip().decode(
                bstack1l11lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᦼ")),
            bstack1l11lll_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᦽ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᦾ"): repo.git.rev_list(
                bstack1l11lll_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᦿ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11llll1l_opy_ = []
        for remote in remotes:
            bstack11ll1111l1l_opy_ = {
                bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᧀ"): remote.name,
                bstack1l11lll_opy_ (u"ࠨࡵࡳ࡮ࠥᧁ"): remote.url,
            }
            bstack11l11llll1l_opy_.append(bstack11ll1111l1l_opy_)
        bstack11l1ll1111l_opy_ = {
            bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᧂ"): bstack1l11lll_opy_ (u"ࠣࡩ࡬ࡸࠧᧃ"),
            **info,
            bstack1l11lll_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᧄ"): bstack11l11llll1l_opy_
        }
        bstack11l1ll1111l_opy_ = bstack11ll111ll11_opy_(bstack11l1ll1111l_opy_)
        return bstack11l1ll1111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᧅ").format(err))
        return {}
def bstack11ll111ll11_opy_(bstack11l1ll1111l_opy_):
    bstack11l1ll1lll1_opy_ = bstack11ll11ll1l1_opy_(bstack11l1ll1111l_opy_)
    if bstack11l1ll1lll1_opy_ and bstack11l1ll1lll1_opy_ > bstack11ll1lll111_opy_:
        bstack11ll11ll11l_opy_ = bstack11l1ll1lll1_opy_ - bstack11ll1lll111_opy_
        bstack11l11lll111_opy_ = bstack11ll111llll_opy_(bstack11l1ll1111l_opy_[bstack1l11lll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᧆ")], bstack11ll11ll11l_opy_)
        bstack11l1ll1111l_opy_[bstack1l11lll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᧇ")] = bstack11l11lll111_opy_
        logger.info(bstack1l11lll_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣᧈ")
                    .format(bstack11ll11ll1l1_opy_(bstack11l1ll1111l_opy_) / 1024))
    return bstack11l1ll1111l_opy_
def bstack11ll11ll1l1_opy_(bstack1l1111111_opy_):
    try:
        if bstack1l1111111_opy_:
            bstack11l1lll1lll_opy_ = json.dumps(bstack1l1111111_opy_)
            bstack11l11lllll1_opy_ = sys.getsizeof(bstack11l1lll1lll_opy_)
            return bstack11l11lllll1_opy_
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢᧉ").format(e))
    return -1
def bstack11ll111llll_opy_(field, bstack11l1l1l1l11_opy_):
    try:
        bstack11l1l1lll11_opy_ = len(bytes(bstack11ll1l1ll1l_opy_, bstack1l11lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᧊")))
        bstack11l1l1111ll_opy_ = bytes(field, bstack1l11lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᧋"))
        bstack11l1lllllll_opy_ = len(bstack11l1l1111ll_opy_)
        bstack11l1l1l11l1_opy_ = ceil(bstack11l1lllllll_opy_ - bstack11l1l1l1l11_opy_ - bstack11l1l1lll11_opy_)
        if bstack11l1l1l11l1_opy_ > 0:
            bstack11l1l11l11l_opy_ = bstack11l1l1111ll_opy_[:bstack11l1l1l11l1_opy_].decode(bstack1l11lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧌"), errors=bstack1l11lll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ᧍")) + bstack11ll1l1ll1l_opy_
            return bstack11l1l11l11l_opy_
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ᧎").format(e))
    return field
def bstack1lll1ll1ll_opy_():
    env = os.environ
    if (bstack1l11lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᧏") in env and len(env[bstack1l11lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᧐")]) > 0) or (
            bstack1l11lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᧑") in env and len(env[bstack1l11lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᧒")]) > 0):
        return {
            bstack1l11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᧓"): bstack1l11lll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ᧔"),
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᧕"): env.get(bstack1l11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᧖")),
            bstack1l11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧗"): env.get(bstack1l11lll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ᧘")),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧙"): env.get(bstack1l11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᧚"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠦࡈࡏࠢ᧛")) == bstack1l11lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᧜") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ᧝"))):
        return {
            bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧞"): bstack1l11lll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ᧟"),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧠"): env.get(bstack1l11lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᧡")),
            bstack1l11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧢"): env.get(bstack1l11lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ᧣")),
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧤"): env.get(bstack1l11lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ᧥"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠣࡅࡌࠦ᧦")) == bstack1l11lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧧") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ᧨"))):
        return {
            bstack1l11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧩"): bstack1l11lll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᧪"),
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧫"): env.get(bstack1l11lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢ᧬")),
            bstack1l11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧭"): env.get(bstack1l11lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᧮")),
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧯"): env.get(bstack1l11lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᧰"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠧࡉࡉࠣ᧱")) == bstack1l11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧲") and env.get(bstack1l11lll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ᧳")) == bstack1l11lll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᧴"):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧵"): bstack1l11lll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ᧶"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧷"): None,
            bstack1l11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧸"): None,
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧹"): None
        }
    if env.get(bstack1l11lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ᧺")) and env.get(bstack1l11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦ᧻")):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧼"): bstack1l11lll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨ᧽"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧾"): env.get(bstack1l11lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥ᧿")),
            bstack1l11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨀ"): None,
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨁ"): env.get(bstack1l11lll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᨂ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠤࡆࡍࠧᨃ")) == bstack1l11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨄ") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᨅ"))):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨆ"): bstack1l11lll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᨇ"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨈ"): env.get(bstack1l11lll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᨉ")),
            bstack1l11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨊ"): None,
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨋ"): env.get(bstack1l11lll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨌ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠧࡉࡉࠣᨍ")) == bstack1l11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦᨎ") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᨏ"))):
        return {
            bstack1l11lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᨐ"): bstack1l11lll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᨑ"),
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨒ"): env.get(bstack1l11lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᨓ")),
            bstack1l11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨔ"): env.get(bstack1l11lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᨕ")),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨖ"): env.get(bstack1l11lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᨗ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠤࡆࡍᨘࠧ")) == bstack1l11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᨙ") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᨚ"))):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨛ"): bstack1l11lll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ᨜"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᨝"): env.get(bstack1l11lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ᨞")),
            bstack1l11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᨟"): env.get(bstack1l11lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᨠ")),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨡ"): env.get(bstack1l11lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᨢ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠨࡃࡊࠤᨣ")) == bstack1l11lll_opy_ (u"ࠢࡵࡴࡸࡩࠧᨤ") and bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᨥ"))):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨦ"): bstack1l11lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᨧ"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨨ"): env.get(bstack1l11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᨩ")),
            bstack1l11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨪ"): env.get(bstack1l11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᨫ")) or env.get(bstack1l11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᨬ")),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨭ"): env.get(bstack1l11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨮ"))
        }
    if bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᨯ"))):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨰ"): bstack1l11lll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᨱ"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᨲ"): bstack1l11lll_opy_ (u"ࠣࡽࢀࡿࢂࠨᨳ").format(env.get(bstack1l11lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᨴ")), env.get(bstack1l11lll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᨵ"))),
            bstack1l11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨶ"): env.get(bstack1l11lll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᨷ")),
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨸ"): env.get(bstack1l11lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᨹ"))
        }
    if bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᨺ"))):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨻ"): bstack1l11lll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᨼ"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨽ"): bstack1l11lll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᨾ").format(env.get(bstack1l11lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᨿ")), env.get(bstack1l11lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᩀ")), env.get(bstack1l11lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᩁ")), env.get(bstack1l11lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᩂ"))),
            bstack1l11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩃ"): env.get(bstack1l11lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᩄ")),
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩅ"): env.get(bstack1l11lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᩆ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᩇ")) and env.get(bstack1l11lll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᩈ")):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩉ"): bstack1l11lll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᩊ"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩋ"): bstack1l11lll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᩌ").format(env.get(bstack1l11lll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᩍ")), env.get(bstack1l11lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᩎ")), env.get(bstack1l11lll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᩏ"))),
            bstack1l11lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᩐ"): env.get(bstack1l11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᩑ")),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩒ"): env.get(bstack1l11lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩓ"))
        }
    if any([env.get(bstack1l11lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩔ")), env.get(bstack1l11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᩕ")), env.get(bstack1l11lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᩖ"))]):
        return {
            bstack1l11lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩗ"): bstack1l11lll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᩘ"),
            bstack1l11lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩙ"): env.get(bstack1l11lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᩚ")),
            bstack1l11lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩛ"): env.get(bstack1l11lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᩜ")),
            bstack1l11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩝ"): env.get(bstack1l11lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩞ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ᩟")):
        return {
            bstack1l11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩠"): bstack1l11lll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᩡ"),
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩢ"): env.get(bstack1l11lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᩣ")),
            bstack1l11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩤ"): env.get(bstack1l11lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᩥ")),
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩦ"): env.get(bstack1l11lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᩧ"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᩨ")) or env.get(bstack1l11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᩩ")):
        return {
            bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩪ"): bstack1l11lll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᩫ"),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩬ"): env.get(bstack1l11lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᩭ")),
            bstack1l11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩮ"): bstack1l11lll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᩯ") if env.get(bstack1l11lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᩰ")) else None,
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩱ"): env.get(bstack1l11lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᩲ"))
        }
    if any([env.get(bstack1l11lll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᩳ")), env.get(bstack1l11lll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᩴ")), env.get(bstack1l11lll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩵"))]):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᩶"): bstack1l11lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧ᩷"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᩸"): None,
            bstack1l11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): env.get(bstack1l11lll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨ᩺")),
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩻"): env.get(bstack1l11lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᩼"))
        }
    if env.get(bstack1l11lll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣ᩽")):
        return {
            bstack1l11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᩾"): bstack1l11lll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧ᩿ࠥ"),
            bstack1l11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪀"): env.get(bstack1l11lll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᪁")),
            bstack1l11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪂"): bstack1l11lll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧ᪃").format(env.get(bstack1l11lll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨ᪄"))) if env.get(bstack1l11lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤ᪅")) else None,
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪆"): env.get(bstack1l11lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᪇"))
        }
    if bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥ᪈"))):
        return {
            bstack1l11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪉"): bstack1l11lll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧ᪊"),
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪋"): env.get(bstack1l11lll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥ᪌")),
            bstack1l11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪍"): env.get(bstack1l11lll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦ᪎")),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪏"): env.get(bstack1l11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᪐"))
        }
    if bstack11ll1l1l11_opy_(env.get(bstack1l11lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧ᪑"))):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪒"): bstack1l11lll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢ᪓"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪔"): bstack1l11lll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤ᪕").format(env.get(bstack1l11lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭᪖")), env.get(bstack1l11lll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧ᪗")), env.get(bstack1l11lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫ᪘"))),
            bstack1l11lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪙"): env.get(bstack1l11lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣ᪚")),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪛"): env.get(bstack1l11lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣ᪜"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠤࡆࡍࠧ᪝")) == bstack1l11lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᪞") and env.get(bstack1l11lll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦ᪟")) == bstack1l11lll_opy_ (u"ࠧ࠷ࠢ᪠"):
        return {
            bstack1l11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪡"): bstack1l11lll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ᪢"),
            bstack1l11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪣"): bstack1l11lll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ᪤").format(env.get(bstack1l11lll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ᪥"))),
            bstack1l11lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪦"): None,
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᪧ"): None,
        }
    if env.get(bstack1l11lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᪨")):
        return {
            bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪩"): bstack1l11lll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ᪪"),
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪫"): None,
            bstack1l11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪬"): env.get(bstack1l11lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ᪭")),
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪮"): env.get(bstack1l11lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪯"))
        }
    if any([env.get(bstack1l11lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥ᪰")), env.get(bstack1l11lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣ᪱")), env.get(bstack1l11lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢ᪲")), env.get(bstack1l11lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦ᪳"))]):
        return {
            bstack1l11lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪴"): bstack1l11lll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥ᪵ࠣ"),
            bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪶"): None,
            bstack1l11lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪷"): env.get(bstack1l11lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᪸")) or None,
            bstack1l11lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ᪹ࠣ"): env.get(bstack1l11lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈ᪺ࠧ"), 0)
        }
    if env.get(bstack1l11lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᪻")):
        return {
            bstack1l11lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪼"): bstack1l11lll_opy_ (u"ࠨࡇࡰࡅࡇ᪽ࠦ"),
            bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪾"): None,
            bstack1l11lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧᪿࠥ"): env.get(bstack1l11lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋᫀࠢ")),
            bstack1l11lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫁"): env.get(bstack1l11lll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ᫂"))
        }
    if env.get(bstack1l11lll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆ᫃ࠥ")):
        return {
            bstack1l11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᫄ࠦ"): bstack1l11lll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥ᫅"),
            bstack1l11lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫆"): env.get(bstack1l11lll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᫇")),
            bstack1l11lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫈"): env.get(bstack1l11lll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢ᫉")),
            bstack1l11lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᫊ࠦ"): env.get(bstack1l11lll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᫋"))
        }
    return {bstack1l11lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᫌ"): None}
def get_host_info():
    return {
        bstack1l11lll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᫍ"): platform.node(),
        bstack1l11lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᫎ"): platform.system(),
        bstack1l11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᫏"): platform.machine(),
        bstack1l11lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᫐"): platform.version(),
        bstack1l11lll_opy_ (u"ࠧࡧࡲࡤࡪࠥ᫑"): platform.architecture()[0]
    }
def bstack111l11l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1lll1111_opy_():
    if bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ᫒")):
        return bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫓")
    return bstack1l11lll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧ᫔")
def bstack11l1ll11ll1_opy_(driver):
    info = {
        bstack1l11lll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᫕"): driver.capabilities,
        bstack1l11lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧ᫖"): driver.session_id,
        bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᫗"): driver.capabilities.get(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᫘"), None),
        bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫙"): driver.capabilities.get(bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫚"), None),
        bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᫛"): driver.capabilities.get(bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᫜"), None),
        bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᫝"):driver.capabilities.get(bstack1l11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫞"), None),
    }
    if bstack11l1lll1111_opy_() == bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᫟"):
        if bstack11ll11l1l_opy_():
            info[bstack1l11lll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ᫠")] = bstack1l11lll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫡")
        elif driver.capabilities.get(bstack1l11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫢"), {}).get(bstack1l11lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭᫣"), False):
            info[bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫤")] = bstack1l11lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᫥")
        else:
            info[bstack1l11lll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᫦")] = bstack1l11lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫧")
    return info
def bstack11ll11l1l_opy_():
    if bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᫨")):
        return True
    if bstack11ll1l1l11_opy_(os.environ.get(bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᫩"), None)):
        return True
    return False
def bstack1l1lll11l_opy_(bstack11ll11l1l11_opy_, url, data, config):
    headers = config.get(bstack1l11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᫪"), None)
    proxies = bstack1llll1111l_opy_(config, url)
    auth = config.get(bstack1l11lll_opy_ (u"ࠪࡥࡺࡺࡨࠨ᫫"), None)
    response = requests.request(
            bstack11ll11l1l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll11ll_opy_(bstack1l1l11l1l1_opy_, size):
    bstack1l11l1l11_opy_ = []
    while len(bstack1l1l11l1l1_opy_) > size:
        bstack111lll11l_opy_ = bstack1l1l11l1l1_opy_[:size]
        bstack1l11l1l11_opy_.append(bstack111lll11l_opy_)
        bstack1l1l11l1l1_opy_ = bstack1l1l11l1l1_opy_[size:]
    bstack1l11l1l11_opy_.append(bstack1l1l11l1l1_opy_)
    return bstack1l11l1l11_opy_
def bstack11l1l1l111l_opy_(message, bstack11ll1111lll_opy_=False):
    os.write(1, bytes(message, bstack1l11lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᫬")))
    os.write(1, bytes(bstack1l11lll_opy_ (u"ࠬࡢ࡮ࠨ᫭"), bstack1l11lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᫮")))
    if bstack11ll1111lll_opy_:
        with open(bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᫯") + os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᫰")] + bstack1l11lll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᫱"), bstack1l11lll_opy_ (u"ࠪࡥࠬ᫲")) as f:
            f.write(message + bstack1l11lll_opy_ (u"ࠫࡡࡴࠧ᫳"))
def bstack1l1ll1lllll_opy_():
    return os.environ[bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᫴")].lower() == bstack1l11lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᫵")
def bstack1111l111_opy_(bstack11l1ll11111_opy_):
    return bstack1l11lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭᫶").format(bstack11ll1l1l1ll_opy_, bstack11l1ll11111_opy_)
def bstack11lll111l1_opy_():
    return bstack111l1lll1l_opy_().replace(tzinfo=None).isoformat() + bstack1l11lll_opy_ (u"ࠨ࡜ࠪ᫷")
def bstack11l1l11111l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l11lll_opy_ (u"ࠩ࡝ࠫ᫸"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l11lll_opy_ (u"ࠪ࡞ࠬ᫹")))).total_seconds() * 1000
def bstack11l1l1111l1_opy_(timestamp):
    return bstack11l1l1ll1ll_opy_(timestamp).isoformat() + bstack1l11lll_opy_ (u"ࠫ࡟࠭᫺")
def bstack11l1l1ll11l_opy_(bstack11l1ll111ll_opy_):
    date_format = bstack1l11lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ᫻")
    bstack11ll11111ll_opy_ = datetime.datetime.strptime(bstack11l1ll111ll_opy_, date_format)
    return bstack11ll11111ll_opy_.isoformat() + bstack1l11lll_opy_ (u"࡚࠭ࠨ᫼")
def bstack11l1l11llll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᫽")
    else:
        return bstack1l11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᫾")
def bstack11ll1l1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᫿")
def bstack11l1ll1l11l_opy_(val):
    return val.__str__().lower() == bstack1l11lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᬀ")
def bstack111l1ll1ll_opy_(bstack11l1lllll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1lllll11_opy_ as e:
                print(bstack1l11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᬁ").format(func.__name__, bstack11l1lllll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll1111ll1_opy_(bstack11l11lll1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11lll1ll_opy_(cls, *args, **kwargs)
            except bstack11l1lllll11_opy_ as e:
                print(bstack1l11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᬂ").format(bstack11l11lll1ll_opy_.__name__, bstack11l1lllll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll1111ll1_opy_
    else:
        return decorator
def bstack1l11l1l1l_opy_(bstack1111ll1lll_opy_):
    if os.getenv(bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᬃ")) is not None:
        return bstack11ll1l1l11_opy_(os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᬄ")))
    if bstack1l11lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬅ") in bstack1111ll1lll_opy_ and bstack11l1ll1l11l_opy_(bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬆ")]):
        return False
    if bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬇ") in bstack1111ll1lll_opy_ and bstack11l1ll1l11l_opy_(bstack1111ll1lll_opy_[bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬈ")]):
        return False
    return True
def bstack11llllll1l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l1l1111_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᬉ"), None)
        return bstack11l1l1l1111_opy_ is None or bstack11l1l1l1111_opy_ == bstack1l11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᬊ")
    except Exception as e:
        return False
def bstack1ll1llll_opy_(hub_url, CONFIG):
    if bstack11l11lllll_opy_() <= version.parse(bstack1l11lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᬋ")):
        if hub_url:
            return bstack1l11lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᬌ") + hub_url + bstack1l11lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᬍ")
        return bstack1l111l1l1l_opy_
    if hub_url:
        return bstack1l11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᬎ") + hub_url + bstack1l11lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᬏ")
    return bstack1lll1ll1_opy_
def bstack11l1ll1l1l1_opy_():
    return isinstance(os.getenv(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᬐ")), str)
def bstack11l1l1l11l_opy_(url):
    return urlparse(url).hostname
def bstack11l1lll1l1_opy_(hostname):
    for bstack1l1l111l1_opy_ in bstack11l11lll_opy_:
        regex = re.compile(bstack1l1l111l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l1l1l1l_opy_(bstack11l1ll11l1l_opy_, file_name, logger):
    bstack1l1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack1l11lll_opy_ (u"࠭ࡾࠨᬑ")), bstack11l1ll11l1l_opy_)
    try:
        if not os.path.exists(bstack1l1l1l1lll_opy_):
            os.makedirs(bstack1l1l1l1lll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l11lll_opy_ (u"ࠧࡿࠩᬒ")), bstack11l1ll11l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l11lll_opy_ (u"ࠨࡹࠪᬓ")):
                pass
            with open(file_path, bstack1l11lll_opy_ (u"ࠤࡺ࠯ࠧᬔ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l11l1ll_opy_.format(str(e)))
def bstack11l1l11l111_opy_(file_name, key, value, logger):
    file_path = bstack11l1l1l1l1l_opy_(bstack1l11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬕ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111l1l11_opy_ = json.load(open(file_path, bstack1l11lll_opy_ (u"ࠫࡷࡨࠧᬖ")))
        else:
            bstack1111l1l11_opy_ = {}
        bstack1111l1l11_opy_[key] = value
        with open(file_path, bstack1l11lll_opy_ (u"ࠧࡽࠫࠣᬗ")) as outfile:
            json.dump(bstack1111l1l11_opy_, outfile)
def bstack1lll111l1l_opy_(file_name, logger):
    file_path = bstack11l1l1l1l1l_opy_(bstack1l11lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᬘ"), file_name, logger)
    bstack1111l1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l11lll_opy_ (u"ࠧࡳࠩᬙ")) as bstack1l111l1l_opy_:
            bstack1111l1l11_opy_ = json.load(bstack1l111l1l_opy_)
    return bstack1111l1l11_opy_
def bstack1111llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬᬚ") + file_path + bstack1l11lll_opy_ (u"ࠩࠣࠫᬛ") + str(e))
def bstack11l11lllll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l11lll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᬜ")
def bstack11l1lll1_opy_(config):
    if bstack1l11lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᬝ") in config:
        del (config[bstack1l11lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᬞ")])
        return False
    if bstack11l11lllll_opy_() < version.parse(bstack1l11lll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᬟ")):
        return False
    if bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᬠ")):
        return True
    if bstack1l11lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᬡ") in config and config[bstack1l11lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᬢ")] is False:
        return False
    else:
        return True
def bstack11lll1ll_opy_(args_list, bstack11l11lll1l1_opy_):
    index = -1
    for value in bstack11l11lll1l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l1111ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l1111ll1_opy_ = bstack11l1111ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᬣ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬤ"), exception=exception)
    def bstack1111l1llll_opy_(self):
        if self.result != bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᬥ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᬦ") in self.exception_type:
            return bstack1l11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᬧ")
        return bstack1l11lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᬨ")
    def bstack11l1l1ll111_opy_(self):
        if self.result != bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬩ"):
            return None
        if self.bstack11l1111ll1_opy_:
            return self.bstack11l1111ll1_opy_
        return bstack11l1l1l1ll1_opy_(self.exception)
def bstack11l1l1l1ll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l1ll1l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l11l1ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11ll1lll_opy_(config, logger):
    try:
        import playwright
        bstack11l1l111ll1_opy_ = playwright.__file__
        bstack11l1ll1ll1l_opy_ = os.path.split(bstack11l1l111ll1_opy_)
        bstack11l1lll1ll1_opy_ = bstack11l1ll1ll1l_opy_[0] + bstack1l11lll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ᬪ")
        os.environ[bstack1l11lll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧᬫ")] = bstack1lll1ll111_opy_(config)
        with open(bstack11l1lll1ll1_opy_, bstack1l11lll_opy_ (u"ࠬࡸࠧᬬ")) as f:
            bstack1111l1l1_opy_ = f.read()
            bstack11l1l11ll11_opy_ = bstack1l11lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬᬭ")
            bstack11ll11l11ll_opy_ = bstack1111l1l1_opy_.find(bstack11l1l11ll11_opy_)
            if bstack11ll11l11ll_opy_ == -1:
              process = subprocess.Popen(bstack1l11lll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦᬮ"), shell=True, cwd=bstack11l1ll1ll1l_opy_[0])
              process.wait()
              bstack11l1lll1l11_opy_ = bstack1l11lll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨᬯ")
              bstack11l1l1l11ll_opy_ = bstack1l11lll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨᬰ")
              bstack11l11llll11_opy_ = bstack1111l1l1_opy_.replace(bstack11l1lll1l11_opy_, bstack11l1l1l11ll_opy_)
              with open(bstack11l1lll1ll1_opy_, bstack1l11lll_opy_ (u"ࠪࡻࠬᬱ")) as f:
                f.write(bstack11l11llll11_opy_)
    except Exception as e:
        logger.error(bstack111ll1lll_opy_.format(str(e)))
def bstack1l11ll11l1_opy_():
  try:
    bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᬲ"))
    bstack11l1l111111_opy_ = []
    if os.path.exists(bstack11l1l111lll_opy_):
      with open(bstack11l1l111lll_opy_) as f:
        bstack11l1l111111_opy_ = json.load(f)
      os.remove(bstack11l1l111lll_opy_)
    return bstack11l1l111111_opy_
  except:
    pass
  return []
def bstack1l1111l11_opy_(bstack11l11llll_opy_):
  try:
    bstack11l1l111111_opy_ = []
    bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬᬳ"))
    if os.path.exists(bstack11l1l111lll_opy_):
      with open(bstack11l1l111lll_opy_) as f:
        bstack11l1l111111_opy_ = json.load(f)
    bstack11l1l111111_opy_.append(bstack11l11llll_opy_)
    with open(bstack11l1l111lll_opy_, bstack1l11lll_opy_ (u"࠭ࡷࠨ᬴")) as f:
        json.dump(bstack11l1l111111_opy_, f)
  except:
    pass
def bstack11lll1l1_opy_(logger, bstack11l1l11l1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l11lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᬵ"), bstack1l11lll_opy_ (u"ࠨࠩᬶ"))
    if test_name == bstack1l11lll_opy_ (u"ࠩࠪᬷ"):
        test_name = threading.current_thread().__dict__.get(bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᬸ"), bstack1l11lll_opy_ (u"ࠫࠬᬹ"))
    bstack11l1l11l1l1_opy_ = bstack1l11lll_opy_ (u"ࠬ࠲ࠠࠨᬺ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1l11l1ll_opy_:
        bstack111l111l_opy_ = os.environ.get(bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᬻ"), bstack1l11lll_opy_ (u"ࠧ࠱ࠩᬼ"))
        bstack1l1l1111l_opy_ = {bstack1l11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᬽ"): test_name, bstack1l11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᬾ"): bstack11l1l11l1l1_opy_, bstack1l11lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᬿ"): bstack111l111l_opy_}
        bstack11l11lll11l_opy_ = []
        bstack11l1llllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᭀ"))
        if os.path.exists(bstack11l1llllll1_opy_):
            with open(bstack11l1llllll1_opy_) as f:
                bstack11l11lll11l_opy_ = json.load(f)
        bstack11l11lll11l_opy_.append(bstack1l1l1111l_opy_)
        with open(bstack11l1llllll1_opy_, bstack1l11lll_opy_ (u"ࠬࡽࠧᭁ")) as f:
            json.dump(bstack11l11lll11l_opy_, f)
    else:
        bstack1l1l1111l_opy_ = {bstack1l11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᭂ"): test_name, bstack1l11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᭃ"): bstack11l1l11l1l1_opy_, bstack1l11lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾ᭄ࠧ"): str(multiprocessing.current_process().name)}
        if bstack1l11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭ᭅ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1111l_opy_)
  except Exception as e:
      logger.warn(bstack1l11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᭆ").format(e))
def bstack1l1l1ll1l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11ll11ll111_opy_ = []
    bstack1l1l1111l_opy_ = {bstack1l11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᭇ"): test_name, bstack1l11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᭈ"): error_message, bstack1l11lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᭉ"): index}
    bstack11ll111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᭊ"))
    if os.path.exists(bstack11ll111l11l_opy_):
        with open(bstack11ll111l11l_opy_) as f:
            bstack11ll11ll111_opy_ = json.load(f)
    bstack11ll11ll111_opy_.append(bstack1l1l1111l_opy_)
    with open(bstack11ll111l11l_opy_, bstack1l11lll_opy_ (u"ࠨࡹࠪᭋ")) as f:
        json.dump(bstack11ll11ll111_opy_, f)
  except Exception as e:
    logger.warn(bstack1l11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᭌ").format(e))
def bstack11l1111l_opy_(bstack111l1l1ll_opy_, name, logger):
  try:
    bstack1l1l1111l_opy_ = {bstack1l11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᭍"): name, bstack1l11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᭎"): bstack111l1l1ll_opy_, bstack1l11lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᭏"): str(threading.current_thread()._name)}
    return bstack1l1l1111l_opy_
  except Exception as e:
    logger.warn(bstack1l11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ᭐").format(e))
  return
def bstack11ll1111111_opy_():
    return platform.system() == bstack1l11lll_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨ᭑")
def bstack1l1111l1l1_opy_(bstack11ll11l11l1_opy_, config, logger):
    bstack11l1ll1l1ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll11l11l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ᭒").format(e))
    return bstack11l1ll1l1ll_opy_
def bstack11l1lll11ll_opy_(bstack11ll11l111l_opy_, bstack11ll11l1l1l_opy_):
    bstack11ll1111l11_opy_ = version.parse(bstack11ll11l111l_opy_)
    bstack11ll111l1l1_opy_ = version.parse(bstack11ll11l1l1l_opy_)
    if bstack11ll1111l11_opy_ > bstack11ll111l1l1_opy_:
        return 1
    elif bstack11ll1111l11_opy_ < bstack11ll111l1l1_opy_:
        return -1
    else:
        return 0
def bstack111l1lll1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1ll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll111ll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l11lll11_opy_(options, framework, bstack1ll1111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l11lll_opy_ (u"ࠩࡪࡩࡹ࠭᭓"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1llllll1l_opy_ = caps.get(bstack1l11lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭔"))
    bstack11l1l1llll1_opy_ = True
    bstack11111lll_opy_ = os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᭕")]
    if bstack11l1ll1l11l_opy_(caps.get(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫ᭖"))) or bstack11l1ll1l11l_opy_(caps.get(bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭᭗"))):
        bstack11l1l1llll1_opy_ = False
    if bstack11l1lll1_opy_({bstack1l11lll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ᭘"): bstack11l1l1llll1_opy_}):
        bstack1llllll1l_opy_ = bstack1llllll1l_opy_ or {}
        bstack1llllll1l_opy_[bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭙")] = bstack11ll111ll1l_opy_(framework)
        bstack1llllll1l_opy_[bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭚")] = bstack1l1ll1lllll_opy_()
        bstack1llllll1l_opy_[bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭛")] = bstack11111lll_opy_
        bstack1llllll1l_opy_[bstack1l11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭜")] = bstack1ll1111l_opy_
        if getattr(options, bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᭝"), None):
            options.set_capability(bstack1l11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᭞"), bstack1llllll1l_opy_)
        else:
            options[bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᭟")] = bstack1llllll1l_opy_
    else:
        if getattr(options, bstack1l11lll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᭠"), None):
            options.set_capability(bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭡"), bstack11ll111ll1l_opy_(framework))
            options.set_capability(bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭢"), bstack1l1ll1lllll_opy_())
            options.set_capability(bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭣"), bstack11111lll_opy_)
            options.set_capability(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭤"), bstack1ll1111l_opy_)
        else:
            options[bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭥")] = bstack11ll111ll1l_opy_(framework)
            options[bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭦")] = bstack1l1ll1lllll_opy_()
            options[bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭧")] = bstack11111lll_opy_
            options[bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭨")] = bstack1ll1111l_opy_
    return options
def bstack11ll11111l1_opy_(bstack11ll11l1lll_opy_, framework):
    bstack1ll1111l_opy_ = bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧ᭩"))
    if bstack11ll11l1lll_opy_ and len(bstack11ll11l1lll_opy_.split(bstack1l11lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭪"))) > 1:
        ws_url = bstack11ll11l1lll_opy_.split(bstack1l11lll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᭫"))[0]
        if bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮᭬ࠩ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11llllll_opy_ = json.loads(urllib.parse.unquote(bstack11ll11l1lll_opy_.split(bstack1l11lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭭"))[1]))
            bstack11l11llllll_opy_ = bstack11l11llllll_opy_ or {}
            bstack11111lll_opy_ = os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᭮")]
            bstack11l11llllll_opy_[bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ᭯")] = str(framework) + str(__version__)
            bstack11l11llllll_opy_[bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᭰")] = bstack1l1ll1lllll_opy_()
            bstack11l11llllll_opy_[bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭᭱")] = bstack11111lll_opy_
            bstack11l11llllll_opy_[bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭᭲")] = bstack1ll1111l_opy_
            bstack11ll11l1lll_opy_ = bstack11ll11l1lll_opy_.split(bstack1l11lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᭳"))[0] + bstack1l11lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭴") + urllib.parse.quote(json.dumps(bstack11l11llllll_opy_))
    return bstack11ll11l1lll_opy_
def bstack11l1l111l1_opy_():
    global bstack11l11ll111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l11ll111_opy_ = BrowserType.connect
    return bstack11l11ll111_opy_
def bstack11ll11ll11_opy_(framework_name):
    global bstack1ll1111ll_opy_
    bstack1ll1111ll_opy_ = framework_name
    return framework_name
def bstack11l1llllll_opy_(self, *args, **kwargs):
    global bstack11l11ll111_opy_
    try:
        global bstack1ll1111ll_opy_
        if bstack1l11lll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ᭵") in kwargs:
            kwargs[bstack1l11lll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭᭶")] = bstack11ll11111l1_opy_(
                kwargs.get(bstack1l11lll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᭷"), None),
                bstack1ll1111ll_opy_
            )
    except Exception as e:
        logger.error(bstack1l11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦ᭸").format(str(e)))
    return bstack11l11ll111_opy_(self, *args, **kwargs)
def bstack11l1ll1llll_opy_(bstack11ll11l1111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1llll1111l_opy_(bstack11ll11l1111_opy_, bstack1l11lll_opy_ (u"ࠧࠨ᭹"))
        if proxies and proxies.get(bstack1l11lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ᭺")):
            parsed_url = urlparse(proxies.get(bstack1l11lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ᭻")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l11lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫ᭼")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l11lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ᭽")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭᭾")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧ᭿")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1llll1ll_opy_(bstack11ll11l1111_opy_):
    bstack11l1l1lllll_opy_ = {
        bstack11ll1l111l1_opy_[bstack11ll111l1ll_opy_]: bstack11ll11l1111_opy_[bstack11ll111l1ll_opy_]
        for bstack11ll111l1ll_opy_ in bstack11ll11l1111_opy_
        if bstack11ll111l1ll_opy_ in bstack11ll1l111l1_opy_
    }
    bstack11l1l1lllll_opy_[bstack1l11lll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᮀ")] = bstack11l1ll1llll_opy_(bstack11ll11l1111_opy_, bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᮁ")))
    bstack11l1llll1l1_opy_ = [element.lower() for element in bstack11ll1l1lll1_opy_]
    bstack11ll11l1ll1_opy_(bstack11l1l1lllll_opy_, bstack11l1llll1l1_opy_)
    return bstack11l1l1lllll_opy_
def bstack11ll11l1ll1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l11lll_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᮂ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll11l1ll1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll11l1ll1_opy_(item, keys)
def bstack1l1llll1lll_opy_():
    bstack11l1lllll1l_opy_ = [os.environ.get(bstack1l11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥᮃ")), os.path.join(os.path.expanduser(bstack1l11lll_opy_ (u"ࠤࢁࠦᮄ")), bstack1l11lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᮅ")), os.path.join(bstack1l11lll_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩᮆ"), bstack1l11lll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᮇ"))]
    for path in bstack11l1lllll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l11lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᮈ") + str(path) + bstack1l11lll_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥᮉ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l11lll_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧᮊ") + str(path) + bstack1l11lll_opy_ (u"ࠤࠪࠦᮋ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l11lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᮌ") + str(path) + bstack1l11lll_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤᮍ"))
            else:
                logger.debug(bstack1l11lll_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢᮎ") + str(path) + bstack1l11lll_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥᮏ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l11lll_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧᮐ") + str(path) + bstack1l11lll_opy_ (u"ࠣࠩ࠱ࠦᮑ"))
            return path
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢᮒ") + str(e) + bstack1l11lll_opy_ (u"ࠥࠦᮓ"))
    logger.debug(bstack1l11lll_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣᮔ"))
    return None
@measure(event_name=EVENTS.bstack11ll1l1l11l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack1llll11111l_opy_(binary_path, bstack1lllll1lll1_opy_, bs_config):
    logger.debug(bstack1l11lll_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦᮕ").format(binary_path))
    bstack11l1l1lll1l_opy_ = bstack1l11lll_opy_ (u"࠭ࠧᮖ")
    bstack11ll111l111_opy_ = {
        bstack1l11lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮗ"): __version__,
        bstack1l11lll_opy_ (u"ࠣࡱࡶࠦᮘ"): platform.system(),
        bstack1l11lll_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥᮙ"): platform.machine(),
        bstack1l11lll_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᮚ"): bstack1l11lll_opy_ (u"ࠫ࠵࠭ᮛ"),
        bstack1l11lll_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦᮜ"): bstack1l11lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᮝ")
    }
    bstack11l1ll11l11_opy_(bstack11ll111l111_opy_)
    try:
        if binary_path:
            bstack11ll111l111_opy_[bstack1l11lll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᮞ")] = subprocess.check_output([binary_path, bstack1l11lll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᮟ")]).strip().decode(bstack1l11lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᮠ"))
        response = requests.request(
            bstack1l11lll_opy_ (u"ࠪࡋࡊ࡚ࠧᮡ"),
            url=bstack1111l111_opy_(bstack11ll1l11l1l_opy_),
            headers=None,
            auth=(bs_config[bstack1l11lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᮢ")], bs_config[bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᮣ")]),
            json=None,
            params=bstack11ll111l111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l11lll_opy_ (u"࠭ࡵࡳ࡮ࠪᮤ") in data.keys() and bstack1l11lll_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᮥ") in data.keys():
            logger.debug(bstack1l11lll_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤᮦ").format(bstack11ll111l111_opy_[bstack1l11lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮧ")]))
            bstack11l1ll11lll_opy_ = bstack11l1l1l1lll_opy_(data[bstack1l11lll_opy_ (u"ࠪࡹࡷࡲࠧᮨ")], bstack1lllll1lll1_opy_)
            bstack11l1l1lll1l_opy_ = os.path.join(bstack1lllll1lll1_opy_, bstack11l1ll11lll_opy_)
            os.chmod(bstack11l1l1lll1l_opy_, 0o777) # bstack11l1llll11l_opy_ permission
            return bstack11l1l1lll1l_opy_
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦᮩ").format(e))
    return binary_path
def bstack11l1ll11l11_opy_(bstack11ll111l111_opy_):
    try:
        if bstack1l11lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻ᮪ࠫ") not in bstack11ll111l111_opy_[bstack1l11lll_opy_ (u"࠭࡯ࡴ᮫ࠩ")].lower():
            return
        if os.path.exists(bstack1l11lll_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᮬ")):
            with open(bstack1l11lll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᮭ"), bstack1l11lll_opy_ (u"ࠤࡵࠦᮮ")) as f:
                bstack11l1lll1l1l_opy_ = {}
                for line in f:
                    if bstack1l11lll_opy_ (u"ࠥࡁࠧᮯ") in line:
                        key, value = line.rstrip().split(bstack1l11lll_opy_ (u"ࠦࡂࠨ᮰"), 1)
                        bstack11l1lll1l1l_opy_[key] = value.strip(bstack1l11lll_opy_ (u"ࠬࠨ࡜ࠨࠩ᮱"))
                bstack11ll111l111_opy_[bstack1l11lll_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭᮲")] = bstack11l1lll1l1l_opy_.get(bstack1l11lll_opy_ (u"ࠢࡊࡆࠥ᮳"), bstack1l11lll_opy_ (u"ࠣࠤ᮴"))
        elif os.path.exists(bstack1l11lll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ᮵")):
            bstack11ll111l111_opy_[bstack1l11lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪ᮶")] = bstack1l11lll_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫ᮷")
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢ᮸") + e)
@measure(event_name=EVENTS.bstack11ll1ll111l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
def bstack11l1l1l1lll_opy_(bstack11l1lll111l_opy_, bstack11l1l11lll1_opy_):
    logger.debug(bstack1l11lll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣ᮹") + str(bstack11l1lll111l_opy_) + bstack1l11lll_opy_ (u"ࠢࠣᮺ"))
    zip_path = os.path.join(bstack11l1l11lll1_opy_, bstack1l11lll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢᮻ"))
    bstack11l1ll11lll_opy_ = bstack1l11lll_opy_ (u"ࠩࠪᮼ")
    with requests.get(bstack11l1lll111l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l11lll_opy_ (u"ࠥࡻࡧࠨᮽ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l11lll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨᮾ"))
    with zipfile.ZipFile(zip_path, bstack1l11lll_opy_ (u"ࠬࡸࠧᮿ")) as zip_ref:
        bstack11ll11lll11_opy_ = zip_ref.namelist()
        if len(bstack11ll11lll11_opy_) > 0:
            bstack11l1ll11lll_opy_ = bstack11ll11lll11_opy_[0] # bstack11l1ll111l1_opy_ bstack11ll1l1llll_opy_ will be bstack11l1l11ll1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1l11lll1_opy_)
        logger.debug(bstack1l11lll_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧᯀ") + str(bstack11l1l11lll1_opy_) + bstack1l11lll_opy_ (u"ࠢࠨࠤᯁ"))
    os.remove(zip_path)
    return bstack11l1ll11lll_opy_
def get_cli_dir():
    bstack11l1ll1ll11_opy_ = bstack1l1llll1lll_opy_()
    if bstack11l1ll1ll11_opy_:
        bstack1lllll1lll1_opy_ = os.path.join(bstack11l1ll1ll11_opy_, bstack1l11lll_opy_ (u"ࠣࡥ࡯࡭ࠧᯂ"))
        if not os.path.exists(bstack1lllll1lll1_opy_):
            os.makedirs(bstack1lllll1lll1_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll1lll1_opy_
    else:
        raise FileNotFoundError(bstack1l11lll_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧᯃ"))
def bstack1lll11lll11_opy_(bstack1lllll1lll1_opy_):
    bstack1l11lll_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢᯄ")
    bstack11l1l111l1l_opy_ = [
        os.path.join(bstack1lllll1lll1_opy_, f)
        for f in os.listdir(bstack1lllll1lll1_opy_)
        if os.path.isfile(os.path.join(bstack1lllll1lll1_opy_, f)) and f.startswith(bstack1l11lll_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧᯅ"))
    ]
    if len(bstack11l1l111l1l_opy_) > 0:
        return max(bstack11l1l111l1l_opy_, key=os.path.getmtime) # get bstack11l1l111l11_opy_ binary
    return bstack1l11lll_opy_ (u"ࠧࠨᯆ")
def bstack1ll1l1l1l1l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1l1l1l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d