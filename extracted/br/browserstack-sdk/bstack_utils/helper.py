# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
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
from bstack_utils.constants import (bstack1111ll1l1_opy_, bstack11ll1l1lll_opy_, bstack1llllllll1_opy_,
                                    bstack111111ll11l_opy_, bstack111111l11ll_opy_, bstack111111l1l1l_opy_, bstack11111l111ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11ll11ll_opy_, bstack1l1ll111_opy_
from bstack_utils.proxy import bstack1111ll1l1l_opy_, bstack1l1llll111_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11111111l1_opy_ import bstack111l1l1l1l_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1ll11ll111_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111ll1llll_opy_(config):
    return config[bstack1l111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭↊")]
def bstack1111l1l1lll_opy_(config):
    return config[bstack1l111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ↋")]
def bstack111ll1111_opy_():
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
def bstack1lllll11111l_opy_(obj):
    values = []
    bstack1llll11l1111_opy_ = re.compile(bstack1l111l_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥ↌"), re.I)
    for key in obj.keys():
        if bstack1llll11l1111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1lllll1lll1l_opy_(config):
    tags = []
    tags.extend(bstack1lllll11111l_opy_(os.environ))
    tags.extend(bstack1lllll11111l_opy_(config))
    return tags
def bstack1llll1l1l1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llll111ll11_opy_(bstack1lllll11ll1l_opy_):
    if not bstack1lllll11ll1l_opy_:
        return bstack1l111l_opy_ (u"ࠧࠨ↍")
    return bstack1l111l_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤ↎").format(bstack1lllll11ll1l_opy_.name, bstack1lllll11ll1l_opy_.email)
def bstack1111lll11ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1llll11ll11l_opy_ = repo.common_dir
        info = {
            bstack1l111l_opy_ (u"ࠤࡶ࡬ࡦࠨ↏"): repo.head.commit.hexsha,
            bstack1l111l_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨ←"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l111l_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦ↑"): repo.active_branch.name,
            bstack1l111l_opy_ (u"ࠧࡺࡡࡨࠤ→"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤ↓"): bstack1llll111ll11_opy_(repo.head.commit.committer),
            bstack1l111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣ↔"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l111l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣ↕"): bstack1llll111ll11_opy_(repo.head.commit.author),
            bstack1l111l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢ↖"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ↗"): repo.head.commit.message,
            bstack1l111l_opy_ (u"ࠦࡷࡵ࡯ࡵࠤ↘"): repo.git.rev_parse(bstack1l111l_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢ↙")),
            bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ↚"): bstack1llll11ll11l_opy_,
            bstack1l111l_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ↛"): subprocess.check_output([bstack1l111l_opy_ (u"ࠣࡩ࡬ࡸࠧ↜"), bstack1l111l_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧ↝"), bstack1l111l_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨ↞")]).strip().decode(
                bstack1l111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ↟")),
            bstack1l111l_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ↠"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣ↡"): repo.git.rev_list(
                bstack1l111l_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢ↢").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1llllll11l1l_opy_ = []
        for remote in remotes:
            bstack1lllllll11l1_opy_ = {
                bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ↣"): remote.name,
                bstack1l111l_opy_ (u"ࠤࡸࡶࡱࠨ↤"): remote.url,
            }
            bstack1llllll11l1l_opy_.append(bstack1lllllll11l1_opy_)
        bstack1llllll1llll_opy_ = {
            bstack1l111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ↥"): bstack1l111l_opy_ (u"ࠦ࡬࡯ࡴࠣ↦"),
            **info,
            bstack1l111l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨ↧"): bstack1llllll11l1l_opy_
        }
        bstack1llllll1llll_opy_ = bstack1lllllll111l_opy_(bstack1llllll1llll_opy_)
        return bstack1llllll1llll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ↨").format(err))
        return {}
def bstack1llll1l1lll1_opy_(bstack1lllll11l111_opy_=None):
    bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࡦࡲ࡬ࡺࠢࡩࡳࡷࡳࡡࡵࡶࡨࡨࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡷࡶࡩࠥࡩࡡࡴࡧࡶࠤ࡫ࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡰ࡮ࡧࡩࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡩࡳࡱࡪࡥࡳࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡐࡲࡲࡪࡀࠠࡎࡱࡱࡳ࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬࠱ࠦࡵࡴࡧࡶࠤࡨࡻࡲࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡴࡹࡿࠠ࡭࡫ࡶࡸࠥࡡ࡝࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦ࡮ࡰࠢࡶࡳࡺࡸࡣࡦࡵࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠬࠡࡴࡨࡸࡺࡸ࡮ࡴࠢ࡞ࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡴࡰࠢࡤࡲࡦࡲࡹࡻࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡨ࡮ࡩࡴࡴ࠮ࠣࡩࡦࡩࡨࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡣࠣࡪࡴࡲࡤࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ↩")
    if bstack1lllll11l111_opy_ is None:
        bstack1lllll11l111_opy_ = [os.getcwd()]
    elif isinstance(bstack1lllll11l111_opy_, list) and len(bstack1lllll11l111_opy_) == 0:
        return []
    results = []
    for folder in bstack1lllll11l111_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l111l_opy_ (u"ࠣࡈࡲࡰࡩ࡫ࡲࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨ↪").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l111l_opy_ (u"ࠤࡳࡶࡎࡪࠢ↫"): bstack1l111l_opy_ (u"ࠥࠦ↬"),
                bstack1l111l_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ↭"): [],
                bstack1l111l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ↮"): [],
                bstack1l111l_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨ↯"): bstack1l111l_opy_ (u"ࠢࠣ↰"),
                bstack1l111l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤ↱"): [],
                bstack1l111l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ↲"): bstack1l111l_opy_ (u"ࠥࠦ↳"),
                bstack1l111l_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ↴"): bstack1l111l_opy_ (u"ࠧࠨ↵"),
                bstack1l111l_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤ↶"): bstack1l111l_opy_ (u"ࠢࠣ↷")
            }
            bstack1lllll111l1l_opy_ = repo.active_branch.name
            bstack1llllll1111l_opy_ = repo.head.commit
            result[bstack1l111l_opy_ (u"ࠣࡲࡵࡍࡩࠨ↸")] = bstack1llllll1111l_opy_.hexsha
            bstack1llll111l111_opy_ = _1llllll1lll1_opy_(repo)
            logger.debug(bstack1l111l_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥ↹") + str(bstack1llll111l111_opy_) + bstack1l111l_opy_ (u"ࠥࠦ↺"))
            if bstack1llll111l111_opy_:
                try:
                    bstack1llll111111l_opy_ = repo.git.diff(bstack1l111l_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤ↻"), bstack1l1l1llll11_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥ↼")).split(bstack1l111l_opy_ (u"࠭࡜࡯ࠩ↽"))
                    logger.debug(bstack1l111l_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥ↾") + str(bstack1llll111111l_opy_) + bstack1l111l_opy_ (u"ࠣࠤ↿"))
                    result[bstack1l111l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ⇀")] = [f.strip() for f in bstack1llll111111l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1l1llll11_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢ⇁")))
                except Exception:
                    logger.debug(bstack1l111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦ⇂"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ⇃")] = _1llll11lllll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l111l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧ⇄")] = _1llll11lllll_opy_(commits[:5])
            bstack1lllll11l1l1_opy_ = set()
            bstack1llll111l1l1_opy_ = []
            for commit in commits:
                logger.debug(bstack1l111l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨ⇅") + str(commit.message) + bstack1l111l_opy_ (u"ࠣࠤ⇆"))
                bstack1llll11llll1_opy_ = commit.author.name if commit.author else bstack1l111l_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥ⇇")
                bstack1lllll11l1l1_opy_.add(bstack1llll11llll1_opy_)
                bstack1llll111l1l1_opy_.append({
                    bstack1l111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ⇈"): commit.message.strip(),
                    bstack1l111l_opy_ (u"ࠦࡺࡹࡥࡳࠤ⇉"): bstack1llll11llll1_opy_
                })
            result[bstack1l111l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ⇊")] = list(bstack1lllll11l1l1_opy_)
            result[bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢ⇋")] = bstack1llll111l1l1_opy_
            result[bstack1l111l_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢ⇌")] = bstack1llllll1111l_opy_.committed_datetime.strftime(bstack1l111l_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠥ⇍"))
            if (not result[bstack1l111l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥ⇎")] or result[bstack1l111l_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦ⇏")].strip() == bstack1l111l_opy_ (u"ࠦࠧ⇐")) and bstack1llllll1111l_opy_.message:
                bstack1lllll1l1ll1_opy_ = bstack1llllll1111l_opy_.message.strip().splitlines()
                result[bstack1l111l_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ⇑")] = bstack1lllll1l1ll1_opy_[0] if bstack1lllll1l1ll1_opy_ else bstack1l111l_opy_ (u"ࠨࠢ⇒")
                if len(bstack1lllll1l1ll1_opy_) > 2:
                    result[bstack1l111l_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ⇓")] = bstack1l111l_opy_ (u"ࠨ࡞ࡱࠫ⇔").join(bstack1lllll1l1ll1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࢁ࠮ࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ⇕").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1llll1111lll_opy_ = [
        result
        for result in results
        if _1lllll1llll1_opy_(result)
    ]
    return bstack1llll1111lll_opy_
def _1lllll1llll1_opy_(result):
    bstack1l111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡪࡲࡰࡦࡴࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡸࡻ࡬ࡵࠢ࡬ࡷࠥࡼࡡ࡭࡫ࡧࠤ࠭ࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠡࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠠࡢࡰࡧࠤࡦࡻࡴࡩࡱࡵࡷ࠮࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⇖")
    return (
        isinstance(result.get(bstack1l111l_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ⇗"), None), list)
        and len(result[bstack1l111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ⇘")]) > 0
        and isinstance(result.get(bstack1l111l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ⇙"), None), list)
        and len(result[bstack1l111l_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣ⇚")]) > 0
    )
def _1llllll1lll1_opy_(repo):
    bstack1l111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡵࡽࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡮ࡥࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡲࡦࡲࡲࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡮ࡡࡳࡦࡦࡳࡩ࡫ࡤࠡࡰࡤࡱࡪࡹࠠࡢࡰࡧࠤࡼࡵࡲ࡬ࠢࡺ࡭ࡹ࡮ࠠࡢ࡮࡯ࠤ࡛ࡉࡓࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࡶ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡥࡧࡩࡥࡺࡲࡴࠡࡤࡵࡥࡳࡩࡨࠡ࡫ࡩࠤࡵࡵࡳࡴ࡫ࡥࡰࡪ࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⇛")
    try:
        try:
            origin = repo.remotes.origin
            bstack1llll11l111l_opy_ = origin.refs[bstack1l111l_opy_ (u"ࠩࡋࡉࡆࡊࠧ⇜")]
            target = bstack1llll11l111l_opy_.reference.name
            if target.startswith(bstack1l111l_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ⇝")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l111l_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬ⇞")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1llll11lllll_opy_(commits):
    bstack1l111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ⇟")
    bstack1llll111111l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1llll11ll1l1_opy_ in diff:
                        if bstack1llll11ll1l1_opy_.a_path:
                            bstack1llll111111l_opy_.add(bstack1llll11ll1l1_opy_.a_path)
                        if bstack1llll11ll1l1_opy_.b_path:
                            bstack1llll111111l_opy_.add(bstack1llll11ll1l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llll111111l_opy_)
def bstack1lllllll111l_opy_(bstack1llllll1llll_opy_):
    bstack1llllll1ll11_opy_ = bstack1llll11l11ll_opy_(bstack1llllll1llll_opy_)
    if bstack1llllll1ll11_opy_ and bstack1llllll1ll11_opy_ > bstack111111ll11l_opy_:
        bstack1lllll1ll1ll_opy_ = bstack1llllll1ll11_opy_ - bstack111111ll11l_opy_
        bstack1llll1lllll1_opy_ = bstack1llll1ll11l1_opy_(bstack1llllll1llll_opy_[bstack1l111l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ⇠")], bstack1lllll1ll1ll_opy_)
        bstack1llllll1llll_opy_[bstack1l111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ⇡")] = bstack1llll1lllll1_opy_
        logger.info(bstack1l111l_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ⇢")
                    .format(bstack1llll11l11ll_opy_(bstack1llllll1llll_opy_) / 1024))
    return bstack1llllll1llll_opy_
def bstack1llll11l11ll_opy_(json_data):
    try:
        if json_data:
            bstack1llll11l1l1l_opy_ = json.dumps(json_data)
            bstack1llll111l11l_opy_ = sys.getsizeof(bstack1llll11l1l1l_opy_)
            return bstack1llll111l11l_opy_
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ⇣").format(e))
    return -1
def bstack1llll1ll11l1_opy_(field, bstack1lllll1lll11_opy_):
    try:
        bstack1lllll1l1lll_opy_ = len(bytes(bstack111111l11ll_opy_, bstack1l111l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⇤")))
        bstack1llllll1l111_opy_ = bytes(field, bstack1l111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⇥"))
        bstack1llll1ll111l_opy_ = len(bstack1llllll1l111_opy_)
        bstack1llllll11lll_opy_ = ceil(bstack1llll1ll111l_opy_ - bstack1lllll1lll11_opy_ - bstack1lllll1l1lll_opy_)
        if bstack1llllll11lll_opy_ > 0:
            bstack1lllll1ll1l1_opy_ = bstack1llllll1l111_opy_[:bstack1llllll11lll_opy_].decode(bstack1l111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⇦"), errors=bstack1l111l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭⇧")) + bstack111111l11ll_opy_
            return bstack1lllll1ll1l1_opy_
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧ⇨").format(e))
    return field
def bstack1l111ll1l1_opy_():
    env = os.environ
    if (bstack1l111l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ⇩") in env and len(env[bstack1l111l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ⇪")]) > 0) or (
            bstack1l111l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ⇫") in env and len(env[bstack1l111l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ⇬")]) > 0):
        return {
            bstack1l111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⇭"): bstack1l111l_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢ⇮"),
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⇯"): env.get(bstack1l111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⇰")),
            bstack1l111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⇱"): env.get(bstack1l111l_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⇲")),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⇳"): env.get(bstack1l111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ⇴"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠨࡃࡊࠤ⇵")) == bstack1l111l_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇶") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ⇷"))):
        return {
            bstack1l111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⇸"): bstack1l111l_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ⇹"),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⇺"): env.get(bstack1l111l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ⇻")),
            bstack1l111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⇼"): env.get(bstack1l111l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ⇽")),
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⇾"): env.get(bstack1l111l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ⇿"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠥࡇࡎࠨ∀")) == bstack1l111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ∁") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ∂"))):
        return {
            bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ∃"): bstack1l111l_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ∄"),
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ∅"): env.get(bstack1l111l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ∆")),
            bstack1l111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ∇"): env.get(bstack1l111l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ∈")),
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∉"): env.get(bstack1l111l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ∊"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠢࡄࡋࠥ∋")) == bstack1l111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ∌") and env.get(bstack1l111l_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ∍")) == bstack1l111l_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ∎"):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ∏"): bstack1l111l_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ∐"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ∑"): None,
            bstack1l111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ−"): None,
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ∓"): None
        }
    if env.get(bstack1l111l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ∔")) and env.get(bstack1l111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ∕")):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ∖"): bstack1l111l_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ∗"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ∘"): env.get(bstack1l111l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧ∙")),
            bstack1l111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ√"): None,
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ∛"): env.get(bstack1l111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ∜"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠦࡈࡏࠢ∝")) == bstack1l111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ∞") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ∟"))):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∠"): bstack1l111l_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ∡"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∢"): env.get(bstack1l111l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ∣")),
            bstack1l111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∤"): None,
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∥"): env.get(bstack1l111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ∦"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠢࡄࡋࠥ∧")) == bstack1l111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ∨") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ∩"))):
        return {
            bstack1l111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ∪"): bstack1l111l_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ∫"),
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∬"): env.get(bstack1l111l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ∭")),
            bstack1l111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ∮"): env.get(bstack1l111l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ∯")),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ∰"): env.get(bstack1l111l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨ∱"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠦࡈࡏࠢ∲")) == bstack1l111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ∳") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ∴"))):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∵"): bstack1l111l_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ∶"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∷"): env.get(bstack1l111l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ∸")),
            bstack1l111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∹"): env.get(bstack1l111l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ∺")),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ∻"): env.get(bstack1l111l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥ∼"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠣࡅࡌࠦ∽")) == bstack1l111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ∾") and bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨ∿"))):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≀"): bstack1l111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣ≁"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≂"): env.get(bstack1l111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ≃")),
            bstack1l111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ≄"): env.get(bstack1l111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦ≅")) or env.get(bstack1l111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨ≆")),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ≇"): env.get(bstack1l111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ≈"))
        }
    if bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ≉"))):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≊"): bstack1l111l_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣ≋"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≌"): bstack1l111l_opy_ (u"ࠥࡿࢂࢁࡽࠣ≍").format(env.get(bstack1l111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ≎")), env.get(bstack1l111l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬ≏"))),
            bstack1l111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≐"): env.get(bstack1l111l_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨ≑")),
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≒"): env.get(bstack1l111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ≓"))
        }
    if bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧ≔"))):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≕"): bstack1l111l_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢ≖"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≗"): bstack1l111l_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨ≘").format(env.get(bstack1l111l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧ≙")), env.get(bstack1l111l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪ≚")), env.get(bstack1l111l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫ≛")), env.get(bstack1l111l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ≜"))),
            bstack1l111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ≝"): env.get(bstack1l111l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ≞")),
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ≟"): env.get(bstack1l111l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ≠"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥ≡")) and env.get(bstack1l111l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ≢")):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≣"): bstack1l111l_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢ≤"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≥"): bstack1l111l_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥ≦").format(env.get(bstack1l111l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ≧")), env.get(bstack1l111l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧ≨")), env.get(bstack1l111l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ≩"))),
            bstack1l111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≪"): env.get(bstack1l111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ≫")),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≬"): env.get(bstack1l111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ≭"))
        }
    if any([env.get(bstack1l111l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ≮")), env.get(bstack1l111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ≯")), env.get(bstack1l111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ≰"))]):
        return {
            bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≱"): bstack1l111l_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ≲"),
            bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ≳"): env.get(bstack1l111l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ≴")),
            bstack1l111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ≵"): env.get(bstack1l111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ≶")),
            bstack1l111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ≷"): env.get(bstack1l111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ≸"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ≹")):
        return {
            bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ≺"): bstack1l111l_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ≻"),
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ≼"): env.get(bstack1l111l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ≽")),
            bstack1l111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ≾"): env.get(bstack1l111l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ≿")),
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊀"): env.get(bstack1l111l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ⊁"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ⊂")) or env.get(bstack1l111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ⊃")):
        return {
            bstack1l111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⊄"): bstack1l111l_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ⊅"),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⊆"): env.get(bstack1l111l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ⊇")),
            bstack1l111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⊈"): bstack1l111l_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ⊉") if env.get(bstack1l111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ⊊")) else None,
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊋"): env.get(bstack1l111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ⊌"))
        }
    if any([env.get(bstack1l111l_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ⊍")), env.get(bstack1l111l_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ⊎")), env.get(bstack1l111l_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ⊏"))]):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊐"): bstack1l111l_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ⊑"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊒"): None,
            bstack1l111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⊓"): env.get(bstack1l111l_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ⊔")),
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊕"): env.get(bstack1l111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ⊖"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ⊗")):
        return {
            bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊘"): bstack1l111l_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ⊙"),
            bstack1l111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊚"): env.get(bstack1l111l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⊛")),
            bstack1l111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊜"): bstack1l111l_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ⊝").format(env.get(bstack1l111l_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ⊞"))) if env.get(bstack1l111l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ⊟")) else None,
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊠"): env.get(bstack1l111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ⊡"))
        }
    if bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ⊢"))):
        return {
            bstack1l111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊣"): bstack1l111l_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ⊤"),
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊥"): env.get(bstack1l111l_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ⊦")),
            bstack1l111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊧"): env.get(bstack1l111l_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ⊨")),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⊩"): env.get(bstack1l111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ⊪"))
        }
    if bstack111111lll1_opy_(env.get(bstack1l111l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ⊫"))):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⊬"): bstack1l111l_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ⊭"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⊮"): bstack1l111l_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ⊯").format(env.get(bstack1l111l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ⊰")), env.get(bstack1l111l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ⊱")), env.get(bstack1l111l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭⊲"))),
            bstack1l111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ⊳"): env.get(bstack1l111l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥ⊴")),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⊵"): env.get(bstack1l111l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥ⊶"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠦࡈࡏࠢ⊷")) == bstack1l111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⊸") and env.get(bstack1l111l_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ⊹")) == bstack1l111l_opy_ (u"ࠢ࠲ࠤ⊺"):
        return {
            bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊻"): bstack1l111l_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ⊼"),
            bstack1l111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊽"): bstack1l111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ⊾").format(env.get(bstack1l111l_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩ⊿"))),
            bstack1l111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⋀"): None,
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋁"): None,
        }
    if env.get(bstack1l111l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ⋂")):
        return {
            bstack1l111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⋃"): bstack1l111l_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ⋄"),
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⋅"): None,
            bstack1l111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⋆"): env.get(bstack1l111l_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ⋇")),
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋈"): env.get(bstack1l111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ⋉"))
        }
    if any([env.get(bstack1l111l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ⋊")), env.get(bstack1l111l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ⋋")), env.get(bstack1l111l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ⋌")), env.get(bstack1l111l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ⋍"))]):
        return {
            bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⋎"): bstack1l111l_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ⋏"),
            bstack1l111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⋐"): None,
            bstack1l111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⋑"): env.get(bstack1l111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⋒")) or None,
            bstack1l111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⋓"): env.get(bstack1l111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ⋔"), 0)
        }
    if env.get(bstack1l111l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ⋕")):
        return {
            bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⋖"): bstack1l111l_opy_ (u"ࠣࡉࡲࡇࡉࠨ⋗"),
            bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⋘"): None,
            bstack1l111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⋙"): env.get(bstack1l111l_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⋚")),
            bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⋛"): env.get(bstack1l111l_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧ⋜"))
        }
    if env.get(bstack1l111l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ⋝")):
        return {
            bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ⋞"): bstack1l111l_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ⋟"),
            bstack1l111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⋠"): env.get(bstack1l111l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⋡")),
            bstack1l111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⋢"): env.get(bstack1l111l_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ⋣")),
            bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⋤"): env.get(bstack1l111l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⋥"))
        }
    return {bstack1l111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⋦"): None}
def get_host_info():
    return {
        bstack1l111l_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ⋧"): platform.node(),
        bstack1l111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ⋨"): platform.system(),
        bstack1l111l_opy_ (u"ࠧࡺࡹࡱࡧࠥ⋩"): platform.machine(),
        bstack1l111l_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⋪"): platform.version(),
        bstack1l111l_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ⋫"): platform.architecture()[0]
    }
def bstack111l1111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1lllll11l11l_opy_():
    if global_config.get_property(bstack1l111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ⋬")):
        return bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⋭")
    return bstack1l111l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ⋮")
def bstack1ll1l1ll1l1_opy_(driver):
    info = {
        bstack1l111l_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⋯"): driver.capabilities,
        bstack1l111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ⋰"): driver.session_id,
        bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ⋱"): driver.capabilities.get(bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ⋲"), None),
        bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ⋳"): driver.capabilities.get(bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⋴"), None),
        bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ⋵"): driver.capabilities.get(bstack1l111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ⋶"), None),
        bstack1l111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⋷"):driver.capabilities.get(bstack1l111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⋸"), None),
    }
    if bstack1lllll11l11l_opy_() == bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⋹"):
        if bstack11l11l1l11_opy_():
            info[bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ⋺")] = bstack1l111l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⋻")
        elif driver.capabilities.get(bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ⋼"), {}).get(bstack1l111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⋽"), False):
            info[bstack1l111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⋾")] = bstack1l111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⋿")
        else:
            info[bstack1l111l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ⌀")] = bstack1l111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⌁")
    return info
def bstack11l11l1l11_opy_():
    if global_config.get_property(bstack1l111l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⌂")):
        return True
    if bstack111111lll1_opy_(os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⌃"), None)):
        return True
    return False
def bstack1llll1l1ll1l_opy_(bstack1llll1l11l1l_opy_, url, response, headers=None, data=None):
    bstack1l111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡇࡻࡩ࡭ࡦࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹ࠵ࡲࡦࡵࡳࡳࡳࡹࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡳࡸࡩࡸࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧࠤ࠭ࡍࡅࡕ࠮ࠣࡔࡔ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡸࡶࡱࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡗࡕࡐ࠴࡫࡮ࡥࡲࡲ࡭ࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡷ࡫ࡱࡶࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡩࡧࡤࡨࡪࡸࡳ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣ࡬ࡪࡧࡤࡦࡴࡶࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡢࡶࡤ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡊࡔࡑࡑࠤࡩࡧࡴࡢࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠣࡻ࡮ࡺࡨࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠐࠠࠡࠢࠣࠦࠧࠨ⌄")
    bstack1llll1l1llll_opy_ = {
        bstack1l111l_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ⌅"): headers,
        bstack1l111l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ⌆"): bstack1llll1l11l1l_opy_.upper(),
        bstack1l111l_opy_ (u"ࠢࡢࡩࡨࡲࡹࠨ⌇"): None,
        bstack1l111l_opy_ (u"ࠣࡧࡱࡨࡵࡵࡩ࡯ࡶࠥ⌈"): url,
        bstack1l111l_opy_ (u"ࠤ࡭ࡷࡴࡴࠢ⌉"): data
    }
    try:
        bstack1lllll1lllll_opy_ = response.json()
        if isinstance(bstack1lllll1lllll_opy_, dict) and bstack1lllll1lllll_opy_.get(bstack1l111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⌊"), {}).get(bstack1l111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⌋"), {}).get(bstack1l111l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⌌")):
            bstack1llll11lll11_opy_ = json.loads(json.dumps(bstack1lllll1lllll_opy_))
            bstack1llll11lll11_opy_[bstack1l111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⌍")][bstack1l111l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⌎")][bstack1l111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ⌏")] = bstack1l111l_opy_ (u"ࠤ࡞ࡶࡪࡪࡡࡤࡶࡨࡨࠥ࡬࡯ࡳࠢࡥࡶࡪࡼࡩࡵࡻࡠࠦ⌐")
            bstack1lllll1lllll_opy_ = bstack1llll11lll11_opy_
    except Exception:
        bstack1lllll1lllll_opy_ = response.text
    bstack1llll1111111_opy_ = {
        bstack1l111l_opy_ (u"ࠥࡦࡴࡪࡹࠣ⌑"): bstack1lllll1lllll_opy_,
        bstack1l111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࡇࡴࡪࡥࠣ⌒"): response.status_code
    }
    return {
        bstack1l111l_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ⌓"): bstack1llll1l1llll_opy_,
        bstack1l111l_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ⌔"): bstack1llll1111111_opy_
    }
def bstack11l1ll1ll1_opy_(bstack1llll1l11l1l_opy_, url, data, config):
    headers = config.get(bstack1l111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⌕"), None)
    proxies = bstack1111ll1l1l_opy_(config, url)
    auth = config.get(bstack1l111l_opy_ (u"ࠨࡣࡸࡸ࡭࠭⌖"), None)
    response = requests.request(
            bstack1llll1l11l1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1llll1l1ll1l_opy_(bstack1llll1l11l1l_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1l111l_opy_ (u"ࠩ࠯ࠫ⌗"), bstack1l111l_opy_ (u"ࠪ࠾ࠬ⌘"))))
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࡾࢁࠧ⌙").format(e))
    return response
def bstack1llllll1ll1_opy_(bstack1ll1ll1l1_opy_, size):
    bstack1ll1ll111l_opy_ = []
    while len(bstack1ll1ll1l1_opy_) > size:
        bstack11l1ll1lll_opy_ = bstack1ll1ll1l1_opy_[:size]
        bstack1ll1ll111l_opy_.append(bstack11l1ll1lll_opy_)
        bstack1ll1ll1l1_opy_ = bstack1ll1ll1l1_opy_[size:]
    bstack1ll1ll111l_opy_.append(bstack1ll1ll1l1_opy_)
    return bstack1ll1ll111l_opy_
def bstack1llllll11ll1_opy_(message, bstack1llllll1ll1l_opy_=False):
    os.write(1, bytes(message, bstack1l111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⌚")))
    os.write(1, bytes(bstack1l111l_opy_ (u"࠭࡜࡯ࠩ⌛"), bstack1l111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⌜")))
    if bstack1llllll1ll1l_opy_:
        with open(bstack1l111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ⌝") + os.environ[bstack1l111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⌞")] + bstack1l111l_opy_ (u"ࠪ࠲ࡱࡵࡧࠨ⌟"), bstack1l111l_opy_ (u"ࠫࡦ࠭⌠")) as f:
            f.write(message + bstack1l111l_opy_ (u"ࠬࡢ࡮ࠨ⌡"))
def bstack11ll1l1l1l_opy_():
    return os.environ[bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌢")].lower() == bstack1l111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ⌣")
def bstack111111l1l_opy_():
    return bstack1lll11ll11l_opy_().replace(tzinfo=None).isoformat() + bstack1l111l_opy_ (u"ࠨ࡜ࠪ⌤")
def bstack1ll1ll1l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l111l_opy_ (u"ࠩ࡝ࠫ⌥"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l111l_opy_ (u"ࠪ࡞ࠬ⌦")))).total_seconds() * 1000
def bstack1lllll1111ll_opy_(timestamp):
    return bstack1lllll111ll1_opy_(timestamp).isoformat() + bstack1l111l_opy_ (u"ࠫ࡟࠭⌧")
def bstack1llll11111l1_opy_(bstack1llll1l1l1l1_opy_):
    date_format = bstack1l111l_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ⌨")
    bstack1lllll1l111l_opy_ = datetime.datetime.strptime(bstack1llll1l1l1l1_opy_, date_format)
    return bstack1lllll1l111l_opy_.isoformat() + bstack1l111l_opy_ (u"࡚࠭ࠨ〈")
def bstack1llll1ll1lll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ〉")
    else:
        return bstack1l111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⌫")
def bstack111111lll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⌬")
def bstack1lllll1ll111_opy_(val):
    return val.__str__().lower() == bstack1l111l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ⌭")
def error_handler(bstack1llll1ll11ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll1ll11ll_opy_ as e:
                print(bstack1l111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ⌮").format(func.__name__, bstack1llll1ll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1llll111lll1_opy_(bstack1llllll1l11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llllll1l11l_opy_(cls, *args, **kwargs)
            except bstack1llll1ll11ll_opy_ as e:
                print(bstack1l111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧ⌯").format(bstack1llllll1l11l_opy_.__name__, bstack1llll1ll11ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1llll111lll1_opy_
    else:
        return decorator
def bstack11llll1lll_opy_(bstack1llll1lll11_opy_):
    if os.getenv(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ⌰")) is not None:
        return bstack111111lll1_opy_(os.getenv(bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ⌱")))
    if bstack1l111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌲") in bstack1llll1lll11_opy_ and bstack1lllll1ll111_opy_(bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⌳")]):
        return False
    if bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⌴") in bstack1llll1lll11_opy_ and bstack1lllll1ll111_opy_(bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⌵")]):
        return False
    return True
def bstack11l1l1ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1llll1l1l11l_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧ⌶"), None)
        return bstack1llll1l1l11l_opy_ is None or bstack1llll1l1l11l_opy_ == bstack1l111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ⌷")
    except Exception as e:
        return False
def bstack1l1lll111l_opy_(hub_url, CONFIG):
    if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l111l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⌸")):
        if hub_url:
            return bstack1l111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⌹") + hub_url + bstack1l111l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⌺")
        return bstack11ll1l1lll_opy_
    if hub_url:
        return bstack1l111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⌻") + hub_url + bstack1l111l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⌼")
    return bstack1llllllll1_opy_
def bstack1llll111llll_opy_():
    return isinstance(os.getenv(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ⌽")), str)
def bstack1111ll111l_opy_(url):
    return urlparse(url).hostname
def bstack1ll11lll1l_opy_(hostname):
    for bstack11llll11l1_opy_ in bstack1111ll1l1_opy_:
        regex = re.compile(bstack11llll11l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1lll1llllll1_opy_(bstack1llll1l111l1_opy_, file_name, logger):
    bstack1ll1111l11_opy_ = os.path.join(os.path.expanduser(bstack1l111l_opy_ (u"࠭ࡾࠨ⌾")), bstack1llll1l111l1_opy_)
    try:
        if not os.path.exists(bstack1ll1111l11_opy_):
            os.makedirs(bstack1ll1111l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l111l_opy_ (u"ࠧࡿࠩ⌿")), bstack1llll1l111l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l111l_opy_ (u"ࠨࡹࠪ⍀")):
                pass
            with open(file_path, bstack1l111l_opy_ (u"ࠤࡺ࠯ࠧ⍁")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11ll11ll_opy_.format(str(e)))
def bstack1llll11l11l1_opy_(file_name, key, value, logger):
    file_path = bstack1lll1llllll1_opy_(bstack1l111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ⍂"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11ll1l11l1_opy_ = json.load(open(file_path, bstack1l111l_opy_ (u"ࠫࡷࡨࠧ⍃")))
        else:
            bstack11ll1l11l1_opy_ = {}
        bstack11ll1l11l1_opy_[key] = value
        with open(file_path, bstack1l111l_opy_ (u"ࠧࡽࠫࠣ⍄")) as outfile:
            json.dump(bstack11ll1l11l1_opy_, outfile)
def bstack11lllll1_opy_(file_name, logger):
    file_path = bstack1lll1llllll1_opy_(bstack1l111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⍅"), file_name, logger)
    bstack11ll1l11l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l111l_opy_ (u"ࠧࡳࠩ⍆")) as bstack11111lll1l_opy_:
            bstack11ll1l11l1_opy_ = json.load(bstack11111lll1l_opy_)
    return bstack11ll1l11l1_opy_
def bstack1ll1llll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ⍇") + file_path + bstack1l111l_opy_ (u"ࠩࠣࠫ⍈") + str(e))
def bstack1ll1l1ll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l111l_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ⍉")
def bstack1ll111lll1_opy_(config):
    if bstack1l111l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ⍊") in config:
        del (config[bstack1l111l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ⍋")])
        return False
    if bstack1ll1l1ll11_opy_() < version.parse(bstack1l111l_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬ⍌")):
        return False
    if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭⍍")):
        return True
    if bstack1l111l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⍎") in config and config[bstack1l111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⍏")] is False:
        return False
    else:
        return True
def bstack1l111l1ll1_opy_(args_list, bstack1lllll111lll_opy_):
    index = -1
    for value in bstack1lllll111lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111ll1ll1l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111ll1ll1l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll1l111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll1l111l_opy_ = bstack1llll1l111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⍐"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⍑"), exception=exception)
    def bstack1ll111l1l1l_opy_(self):
        if self.result != bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⍒"):
            return None
        if isinstance(self.exception_type, str) and bstack1l111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ⍓") in self.exception_type:
            return bstack1l111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ⍔")
        return bstack1l111l_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ⍕")
    def bstack1llll1ll1l11_opy_(self):
        if self.result != bstack1l111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⍖"):
            return None
        if self.bstack1llll1l111l_opy_:
            return self.bstack1llll1l111l_opy_
        return bstack1lllll11ll11_opy_(self.exception)
def bstack1lllll11ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llll11lll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l111l11l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111l11lll_opy_(config, logger):
    try:
        import playwright
        bstack1lllll111l11_opy_ = playwright.__file__
        bstack1llll1ll1l1l_opy_ = os.path.split(bstack1lllll111l11_opy_)
        bstack1lllll111111_opy_ = bstack1llll1ll1l1l_opy_[0] + bstack1l111l_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭⍗")
        os.environ[bstack1l111l_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧ⍘")] = bstack1l1llll111_opy_(config)
        with open(bstack1lllll111111_opy_, bstack1l111l_opy_ (u"ࠬࡸࠧ⍙")) as f:
            file_content = f.read()
            bstack1llll1111l11_opy_ = bstack1l111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ⍚")
            bstack1lllll11l1ll_opy_ = file_content.find(bstack1llll1111l11_opy_)
            if bstack1lllll11l1ll_opy_ == -1:
              process = subprocess.Popen(bstack1l111l_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦ⍛"), shell=True, cwd=bstack1llll1ll1l1l_opy_[0])
              process.wait()
              bstack1lllll1l1l1l_opy_ = bstack1l111l_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ⍜")
              bstack1lllll11llll_opy_ = bstack1l111l_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ⍝")
              bstack1llll1ll1ll1_opy_ = file_content.replace(bstack1lllll1l1l1l_opy_, bstack1lllll11llll_opy_)
              with open(bstack1lllll111111_opy_, bstack1l111l_opy_ (u"ࠪࡻࠬ⍞")) as f:
                f.write(bstack1llll1ll1ll1_opy_)
    except Exception as e:
        logger.error(bstack1l1ll111_opy_.format(str(e)))
def bstack111l1l1111_opy_():
  try:
    bstack1llll1ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ⍟"))
    bstack1llll111l1ll_opy_ = []
    if os.path.exists(bstack1llll1ll1111_opy_):
      with open(bstack1llll1ll1111_opy_) as f:
        bstack1llll111l1ll_opy_ = json.load(f)
      os.remove(bstack1llll1ll1111_opy_)
    return bstack1llll111l1ll_opy_
  except:
    pass
  return []
def bstack11l11l1111_opy_(bstack111lll11ll_opy_):
  try:
    bstack1llll111l1ll_opy_ = []
    bstack1llll1ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ⍠"))
    if os.path.exists(bstack1llll1ll1111_opy_):
      with open(bstack1llll1ll1111_opy_) as f:
        bstack1llll111l1ll_opy_ = json.load(f)
    bstack1llll111l1ll_opy_.append(bstack111lll11ll_opy_)
    with open(bstack1llll1ll1111_opy_, bstack1l111l_opy_ (u"࠭ࡷࠨ⍡")) as f:
        json.dump(bstack1llll111l1ll_opy_, f)
  except:
    pass
def bstack11l1lll1l_opy_(logger, bstack1lllll1l1l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⍢"), bstack1l111l_opy_ (u"ࠨࠩ⍣"))
    if test_name == bstack1l111l_opy_ (u"ࠩࠪ⍤"):
        test_name = threading.current_thread().__dict__.get(bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ⍥"), bstack1l111l_opy_ (u"ࠫࠬ⍦"))
    bstack1llll1lll1ll_opy_ = bstack1l111l_opy_ (u"ࠬ࠲ࠠࠨ⍧").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1lllll1l1l11_opy_:
        bstack11111l1l1l_opy_ = os.environ.get(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⍨"), bstack1l111l_opy_ (u"ࠧ࠱ࠩ⍩"))
        bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⍪"): test_name, bstack1l111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⍫"): bstack1llll1lll1ll_opy_, bstack1l111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⍬"): bstack11111l1l1l_opy_}
        bstack1llll1l1111l_opy_ = []
        bstack1llll1l1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⍭"))
        if os.path.exists(bstack1llll1l1ll11_opy_):
            with open(bstack1llll1l1ll11_opy_) as f:
                bstack1llll1l1111l_opy_ = json.load(f)
        bstack1llll1l1111l_opy_.append(bstack11l1l11l1_opy_)
        with open(bstack1llll1l1ll11_opy_, bstack1l111l_opy_ (u"ࠬࡽࠧ⍮")) as f:
            json.dump(bstack1llll1l1111l_opy_, f)
    else:
        bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⍯"): test_name, bstack1l111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⍰"): bstack1llll1lll1ll_opy_, bstack1l111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⍱"): str(multiprocessing.current_process().name)}
        if bstack1l111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭⍲") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l1l11l1_opy_)
  except Exception as e:
      logger.warn(bstack1l111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⍳").format(e))
def bstack1l1llll11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l111l_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ⍴"))
    try:
      bstack1llllll111l1_opy_ = []
      bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍵"): test_name, bstack1l111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⍶"): error_message, bstack1l111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⍷"): index}
      bstack1llll11111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⍸"))
      if os.path.exists(bstack1llll11111ll_opy_):
          with open(bstack1llll11111ll_opy_) as f:
              bstack1llllll111l1_opy_ = json.load(f)
      bstack1llllll111l1_opy_.append(bstack11l1l11l1_opy_)
      with open(bstack1llll11111ll_opy_, bstack1l111l_opy_ (u"ࠩࡺࠫ⍹")) as f:
          json.dump(bstack1llllll111l1_opy_, f)
    except Exception as e:
      logger.warn(bstack1l111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⍺").format(e))
    return
  bstack1llllll111l1_opy_ = []
  bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⍻"): test_name, bstack1l111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⍼"): error_message, bstack1l111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⍽"): index}
  bstack1llll11111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⍾"))
  lock_file = bstack1llll11111ll_opy_ + bstack1l111l_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ⍿")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll11111ll_opy_):
          with open(bstack1llll11111ll_opy_, bstack1l111l_opy_ (u"ࠩࡵࠫ⎀")) as f:
              content = f.read().strip()
              if content:
                  bstack1llllll111l1_opy_ = json.load(open(bstack1llll11111ll_opy_))
      bstack1llllll111l1_opy_.append(bstack11l1l11l1_opy_)
      with open(bstack1llll11111ll_opy_, bstack1l111l_opy_ (u"ࠪࡻࠬ⎁")) as f:
          json.dump(bstack1llllll111l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1l111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦ⎂").format(e))
def bstack1111l1llll_opy_(bstack11l11111ll_opy_, name, logger):
  try:
    bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⎃"): name, bstack1l111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⎄"): bstack11l11111ll_opy_, bstack1l111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⎅"): str(threading.current_thread()._name)}
    return bstack11l1l11l1_opy_
  except Exception as e:
    logger.warn(bstack1l111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⎆").format(e))
  return
def bstack1llll11ll1ll_opy_():
    return platform.system() == bstack1l111l_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ⎇")
def bstack1111lll1l_opy_(bstack1llll1l11lll_opy_, config, logger):
    bstack1llllll111ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1llll1l11lll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⎈").format(e))
    return bstack1llllll111ll_opy_
def bstack1llll1l11111_opy_(bstack1llll1l11ll1_opy_, bstack1llll1111ll1_opy_):
    bstack1lllll1l11ll_opy_ = version.parse(bstack1llll1l11ll1_opy_)
    bstack1llll11l1l11_opy_ = version.parse(bstack1llll1111ll1_opy_)
    if bstack1lllll1l11ll_opy_ > bstack1llll11l1l11_opy_:
        return 1
    elif bstack1lllll1l11ll_opy_ < bstack1llll11l1l11_opy_:
        return -1
    else:
        return 0
def bstack1lll11ll11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllll111ll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll11l1ll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11lllllll1_opy_(options, framework, config, bstack111llll11l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l111l_opy_ (u"ࠫ࡬࡫ࡴࠨ⎉"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1llllll11l_opy_ = caps.get(bstack1l111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⎊"))
    bstack1llll1l11l11_opy_ = True
    bstack1ll1l111l_opy_ = os.environ[bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⎋")]
    bstack11lllll11ll_opy_ = config.get(bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⎌"), False)
    if bstack11lllll11ll_opy_:
        bstack1l11l111ll1_opy_ = config.get(bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎍"), {})
        bstack1l11l111ll1_opy_[bstack1l111l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ⎎")] = os.getenv(bstack1l111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⎏"))
        bstack11111l1111_opy_ = json.loads(os.getenv(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⎐"), bstack1l111l_opy_ (u"ࠬࢁࡽࠨ⎑"))).get(bstack1l111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⎒"))
    if bstack1lllll1ll111_opy_(caps.get(bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭⎓"))) or bstack1lllll1ll111_opy_(caps.get(bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ⎔"))):
        bstack1llll1l11l11_opy_ = False
    if bstack1ll111lll1_opy_({bstack1l111l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ⎕"): bstack1llll1l11l11_opy_}):
        bstack1llllll11l_opy_ = bstack1llllll11l_opy_ or {}
        bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⎖")] = bstack1llll11l1ll1_opy_(framework)
        bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⎗")] = bstack11ll1l1l1l_opy_()
        bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⎘")] = bstack1ll1l111l_opy_
        bstack1llllll11l_opy_[bstack1l111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⎙")] = bstack111llll11l_opy_
        if bstack11lllll11ll_opy_:
            bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⎚")] = bstack11lllll11ll_opy_
            bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎛")] = bstack1l11l111ll1_opy_
            bstack1llllll11l_opy_[bstack1l111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎜")][bstack1l111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⎝")] = bstack11111l1111_opy_
        if getattr(options, bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ⎞"), None):
            options.set_capability(bstack1l111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭⎟"), bstack1llllll11l_opy_)
        else:
            options[bstack1l111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⎠")] = bstack1llllll11l_opy_
    else:
        if getattr(options, bstack1l111l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⎡"), None):
            options.set_capability(bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎢"), bstack1llll11l1ll1_opy_(framework))
            options.set_capability(bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎣"), bstack11ll1l1l1l_opy_())
            options.set_capability(bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎤"), bstack1ll1l111l_opy_)
            options.set_capability(bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎥"), bstack111llll11l_opy_)
            if bstack11lllll11ll_opy_:
                options.set_capability(bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎦"), bstack11lllll11ll_opy_)
                options.set_capability(bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎧"), bstack1l11l111ll1_opy_)
                options.set_capability(bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⎨"), bstack11111l1111_opy_)
        else:
            options[bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎩")] = bstack1llll11l1ll1_opy_(framework)
            options[bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎪")] = bstack11ll1l1l1l_opy_()
            options[bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎫")] = bstack1ll1l111l_opy_
            options[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎬")] = bstack111llll11l_opy_
            if bstack11lllll11ll_opy_:
                options[bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎭")] = bstack11lllll11ll_opy_
                options[bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎮")] = bstack1l11l111ll1_opy_
                options[bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⎯")][bstack1l111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⎰")] = bstack11111l1111_opy_
    return options
def bstack1llllll1l1l1_opy_(ws_endpoint, framework):
    bstack111llll11l_opy_ = global_config.get_property(bstack1l111l_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ⎱"))
    if ws_endpoint and len(ws_endpoint.split(bstack1l111l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ⎲"))) > 1:
        ws_url = ws_endpoint.split(bstack1l111l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ⎳"))[0]
        if bstack1l111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ⎴") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1llll1llll11_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1l111l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⎵"))[1]))
            bstack1llll1llll11_opy_ = bstack1llll1llll11_opy_ or {}
            bstack1ll1l111l_opy_ = os.environ[bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⎶")]
            bstack1llll1llll11_opy_[bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⎷")] = str(framework) + str(__version__)
            bstack1llll1llll11_opy_[bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⎸")] = bstack11ll1l1l1l_opy_()
            bstack1llll1llll11_opy_[bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ⎹")] = bstack1ll1l111l_opy_
            bstack1llll1llll11_opy_[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ⎺")] = bstack111llll11l_opy_
            ws_endpoint = ws_endpoint.split(bstack1l111l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ⎻"))[0] + bstack1l111l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⎼") + urllib.parse.quote(json.dumps(bstack1llll1llll11_opy_))
    return ws_endpoint
def bstack1l11l1l1_opy_():
    global bstack11l1lll1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1lll1_opy_ = BrowserType.connect
    return bstack11l1lll1_opy_
def bstack1lllll1l1111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l11l1lll_opy_(self, *args, **kwargs):
    global bstack11l1lll1_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1l111l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ⎽") in kwargs:
            kwargs[bstack1l111l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ⎾")] = bstack1llllll1l1l1_opy_(
                kwargs.get(bstack1l111l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭⎿"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1l111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ⏀").format(str(e)))
    return bstack11l1lll1_opy_(self, *args, **kwargs)
def bstack1llllll1l1ll_opy_(bstack1llll1l111ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1111ll1l1l_opy_(bstack1llll1l111ll_opy_, bstack1l111l_opy_ (u"ࠦࠧ⏁"))
        if proxies and proxies.get(bstack1l111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ⏂")):
            parsed_url = urlparse(proxies.get(bstack1l111l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ⏃")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ⏄")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ⏅")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ⏆")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭⏇")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1llll1l1l_opy_(bstack1llll1l111ll_opy_):
    bstack1lllll11lll1_opy_ = {
        bstack11111l111ll_opy_[bstack1llllll11l11_opy_]: bstack1llll1l111ll_opy_[bstack1llllll11l11_opy_]
        for bstack1llllll11l11_opy_ in bstack1llll1l111ll_opy_
        if bstack1llllll11l11_opy_ in bstack11111l111ll_opy_
    }
    bstack1lllll11lll1_opy_[bstack1l111l_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ⏈")] = bstack1llllll1l1ll_opy_(bstack1llll1l111ll_opy_, global_config.get_property(bstack1l111l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧ⏉")))
    bstack1llllll11111_opy_ = [element.lower() for element in bstack111111l1l1l_opy_]
    bstack1llll1l1l111_opy_(bstack1lllll11lll1_opy_, bstack1llllll11111_opy_)
    return bstack1lllll11lll1_opy_
def bstack1llll1l1l111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l111l_opy_ (u"ࠨࠪࠫࠬ࠭ࠦ⏊")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llll1l1l111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llll1l1l111_opy_(item, keys)
def bstack11ll111ll11_opy_():
    bstack1lllllll11ll_opy_ = [os.environ.get(bstack1l111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤ⏋")), os.path.join(os.path.expanduser(bstack1l111l_opy_ (u"ࠣࢀࠥ⏌")), bstack1l111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⏍")), os.path.join(bstack1l111l_opy_ (u"ࠪ࠳ࡹࡳࡰࠨ⏎"), bstack1l111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⏏"))]
    for path in bstack1lllllll11ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l111l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ⏐") + str(path) + bstack1l111l_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ⏑"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l111l_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ⏒") + str(path) + bstack1l111l_opy_ (u"ࠣࠩࠥ⏓"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l111l_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ⏔") + str(path) + bstack1l111l_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ⏕"))
            else:
                logger.debug(bstack1l111l_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ⏖") + str(path) + bstack1l111l_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ⏗"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l111l_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ⏘") + str(path) + bstack1l111l_opy_ (u"ࠢࠨ࠰ࠥ⏙"))
            return path
        except Exception as e:
            logger.debug(bstack1l111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ⏚") + str(e) + bstack1l111l_opy_ (u"ࠤࠥ⏛"))
    logger.debug(bstack1l111l_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ⏜"))
    return None
@measure(event_name=EVENTS.bstack11111l11lll_opy_, stage=STAGE.bstack1l11llll1_opy_)
def bstack1ll1l11l1ll_opy_(binary_path, bstack1ll1l11l11l_opy_, bs_config):
    logger.debug(bstack1l111l_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ⏝").format(binary_path))
    bstack1lllll1l11l1_opy_ = bstack1l111l_opy_ (u"ࠬ࠭⏞")
    bstack1lllll1ll11l_opy_ = {
        bstack1l111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⏟"): __version__,
        bstack1l111l_opy_ (u"ࠢࡰࡵࠥ⏠"): platform.system(),
        bstack1l111l_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ⏡"): platform.machine(),
        bstack1l111l_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ⏢"): bstack1l111l_opy_ (u"ࠪ࠴ࠬ⏣"),
        bstack1l111l_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ⏤"): bstack1l111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⏥")
    }
    bstack1llll11ll111_opy_(bstack1lllll1ll11l_opy_)
    try:
        if binary_path:
            if bstack1llll11ll1ll_opy_():
                bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⏦")] = subprocess.check_output([binary_path, bstack1l111l_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⏧")]).strip().decode(bstack1l111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⏨"))
            else:
                bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏩")] = subprocess.check_output([binary_path, bstack1l111l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ⏪")], stderr=subprocess.DEVNULL).strip().decode(bstack1l111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⏫"))
        response = requests.request(
            bstack1l111l_opy_ (u"ࠬࡍࡅࡕࠩ⏬"),
            url=bstack111l1l1l1l_opy_(bstack1111111ll1l_opy_),
            headers=None,
            auth=(bs_config[bstack1l111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⏭")], bs_config[bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⏮")]),
            json=None,
            params=bstack1lllll1ll11l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l111l_opy_ (u"ࠨࡷࡵࡰࠬ⏯") in data.keys() and bstack1l111l_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⏰") in data.keys():
            logger.debug(bstack1l111l_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦ⏱").format(bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⏲")]))
            if bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ⏳") in os.environ:
                logger.debug(bstack1l111l_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡥࡸࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤ⏴"))
                data[bstack1l111l_opy_ (u"ࠧࡶࡴ࡯ࠫ⏵")] = os.environ[bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫ⏶")]
            bstack1llll1111l1l_opy_ = bstack1llll1lll1l1_opy_(data[bstack1l111l_opy_ (u"ࠩࡸࡶࡱ࠭⏷")], bstack1ll1l11l11l_opy_)
            bstack1lllll1l11l1_opy_ = os.path.join(bstack1ll1l11l11l_opy_, bstack1llll1111l1l_opy_)
            os.chmod(bstack1lllll1l11l1_opy_, 0o777) # bstack1lllllll1111_opy_ permission
            return bstack1lllll1l11l1_opy_
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ⏸").format(e))
    return binary_path
def bstack1llll11ll111_opy_(bstack1lllll1ll11l_opy_):
    try:
        if bstack1l111l_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ⏹") not in bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"ࠬࡵࡳࠨ⏺")].lower():
            return
        if os.path.exists(bstack1l111l_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⏻")):
            with open(bstack1l111l_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⏼"), bstack1l111l_opy_ (u"ࠣࡴࠥ⏽")) as f:
                bstack1llll1lll111_opy_ = {}
                for line in f:
                    if bstack1l111l_opy_ (u"ࠤࡀࠦ⏾") in line:
                        key, value = line.rstrip().split(bstack1l111l_opy_ (u"ࠥࡁࠧ⏿"), 1)
                        bstack1llll1lll111_opy_[key] = value.strip(bstack1l111l_opy_ (u"ࠫࠧࡢࠧࠨ␀"))
                bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ␁")] = bstack1llll1lll111_opy_.get(bstack1l111l_opy_ (u"ࠨࡉࡅࠤ␂"), bstack1l111l_opy_ (u"ࠢࠣ␃"))
        elif os.path.exists(bstack1l111l_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵ࡡ࡭ࡲ࡬ࡲࡪ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ␄")):
            bstack1lllll1ll11l_opy_[bstack1l111l_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩ␅")] = bstack1l111l_opy_ (u"ࠪࡥࡱࡶࡩ࡯ࡧࠪ␆")
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡩ࡯ࡳࡵࡴࡲࠤࡴ࡬ࠠ࡭࡫ࡱࡹࡽࠨ␇") + e)
@measure(event_name=EVENTS.bstack111111ll111_opy_, stage=STAGE.bstack1l11llll1_opy_)
def bstack1llll1lll1l1_opy_(bstack1llll1lll11l_opy_, bstack1lllll1111l1_opy_):
    logger.debug(bstack1l111l_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱ࠿ࠦࠢ␈") + str(bstack1llll1lll11l_opy_) + bstack1l111l_opy_ (u"ࠨࠢ␉"))
    zip_path = os.path.join(bstack1lllll1111l1_opy_, bstack1l111l_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡣ࡫࡯࡬ࡦ࠰ࡽ࡭ࡵࠨ␊"))
    bstack1llll1111l1l_opy_ = bstack1l111l_opy_ (u"ࠨࠩ␋")
    with requests.get(bstack1llll1lll11l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l111l_opy_ (u"ࠤࡺࡦࠧ␌")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l111l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠧ␍"))
    with zipfile.ZipFile(zip_path, bstack1l111l_opy_ (u"ࠫࡷ࠭␎")) as zip_ref:
        bstack1llll111ll1l_opy_ = zip_ref.namelist()
        if len(bstack1llll111ll1l_opy_) > 0:
            bstack1llll1111l1l_opy_ = bstack1llll111ll1l_opy_[0] # bstack1lll1lllll1l_opy_ bstack1111111l1l1_opy_ will be bstack1llll1llll1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1lllll1111l1_opy_)
        logger.debug(bstack1l111l_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦ␏") + str(bstack1lllll1111l1_opy_) + bstack1l111l_opy_ (u"ࠨࠧࠣ␐"))
    os.remove(zip_path)
    return bstack1llll1111l1l_opy_
def get_cli_dir():
    bstack1llll1llllll_opy_ = bstack11ll111ll11_opy_()
    if bstack1llll1llllll_opy_:
        bstack1ll1l11l11l_opy_ = os.path.join(bstack1llll1llllll_opy_, bstack1l111l_opy_ (u"ࠢࡤ࡮࡬ࠦ␑"))
        if not os.path.exists(bstack1ll1l11l11l_opy_):
            os.makedirs(bstack1ll1l11l11l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l11l11l_opy_
    else:
        raise FileNotFoundError(bstack1l111l_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦ␒"))
def bstack1ll1l111l1l_opy_(bstack1ll1l11l11l_opy_):
    bstack1l111l_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨ␓")
    bstack1lll1lllll11_opy_ = [
        os.path.join(bstack1ll1l11l11l_opy_, f)
        for f in os.listdir(bstack1ll1l11l11l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l11l11l_opy_, f)) and f.startswith(bstack1l111l_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦ␔"))
    ]
    if len(bstack1lll1lllll11_opy_) > 0:
        return max(bstack1lll1lllll11_opy_, key=os.path.getmtime) # get bstack1llll11l1lll_opy_ binary
    return bstack1l111l_opy_ (u"ࠦࠧ␕")
def bstack1111ll111ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111l1l1ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l111l1l1ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111lll1ll_opy_(data, keys, default=None):
    bstack1l111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ␖")
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
def bstack1lllllll1ll_opy_(bstack1lll1lllllll_opy_, key, value):
    bstack1l111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧ␗")
    if key in bstack111l1lll1l_opy_:
        bstack111l11lll_opy_ = bstack111l1lll1l_opy_[key]
        if isinstance(bstack111l11lll_opy_, list):
            for env_name in bstack111l11lll_opy_:
                bstack1lll1lllllll_opy_[env_name] = value
        else:
            bstack1lll1lllllll_opy_[bstack111l11lll_opy_] = value