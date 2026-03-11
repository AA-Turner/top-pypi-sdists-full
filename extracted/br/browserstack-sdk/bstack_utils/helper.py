# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
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
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l11llll11_opy_, bstack11l11l11l1_opy_, HTTPS_HUB,
                                    bstack111l1l111ll_opy_, bstack111l1ll1lll_opy_, bstack111llll1111_opy_, bstack111ll111111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l11l1l1_opy_, bstack11l11l1l_opy_
from bstack_utils.proxy import bstack111lllllll_opy_, bstack11lll11l_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11l11ll11_opy_ import bstack1lll1l11_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l111l_opy_())
bstack1l11llll_opy_ = logger_utils.bstack1111l1ll1_opy_(__name__)
def bstack11l111111ll_opy_(config):
    return config[bstack1ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᦎ")]
def bstack111llll11l1_opy_(config):
    return config[bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᦏ")]
def bstack1l1l111l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def is_robot_playwright_installed():
    try:
        import Browser
        return True
    except ImportError:
        return False
def bstack111l1ll11l1_opy_(obj):
    values = []
    bstack111l1lllll1_opy_ = re.compile(bstack1ll111_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᦐ"), re.I)
    for key in obj.keys():
        if bstack111l1lllll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1ll1l1l_opy_(config):
    tags = []
    tags.extend(bstack111l1ll11l1_opy_(os.environ))
    tags.extend(bstack111l1ll11l1_opy_(config))
    return tags
def bstack111l111ll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111ll11l1ll_opy_(bstack111l1l111l1_opy_):
    if not bstack111l1l111l1_opy_:
        return bstack1ll111_opy_ (u"ࠧࠨᦑ")
    return bstack1ll111_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᦒ").format(bstack111l1l111l1_opy_.name, bstack111l1l111l1_opy_.email)
def bstack111l1l1111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111ll111l11_opy_ = repo.common_dir
        info = {
            bstack1ll111_opy_ (u"ࠤࡶ࡬ࡦࠨᦓ"): repo.head.commit.hexsha,
            bstack1ll111_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᦔ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll111_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᦕ"): repo.active_branch.name,
            bstack1ll111_opy_ (u"ࠧࡺࡡࡨࠤᦖ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᦗ"): bstack111ll11l1ll_opy_(repo.head.commit.committer),
            bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᦘ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᦙ"): bstack111ll11l1ll_opy_(repo.head.commit.author),
            bstack1ll111_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᦚ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᦛ"): repo.head.commit.message,
            bstack1ll111_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᦜ"): repo.git.rev_parse(bstack1ll111_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᦝ")),
            bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᦞ"): bstack111ll111l11_opy_,
            bstack1ll111_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᦟ"): subprocess.check_output([bstack1ll111_opy_ (u"ࠣࡩ࡬ࡸࠧᦠ"), bstack1ll111_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᦡ"), bstack1ll111_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᦢ")]).strip().decode(
                bstack1ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᦣ")),
            bstack1ll111_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᦤ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᦥ"): repo.git.rev_list(
                bstack1ll111_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᦦ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l1llll1l_opy_ = []
        for remote in remotes:
            bstack111ll111ll1_opy_ = {
                bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨᦧ"): remote.name,
                bstack1ll111_opy_ (u"ࠤࡸࡶࡱࠨᦨ"): remote.url,
            }
            bstack111l1llll1l_opy_.append(bstack111ll111ll1_opy_)
        bstack111l1l1llll_opy_ = {
            bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᦩ"): bstack1ll111_opy_ (u"ࠦ࡬࡯ࡴࠣᦪ"),
            **info,
            bstack1ll111_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᦫ"): bstack111l1llll1l_opy_
        }
        bstack111l1l1llll_opy_ = bstack111llllll11_opy_(bstack111l1l1llll_opy_)
        return bstack111l1l1llll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ᦬").format(err))
        return {}
def bstack111l11l111l_opy_(bstack111llllll1l_opy_=None):
    bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࡦࡲ࡬ࡺࠢࡩࡳࡷࡳࡡࡵࡶࡨࡨࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡷࡶࡩࠥࡩࡡࡴࡧࡶࠤ࡫ࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡰ࡮ࡧࡩࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡩࡳࡱࡪࡥࡳࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡐࡲࡲࡪࡀࠠࡎࡱࡱࡳ࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬࠱ࠦࡵࡴࡧࡶࠤࡨࡻࡲࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡴࡹࡿࠠ࡭࡫ࡶࡸࠥࡡ࡝࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦ࡮ࡰࠢࡶࡳࡺࡸࡣࡦࡵࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠬࠡࡴࡨࡸࡺࡸ࡮ࡴࠢ࡞ࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡴࡰࠢࡤࡲࡦࡲࡹࡻࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡨ࡮ࡩࡴࡴ࠮ࠣࡩࡦࡩࡨࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡣࠣࡪࡴࡲࡤࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ᦭")
    if bstack111llllll1l_opy_ is None:
        bstack111llllll1l_opy_ = [os.getcwd()]
    elif isinstance(bstack111llllll1l_opy_, list) and len(bstack111llllll1l_opy_) == 0:
        return []
    results = []
    for folder in bstack111llllll1l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll111_opy_ (u"ࠣࡈࡲࡰࡩ࡫ࡲࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨ᦮").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll111_opy_ (u"ࠤࡳࡶࡎࡪࠢ᦯"): bstack1ll111_opy_ (u"ࠥࠦᦰ"),
                bstack1ll111_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᦱ"): [],
                bstack1ll111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᦲ"): [],
                bstack1ll111_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨᦳ"): bstack1ll111_opy_ (u"ࠢࠣᦴ"),
                bstack1ll111_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᦵ"): [],
                bstack1ll111_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᦶ"): bstack1ll111_opy_ (u"ࠥࠦᦷ"),
                bstack1ll111_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦᦸ"): bstack1ll111_opy_ (u"ࠧࠨᦹ"),
                bstack1ll111_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤᦺ"): bstack1ll111_opy_ (u"ࠢࠣᦻ")
            }
            bstack111l1l1l111_opy_ = repo.active_branch.name
            bstack111l11l1l11_opy_ = repo.head.commit
            result[bstack1ll111_opy_ (u"ࠣࡲࡵࡍࡩࠨᦼ")] = bstack111l11l1l11_opy_.hexsha
            bstack111l1lll1ll_opy_ = _111l1l11111_opy_(repo)
            logger.debug(bstack1ll111_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥᦽ") + str(bstack111l1lll1ll_opy_) + bstack1ll111_opy_ (u"ࠥࠦᦾ"))
            if bstack111l1lll1ll_opy_:
                try:
                    bstack11l1111111l_opy_ = repo.git.diff(bstack1ll111_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤᦿ"), bstack1ll1l11llll_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥᧀ")).split(bstack1ll111_opy_ (u"࠭࡜࡯ࠩᧁ"))
                    logger.debug(bstack1ll111_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥᧂ") + str(bstack11l1111111l_opy_) + bstack1ll111_opy_ (u"ࠣࠤᧃ"))
                    result[bstack1ll111_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᧄ")] = [f.strip() for f in bstack11l1111111l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1l11llll_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢᧅ")))
                except Exception:
                    logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦᧆ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᧇ")] = _111l1l11ll1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll111_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᧈ")] = _111l1l11ll1_opy_(commits[:5])
            bstack111l11l1ll1_opy_ = set()
            bstack111l1l1lll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨᧉ") + str(commit.message) + bstack1ll111_opy_ (u"ࠣࠤ᧊"))
                bstack111l1l1l11l_opy_ = commit.author.name if commit.author else bstack1ll111_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥ᧋")
                bstack111l11l1ll1_opy_.add(bstack111l1l1l11l_opy_)
                bstack111l1l1lll1_opy_.append({
                    bstack1ll111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᧌"): commit.message.strip(),
                    bstack1ll111_opy_ (u"ࠦࡺࡹࡥࡳࠤ᧍"): bstack111l1l1l11l_opy_
                })
            result[bstack1ll111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ᧎")] = list(bstack111l11l1ll1_opy_)
            result[bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢ᧏")] = bstack111l1l1lll1_opy_
            result[bstack1ll111_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢ᧐")] = bstack111l11l1l11_opy_.committed_datetime.strftime(bstack1ll111_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠥ᧑"))
            if (not result[bstack1ll111_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ᧒")] or result[bstack1ll111_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦ᧓")].strip() == bstack1ll111_opy_ (u"ࠦࠧ᧔")) and bstack111l11l1l11_opy_.message:
                bstack111llll11ll_opy_ = bstack111l11l1l11_opy_.message.strip().splitlines()
                result[bstack1ll111_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ᧕")] = bstack111llll11ll_opy_[0] if bstack111llll11ll_opy_ else bstack1ll111_opy_ (u"ࠨࠢ᧖")
                if len(bstack111llll11ll_opy_) > 2:
                    result[bstack1ll111_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ᧗")] = bstack1ll111_opy_ (u"ࠨ࡞ࡱࠫ᧘").join(bstack111llll11ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࢁ࠮ࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ᧙").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack11l1111ll1l_opy_ = [
        result
        for result in results
        if _111ll1111ll_opy_(result)
    ]
    return bstack11l1111ll1l_opy_
def _111ll1111ll_opy_(result):
    bstack1ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡪࡲࡰࡦࡴࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡸࡻ࡬ࡵࠢ࡬ࡷࠥࡼࡡ࡭࡫ࡧࠤ࠭ࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠡࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠠࡢࡰࡧࠤࡦࡻࡴࡩࡱࡵࡷ࠮࠴ࠊࠡࠢࠣࠤࠧࠨࠢ᧚")
    return (
        isinstance(result.get(bstack1ll111_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ᧛"), None), list)
        and len(result[bstack1ll111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ᧜")]) > 0
        and isinstance(result.get(bstack1ll111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ᧝"), None), list)
        and len(result[bstack1ll111_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ᧞")]) > 0
    )
def _111l1l11111_opy_(repo):
    bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡵࡽࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡮ࡥࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡲࡦࡲࡲࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡮ࡡࡳࡦࡦࡳࡩ࡫ࡤࠡࡰࡤࡱࡪࡹࠠࡢࡰࡧࠤࡼࡵࡲ࡬ࠢࡺ࡭ࡹ࡮ࠠࡢ࡮࡯ࠤ࡛ࡉࡓࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࡶ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡥࡧࡩࡥࡺࡲࡴࠡࡤࡵࡥࡳࡩࡨࠡ࡫ࡩࠤࡵࡵࡳࡴ࡫ࡥࡰࡪ࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ᧟")
    try:
        try:
            origin = repo.remotes.origin
            bstack111l111llll_opy_ = origin.refs[bstack1ll111_opy_ (u"ࠩࡋࡉࡆࡊࠧ᧠")]
            target = bstack111l111llll_opy_.reference.name
            if target.startswith(bstack1ll111_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ᧡")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll111_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ᧢")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111l1l11ll1_opy_(commits):
    bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᧣")
    bstack11l1111111l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111l11l11l1_opy_ in diff:
                        if bstack111l11l11l1_opy_.a_path:
                            bstack11l1111111l_opy_.add(bstack111l11l11l1_opy_.a_path)
                        if bstack111l11l11l1_opy_.b_path:
                            bstack11l1111111l_opy_.add(bstack111l11l11l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l1111111l_opy_)
def bstack111llllll11_opy_(bstack111l1l1llll_opy_):
    bstack111l11l1l1l_opy_ = bstack111ll1lll11_opy_(bstack111l1l1llll_opy_)
    if bstack111l11l1l1l_opy_ and bstack111l11l1l1l_opy_ > bstack111l1l111ll_opy_:
        bstack111ll1ll1ll_opy_ = bstack111l11l1l1l_opy_ - bstack111l1l111ll_opy_
        bstack111l11lll11_opy_ = bstack111lll111l1_opy_(bstack111l1l1llll_opy_[bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᧤")], bstack111ll1ll1ll_opy_)
        bstack111l1l1llll_opy_[bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᧥")] = bstack111l11lll11_opy_
        logger.info(bstack1ll111_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ᧦")
                    .format(bstack111ll1lll11_opy_(bstack111l1l1llll_opy_) / 1024))
    return bstack111l1l1llll_opy_
def bstack111ll1lll11_opy_(json_data):
    try:
        if json_data:
            bstack111ll11ll1l_opy_ = json.dumps(json_data)
            bstack111lll111ll_opy_ = sys.getsizeof(bstack111ll11ll1l_opy_)
            return bstack111lll111ll_opy_
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ᧧").format(e))
    return -1
def bstack111lll111l1_opy_(field, bstack111lllll1ll_opy_):
    try:
        bstack111lll1llll_opy_ = len(bytes(bstack111l1ll1lll_opy_, bstack1ll111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧨")))
        bstack111l1ll11ll_opy_ = bytes(field, bstack1ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᧩"))
        bstack111lllll11l_opy_ = len(bstack111l1ll11ll_opy_)
        bstack111l1lll111_opy_ = ceil(bstack111lllll11l_opy_ - bstack111lllll1ll_opy_ - bstack111lll1llll_opy_)
        if bstack111l1lll111_opy_ > 0:
            bstack111ll1lll1l_opy_ = bstack111l1ll11ll_opy_[:bstack111l1lll111_opy_].decode(bstack1ll111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᧪"), errors=bstack1ll111_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭᧫")) + bstack111l1ll1lll_opy_
            return bstack111ll1lll1l_opy_
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧ᧬").format(e))
    return field
def bstack1ll1lll111_opy_():
    env = os.environ
    if (bstack1ll111_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᧭") in env and len(env[bstack1ll111_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ᧮")]) > 0) or (
            bstack1ll111_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᧯") in env and len(env[bstack1ll111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᧰")]) > 0):
        return {
            bstack1ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧱"): bstack1ll111_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢ᧲"),
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧳"): env.get(bstack1ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᧴")),
            bstack1ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧵"): env.get(bstack1ll111_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᧶")),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧷"): env.get(bstack1ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᧸"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠨࡃࡊࠤ᧹")) == bstack1ll111_opy_ (u"ࠢࡵࡴࡸࡩࠧ᧺") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᧻"))):
        return {
            bstack1ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧼"): bstack1ll111_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᧽"),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧾"): env.get(bstack1ll111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᧿")),
            bstack1ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨀ"): env.get(bstack1ll111_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦᨁ")),
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨂ"): env.get(bstack1ll111_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧᨃ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠥࡇࡎࠨᨄ")) == bstack1ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᨅ") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧᨆ"))):
        return {
            bstack1ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨇ"): bstack1ll111_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥᨈ"),
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨉ"): env.get(bstack1ll111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤᨊ")),
            bstack1ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨋ"): env.get(bstack1ll111_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨌ")),
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨍ"): env.get(bstack1ll111_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨎ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠢࡄࡋࠥᨏ")) == bstack1ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨᨐ") and env.get(bstack1ll111_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥᨑ")) == bstack1ll111_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧᨒ"):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨓ"): bstack1ll111_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢᨔ"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨕ"): None,
            bstack1ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨖ"): None,
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨗ"): None
        }
    if env.get(bstack1ll111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌᨘࠧ")) and env.get(bstack1ll111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᨙ")):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨚ"): bstack1ll111_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣᨛ"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᨜"): env.get(bstack1ll111_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ᨝")),
            bstack1ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᨞"): None,
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᨟"): env.get(bstack1ll111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨠ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠦࡈࡏࠢᨡ")) == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥᨢ") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᨣ"))):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨤ"): bstack1ll111_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢᨥ"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨦ"): env.get(bstack1ll111_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᨧ")),
            bstack1ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨨ"): None,
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨩ"): env.get(bstack1ll111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᨪ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠢࡄࡋࠥᨫ")) == bstack1ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨᨬ") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᨭ"))):
        return {
            bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᨮ"): bstack1ll111_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᨯ"),
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨰ"): env.get(bstack1ll111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧᨱ")),
            bstack1ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨲ"): env.get(bstack1ll111_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨳ")),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨴ"): env.get(bstack1ll111_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᨵ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠦࡈࡏࠢᨶ")) == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥᨷ") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤᨸ"))):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨹ"): bstack1ll111_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣᨺ"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨻ"): env.get(bstack1ll111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᨼ")),
            bstack1ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨽ"): env.get(bstack1ll111_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᨾ")),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨿ"): env.get(bstack1ll111_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᩀ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠣࡅࡌࠦᩁ")) == bstack1ll111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᩂ") and bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᩃ"))):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩄ"): bstack1ll111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᩅ"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩆ"): env.get(bstack1ll111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᩇ")),
            bstack1ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩈ"): env.get(bstack1ll111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᩉ")) or env.get(bstack1ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᩊ")),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᩋ"): env.get(bstack1ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᩌ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᩍ"))):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩎ"): bstack1ll111_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᩏ"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᩐ"): bstack1ll111_opy_ (u"ࠥࡿࢂࢁࡽࠣᩑ").format(env.get(bstack1ll111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᩒ")), env.get(bstack1ll111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᩓ"))),
            bstack1ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩔ"): env.get(bstack1ll111_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᩕ")),
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩖ"): env.get(bstack1ll111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᩗ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᩘ"))):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩙ"): bstack1ll111_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᩚ"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩛ"): bstack1ll111_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᩜ").format(env.get(bstack1ll111_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᩝ")), env.get(bstack1ll111_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᩞ")), env.get(bstack1ll111_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫ᩟")), env.get(bstack1ll111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ᩠"))),
            bstack1ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩡ"): env.get(bstack1ll111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᩢ")),
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩣ"): env.get(bstack1ll111_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᩤ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᩥ")) and env.get(bstack1ll111_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᩦ")):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩧ"): bstack1ll111_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᩨ"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩩ"): bstack1ll111_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᩪ").format(env.get(bstack1ll111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᩫ")), env.get(bstack1ll111_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᩬ")), env.get(bstack1ll111_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᩭ"))),
            bstack1ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩮ"): env.get(bstack1ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩯ")),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩰ"): env.get(bstack1ll111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩱ"))
        }
    if any([env.get(bstack1ll111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᩲ")), env.get(bstack1ll111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᩳ")), env.get(bstack1ll111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᩴ"))]):
        return {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩵"): bstack1ll111_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ᩶"),
            bstack1ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᩷"): env.get(bstack1ll111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᩸")),
            bstack1ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): env.get(bstack1ll111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᩺")),
            bstack1ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩻"): env.get(bstack1ll111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᩼"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ᩽")):
        return {
            bstack1ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᩾"): bstack1ll111_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵ᩿ࠢ"),
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᪀"): env.get(bstack1ll111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ᪁")),
            bstack1ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪂"): env.get(bstack1ll111_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ᪃")),
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪄"): env.get(bstack1ll111_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᪅"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ᪆")) or env.get(bstack1ll111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᪇")):
        return {
            bstack1ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪈"): bstack1ll111_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ᪉"),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪊"): env.get(bstack1ll111_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᪋")),
            bstack1ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪌"): bstack1ll111_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ᪍") if env.get(bstack1ll111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᪎")) else None,
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪏"): env.get(bstack1ll111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ᪐"))
        }
    if any([env.get(bstack1ll111_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ᪑")), env.get(bstack1ll111_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᪒")), env.get(bstack1ll111_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᪓"))]):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪔"): bstack1ll111_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ᪕"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪖"): None,
            bstack1ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᪗"): env.get(bstack1ll111_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ᪘")),
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᪙"): env.get(bstack1ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᪚"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ᪛")):
        return {
            bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪜"): bstack1ll111_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ᪝"),
            bstack1ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪞"): env.get(bstack1ll111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᪟")),
            bstack1ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪠"): bstack1ll111_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ᪡").format(env.get(bstack1ll111_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ᪢"))) if env.get(bstack1ll111_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ᪣")) else None,
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪤"): env.get(bstack1ll111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪥"))
        }
    if bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ᪦"))):
        return {
            bstack1ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᪧ"): bstack1ll111_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ᪨"),
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪩"): env.get(bstack1ll111_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ᪪")),
            bstack1ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪫"): env.get(bstack1ll111_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ᪬")),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪭"): env.get(bstack1ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᪮"))
        }
    if bstack1l11lll111_opy_(env.get(bstack1ll111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ᪯"))):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪰"): bstack1ll111_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ᪱"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪲"): bstack1ll111_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ᪳").format(env.get(bstack1ll111_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ᪴")), env.get(bstack1ll111_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚᪵ࠩ")), env.get(bstack1ll111_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ᪶࠭"))),
            bstack1ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪷"): env.get(bstack1ll111_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙᪸ࠥ")),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ᪹ࠣ"): env.get(bstack1ll111_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆ᪺ࠥ"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠦࡈࡏࠢ᪻")) == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥ᪼") and env.get(bstack1ll111_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ᪽")) == bstack1ll111_opy_ (u"ࠢ࠲ࠤ᪾"):
        return {
            bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨᪿ"): bstack1ll111_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤᫀ"),
            bstack1ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫁"): bstack1ll111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ᫂").format(env.get(bstack1ll111_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍ᫃ࠩ"))),
            bstack1ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᫄ࠣ"): None,
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫅"): None,
        }
    if env.get(bstack1ll111_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ᫆")):
        return {
            bstack1ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇"): bstack1ll111_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ᫈"),
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫉"): None,
            bstack1ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᫊ࠢ"): env.get(bstack1ll111_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ᫋")),
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᫌ"): env.get(bstack1ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᫍ"))
        }
    if any([env.get(bstack1ll111_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧᫎ")), env.get(bstack1ll111_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ᫏")), env.get(bstack1ll111_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ᫐")), env.get(bstack1ll111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ᫑"))]):
        return {
            bstack1ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫒"): bstack1ll111_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ᫓"),
            bstack1ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᫔"): None,
            bstack1ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᫕"): env.get(bstack1ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᫖")) or None,
            bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫗"): env.get(bstack1ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᫘"), 0)
        }
    if env.get(bstack1ll111_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᫙")):
        return {
            bstack1ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫚"): bstack1ll111_opy_ (u"ࠣࡉࡲࡇࡉࠨ᫛"),
            bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫜"): None,
            bstack1ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫝"): env.get(bstack1ll111_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᫞")),
            bstack1ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᫟"): env.get(bstack1ll111_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧ᫠"))
        }
    if env.get(bstack1ll111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᫡")):
        return {
            bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨ᫢"): bstack1ll111_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ᫣"),
            bstack1ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫤"): env.get(bstack1ll111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᫥")),
            bstack1ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᫦"): env.get(bstack1ll111_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᫧")),
            bstack1ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᫨"): env.get(bstack1ll111_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᫩"))
        }
    return {bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫪"): None}
def get_host_info():
    return {
        bstack1ll111_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ᫫"): platform.node(),
        bstack1ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ᫬"): platform.system(),
        bstack1ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥ᫭"): platform.machine(),
        bstack1ll111_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᫮"): platform.version(),
        bstack1ll111_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ᫯"): platform.architecture()[0]
    }
def bstack11ll1ll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lll1ll11_opy_():
    if global_config.get_property(bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ᫰")):
        return bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᫱")
    return bstack1ll111_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ᫲")
def bstack111ll11ll11_opy_(driver):
    info = {
        bstack1ll111_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᫳"): driver.capabilities,
        bstack1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ᫴"): driver.session_id,
        bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᫵"): driver.capabilities.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᫶"), None),
        bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᫷"): driver.capabilities.get(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᫸"), None),
        bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ᫹"): driver.capabilities.get(bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᫺"), None),
        bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫻"):driver.capabilities.get(bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫼"), None),
    }
    if bstack111lll1ll11_opy_() == bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫽"):
        if bstack1l11l11111_opy_():
            info[bstack1ll111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫾")] = bstack1ll111_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫿")
        elif driver.capabilities.get(bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᬀ"), {}).get(bstack1ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᬁ"), False):
            info[bstack1ll111_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᬂ")] = bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᬃ")
        else:
            info[bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᬄ")] = bstack1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᬅ")
    return info
def bstack1l11l11111_opy_():
    if global_config.get_property(bstack1ll111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᬆ")):
        return True
    if bstack1l11lll111_opy_(os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᬇ"), None)):
        return True
    return False
def bstack11l11111l11_opy_(bstack111ll1ll1l1_opy_, url, response, headers=None, data=None):
    bstack1ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡇࡻࡩ࡭ࡦࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹ࠵ࡲࡦࡵࡳࡳࡳࡹࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡳࡸࡩࡸࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧࠤ࠭ࡍࡅࡕ࠮ࠣࡔࡔ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡸࡶࡱࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡗࡕࡐ࠴࡫࡮ࡥࡲࡲ࡭ࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡷ࡫ࡱࡶࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡩࡧࡤࡨࡪࡸࡳ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣ࡬ࡪࡧࡤࡦࡴࡶࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡢࡶࡤ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡊࡔࡑࡑࠤࡩࡧࡴࡢࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠣࡻ࡮ࡺࡨࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠐࠠࠡࠢࠣࠦࠧࠨᬈ")
    bstack111lll1lll1_opy_ = {
        bstack1ll111_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨᬉ"): headers,
        bstack1ll111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᬊ"): bstack111ll1ll1l1_opy_.upper(),
        bstack1ll111_opy_ (u"ࠢࡢࡩࡨࡲࡹࠨᬋ"): None,
        bstack1ll111_opy_ (u"ࠣࡧࡱࡨࡵࡵࡩ࡯ࡶࠥᬌ"): url,
        bstack1ll111_opy_ (u"ࠤ࡭ࡷࡴࡴࠢᬍ"): data
    }
    try:
        bstack111l1l1ll11_opy_ = response.json()
    except Exception:
        bstack111l1l1ll11_opy_ = response.text
    bstack111lllll1l1_opy_ = {
        bstack1ll111_opy_ (u"ࠥࡦࡴࡪࡹࠣᬎ"): bstack111l1l1ll11_opy_,
        bstack1ll111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࡇࡴࡪࡥࠣᬏ"): response.status_code
    }
    return {
        bstack1ll111_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨᬐ"): bstack111lll1lll1_opy_,
        bstack1ll111_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᬑ"): bstack111lllll1l1_opy_
    }
def bstack11111l1l_opy_(bstack111ll1ll1l1_opy_, url, data, config):
    headers = config.get(bstack1ll111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᬒ"), None)
    proxies = bstack111lllllll_opy_(config, url)
    auth = config.get(bstack1ll111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᬓ"), None)
    response = requests.request(
            bstack111ll1ll1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack11l11111l11_opy_(bstack111ll1ll1l1_opy_, url, response, headers, data)
        bstack1l11llll_opy_.debug(json.dumps(log_message, separators=(bstack1ll111_opy_ (u"ࠩ࠯ࠫᬔ"), bstack1ll111_opy_ (u"ࠪ࠾ࠬᬕ"))))
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࡾࢁࠧᬖ").format(e))
    return response
def bstack1l111ll11l_opy_(bstack1ll111l1l_opy_, size):
    bstack1ll11l1l_opy_ = []
    while len(bstack1ll111l1l_opy_) > size:
        bstack1ll1l11l1l_opy_ = bstack1ll111l1l_opy_[:size]
        bstack1ll11l1l_opy_.append(bstack1ll1l11l1l_opy_)
        bstack1ll111l1l_opy_ = bstack1ll111l1l_opy_[size:]
    bstack1ll11l1l_opy_.append(bstack1ll111l1l_opy_)
    return bstack1ll11l1l_opy_
def bstack111l111ll11_opy_(message, bstack111ll111l1l_opy_=False):
    os.write(1, bytes(message, bstack1ll111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᬗ")))
    os.write(1, bytes(bstack1ll111_opy_ (u"࠭࡜࡯ࠩᬘ"), bstack1ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬙ")))
    if bstack111ll111l1l_opy_:
        with open(bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧᬚ") + os.environ[bstack1ll111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᬛ")] + bstack1ll111_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᬜ"), bstack1ll111_opy_ (u"ࠫࡦ࠭ᬝ")) as f:
            f.write(message + bstack1ll111_opy_ (u"ࠬࡢ࡮ࠨᬞ"))
def bstack1lll111l1_opy_():
    return os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᬟ")].lower() == bstack1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬᬠ")
def current_time():
    return bstack1lllllll1ll_opy_().replace(tzinfo=None).isoformat() + bstack1ll111_opy_ (u"ࠨ࡜ࠪᬡ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll111_opy_ (u"ࠩ࡝ࠫᬢ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll111_opy_ (u"ࠪ࡞ࠬᬣ")))).total_seconds() * 1000
def bstack111lll1l11l_opy_(timestamp):
    return bstack11l11111111_opy_(timestamp).isoformat() + bstack1ll111_opy_ (u"ࠫ࡟࠭ᬤ")
def bstack111lll1l111_opy_(bstack11l111l111l_opy_):
    date_format = bstack1ll111_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪᬥ")
    bstack111lll11l1l_opy_ = datetime.datetime.strptime(bstack11l111l111l_opy_, date_format)
    return bstack111lll11l1l_opy_.isoformat() + bstack1ll111_opy_ (u"࡚࠭ࠨᬦ")
def bstack111l1l1ll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬧ")
    else:
        return bstack1ll111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᬨ")
def bstack1l11lll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᬩ")
def bstack111l1llll11_opy_(val):
    return val.__str__().lower() == bstack1ll111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᬪ")
def error_handler(bstack111llllllll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111llllllll_opy_ as e:
                print(bstack1ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᬫ").format(func.__name__, bstack111llllllll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lllll111_opy_(bstack111l11ll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l11ll11l_opy_(cls, *args, **kwargs)
            except bstack111llllllll_opy_ as e:
                print(bstack1ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᬬ").format(bstack111l11ll11l_opy_.__name__, bstack111llllllll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lllll111_opy_
    else:
        return decorator
def bstack1l111l111_opy_(bstack1lll1lllll1_opy_):
    if os.getenv(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᬭ")) is not None:
        return bstack1l11lll111_opy_(os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᬮ")))
    if bstack1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬯ") in bstack1lll1lllll1_opy_ and bstack111l1llll11_opy_(bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬰ")]):
        return False
    if bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᬱ") in bstack1lll1lllll1_opy_ and bstack111l1llll11_opy_(bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᬲ")]):
        return False
    return True
def bstack11l11l1111_opy_():
    try:
        from pytest_bdd import reporting
        bstack111lllllll1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧᬳ"), None)
        return bstack111lllllll1_opy_ is None or bstack111lllllll1_opy_ == bstack1ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦ᬴ࠥ")
    except Exception as e:
        return False
def bstack1ll1l111_opy_(hub_url, CONFIG):
    if bstack11l1l1l11_opy_() <= version.parse(bstack1ll111_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᬵ")):
        if hub_url:
            return bstack1ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᬶ") + hub_url + bstack1ll111_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᬷ")
        return bstack11l11l11l1_opy_
    if hub_url:
        return bstack1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᬸ") + hub_url + bstack1ll111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᬹ")
    return HTTPS_HUB
def bstack111l1ll111l_opy_():
    return isinstance(os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫᬺ")), str)
def bstack111l1lllll_opy_(url):
    return urlparse(url).hostname
def bstack1111ll1lll_opy_(hostname):
    for bstack1l1l1111_opy_ in bstack1l11llll11_opy_:
        regex = re.compile(bstack1l1l1111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111ll1111l1_opy_(bstack111l11l1111_opy_, file_name, logger):
    bstack111l1ll11_opy_ = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"࠭ࡾࠨᬻ")), bstack111l11l1111_opy_)
    try:
        if not os.path.exists(bstack111l1ll11_opy_):
            os.makedirs(bstack111l1ll11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠧࡿࠩᬼ")), bstack111l11l1111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll111_opy_ (u"ࠨࡹࠪᬽ")):
                pass
            with open(file_path, bstack1ll111_opy_ (u"ࠤࡺ࠯ࠧᬾ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111l11l1l1_opy_.format(str(e)))
def bstack11l11111ll1_opy_(file_name, key, value, logger):
    file_path = bstack111ll1111l1_opy_(bstack1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬿ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll11l1l_opy_ = json.load(open(file_path, bstack1ll111_opy_ (u"ࠫࡷࡨࠧᭀ")))
        else:
            bstack1lll11l1l_opy_ = {}
        bstack1lll11l1l_opy_[key] = value
        with open(file_path, bstack1ll111_opy_ (u"ࠧࡽࠫࠣᭁ")) as outfile:
            json.dump(bstack1lll11l1l_opy_, outfile)
def bstack11l1l11ll_opy_(file_name, logger):
    file_path = bstack111ll1111l1_opy_(bstack1ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᭂ"), file_name, logger)
    bstack1lll11l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll111_opy_ (u"ࠧࡳࠩᭃ")) as bstack111l1l1l1l_opy_:
            bstack1lll11l1l_opy_ = json.load(bstack111l1l1l1l_opy_)
    return bstack1lll11l1l_opy_
def bstack1111ll1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤ᭄ࠬ") + file_path + bstack1ll111_opy_ (u"ࠩࠣࠫᭅ") + str(e))
def bstack11l1l1l11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll111_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧᭆ")
def bstack1111lllll_opy_(config):
    if bstack1ll111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᭇ") in config:
        del (config[bstack1ll111_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᭈ")])
        return False
    if bstack11l1l1l11_opy_() < version.parse(bstack1ll111_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬᭉ")):
        return False
    if bstack11l1l1l11_opy_() >= version.parse(bstack1ll111_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ᭊ")):
        return True
    if bstack1ll111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᭋ") in config and config[bstack1ll111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᭌ")] is False:
        return False
    else:
        return True
def bstack1lll11ll1_opy_(args_list, bstack111lll11lll_opy_):
    index = -1
    for value in bstack111lll11lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1111ll11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1111ll11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11111ll1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᭍"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᭎"), exception=exception)
    def bstack1lll11ll1l1_opy_(self):
        if self.result != bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᭏"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᭐") in self.exception_type:
            return bstack1ll111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ᭑")
        return bstack1ll111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ᭒")
    def bstack11l111l1111_opy_(self):
        if self.result != bstack1ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᭓"):
            return None
        if self.bstack11111ll1ll_opy_:
            return self.bstack11111ll1ll_opy_
        return bstack111ll1l111l_opy_(self.exception)
def bstack111ll1l111l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111ll11llll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11llll11l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l11ll11l_opy_(config, logger):
    try:
        import playwright
        bstack111l11l1lll_opy_ = playwright.__file__
        bstack111ll1llll1_opy_ = os.path.split(bstack111l11l1lll_opy_)
        bstack111l1l11lll_opy_ = bstack111ll1llll1_opy_[0] + bstack1ll111_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭᭔")
        os.environ[bstack1ll111_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ᭕")] = bstack11lll11l_opy_(config)
        with open(bstack111l1l11lll_opy_, bstack1ll111_opy_ (u"ࠬࡸࠧ᭖")) as f:
            file_content = f.read()
            bstack111ll1ll111_opy_ = bstack1ll111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ᭗")
            bstack111lll11111_opy_ = file_content.find(bstack111ll1ll111_opy_)
            if bstack111lll11111_opy_ == -1:
              process = subprocess.Popen(bstack1ll111_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ᭘"), shell=True, cwd=bstack111ll1llll1_opy_[0])
              process.wait()
              bstack111lll11ll1_opy_ = bstack1ll111_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ᭙")
              bstack111l1lll1l1_opy_ = bstack1ll111_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ᭚")
              bstack111ll1l1ll1_opy_ = file_content.replace(bstack111lll11ll1_opy_, bstack111l1lll1l1_opy_)
              with open(bstack111l1l11lll_opy_, bstack1ll111_opy_ (u"ࠪࡻࠬ᭛")) as f:
                f.write(bstack111ll1l1ll1_opy_)
    except Exception as e:
        logger.error(bstack11l11l1l_opy_.format(str(e)))
def bstack1l1lll11ll_opy_():
  try:
    bstack111llll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ᭜"))
    bstack11l11111l1l_opy_ = []
    if os.path.exists(bstack111llll1ll1_opy_):
      with open(bstack111llll1ll1_opy_) as f:
        bstack11l11111l1l_opy_ = json.load(f)
      os.remove(bstack111llll1ll1_opy_)
    return bstack11l11111l1l_opy_
  except:
    pass
  return []
def bstack1l111ll11_opy_(bstack11l1ll111_opy_):
  try:
    bstack11l11111l1l_opy_ = []
    bstack111llll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ᭝"))
    if os.path.exists(bstack111llll1ll1_opy_):
      with open(bstack111llll1ll1_opy_) as f:
        bstack11l11111l1l_opy_ = json.load(f)
    bstack11l11111l1l_opy_.append(bstack11l1ll111_opy_)
    with open(bstack111llll1ll1_opy_, bstack1ll111_opy_ (u"࠭ࡷࠨ᭞")) as f:
        json.dump(bstack11l11111l1l_opy_, f)
  except:
    pass
def bstack1111l11l1l_opy_(logger, bstack111ll11l111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ᭟"), bstack1ll111_opy_ (u"ࠨࠩ᭠"))
    if test_name == bstack1ll111_opy_ (u"ࠩࠪ᭡"):
        test_name = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ᭢"), bstack1ll111_opy_ (u"ࠫࠬ᭣"))
    bstack11l1111lll1_opy_ = bstack1ll111_opy_ (u"ࠬ࠲ࠠࠨ᭤").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111ll11l111_opy_:
        bstack1l1ll1l1l_opy_ = os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᭥"), bstack1ll111_opy_ (u"ࠧ࠱ࠩ᭦"))
        bstack1l1ll11l1_opy_ = {bstack1ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭᭧"): test_name, bstack1ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᭨"): bstack11l1111lll1_opy_, bstack1ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᭩"): bstack1l1ll1l1l_opy_}
        bstack111l11lll1l_opy_ = []
        bstack111ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ᭪"))
        if os.path.exists(bstack111ll1l1111_opy_):
            with open(bstack111ll1l1111_opy_) as f:
                bstack111l11lll1l_opy_ = json.load(f)
        bstack111l11lll1l_opy_.append(bstack1l1ll11l1_opy_)
        with open(bstack111ll1l1111_opy_, bstack1ll111_opy_ (u"ࠬࡽࠧ᭫")) as f:
            json.dump(bstack111l11lll1l_opy_, f)
    else:
        bstack1l1ll11l1_opy_ = {bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨ᭬ࠫ"): test_name, bstack1ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᭭"): bstack11l1111lll1_opy_, bstack1ll111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᭮"): str(multiprocessing.current_process().name)}
        if bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭᭯") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1ll11l1_opy_)
  except Exception as e:
      logger.warn(bstack1ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᭰").format(e))
def bstack11111lll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ᭱"))
    try:
      bstack111lll1ll1l_opy_ = []
      bstack1l1ll11l1_opy_ = {bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᭲"): test_name, bstack1ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᭳"): error_message, bstack1ll111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᭴"): index}
      bstack111ll1lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ᭵"))
      if os.path.exists(bstack111ll1lllll_opy_):
          with open(bstack111ll1lllll_opy_) as f:
              bstack111lll1ll1l_opy_ = json.load(f)
      bstack111lll1ll1l_opy_.append(bstack1l1ll11l1_opy_)
      with open(bstack111ll1lllll_opy_, bstack1ll111_opy_ (u"ࠩࡺࠫ᭶")) as f:
          json.dump(bstack111lll1ll1l_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ᭷").format(e))
    return
  bstack111lll1ll1l_opy_ = []
  bstack1l1ll11l1_opy_ = {bstack1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭸"): test_name, bstack1ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᭹"): error_message, bstack1ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᭺"): index}
  bstack111ll1lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᭻"))
  lock_file = bstack111ll1lllll_opy_ + bstack1ll111_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ᭼")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111ll1lllll_opy_):
          with open(bstack111ll1lllll_opy_, bstack1ll111_opy_ (u"ࠩࡵࠫ᭽")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1ll1l_opy_ = json.load(open(bstack111ll1lllll_opy_))
      bstack111lll1ll1l_opy_.append(bstack1l1ll11l1_opy_)
      with open(bstack111ll1lllll_opy_, bstack1ll111_opy_ (u"ࠪࡻࠬ᭾")) as f:
          json.dump(bstack111lll1ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦ᭿").format(e))
def bstack11l1llll1_opy_(bstack1ll11l11l_opy_, name, logger):
  try:
    bstack1l1ll11l1_opy_ = {bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᮀ"): name, bstack1ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᮁ"): bstack1ll11l11l_opy_, bstack1ll111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᮂ"): str(threading.current_thread()._name)}
    return bstack1l1ll11l1_opy_
  except Exception as e:
    logger.warn(bstack1ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᮃ").format(e))
  return
def bstack11l111111l1_opy_():
    return platform.system() == bstack1ll111_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᮄ")
def bstack1111ll11l_opy_(bstack111l111lll1_opy_, config, logger):
    bstack111l1l1l1l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l111lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᮅ").format(e))
    return bstack111l1l1l1l1_opy_
def bstack11l1111l1l1_opy_(bstack11l1111llll_opy_, bstack111llll1lll_opy_):
    bstack111l11ll1l1_opy_ = version.parse(bstack11l1111llll_opy_)
    bstack111llll1l1l_opy_ = version.parse(bstack111llll1lll_opy_)
    if bstack111l11ll1l1_opy_ > bstack111llll1l1l_opy_:
        return 1
    elif bstack111l11ll1l1_opy_ < bstack111llll1l1l_opy_:
        return -1
    else:
        return 0
def bstack1lllllll1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11111111_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111lll11l11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll11l11_opy_(options, framework, config, bstack1ll11l1l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll111_opy_ (u"ࠫ࡬࡫ࡴࠨᮆ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll111ll11_opy_ = caps.get(bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᮇ"))
    bstack111llll111l_opy_ = True
    bstack111l11lll1_opy_ = os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᮈ")]
    bstack1l11lll11l1_opy_ = config.get(bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᮉ"), False)
    if bstack1l11lll11l1_opy_:
        bstack1l1ll11l1ll_opy_ = config.get(bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᮊ"), {})
        bstack1l1ll11l1ll_opy_[bstack1ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᮋ")] = os.getenv(bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᮌ"))
        bstack111l1lll11l_opy_ = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᮍ"), bstack1ll111_opy_ (u"ࠬࢁࡽࠨᮎ"))).get(bstack1ll111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᮏ"))
    if bstack111l1llll11_opy_(caps.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᮐ"))) or bstack111l1llll11_opy_(caps.get(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᮑ"))):
        bstack111llll111l_opy_ = False
    if bstack1111lllll_opy_({bstack1ll111_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᮒ"): bstack111llll111l_opy_}):
        bstack1ll111ll11_opy_ = bstack1ll111ll11_opy_ or {}
        bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᮓ")] = bstack111lll11l11_opy_(framework)
        bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᮔ")] = bstack1lll111l1_opy_()
        bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᮕ")] = bstack111l11lll1_opy_
        bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᮖ")] = bstack1ll11l1l11_opy_
        if bstack1l11lll11l1_opy_:
            bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᮗ")] = bstack1l11lll11l1_opy_
            bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᮘ")] = bstack1l1ll11l1ll_opy_
            bstack1ll111ll11_opy_[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᮙ")][bstack1ll111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᮚ")] = bstack111l1lll11l_opy_
        if getattr(options, bstack1ll111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᮛ"), None):
            options.set_capability(bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᮜ"), bstack1ll111ll11_opy_)
        else:
            options[bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᮝ")] = bstack1ll111ll11_opy_
    else:
        if getattr(options, bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᮞ"), None):
            options.set_capability(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᮟ"), bstack111lll11l11_opy_(framework))
            options.set_capability(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᮠ"), bstack1lll111l1_opy_())
            options.set_capability(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᮡ"), bstack111l11lll1_opy_)
            options.set_capability(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᮢ"), bstack1ll11l1l11_opy_)
            if bstack1l11lll11l1_opy_:
                options.set_capability(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᮣ"), bstack1l11lll11l1_opy_)
                options.set_capability(bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᮤ"), bstack1l1ll11l1ll_opy_)
                options.set_capability(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᮥ"), bstack111l1lll11l_opy_)
        else:
            options[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᮦ")] = bstack111lll11l11_opy_(framework)
            options[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᮧ")] = bstack1lll111l1_opy_()
            options[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᮨ")] = bstack111l11lll1_opy_
            options[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᮩ")] = bstack1ll11l1l11_opy_
            if bstack1l11lll11l1_opy_:
                options[bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ᮪ࠫ")] = bstack1l11lll11l1_opy_
                options[bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ᮫ࠬ")] = bstack1l1ll11l1ll_opy_
                options[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮬ")][bstack1ll111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᮭ")] = bstack111l1lll11l_opy_
    return options
def bstack111ll11l11l_opy_(ws_endpoint, framework):
    bstack1ll11l1l11_opy_ = global_config.get_property(bstack1ll111_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᮮ"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᮯ"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᮰"))[0]
        if bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ᮱") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1111l111_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᮲"))[1]))
            bstack11l1111l111_opy_ = bstack11l1111l111_opy_ or {}
            bstack111l11lll1_opy_ = os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᮳")]
            bstack11l1111l111_opy_[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᮴")] = str(framework) + str(__version__)
            bstack11l1111l111_opy_[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᮵")] = bstack1lll111l1_opy_()
            bstack11l1111l111_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᮶")] = bstack111l11lll1_opy_
            bstack11l1111l111_opy_[bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᮷")] = bstack1ll11l1l11_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ᮸"))[0] + bstack1ll111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᮹") + urllib.parse.quote(json.dumps(bstack11l1111l111_opy_))
    return ws_endpoint
def bstack1ll1lll11_opy_():
    global bstack1111111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1111111l_opy_ = BrowserType.connect
    return bstack1111111l_opy_
def bstack111ll1l11l1_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1ll1ll111_opy_(self, *args, **kwargs):
    global bstack1111111l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll111_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᮺ") in kwargs:
            kwargs[bstack1ll111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᮻ")] = bstack111ll11l11l_opy_(
                kwargs.get(bstack1ll111_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᮼ"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᮽ").format(str(e)))
    return bstack1111111l_opy_(self, *args, **kwargs)
def bstack111ll11lll1_opy_(bstack11l11111lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111lllllll_opy_(bstack11l11111lll_opy_, bstack1ll111_opy_ (u"ࠦࠧᮾ"))
        if proxies and proxies.get(bstack1ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᮿ")):
            parsed_url = urlparse(proxies.get(bstack1ll111_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᯀ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᯁ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᯂ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᯃ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᯄ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1ll1ll_opy_(bstack11l11111lll_opy_):
    bstack111ll1l11ll_opy_ = {
        bstack111ll111111_opy_[bstack111lll1l1l1_opy_]: bstack11l11111lll_opy_[bstack111lll1l1l1_opy_]
        for bstack111lll1l1l1_opy_ in bstack11l11111lll_opy_
        if bstack111lll1l1l1_opy_ in bstack111ll111111_opy_
    }
    bstack111ll1l11ll_opy_[bstack1ll111_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᯅ")] = bstack111ll11lll1_opy_(bstack11l11111lll_opy_, global_config.get_property(bstack1ll111_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᯆ")))
    bstack11l1111l11l_opy_ = [element.lower() for element in bstack111llll1111_opy_]
    bstack111l11lllll_opy_(bstack111ll1l11ll_opy_, bstack11l1111l11l_opy_)
    return bstack111ll1l11ll_opy_
def bstack111l11lllll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll111_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᯇ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l11lllll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l11lllll_opy_(item, keys)
def bstack1l1111ll1ll_opy_():
    bstack111ll1l1lll_opy_ = [os.environ.get(bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᯈ")), os.path.join(os.path.expanduser(bstack1ll111_opy_ (u"ࠣࢀࠥᯉ")), bstack1ll111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᯊ")), os.path.join(bstack1ll111_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᯋ"), bstack1ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᯌ"))]
    for path in bstack111ll1l1lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll111_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᯍ") + str(path) + bstack1ll111_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᯎ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll111_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᯏ") + str(path) + bstack1ll111_opy_ (u"ࠣࠩࠥᯐ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᯑ") + str(path) + bstack1ll111_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᯒ"))
            else:
                logger.debug(bstack1ll111_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᯓ") + str(path) + bstack1ll111_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᯔ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll111_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦᯕ") + str(path) + bstack1ll111_opy_ (u"ࠢࠨ࠰ࠥᯖ"))
            return path
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨᯗ") + str(e) + bstack1ll111_opy_ (u"ࠤࠥᯘ"))
    logger.debug(bstack1ll111_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢᯙ"))
    return None
@measure(event_name=EVENTS.bstack111l11ll111_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack1llll1l1l1l_opy_(binary_path, bstack1llll1ll111_opy_, bs_config):
    logger.debug(bstack1ll111_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᯚ").format(binary_path))
    bstack111l11ll1ll_opy_ = bstack1ll111_opy_ (u"ࠬ࠭ᯛ")
    bstack111l1l1l1ll_opy_ = {
        bstack1ll111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᯜ"): __version__,
        bstack1ll111_opy_ (u"ࠢࡰࡵࠥᯝ"): platform.system(),
        bstack1ll111_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᯞ"): platform.machine(),
        bstack1ll111_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᯟ"): bstack1ll111_opy_ (u"ࠪ࠴ࠬᯠ"),
        bstack1ll111_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᯡ"): bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᯢ")
    }
    bstack111l11l11ll_opy_(bstack111l1l1l1ll_opy_)
    try:
        if binary_path:
            if bstack11l111111l1_opy_():
                bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᯣ")] = subprocess.check_output([binary_path, bstack1ll111_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᯤ")]).strip().decode(bstack1ll111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᯥ"))
            else:
                bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴ᯦ࠧ")] = subprocess.check_output([binary_path, bstack1ll111_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᯧ")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᯨ"))
        response = requests.request(
            bstack1ll111_opy_ (u"ࠬࡍࡅࡕࠩᯩ"),
            url=bstack1lll1l11_opy_(bstack111l1ll1l11_opy_),
            headers=None,
            auth=(bs_config[bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᯪ")], bs_config[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᯫ")]),
            json=None,
            params=bstack111l1l1l1ll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll111_opy_ (u"ࠨࡷࡵࡰࠬᯬ") in data.keys() and bstack1ll111_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᯭ") in data.keys():
            logger.debug(bstack1ll111_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦᯮ").format(bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᯯ")]))
            if bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᯰ") in os.environ:
                logger.debug(bstack1ll111_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡥࡸࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤᯱ"))
                data[bstack1ll111_opy_ (u"ࠧࡶࡴ࡯᯲ࠫ")] = os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏ᯳ࠫ")]
            bstack111l1llllll_opy_ = bstack111ll1ll11l_opy_(data[bstack1ll111_opy_ (u"ࠩࡸࡶࡱ࠭᯴")], bstack1llll1ll111_opy_)
            bstack111l11ll1ll_opy_ = os.path.join(bstack1llll1ll111_opy_, bstack111l1llllll_opy_)
            os.chmod(bstack111l11ll1ll_opy_, 0o777) # bstack111l1ll1ll1_opy_ permission
            return bstack111l11ll1ll_opy_
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ᯵").format(e))
    return binary_path
def bstack111l11l11ll_opy_(bstack111l1l1l1ll_opy_):
    try:
        if bstack1ll111_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ᯶") not in bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬࡵࡳࠨ᯷")].lower():
            return
        if os.path.exists(bstack1ll111_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ᯸")):
            with open(bstack1ll111_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ᯹"), bstack1ll111_opy_ (u"ࠣࡴࠥ᯺")) as f:
                bstack111l1l11l11_opy_ = {}
                for line in f:
                    if bstack1ll111_opy_ (u"ࠤࡀࠦ᯻") in line:
                        key, value = line.rstrip().split(bstack1ll111_opy_ (u"ࠥࡁࠧ᯼"), 1)
                        bstack111l1l11l11_opy_[key] = value.strip(bstack1ll111_opy_ (u"ࠫࠧࡢࠧࠨ᯽"))
                bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ᯾")] = bstack111l1l11l11_opy_.get(bstack1ll111_opy_ (u"ࠨࡉࡅࠤ᯿"), bstack1ll111_opy_ (u"ࠢࠣᰀ"))
        elif os.path.exists(bstack1ll111_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵ࡡ࡭ࡲ࡬ࡲࡪ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢᰁ")):
            bstack111l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᰂ")] = bstack1ll111_opy_ (u"ࠪࡥࡱࡶࡩ࡯ࡧࠪᰃ")
    except Exception as e:
        logger.debug(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡩ࡯ࡳࡵࡴࡲࠤࡴ࡬ࠠ࡭࡫ࡱࡹࡽࠨᰄ") + e)
@measure(event_name=EVENTS.bstack111ll1l1l1l_opy_, stage=STAGE.bstack11ll1111_opy_)
def bstack111ll1ll11l_opy_(bstack111l1l11l1l_opy_, bstack111ll11111l_opy_):
    logger.debug(bstack1ll111_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱ࠿ࠦࠢᰅ") + str(bstack111l1l11l1l_opy_) + bstack1ll111_opy_ (u"ࠨࠢᰆ"))
    zip_path = os.path.join(bstack111ll11111l_opy_, bstack1ll111_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡣ࡫࡯࡬ࡦ࠰ࡽ࡭ࡵࠨᰇ"))
    bstack111l1llllll_opy_ = bstack1ll111_opy_ (u"ࠨࠩᰈ")
    with requests.get(bstack111l1l11l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll111_opy_ (u"ࠤࡺࡦࠧᰉ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll111_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠧᰊ"))
    with zipfile.ZipFile(zip_path, bstack1ll111_opy_ (u"ࠫࡷ࠭ᰋ")) as zip_ref:
        bstack111ll1l1l11_opy_ = zip_ref.namelist()
        if len(bstack111ll1l1l11_opy_) > 0:
            bstack111l1llllll_opy_ = bstack111ll1l1l11_opy_[0] # bstack111llll1l11_opy_ bstack111lll1l1ll_opy_ will be bstack11l1111l1ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111ll11111l_opy_)
        logger.debug(bstack1ll111_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦᰌ") + str(bstack111ll11111l_opy_) + bstack1ll111_opy_ (u"ࠨࠧࠣᰍ"))
    os.remove(zip_path)
    return bstack111l1llllll_opy_
def get_cli_dir():
    bstack111l11llll1_opy_ = bstack1l1111ll1ll_opy_()
    if bstack111l11llll1_opy_:
        bstack1llll1ll111_opy_ = os.path.join(bstack111l11llll1_opy_, bstack1ll111_opy_ (u"ࠢࡤ࡮࡬ࠦᰎ"))
        if not os.path.exists(bstack1llll1ll111_opy_):
            os.makedirs(bstack1llll1ll111_opy_, mode=0o777, exist_ok=True)
        return bstack1llll1ll111_opy_
    else:
        raise FileNotFoundError(bstack1ll111_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦᰏ"))
def bstack1llll1l1l11_opy_(bstack1llll1ll111_opy_):
    bstack1ll111_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨᰐ")
    bstack111l1ll1111_opy_ = [
        os.path.join(bstack1llll1ll111_opy_, f)
        for f in os.listdir(bstack1llll1ll111_opy_)
        if os.path.isfile(os.path.join(bstack1llll1ll111_opy_, f)) and f.startswith(bstack1ll111_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦᰑ"))
    ]
    if len(bstack111l1ll1111_opy_) > 0:
        return max(bstack111l1ll1111_opy_, key=os.path.getmtime) # get bstack111lll1111l_opy_ binary
    return bstack1ll111_opy_ (u"ࠦࠧᰒ")
def bstack111ll111lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l11111l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l11111l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll11lll_opy_(data, keys, default=None):
    bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᰓ")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default
def bstack1l111l11l_opy_(bstack111ll11l1l1_opy_, key, value):
    bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧᰔ")
    if key in bstack111ll1ll1_opy_:
        bstack111llll1ll_opy_ = bstack111ll1ll1_opy_[key]
        if isinstance(bstack111llll1ll_opy_, list):
            for env_name in bstack111llll1ll_opy_:
                bstack111ll11l1l1_opy_[env_name] = value
        else:
            bstack111ll11l1l1_opy_[bstack111llll1ll_opy_] = value