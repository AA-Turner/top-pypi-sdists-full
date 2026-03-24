# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
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
from bstack_utils.constants import (bstack1llllll11l_opy_, bstack1l1l11l111_opy_, HTTPS_HUB,
                                    bstack111l1l1l1ll_opy_, bstack111l1111l1l_opy_, bstack111l111l1l1_opy_, bstack111l11l1ll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1ll1l11_opy_, bstack1lll1111l_opy_
from bstack_utils.proxy import bstack11ll1l111l_opy_, bstack111ll1ll11_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11l1l1111l_opy_ import bstack11l1l1111_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack111ll11l11l_opy_(config):
    return config[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ὠ")]
def bstack111lll1llll_opy_(config):
    return config[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨὩ")]
def bstack11lllll11l_opy_():
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
def bstack111111ll11l_opy_(obj):
    values = []
    bstack111111lll11_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥὪ"), re.I)
    for key in obj.keys():
        if bstack111111lll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111l111ll1_opy_(config):
    tags = []
    tags.extend(bstack111111ll11l_opy_(os.environ))
    tags.extend(bstack111111ll11l_opy_(config))
    return tags
def bstack11111l1l1l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l1l111l_opy_(bstack1111ll1l11l_opy_):
    if not bstack1111ll1l11l_opy_:
        return bstack1ll1lll_opy_ (u"ࠧࠨὫ")
    return bstack1ll1lll_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤὬ").format(bstack1111ll1l11l_opy_.name, bstack1111ll1l11l_opy_.email)
def bstack111lll11lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111l1l11l1_opy_ = repo.common_dir
        info = {
            bstack1ll1lll_opy_ (u"ࠤࡶ࡬ࡦࠨὭ"): repo.head.commit.hexsha,
            bstack1ll1lll_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨὮ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1lll_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦὯ"): repo.active_branch.name,
            bstack1ll1lll_opy_ (u"ࠧࡺࡡࡨࠤὰ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤά"): bstack1111l1l111l_opy_(repo.head.commit.committer),
            bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣὲ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1lll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣέ"): bstack1111l1l111l_opy_(repo.head.commit.author),
            bstack1ll1lll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢὴ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦή"): repo.head.commit.message,
            bstack1ll1lll_opy_ (u"ࠦࡷࡵ࡯ࡵࠤὶ"): repo.git.rev_parse(bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢί")),
            bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢὸ"): bstack1111l1l11l1_opy_,
            bstack1ll1lll_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥό"): subprocess.check_output([bstack1ll1lll_opy_ (u"ࠣࡩ࡬ࡸࠧὺ"), bstack1ll1lll_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧύ"), bstack1ll1lll_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨὼ")]).strip().decode(
                bstack1ll1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪώ")),
            bstack1ll1lll_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ὾"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣ὿"): repo.git.rev_list(
                bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᾀ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111l1l1l1l_opy_ = []
        for remote in remotes:
            bstack11111llllll_opy_ = {
                bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᾁ"): remote.name,
                bstack1ll1lll_opy_ (u"ࠤࡸࡶࡱࠨᾂ"): remote.url,
            }
            bstack1111l1l1l1l_opy_.append(bstack11111llllll_opy_)
        bstack1llllllll1l1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᾃ"): bstack1ll1lll_opy_ (u"ࠦ࡬࡯ࡴࠣᾄ"),
            **info,
            bstack1ll1lll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᾅ"): bstack1111l1l1l1l_opy_
        }
        bstack1llllllll1l1_opy_ = bstack11111111l1l_opy_(bstack1llllllll1l1_opy_)
        return bstack1llllllll1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᾆ").format(err))
        return {}
def bstack1lllllllllll_opy_(bstack1111111l1l1_opy_=None):
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࡦࡲ࡬ࡺࠢࡩࡳࡷࡳࡡࡵࡶࡨࡨࠥ࡬࡯ࡳࠢࡄࡍࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡷࡶࡩࠥࡩࡡࡴࡧࡶࠤ࡫ࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡰ࡮ࡧࡩࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡩࡳࡱࡪࡥࡳࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡐࡲࡲࡪࡀࠠࡎࡱࡱࡳ࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬࠱ࠦࡵࡴࡧࡶࠤࡨࡻࡲࡳࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡝ࡲࡷ࠳࡭ࡥࡵࡥࡺࡨ࠭࠯࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡴࡹࡿࠠ࡭࡫ࡶࡸࠥࡡ࡝࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦ࡮ࡰࠢࡶࡳࡺࡸࡣࡦࡵࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠬࠡࡴࡨࡸࡺࡸ࡮ࡴࠢ࡞ࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡷࡵ࡫ࡣࡪࡨ࡬ࡧࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡴࡰࠢࡤࡲࡦࡲࡹࡻࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡰ࡮ࡹࡴ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡨ࡮ࡩࡴࡴ࠮ࠣࡩࡦࡩࡨࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡣࠣࡪࡴࡲࡤࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᾇ")
    if bstack1111111l1l1_opy_ is None:
        bstack1111111l1l1_opy_ = [os.getcwd()]
    elif isinstance(bstack1111111l1l1_opy_, list) and len(bstack1111111l1l1_opy_) == 0:
        return []
    results = []
    for folder in bstack1111111l1l1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll1lll_opy_ (u"ࠣࡈࡲࡰࡩ࡫ࡲࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᾈ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll1lll_opy_ (u"ࠤࡳࡶࡎࡪࠢᾉ"): bstack1ll1lll_opy_ (u"ࠥࠦᾊ"),
                bstack1ll1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᾋ"): [],
                bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᾌ"): [],
                bstack1ll1lll_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨᾍ"): bstack1ll1lll_opy_ (u"ࠢࠣᾎ"),
                bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᾏ"): [],
                bstack1ll1lll_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᾐ"): bstack1ll1lll_opy_ (u"ࠥࠦᾑ"),
                bstack1ll1lll_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦᾒ"): bstack1ll1lll_opy_ (u"ࠧࠨᾓ"),
                bstack1ll1lll_opy_ (u"ࠨࡰࡳࡔࡤࡻࡉ࡯ࡦࡧࠤᾔ"): bstack1ll1lll_opy_ (u"ࠢࠣᾕ")
            }
            bstack111111l11l1_opy_ = repo.active_branch.name
            bstack1111111lll1_opy_ = repo.head.commit
            result[bstack1ll1lll_opy_ (u"ࠣࡲࡵࡍࡩࠨᾖ")] = bstack1111111lll1_opy_.hexsha
            bstack1111l1l1lll_opy_ = _1111ll11l11_opy_(repo)
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡅࡥࡸ࡫ࠠࡣࡴࡤࡲࡨ࡮ࠠࡧࡱࡵࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠻ࠢࠥᾗ") + str(bstack1111l1l1lll_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦᾘ"))
            if bstack1111l1l1lll_opy_:
                try:
                    bstack1111ll1ll11_opy_ = repo.git.diff(bstack1ll1lll_opy_ (u"ࠦ࠲࠳࡮ࡢ࡯ࡨ࠱ࡴࡴ࡬ࡺࠤᾙ"), bstack1ll11ll11l1_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥᾚ")).split(bstack1ll1lll_opy_ (u"࠭࡜࡯ࠩᾛ"))
                    logger.debug(bstack1ll1lll_opy_ (u"ࠢࡄࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡣࡧࡷࡻࡪ࡫࡮ࠡࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽࠡࡣࡱࡨࠥࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠻ࠢࠥᾜ") + str(bstack1111ll1ll11_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᾝ"))
                    result[bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᾞ")] = [f.strip() for f in bstack1111ll1ll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll11ll11l1_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢᾟ")))
                except Exception:
                    logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡨ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡥࡶࡦࡴࡣࡩࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳ࠴ࠠࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡵࡩࡨ࡫࡮ࡵࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠦᾠ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll1lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᾡ")] = _11111111111_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll1lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᾢ")] = _11111111111_opy_(commits[:5])
            bstack1111l11l111_opy_ = set()
            bstack11111l1llll_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮࡫ࡷ࠾ࠥࠨᾣ") + str(commit.message) + bstack1ll1lll_opy_ (u"ࠣࠤᾤ"))
                bstack1llllllllll1_opy_ = commit.author.name if commit.author else bstack1ll1lll_opy_ (u"ࠤࡘࡲࡰࡴ࡯ࡸࡰࠥᾥ")
                bstack1111l11l111_opy_.add(bstack1llllllllll1_opy_)
                bstack11111l1llll_opy_.append({
                    bstack1ll1lll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᾦ"): commit.message.strip(),
                    bstack1ll1lll_opy_ (u"ࠦࡺࡹࡥࡳࠤᾧ"): bstack1llllllllll1_opy_
                })
            result[bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᾨ")] = list(bstack1111l11l111_opy_)
            result[bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᾩ")] = bstack11111l1llll_opy_
            result[bstack1ll1lll_opy_ (u"ࠢࡱࡴࡇࡥࡹ࡫ࠢᾪ")] = bstack1111111lll1_opy_.committed_datetime.strftime(bstack1ll1lll_opy_ (u"ࠣࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠥᾫ"))
            if (not result[bstack1ll1lll_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᾬ")] or result[bstack1ll1lll_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᾭ")].strip() == bstack1ll1lll_opy_ (u"ࠦࠧᾮ")) and bstack1111111lll1_opy_.message:
                bstack111111111l1_opy_ = bstack1111111lll1_opy_.message.strip().splitlines()
                result[bstack1ll1lll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᾯ")] = bstack111111111l1_opy_[0] if bstack111111111l1_opy_ else bstack1ll1lll_opy_ (u"ࠨࠢᾰ")
                if len(bstack111111111l1_opy_) > 2:
                    result[bstack1ll1lll_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢᾱ")] = bstack1ll1lll_opy_ (u"ࠨ࡞ࡱࠫᾲ").join(bstack111111111l1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࠩࡨࡲࡰࡩ࡫ࡲ࠻ࠢࡾࢁ࠮ࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣᾳ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1111111111l_opy_ = [
        result
        for result in results
        if _1111l1ll1l1_opy_(result)
    ]
    return bstack1111111111l_opy_
def _1111l1ll1l1_opy_(result):
    bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡌࡪࡲࡰࡦࡴࠣࡸࡴࠦࡣࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡣࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡸࡻ࡬ࡵࠢ࡬ࡷࠥࡼࡡ࡭࡫ࡧࠤ࠭ࡴ࡯࡯࠯ࡨࡱࡵࡺࡹࠡࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠠࡢࡰࡧࠤࡦࡻࡴࡩࡱࡵࡷ࠮࠴ࠊࠡࠢࠣࠤࠧࠨࠢᾴ")
    return (
        isinstance(result.get(bstack1ll1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥ᾵"), None), list)
        and len(result[bstack1ll1lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᾶ")]) > 0
        and isinstance(result.get(bstack1ll1lll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢᾷ"), None), list)
        and len(result[bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᾸ")]) > 0
    )
def _1111ll11l11_opy_(repo):
    bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡵࡽࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡮ࡥࠡࡤࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡲࡦࡲࡲࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡮ࡡࡳࡦࡦࡳࡩ࡫ࡤࠡࡰࡤࡱࡪࡹࠠࡢࡰࡧࠤࡼࡵࡲ࡬ࠢࡺ࡭ࡹ࡮ࠠࡢ࡮࡯ࠤ࡛ࡉࡓࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࡶ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡥࡧࡩࡥࡺࡲࡴࠡࡤࡵࡥࡳࡩࡨࠡ࡫ࡩࠤࡵࡵࡳࡴ࡫ࡥࡰࡪ࠲ࠠࡦ࡮ࡶࡩࠥࡔ࡯࡯ࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᾹ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111ll1111l_opy_ = origin.refs[bstack1ll1lll_opy_ (u"ࠩࡋࡉࡆࡊࠧᾺ")]
            target = bstack1111ll1111l_opy_.reference.name
            if target.startswith(bstack1ll1lll_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫΆ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll1lll_opy_ (u"ࠫࡴࡸࡩࡨ࡫ࡱ࠳ࠬᾼ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _11111111111_opy_(commits):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᾽")
    bstack1111ll1ll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11111l11ll1_opy_ in diff:
                        if bstack11111l11ll1_opy_.a_path:
                            bstack1111ll1ll11_opy_.add(bstack11111l11ll1_opy_.a_path)
                        if bstack11111l11ll1_opy_.b_path:
                            bstack1111ll1ll11_opy_.add(bstack11111l11ll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack1111ll1ll11_opy_)
def bstack11111111l1l_opy_(bstack1llllllll1l1_opy_):
    bstack111111l1ll1_opy_ = bstack1111111ll1l_opy_(bstack1llllllll1l1_opy_)
    if bstack111111l1ll1_opy_ and bstack111111l1ll1_opy_ > bstack111l1l1l1ll_opy_:
        bstack1111l1l1ll1_opy_ = bstack111111l1ll1_opy_ - bstack111l1l1l1ll_opy_
        bstack111111ll111_opy_ = bstack111111llll1_opy_(bstack1llllllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢι")], bstack1111l1l1ll1_opy_)
        bstack1llllllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᾿")] = bstack111111ll111_opy_
        logger.info(bstack1ll1lll_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ῀")
                    .format(bstack1111111ll1l_opy_(bstack1llllllll1l1_opy_) / 1024))
    return bstack1llllllll1l1_opy_
def bstack1111111ll1l_opy_(json_data):
    try:
        if json_data:
            bstack1111l1111l1_opy_ = json.dumps(json_data)
            bstack1111ll1l1l1_opy_ = sys.getsizeof(bstack1111l1111l1_opy_)
            return bstack1111ll1l1l1_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ῁").format(e))
    return -1
def bstack111111llll1_opy_(field, bstack1111ll1ll1l_opy_):
    try:
        bstack1111l1lll11_opy_ = len(bytes(bstack111l1111l1l_opy_, bstack1ll1lll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩῂ")))
        bstack11111ll11l1_opy_ = bytes(field, bstack1ll1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪῃ"))
        bstack1111ll1l111_opy_ = len(bstack11111ll11l1_opy_)
        bstack11111l1l11l_opy_ = ceil(bstack1111ll1l111_opy_ - bstack1111ll1ll1l_opy_ - bstack1111l1lll11_opy_)
        if bstack11111l1l11l_opy_ > 0:
            bstack1lllllll1l1l_opy_ = bstack11111ll11l1_opy_[:bstack11111l1l11l_opy_].decode(bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫῄ"), errors=bstack1ll1lll_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭῅")) + bstack111l1111l1l_opy_
            return bstack1lllllll1l1l_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧῆ").format(e))
    return field
def bstack1l1l1ll1l_opy_():
    env = os.environ
    if (bstack1ll1lll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨῇ") in env and len(env[bstack1ll1lll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢῈ")]) > 0) or (
            bstack1ll1lll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤΈ") in env and len(env[bstack1ll1lll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥῊ")]) > 0):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥΉ"): bstack1ll1lll_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢῌ"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ῍"): env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ῎")),
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ῏"): env.get(bstack1ll1lll_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧῐ")),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥῑ"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦῒ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡊࠤΐ")) == bstack1ll1lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ῔") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ῕"))):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢῖ"): bstack1ll1lll_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧῗ"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢῘ"): env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣῙ")),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣῚ"): env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦΊ")),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ῜"): env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ῝"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡎࠨ῞")) == bstack1ll1lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ῟") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧῠ"))):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦῡ"): bstack1ll1lll_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥῢ"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦΰ"): env.get(bstack1ll1lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤῤ")),
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧῥ"): env.get(bstack1ll1lll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨῦ")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦῧ"): env.get(bstack1ll1lll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧῨ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࠥῩ")) == bstack1ll1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨῪ") and env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥΎ")) == bstack1ll1lll_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧῬ"):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ῭"): bstack1ll1lll_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ΅"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ`"): None,
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ῰"): None,
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ῱"): None
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧῲ")) and env.get(bstack1ll1lll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨῳ")):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤῴ"): bstack1ll1lll_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ῵"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤῶ"): env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧῷ")),
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥῸ"): None,
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣΌ"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧῺ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡏࠢΏ")) == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥῼ") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧ´"))):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ῾"): bstack1ll1lll_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ῿"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ "): env.get(bstack1ll1lll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨ ")),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ "): None,
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ "): env.get(bstack1ll1lll_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ "))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࠥ ")) == bstack1ll1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ ") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ "))):
        return {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ "): bstack1ll1lll_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ "),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ "): env.get(bstack1ll1lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ​")),
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ‌"): env.get(bstack1ll1lll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ‍")),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ‎"): env.get(bstack1ll1lll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨ‏"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡏࠢ‐")) == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ‑") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ‒"))):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ–"): bstack1ll1lll_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ—"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ―"): env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ‖")),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ‗"): env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ‘")),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ’"): env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥ‚"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡌࠦ‛")) == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ“") and bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨ”"))):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ„"): bstack1ll1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣ‟"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ†"): env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ‡")),
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ•"): env.get(bstack1ll1lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦ‣")) or env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨ․")),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ‥"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ…"))
        }
    if bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ‧"))):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ "): bstack1ll1lll_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣ "),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ‪"): bstack1ll1lll_opy_ (u"ࠥࡿࢂࢁࡽࠣ‫").format(env.get(bstack1ll1lll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ‬")), env.get(bstack1ll1lll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬ‭"))),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ‮"): env.get(bstack1ll1lll_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨ ")),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ‰"): env.get(bstack1ll1lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ‱"))
        }
    if bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧ′"))):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ″"): bstack1ll1lll_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢ‴"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ‵"): bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨ‶").format(env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧ‷")), env.get(bstack1ll1lll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪ‸")), env.get(bstack1ll1lll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫ‹")), env.get(bstack1ll1lll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ›"))),
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ※"): env.get(bstack1ll1lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ‼")),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ‽"): env.get(bstack1ll1lll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ‾"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥ‿")) and env.get(bstack1ll1lll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ⁀")):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁁"): bstack1ll1lll_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢ⁂"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⁃"): bstack1ll1lll_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥ⁄").format(env.get(bstack1ll1lll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ⁅")), env.get(bstack1ll1lll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧ⁆")), env.get(bstack1ll1lll_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ⁇"))),
            bstack1ll1lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ⁈"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ⁉")),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ⁊"): env.get(bstack1ll1lll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ⁋"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⁌")), env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣ⁍")), env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ⁎"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⁏"): bstack1ll1lll_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧ⁐"),
            bstack1ll1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⁑"): env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ⁒")),
            bstack1ll1lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⁓"): env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ⁔")),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⁕"): env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ⁖"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ⁗")):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ⁘"): bstack1ll1lll_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ⁙"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ⁚"): env.get(bstack1ll1lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ⁛")),
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⁜"): env.get(bstack1ll1lll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ⁝")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁞"): env.get(bstack1ll1lll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ "))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ⁠")) or env.get(bstack1ll1lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ⁡")):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⁢"): bstack1ll1lll_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ⁣"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⁤"): env.get(bstack1ll1lll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ⁥")),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⁦"): bstack1ll1lll_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ⁧") if env.get(bstack1ll1lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ⁨")) else None,
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⁩"): env.get(bstack1ll1lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ⁪"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ⁫")), env.get(bstack1ll1lll_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ⁬")), env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ⁭"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⁮"): bstack1ll1lll_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ⁯"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⁰"): None,
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧⁱ"): env.get(bstack1ll1lll_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ⁲")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⁳"): env.get(bstack1ll1lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ⁴"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ⁵")):
        return {
            bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⁶"): bstack1ll1lll_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ⁷"),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⁸"): env.get(bstack1ll1lll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ⁹")),
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⁺"): bstack1ll1lll_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ⁻").format(env.get(bstack1ll1lll_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ⁼"))) if env.get(bstack1ll1lll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ⁽")) else None,
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⁾"): env.get(bstack1ll1lll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧⁿ"))
        }
    if bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ₀"))):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ₁"): bstack1ll1lll_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ₂"),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ₃"): env.get(bstack1ll1lll_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ₄")),
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ₅"): env.get(bstack1ll1lll_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ₆")),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ₇"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ₈"))
        }
    if bstack11llll111l_opy_(env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ₉"))):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₊"): bstack1ll1lll_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ₋"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₌"): bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ₍").format(env.get(bstack1ll1lll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ₎")), env.get(bstack1ll1lll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ₏")), env.get(bstack1ll1lll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ₐ"))),
            bstack1ll1lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤₑ"): env.get(bstack1ll1lll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥₒ")),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣₓ"): env.get(bstack1ll1lll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥₔ"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡏࠢₕ")) == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥₖ") and env.get(bstack1ll1lll_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨₗ")) == bstack1ll1lll_opy_ (u"ࠢ࠲ࠤₘ"):
        return {
            bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨₙ"): bstack1ll1lll_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤₚ"),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨₛ"): bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢₜ").format(env.get(bstack1ll1lll_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩ₝"))),
            bstack1ll1lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ₞"): None,
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₟"): None,
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ₠")):
        return {
            bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ₡"): bstack1ll1lll_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ₢"),
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ₣"): None,
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ₤"): env.get(bstack1ll1lll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ₥")),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ₦"): env.get(bstack1ll1lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ₧"))
        }
    if any([env.get(bstack1ll1lll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ₨")), env.get(bstack1ll1lll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ₩")), env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ₪")), env.get(bstack1ll1lll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ₫"))]):
        return {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ€"): bstack1ll1lll_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ₭"),
            bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ₮"): None,
            bstack1ll1lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ₯"): env.get(bstack1ll1lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ₰")) or None,
            bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ₱"): env.get(bstack1ll1lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ₲"), 0)
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ₳")):
        return {
            bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ₴"): bstack1ll1lll_opy_ (u"ࠣࡉࡲࡇࡉࠨ₵"),
            bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ₶"): None,
            bstack1ll1lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ₷"): env.get(bstack1ll1lll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ₸")),
            bstack1ll1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ₹"): env.get(bstack1ll1lll_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧ₺"))
        }
    if env.get(bstack1ll1lll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ₻")):
        return {
            bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ₼"): bstack1ll1lll_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ₽"),
            bstack1ll1lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ₾"): env.get(bstack1ll1lll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ₿")),
            bstack1ll1lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⃀"): env.get(bstack1ll1lll_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ⃁")),
            bstack1ll1lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⃂"): env.get(bstack1ll1lll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ⃃"))
        }
    return {bstack1ll1lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ⃄"): None}
def get_host_info():
    return {
        bstack1ll1lll_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ⃅"): platform.node(),
        bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ⃆"): platform.system(),
        bstack1ll1lll_opy_ (u"ࠧࡺࡹࡱࡧࠥ⃇"): platform.machine(),
        bstack1ll1lll_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⃈"): platform.version(),
        bstack1ll1lll_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ⃉"): platform.architecture()[0]
    }
def bstack11llllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11111llll11_opy_():
    if global_config.get_property(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ⃊")):
        return bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ⃋")
    return bstack1ll1lll_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ⃌")
def bstack1111l1ll1ll_opy_(driver):
    info = {
        bstack1ll1lll_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⃍"): driver.capabilities,
        bstack1ll1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ⃎"): driver.session_id,
        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ⃏"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ⃐"), None),
        bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ⃑"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰ⃒ࠪ"), None),
        bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ⃓ࠬ"): driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ⃔"), None),
        bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⃕"):driver.capabilities.get(bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⃖"), None),
    }
    if bstack11111llll11_opy_() == bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭⃗"):
        if bstack1ll1l11111_opy_():
            info[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵ⃘ࠩ")] = bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃙")
        elif driver.capabilities.get(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶ⃚ࠫ"), {}).get(bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⃛"), False):
            info[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭⃜")] = bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⃝")
        else:
            info[bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ⃞")] = bstack1ll1lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⃟")
    return info
def bstack1ll1l11111_opy_():
    if global_config.get_property(bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃠")):
        return True
    if bstack11llll111l_opy_(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⃡"), None)):
        return True
    return False
def bstack1lllllllll1l_opy_(bstack111111l11ll_opy_, url, response, headers=None, data=None):
    bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡇࡻࡩ࡭ࡦࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠ࡭ࡱࡪࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠡࡨࡲࡶࠥࡸࡥࡲࡷࡨࡷࡹ࠵ࡲࡦࡵࡳࡳࡳࡹࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡳࡸࡩࡸࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧࠤ࠭ࡍࡅࡕ࠮ࠣࡔࡔ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡸࡶࡱࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡗࡕࡐ࠴࡫࡮ࡥࡲࡲ࡭ࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡦࡳࡱࡰࠤࡷ࡫ࡱࡶࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡩࡧࡤࡨࡪࡸࡳ࠻ࠢࡕࡩࡶࡻࡥࡴࡶࠣ࡬ࡪࡧࡤࡦࡴࡶࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡢࡶࡤ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡊࡔࡑࡑࠤࡩࡧࡴࡢࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡉࡳࡷࡳࡡࡵࡶࡨࡨࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠣࡻ࡮ࡺࡨࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡤࡲࡩࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡦࡤࡸࡦࠐࠠࠡࠢࠣࠦࠧࠨ⃢")
    bstack11111l1l1ll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨ⃣"): headers,
        bstack1ll1lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ⃤"): bstack111111l11ll_opy_.upper(),
        bstack1ll1lll_opy_ (u"ࠢࡢࡩࡨࡲࡹࠨ⃥"): None,
        bstack1ll1lll_opy_ (u"ࠣࡧࡱࡨࡵࡵࡩ࡯ࡶ⃦ࠥ"): url,
        bstack1ll1lll_opy_ (u"ࠤ࡭ࡷࡴࡴࠢ⃧"): data
    }
    try:
        bstack11111lllll1_opy_ = response.json()
        if isinstance(bstack11111lllll1_opy_, dict) and bstack11111lllll1_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ⃨ࠪ"), {}).get(bstack1ll1lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⃩"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ⃪࠭")):
            bstack11111l11lll_opy_ = json.loads(json.dumps(bstack11111lllll1_opy_))
            bstack11111l11lll_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ⃫࠭")][bstack1ll1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃬")][bstack1ll1lll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴ⃭ࠩ")] = bstack1ll1lll_opy_ (u"ࠤ࡞ࡶࡪࡪࡡࡤࡶࡨࡨࠥ࡬࡯ࡳࠢࡥࡶࡪࡼࡩࡵࡻࡠ⃮ࠦ")
            bstack11111lllll1_opy_ = bstack11111l11lll_opy_
    except Exception:
        bstack11111lllll1_opy_ = response.text
    bstack11111ll1l1l_opy_ = {
        bstack1ll1lll_opy_ (u"ࠥࡦࡴࡪࡹ⃯ࠣ"): bstack11111lllll1_opy_,
        bstack1ll1lll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࡇࡴࡪࡥࠣ⃰"): response.status_code
    }
    return {
        bstack1ll1lll_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ⃱"): bstack11111l1l1ll_opy_,
        bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ⃲"): bstack11111ll1l1l_opy_
    }
def bstack111l1l111l_opy_(bstack111111l11ll_opy_, url, data, config):
    headers = config.get(bstack1ll1lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⃳"), None)
    proxies = bstack11ll1l111l_opy_(config, url)
    auth = config.get(bstack1ll1lll_opy_ (u"ࠨࡣࡸࡸ࡭࠭⃴"), None)
    response = requests.request(
            bstack111111l11ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1lllllllll1l_opy_(bstack111111l11ll_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1ll1lll_opy_ (u"ࠩ࠯ࠫ⃵"), bstack1ll1lll_opy_ (u"ࠪ࠾ࠬ⃶"))))
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴ࠻ࠢࡾࢁࠧ⃷").format(e))
    return response
def bstack1l11l1lll1_opy_(bstack1111llll11_opy_, size):
    bstack11lll11l_opy_ = []
    while len(bstack1111llll11_opy_) > size:
        bstack11ll1llll_opy_ = bstack1111llll11_opy_[:size]
        bstack11lll11l_opy_.append(bstack11ll1llll_opy_)
        bstack1111llll11_opy_ = bstack1111llll11_opy_[size:]
    bstack11lll11l_opy_.append(bstack1111llll11_opy_)
    return bstack11lll11l_opy_
def bstack1llllllll1ll_opy_(message, bstack111111lllll_opy_=False):
    os.write(1, bytes(message, bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ⃸")))
    os.write(1, bytes(bstack1ll1lll_opy_ (u"࠭࡜࡯ࠩ⃹"), bstack1ll1lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⃺")))
    if bstack111111lllll_opy_:
        with open(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ⃻") + os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⃼")] + bstack1ll1lll_opy_ (u"ࠪ࠲ࡱࡵࡧࠨ⃽"), bstack1ll1lll_opy_ (u"ࠫࡦ࠭⃾")) as f:
            f.write(message + bstack1ll1lll_opy_ (u"ࠬࡢ࡮ࠨ⃿"))
def bstack1l11l1111l_opy_():
    return os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ℀")].lower() == bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬ℁")
def current_time():
    return bstack1llll1ll111_opy_().replace(tzinfo=None).isoformat() + bstack1ll1lll_opy_ (u"ࠨ࡜ࠪℂ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1lll_opy_ (u"ࠩ࡝ࠫ℃"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1lll_opy_ (u"ࠪ࡞ࠬ℄")))).total_seconds() * 1000
def bstack11111lll11l_opy_(timestamp):
    return bstack11111ll1l11_opy_(timestamp).isoformat() + bstack1ll1lll_opy_ (u"ࠫ࡟࠭℅")
def bstack11111l1ll11_opy_(bstack1111l11ll11_opy_):
    date_format = bstack1ll1lll_opy_ (u"࡙ࠬࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪ℆")
    bstack1111ll11ll1_opy_ = datetime.datetime.strptime(bstack1111l11ll11_opy_, date_format)
    return bstack1111ll11ll1_opy_.isoformat() + bstack1ll1lll_opy_ (u"࡚࠭ࠨℇ")
def bstack1111l11ll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ℈")
    else:
        return bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ℉")
def bstack11llll111l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧℊ")
def bstack11111llll1l_opy_(val):
    return val.__str__().lower() == bstack1ll1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩℋ")
def error_handler(bstack111111l1l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111111l1l1l_opy_ as e:
                print(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦℌ").format(func.__name__, bstack111111l1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111l1111l_opy_(bstack11111ll1111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111ll1111_opy_(cls, *args, **kwargs)
            except bstack111111l1l1l_opy_ as e:
                print(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧℍ").format(bstack11111ll1111_opy_.__name__, bstack111111l1l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111l1111l_opy_
    else:
        return decorator
def bstack1l111llll_opy_(bstack1lll11111l1_opy_):
    if os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩℎ")) is not None:
        return bstack11llll111l_opy_(os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪℏ")))
    if bstack1ll1lll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬℐ") in bstack1lll11111l1_opy_ and bstack11111llll1l_opy_(bstack1lll11111l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℑ")]):
        return False
    if bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬℒ") in bstack1lll11111l1_opy_ and bstack11111llll1l_opy_(bstack1lll11111l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℓ")]):
        return False
    return True
def bstack1l11ll1lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack1111111l111_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧ℔"), None)
        return bstack1111111l111_opy_ is None or bstack1111111l111_opy_ == bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥℕ")
    except Exception as e:
        return False
def bstack1ll111lll_opy_(hub_url, CONFIG):
    if bstack1l11ll1l1l_opy_() <= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ№")):
        if hub_url:
            return bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ℗") + hub_url + bstack1ll1lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ℘")
        return bstack1l1l11l111_opy_
    if hub_url:
        return bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧℙ") + hub_url + bstack1ll1lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧℚ")
    return HTTPS_HUB
def bstack11111ll1ll1_opy_():
    return isinstance(os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫℛ")), str)
def bstack1ll1l1111_opy_(url):
    return urlparse(url).hostname
def bstack1ll1l1l11_opy_(hostname):
    for bstack1ll1l11l1_opy_ in bstack1llllll11l_opy_:
        regex = re.compile(bstack1ll1l11l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111ll111l1_opy_(bstack1111ll1l1ll_opy_, file_name, logger):
    bstack111l11l11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"࠭ࡾࠨℜ")), bstack1111ll1l1ll_opy_)
    try:
        if not os.path.exists(bstack111l11l11_opy_):
            os.makedirs(bstack111l11l11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠧࡿࠩℝ")), bstack1111ll1l1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1lll_opy_ (u"ࠨࡹࠪ℞")):
                pass
            with open(file_path, bstack1ll1lll_opy_ (u"ࠤࡺ࠯ࠧ℟")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1ll1l11_opy_.format(str(e)))
def bstack1111l1ll11l_opy_(file_name, key, value, logger):
    file_path = bstack1111ll111l1_opy_(bstack1ll1lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ℠"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l111lll11_opy_ = json.load(open(file_path, bstack1ll1lll_opy_ (u"ࠫࡷࡨࠧ℡")))
        else:
            bstack1l111lll11_opy_ = {}
        bstack1l111lll11_opy_[key] = value
        with open(file_path, bstack1ll1lll_opy_ (u"ࠧࡽࠫࠣ™")) as outfile:
            json.dump(bstack1l111lll11_opy_, outfile)
def bstack1l1111lll_opy_(file_name, logger):
    file_path = bstack1111ll111l1_opy_(bstack1ll1lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭℣"), file_name, logger)
    bstack1l111lll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1lll_opy_ (u"ࠧࡳࠩℤ")) as bstack1lll1111ll_opy_:
            bstack1l111lll11_opy_ = json.load(bstack1lll1111ll_opy_)
    return bstack1l111lll11_opy_
def bstack1l11l1l1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ℥") + file_path + bstack1ll1lll_opy_ (u"ࠩࠣࠫΩ") + str(e))
def bstack1l11ll1l1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1lll_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧ℧")
def bstack11l11l1111_opy_(config):
    if bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪℨ") in config:
        del (config[bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ℩")])
        return False
    if bstack1l11ll1l1l_opy_() < version.parse(bstack1ll1lll_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬK")):
        return False
    if bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭Å")):
        return True
    if bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨℬ") in config and config[bstack1ll1lll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩℭ")] is False:
        return False
    else:
        return True
def bstack1l1lllllll_opy_(args_list, bstack11111ll111l_opy_):
    index = -1
    for value in bstack11111ll111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack111ll1l1l1l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack111ll1l1l1l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llllllll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llllllll1l_opy_ = bstack1llllllll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ℮"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫℯ"), exception=exception)
    def bstack1ll1llll1ll_opy_(self):
        if self.result != bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬℰ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤℱ") in self.exception_type:
            return bstack1ll1lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣℲ")
        return bstack1ll1lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤℳ")
    def bstack11111111ll1_opy_(self):
        if self.result != bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩℴ"):
            return None
        if self.bstack1llllllll1l_opy_:
            return self.bstack1llllllll1l_opy_
        return bstack111111ll1l1_opy_(self.exception)
def bstack111111ll1l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11111ll11ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111l1lll11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll11ll1l_opy_(config, logger):
    try:
        import playwright
        bstack1lllllll1lll_opy_ = playwright.__file__
        bstack1111111llll_opy_ = os.path.split(bstack1lllllll1lll_opy_)
        bstack11111lll111_opy_ = bstack1111111llll_opy_[0] + bstack1ll1lll_opy_ (u"ࠪ࠳ࡩࡸࡩࡷࡧࡵ࠳ࡵࡧࡣ࡬ࡣࡪࡩ࠴ࡲࡩࡣ࠱ࡦࡰ࡮࠵ࡣ࡭࡫࠱࡮ࡸ࠭ℵ")
        os.environ[bstack1ll1lll_opy_ (u"ࠫࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠧℶ")] = bstack111ll1ll11_opy_(config)
        with open(bstack11111lll111_opy_, bstack1ll1lll_opy_ (u"ࠬࡸࠧℷ")) as f:
            file_content = f.read()
            bstack1111ll111ll_opy_ = bstack1ll1lll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬℸ")
            bstack1111ll11lll_opy_ = file_content.find(bstack1111ll111ll_opy_)
            if bstack1111ll11lll_opy_ == -1:
              process = subprocess.Popen(bstack1ll1lll_opy_ (u"ࠢ࡯ࡲࡰࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠦℹ"), shell=True, cwd=bstack1111111llll_opy_[0])
              process.wait()
              bstack1111l1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠨࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࠨ࠻ࠨ℺")
              bstack1llllllll11l_opy_ = bstack1ll1lll_opy_ (u"ࠤࠥࠦࠥࡢࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࡠࠧࡁࠠࡤࡱࡱࡷࡹࠦࡻࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤࢂࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩࠬ࠿ࠥ࡯ࡦࠡࠪࡳࡶࡴࡩࡥࡴࡵ࠱ࡩࡳࡼ࠮ࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠬࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠨࠪ࠽ࠣࠦࠧࠨ℻")
              bstack11111lll1ll_opy_ = file_content.replace(bstack1111l1l1111_opy_, bstack1llllllll11l_opy_)
              with open(bstack11111lll111_opy_, bstack1ll1lll_opy_ (u"ࠪࡻࠬℼ")) as f:
                f.write(bstack11111lll1ll_opy_)
    except Exception as e:
        logger.error(bstack1lll1111l_opy_.format(str(e)))
def bstack1l111lllll_opy_():
  try:
    bstack1111l11llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫℽ"))
    bstack1111l1l1l11_opy_ = []
    if os.path.exists(bstack1111l11llll_opy_):
      with open(bstack1111l11llll_opy_) as f:
        bstack1111l1l1l11_opy_ = json.load(f)
      os.remove(bstack1111l11llll_opy_)
    return bstack1111l1l1l11_opy_
  except:
    pass
  return []
def bstack11l1111l11_opy_(bstack111l111l1l_opy_):
  try:
    bstack1111l1l1l11_opy_ = []
    bstack1111l11llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬℾ"))
    if os.path.exists(bstack1111l11llll_opy_):
      with open(bstack1111l11llll_opy_) as f:
        bstack1111l1l1l11_opy_ = json.load(f)
    bstack1111l1l1l11_opy_.append(bstack111l111l1l_opy_)
    with open(bstack1111l11llll_opy_, bstack1ll1lll_opy_ (u"࠭ࡷࠨℿ")) as f:
        json.dump(bstack1111l1l1l11_opy_, f)
  except:
    pass
def bstack1l111llll1_opy_(logger, bstack1llllllll111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⅀"), bstack1ll1lll_opy_ (u"ࠨࠩ⅁"))
    if test_name == bstack1ll1lll_opy_ (u"ࠩࠪ⅂"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡅࡨࡩࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩ⅃"), bstack1ll1lll_opy_ (u"ࠫࠬ⅄"))
    bstack11111l111ll_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠲ࠠࠨⅅ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llllllll111_opy_:
        bstack111111lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ⅆ"), bstack1ll1lll_opy_ (u"ࠧ࠱ࠩⅇ"))
        bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ⅈ"): test_name, bstack1ll1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨⅉ"): bstack11111l111ll_opy_, bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⅊"): bstack111111lll1_opy_}
        bstack111111l111l_opy_ = []
        bstack1111l11l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ⅋"))
        if os.path.exists(bstack1111l11l11l_opy_):
            with open(bstack1111l11l11l_opy_) as f:
                bstack111111l111l_opy_ = json.load(f)
        bstack111111l111l_opy_.append(bstack111l11l1ll_opy_)
        with open(bstack1111l11l11l_opy_, bstack1ll1lll_opy_ (u"ࠬࡽࠧ⅌")) as f:
            json.dump(bstack111111l111l_opy_, f)
    else:
        bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⅍"): test_name, bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ⅎ"): bstack11111l111ll_opy_, bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⅏"): str(multiprocessing.current_process().name)}
        if bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭⅐") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack111l11l1ll_opy_)
  except Exception as e:
      logger.warn(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⅑").format(e))
def bstack1l11llll1_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡢࡵ࡬ࡧࠥ࡬ࡩ࡭ࡧࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠧ⅒"))
    try:
      bstack1111l11111l_opy_ = []
      bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⅓"): test_name, bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⅔"): error_message, bstack1ll1lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⅕"): index}
      bstack111111l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⅖"))
      if os.path.exists(bstack111111l1l11_opy_):
          with open(bstack111111l1l11_opy_) as f:
              bstack1111l11111l_opy_ = json.load(f)
      bstack1111l11111l_opy_.append(bstack111l11l1ll_opy_)
      with open(bstack111111l1l11_opy_, bstack1ll1lll_opy_ (u"ࠩࡺࠫ⅗")) as f:
          json.dump(bstack1111l11111l_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⅘").format(e))
    return
  bstack1111l11111l_opy_ = []
  bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⅙"): test_name, bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⅚"): error_message, bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⅛"): index}
  bstack111111l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ⅜"))
  lock_file = bstack111111l1l11_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠰࡯ࡳࡨࡱࠧ⅝")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111111l1l11_opy_):
          with open(bstack111111l1l11_opy_, bstack1ll1lll_opy_ (u"ࠩࡵࠫ⅞")) as f:
              content = f.read().strip()
              if content:
                  bstack1111l11111l_opy_ = json.load(open(bstack111111l1l11_opy_))
      bstack1111l11111l_opy_.append(bstack111l11l1ll_opy_)
      with open(bstack111111l1l11_opy_, bstack1ll1lll_opy_ (u"ࠪࡻࠬ⅟")) as f:
          json.dump(bstack1111l11111l_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡨ࡬ࡰࡪࠦ࡬ࡰࡥ࡮࡭ࡳ࡭࠺ࠡࡽࢀࠦⅠ").format(e))
def bstack11ll1l111_opy_(bstack11l1111ll_opy_, name, logger):
  try:
    bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪⅡ"): name, bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬⅢ"): bstack11l1111ll_opy_, bstack1ll1lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭Ⅳ"): str(threading.current_thread()._name)}
    return bstack111l11l1ll_opy_
  except Exception as e:
    logger.warn(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧⅤ").format(e))
  return
def bstack11111l1l111_opy_():
    return platform.system() == bstack1ll1lll_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪⅥ")
def bstack1l1llll1ll_opy_(bstack111111l1111_opy_, config, logger):
    bstack111111111ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111111l1111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤⅦ").format(e))
    return bstack111111111ll_opy_
def bstack1111l111lll_opy_(bstack1111l1111ll_opy_, bstack1111l1lll1l_opy_):
    bstack1111ll11l1l_opy_ = version.parse(bstack1111l1111ll_opy_)
    bstack11111lll1l1_opy_ = version.parse(bstack1111l1lll1l_opy_)
    if bstack1111ll11l1l_opy_ > bstack11111lll1l1_opy_:
        return 1
    elif bstack1111ll11l1l_opy_ < bstack11111lll1l1_opy_:
        return -1
    else:
        return 0
def bstack1llll1ll111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11111ll1l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111111l1lll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll111111_opy_(options, framework, config, bstack11l11l111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll1lll_opy_ (u"ࠫ࡬࡫ࡴࠨⅧ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1llllllll1_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭Ⅸ"))
    bstack1111l11l1l1_opy_ = True
    bstack111ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫⅩ")]
    bstack1l1l111l111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧⅪ"), False)
    if bstack1l1l111l111_opy_:
        bstack1l1llll1lll_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨⅫ"), {})
        bstack1l1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬⅬ")] = os.getenv(bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨⅭ"))
        bstack1llll111ll_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬⅮ"), bstack1ll1lll_opy_ (u"ࠬࢁࡽࠨⅯ"))).get(bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧⅰ"))
    if bstack11111llll1l_opy_(caps.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ⅱ"))) or bstack11111llll1l_opy_(caps.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨⅲ"))):
        bstack1111l11l1l1_opy_ = False
    if bstack11l11l1111_opy_({bstack1ll1lll_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤⅳ"): bstack1111l11l1l1_opy_}):
        bstack1llllllll1_opy_ = bstack1llllllll1_opy_ or {}
        bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬⅴ")] = bstack111111l1lll_opy_(framework)
        bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ⅵ")] = bstack1l11l1111l_opy_()
        bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨⅶ")] = bstack111ll11l_opy_
        bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨⅷ")] = bstack11l11l111l_opy_
        if bstack1l1l111l111_opy_:
            bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧⅸ")] = bstack1l1l111l111_opy_
            bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨⅹ")] = bstack1l1llll1lll_opy_
            bstack1llllllll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩⅺ")][bstack1ll1lll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫⅻ")] = bstack1llll111ll_opy_
        if getattr(options, bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬⅼ"), None):
            options.set_capability(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ⅽ"), bstack1llllllll1_opy_)
        else:
            options[bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧⅾ")] = bstack1llllllll1_opy_
    else:
        if getattr(options, bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨⅿ"), None):
            options.set_capability(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩↀ"), bstack111111l1lll_opy_(framework))
            options.set_capability(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪↁ"), bstack1l11l1111l_opy_())
            options.set_capability(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬↂ"), bstack111ll11l_opy_)
            options.set_capability(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬↃ"), bstack11l11l111l_opy_)
            if bstack1l1l111l111_opy_:
                options.set_capability(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫↄ"), bstack1l1l111l111_opy_)
                options.set_capability(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬↅ"), bstack1l1llll1lll_opy_)
                options.set_capability(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧↆ"), bstack1llll111ll_opy_)
        else:
            options[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩↇ")] = bstack111111l1lll_opy_(framework)
            options[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪↈ")] = bstack1l11l1111l_opy_()
            options[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ↉")] = bstack111ll11l_opy_
            options[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ↊")] = bstack11l11l111l_opy_
            if bstack1l1l111l111_opy_:
                options[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ↋")] = bstack1l1l111l111_opy_
                options[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ↌")] = bstack1l1llll1lll_opy_
                options[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↍")][bstack1ll1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ↎")] = bstack1llll111ll_opy_
    return options
def bstack111111lll1l_opy_(ws_endpoint, framework):
    bstack11l11l111l_opy_ = global_config.get_property(bstack1ll1lll_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ↏"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ←"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ↑"))[0]
        if bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ→") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l11111_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll1lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ↓"))[1]))
            bstack11111l11111_opy_ = bstack11111l11111_opy_ or {}
            bstack111ll11l_opy_ = os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↔")]
            bstack11111l11111_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ↕")] = str(framework) + str(__version__)
            bstack11111l11111_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ↖")] = bstack1l11l1111l_opy_()
            bstack11111l11111_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ↗")] = bstack111ll11l_opy_
            bstack11111l11111_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ↘")] = bstack11l11l111l_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll1lll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫ↙"))[0] + bstack1ll1lll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ↚") + urllib.parse.quote(json.dumps(bstack11111l11111_opy_))
    return ws_endpoint
def bstack11l1lll1ll_opy_():
    global bstack11lll1ll1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11lll1ll1l_opy_ = BrowserType.connect
    return bstack11lll1ll1l_opy_
def bstack1111l1ll111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l1l1lll1l1_opy_(self, *args, **kwargs):
    global bstack11lll1ll1l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll1lll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫ↛") in kwargs:
            kwargs[bstack1ll1lll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬ↜")] = bstack111111lll1l_opy_(
                kwargs.get(bstack1ll1lll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭↝"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥ↞").format(str(e)))
    return bstack11lll1ll1l_opy_(self, *args, **kwargs)
def bstack1111l111l1l_opy_(bstack1lllllllll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11ll1l111l_opy_(bstack1lllllllll11_opy_, bstack1ll1lll_opy_ (u"ࠦࠧ↟"))
        if proxies and proxies.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ↠")):
            parsed_url = urlparse(proxies.get(bstack1ll1lll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ↡")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪ↢")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫ↣")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬ↤")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭↥")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l111l1_opy_(bstack1lllllllll11_opy_):
    bstack11111l11l1l_opy_ = {
        bstack111l11l1ll1_opy_[bstack1111111l11l_opy_]: bstack1lllllllll11_opy_[bstack1111111l11l_opy_]
        for bstack1111111l11l_opy_ in bstack1lllllllll11_opy_
        if bstack1111111l11l_opy_ in bstack111l11l1ll1_opy_
    }
    bstack11111l11l1l_opy_[bstack1ll1lll_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦ↦")] = bstack1111l111l1l_opy_(bstack1lllllllll11_opy_, global_config.get_property(bstack1ll1lll_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧ↧")))
    bstack1lllllll1ll1_opy_ = [element.lower() for element in bstack111l111l1l1_opy_]
    bstack1111111ll11_opy_(bstack11111l11l1l_opy_, bstack1lllllll1ll1_opy_)
    return bstack11111l11l1l_opy_
def bstack1111111ll11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1lll_opy_ (u"ࠨࠪࠫࠬ࠭ࠦ↨")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111111ll11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111111ll11_opy_(item, keys)
def bstack11llllll1l1_opy_():
    bstack1111l1lllll_opy_ = [os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤ↩")), os.path.join(os.path.expanduser(bstack1ll1lll_opy_ (u"ࠣࢀࠥ↪")), bstack1ll1lll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ↫")), os.path.join(bstack1ll1lll_opy_ (u"ࠪ࠳ࡹࡳࡰࠨ↬"), bstack1ll1lll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ↭"))]
    for path in bstack1111l1lllll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ↮") + str(path) + bstack1ll1lll_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ↯"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll1lll_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ↰") + str(path) + bstack1ll1lll_opy_ (u"ࠣࠩࠥ↱"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ↲") + str(path) + bstack1ll1lll_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ↳"))
            else:
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ↴") + str(path) + bstack1ll1lll_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ↵"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ↶") + str(path) + bstack1ll1lll_opy_ (u"ࠢࠨ࠰ࠥ↷"))
            return path
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ↸") + str(e) + bstack1ll1lll_opy_ (u"ࠤࠥ↹"))
    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ↺"))
    return None
@measure(event_name=EVENTS.bstack111l1l111ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1lll1ll1l1l_opy_(binary_path, bstack1lll1lll1ll_opy_, bs_config):
    logger.debug(bstack1ll1lll_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ↻").format(binary_path))
    bstack11111l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠬ࠭↼")
    bstack1111l111l11_opy_ = {
        bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ↽"): __version__,
        bstack1ll1lll_opy_ (u"ࠢࡰࡵࠥ↾"): platform.system(),
        bstack1ll1lll_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ↿"): platform.machine(),
        bstack1ll1lll_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ⇀"): bstack1ll1lll_opy_ (u"ࠪ࠴ࠬ⇁"),
        bstack1ll1lll_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ⇂"): bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⇃")
    }
    bstack11111111l11_opy_(bstack1111l111l11_opy_)
    try:
        if binary_path:
            if bstack11111l1l111_opy_():
                bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⇄")] = subprocess.check_output([binary_path, bstack1ll1lll_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ⇅")]).strip().decode(bstack1ll1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⇆"))
            else:
                bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⇇")] = subprocess.check_output([binary_path, bstack1ll1lll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ⇈")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll1lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⇉"))
        response = requests.request(
            bstack1ll1lll_opy_ (u"ࠬࡍࡅࡕࠩ⇊"),
            url=bstack11l1l1111_opy_(bstack111l11l1l11_opy_),
            headers=None,
            auth=(bs_config[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ⇋")], bs_config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ⇌")]),
            json=None,
            params=bstack1111l111l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll1lll_opy_ (u"ࠨࡷࡵࡰࠬ⇍") in data.keys() and bstack1ll1lll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⇎") in data.keys():
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦ⇏").format(bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⇐")]))
            if bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨ⇑") in os.environ:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡥࡸࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠢ࡬ࡷࠥࡹࡥࡵࠤ⇒"))
                data[bstack1ll1lll_opy_ (u"ࠧࡶࡴ࡯ࠫ⇓")] = os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫ⇔")]
            bstack11111111lll_opy_ = bstack1111l1l11ll_opy_(data[bstack1ll1lll_opy_ (u"ࠩࡸࡶࡱ࠭⇕")], bstack1lll1lll1ll_opy_)
            bstack11111l1lll1_opy_ = os.path.join(bstack1lll1lll1ll_opy_, bstack11111111lll_opy_)
            os.chmod(bstack11111l1lll1_opy_, 0o777) # bstack1111l1llll1_opy_ permission
            return bstack11111l1lll1_opy_
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ⇖").format(e))
    return binary_path
def bstack11111111l11_opy_(bstack1111l111l11_opy_):
    try:
        if bstack1ll1lll_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪ⇗") not in bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡵࡳࠨ⇘")].lower():
            return
        if os.path.exists(bstack1ll1lll_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣ⇙")):
            with open(bstack1ll1lll_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤ⇚"), bstack1ll1lll_opy_ (u"ࠣࡴࠥ⇛")) as f:
                bstack111111ll1ll_opy_ = {}
                for line in f:
                    if bstack1ll1lll_opy_ (u"ࠤࡀࠦ⇜") in line:
                        key, value = line.rstrip().split(bstack1ll1lll_opy_ (u"ࠥࡁࠧ⇝"), 1)
                        bstack111111ll1ll_opy_[key] = value.strip(bstack1ll1lll_opy_ (u"ࠫࠧࡢࠧࠨ⇞"))
                bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ⇟")] = bstack111111ll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡉࡅࠤ⇠"), bstack1ll1lll_opy_ (u"ࠢࠣ⇡"))
        elif os.path.exists(bstack1ll1lll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵ࡡ࡭ࡲ࡬ࡲࡪ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢ⇢")):
            bstack1111l111l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩ⇣")] = bstack1ll1lll_opy_ (u"ࠪࡥࡱࡶࡩ࡯ࡧࠪ⇤")
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡩ࡯ࡳࡵࡴࡲࠤࡴ࡬ࠠ࡭࡫ࡱࡹࡽࠨ⇥") + e)
@measure(event_name=EVENTS.bstack111l11ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
def bstack1111l1l11ll_opy_(bstack1111111l1ll_opy_, bstack1111l111111_opy_):
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱ࠿ࠦࠢ⇦") + str(bstack1111111l1ll_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢ⇧"))
    zip_path = os.path.join(bstack1111l111111_opy_, bstack1ll1lll_opy_ (u"ࠢࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࡣ࡫࡯࡬ࡦ࠰ࡽ࡭ࡵࠨ⇨"))
    bstack11111111lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩ⇩")
    with requests.get(bstack1111111l1ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll1lll_opy_ (u"ࠤࡺࡦࠧ⇪")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼ࠲ࠧ⇫"))
    with zipfile.ZipFile(zip_path, bstack1ll1lll_opy_ (u"ࠫࡷ࠭⇬")) as zip_ref:
        bstack11111l1ll1l_opy_ = zip_ref.namelist()
        if len(bstack11111l1ll1l_opy_) > 0:
            bstack11111111lll_opy_ = bstack11111l1ll1l_opy_[0] # bstack11111l111l1_opy_ bstack111l111ll1l_opy_ will be bstack11111ll1lll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111l111111_opy_)
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡩ࡭ࡧࡶࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡩࡽࡺࡲࡢࡥࡷࡩࡩࠦࡴࡰࠢࠪࠦ⇭") + str(bstack1111l111111_opy_) + bstack1ll1lll_opy_ (u"ࠨࠧࠣ⇮"))
    os.remove(zip_path)
    return bstack11111111lll_opy_
def get_cli_dir():
    bstack1111l11l1ll_opy_ = bstack11llllll1l1_opy_()
    if bstack1111l11l1ll_opy_:
        bstack1lll1lll1ll_opy_ = os.path.join(bstack1111l11l1ll_opy_, bstack1ll1lll_opy_ (u"ࠢࡤ࡮࡬ࠦ⇯"))
        if not os.path.exists(bstack1lll1lll1ll_opy_):
            os.makedirs(bstack1lll1lll1ll_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1lll1ll_opy_
    else:
        raise FileNotFoundError(bstack1ll1lll_opy_ (u"ࠣࡐࡲࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠦ⇰"))
def bstack1lll1ll11ll_opy_(bstack1lll1lll1ll_opy_):
    bstack1ll1lll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿࠠࡪࡰࠣࡥࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠦࠧࠨ⇱")
    bstack11111l11l11_opy_ = [
        os.path.join(bstack1lll1lll1ll_opy_, f)
        for f in os.listdir(bstack1lll1lll1ll_opy_)
        if os.path.isfile(os.path.join(bstack1lll1lll1ll_opy_, f)) and f.startswith(bstack1ll1lll_opy_ (u"ࠥࡦ࡮ࡴࡡࡳࡻ࠰ࠦ⇲"))
    ]
    if len(bstack11111l11l11_opy_) > 0:
        return max(bstack11111l11l11_opy_, key=os.path.getmtime) # get bstack1111l11lll1_opy_ binary
    return bstack1ll1lll_opy_ (u"ࠦࠧ⇳")
def bstack111ll11l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11lll1lll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l11lll1lll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11llll1l_opy_(data, keys, default=None):
    bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡡࡧࡧ࡯ࡽࠥ࡭ࡥࡵࠢࡤࠤࡳ࡫ࡳࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡣࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡢࡶࡤ࠾࡚ࠥࡨࡦࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺࠠࡵࡱࠣࡸࡷࡧࡶࡦࡴࡶࡩ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣ࡯ࡪࡿࡳ࠻ࠢࡄࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡱࡥࡺࡵ࠲࡭ࡳࡪࡩࡤࡧࡶࠤࡷ࡫ࡰࡳࡧࡶࡩࡳࡺࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡪ࡬ࡡࡶ࡮ࡷ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤࡹࡵࠠࡳࡧࡷࡹࡷࡴࠠࡪࡨࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡸࡥࡵࡷࡵࡲ࠿ࠦࡔࡩࡧࠣࡺࡦࡲࡵࡦࠢࡤࡸࠥࡺࡨࡦࠢࡱࡩࡸࡺࡥࡥࠢࡳࡥࡹ࡮ࠬࠡࡱࡵࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥ࡯ࡦࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ⇴")
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
def bstack1lll11lll_opy_(bstack1111ll11111_opy_, key, value):
    bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡵࡱࡵࡩࠥࡉࡌࡊࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠣࡱࡦࡶࡰࡪࡰࡪࠤ࡮ࡴࠠࡵࡪࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥ࡯࡭ࡤ࡫࡮ࡷࡡࡹࡥࡷࡹ࡟࡮ࡣࡳ࠾ࠥࡊࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡬ࡧࡼ࠾ࠥࡑࡥࡺࠢࡩࡶࡴࡳࠠࡄࡎࡌࡣࡈࡇࡐࡔࡡࡗࡓࡤࡉࡏࡏࡈࡌࡋࠏࠦࠠࠡࠢࠣࠤࠥࠦࡶࡢ࡮ࡸࡩ࠿ࠦࡖࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡧࡴࡳ࡭ࡢࡰࡧࠤࡱ࡯࡮ࡦࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠥࠦࠧ⇵")
    if key in bstack11111l11l1_opy_:
        bstack11llll1lll_opy_ = bstack11111l11l1_opy_[key]
        if isinstance(bstack11llll1lll_opy_, list):
            for env_name in bstack11llll1lll_opy_:
                bstack1111ll11111_opy_[env_name] = value
        else:
            bstack1111ll11111_opy_[bstack11llll1lll_opy_] = value