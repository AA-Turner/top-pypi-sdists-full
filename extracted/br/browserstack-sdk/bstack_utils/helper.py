# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
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
from bstack_utils.constants import (bstack1l11ll1lll_opy_, bstack1l1111ll1_opy_, bstack11l111l1_opy_,
                                    bstack111ll11l1l1_opy_, bstack111lll1ll11_opy_, bstack111ll1ll1l1_opy_, bstack111lll1ll1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111ll11l_opy_, bstack11l1111l1_opy_
from bstack_utils.proxy import bstack1llll1l111_opy_, bstack111l11l11_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack111ll1111l_opy_ import bstack11l111ll1_opy_
from browserstack_sdk._version import __version__
bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l11l1_opy_())
bstack111111l11_opy_ = logger_utils.bstack11llll1l11_opy_(__name__)
def bstack11l11l11lll_opy_(config):
    return config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᴬ")]
def bstack11l111l1ll1_opy_(config):
    return config[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᴭ")]
def bstack1l1lllll1_opy_():
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
def bstack111l111lll1_opy_(obj):
    values = []
    bstack1111l1ll111_opy_ = re.compile(bstack11l11_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᴮ"), re.I)
    for key in obj.keys():
        if bstack1111l1ll111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1111ll1_opy_(config):
    tags = []
    tags.extend(bstack111l111lll1_opy_(os.environ))
    tags.extend(bstack111l111lll1_opy_(config))
    return tags
def bstack1111ll1lll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111lll1l11_opy_(bstack1111l1lll11_opy_):
    if not bstack1111l1lll11_opy_:
        return bstack11l11_opy_ (u"ࠩࠪᴯ")
    return bstack11l11_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦᴰ").format(bstack1111l1lll11_opy_.name, bstack1111l1lll11_opy_.email)
def bstack11l111ll1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111lll1lll_opy_ = repo.common_dir
        info = {
            bstack11l11_opy_ (u"ࠦࡸ࡮ࡡࠣᴱ"): repo.head.commit.hexsha,
            bstack11l11_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣᴲ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l11_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨᴳ"): repo.active_branch.name,
            bstack11l11_opy_ (u"ࠢࡵࡣࡪࠦᴴ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦᴵ"): bstack1111lll1l11_opy_(repo.head.commit.committer),
            bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥᴶ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l11_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥᴷ"): bstack1111lll1l11_opy_(repo.head.commit.author),
            bstack11l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤᴸ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᴹ"): repo.head.commit.message,
            bstack11l11_opy_ (u"ࠨࡲࡰࡱࡷࠦᴺ"): repo.git.rev_parse(bstack11l11_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤᴻ")),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᴼ"): bstack1111lll1lll_opy_,
            bstack11l11_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᴽ"): subprocess.check_output([bstack11l11_opy_ (u"ࠥ࡫࡮ࡺࠢᴾ"), bstack11l11_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢᴿ"), bstack11l11_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᵀ")]).strip().decode(
                bstack11l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᵁ")),
            bstack11l11_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᵂ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᵃ"): repo.git.rev_list(
                bstack11l11_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᵄ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l11l11l1_opy_ = []
        for remote in remotes:
            bstack111l11ll111_opy_ = {
                bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᵅ"): remote.name,
                bstack11l11_opy_ (u"ࠦࡺࡸ࡬ࠣᵆ"): remote.url,
            }
            bstack111l11l11l1_opy_.append(bstack111l11ll111_opy_)
        bstack1111l11lll1_opy_ = {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᵇ"): bstack11l11_opy_ (u"ࠨࡧࡪࡶࠥᵈ"),
            **info,
            bstack11l11_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣᵉ"): bstack111l11l11l1_opy_
        }
        bstack1111l11lll1_opy_ = bstack111l1l111ll_opy_(bstack1111l11lll1_opy_)
        return bstack1111l11lll1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᵊ").format(err))
        return {}
def bstack1111l1ll11l_opy_(bstack111l1l1ll1l_opy_=None):
    bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࡡ࡭࡮ࡼࠤ࡫ࡵࡲ࡮ࡣࡷࡸࡪࡪࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡹࡸ࡫ࠠࡤࡣࡶࡩࡸࠦࡦࡰࡴࠣࡩࡦࡩࡨࠡࡨࡲࡰࡩ࡫ࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥ࠮࡬ࡪࡵࡷ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡒࡴࡴࡥ࠻ࠢࡐࡳࡳࡵ࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠬࠡࡷࡶࡩࡸࠦࡣࡶࡴࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡶࡴࡺࠢ࡯࡭ࡸࡺࠠ࡜࡟࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡰࡲࠤࡸࡵࡵࡳࡥࡨࡷࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥ࠮ࠣࡶࡪࡺࡵࡳࡰࡶࠤࡠࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡲࡤࡸ࡭ࡹ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡶࡲࠤࡦࡴࡡ࡭ࡻࡽࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡲࡩࡴࡶ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡪࡩࡤࡶࡶ࠰ࠥ࡫ࡡࡤࡪࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡥࠥ࡬࡯࡭ࡦࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᵋ")
    if bstack111l1l1ll1l_opy_ is None:
        bstack111l1l1ll1l_opy_ = [os.getcwd()]
    elif isinstance(bstack111l1l1ll1l_opy_, list) and len(bstack111l1l1ll1l_opy_) == 0:
        return []
    results = []
    for folder in bstack111l1l1ll1l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11l11_opy_ (u"ࠥࡊࡴࡲࡤࡦࡴࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᵌ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11l11_opy_ (u"ࠦࡵࡸࡉࡥࠤᵍ"): bstack11l11_opy_ (u"ࠧࠨᵎ"),
                bstack11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᵏ"): [],
                bstack11l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᵐ"): [],
                bstack11l11_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᵑ"): bstack11l11_opy_ (u"ࠤࠥᵒ"),
                bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᵓ"): [],
                bstack11l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᵔ"): bstack11l11_opy_ (u"ࠧࠨᵕ"),
                bstack11l11_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᵖ"): bstack11l11_opy_ (u"ࠢࠣᵗ"),
                bstack11l11_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦᵘ"): bstack11l11_opy_ (u"ࠤࠥᵙ")
            }
            bstack1111llll1l1_opy_ = repo.active_branch.name
            bstack1111l11ll1l_opy_ = repo.head.commit
            result[bstack11l11_opy_ (u"ࠥࡴࡷࡏࡤࠣᵚ")] = bstack1111l11ll1l_opy_.hexsha
            bstack111l1111111_opy_ = _1111ll111l1_opy_(repo)
            logger.debug(bstack11l11_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᵛ") + str(bstack111l1111111_opy_) + bstack11l11_opy_ (u"ࠧࠨᵜ"))
            if bstack111l1111111_opy_:
                try:
                    bstack11111lll1ll_opy_ = repo.git.diff(bstack11l11_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᵝ"), bstack1ll1lllll11_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᵞ")).split(bstack11l11_opy_ (u"ࠨ࡞ࡱࠫᵟ"))
                    logger.debug(bstack11l11_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᵠ") + str(bstack11111lll1ll_opy_) + bstack11l11_opy_ (u"ࠥࠦᵡ"))
                    result[bstack11l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᵢ")] = [f.strip() for f in bstack11111lll1ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1lllll11_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᵣ")))
                except Exception:
                    logger.debug(bstack11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨᵤ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᵥ")] = _111l11lllll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᵦ")] = _111l11lllll_opy_(commits[:5])
            bstack1111l1l1l1l_opy_ = set()
            bstack1111l1l1l11_opy_ = []
            for commit in commits:
                logger.debug(bstack11l11_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᵧ") + str(commit.message) + bstack11l11_opy_ (u"ࠥࠦᵨ"))
                bstack1111lll1l1l_opy_ = commit.author.name if commit.author else bstack11l11_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᵩ")
                bstack1111l1l1l1l_opy_.add(bstack1111lll1l1l_opy_)
                bstack1111l1l1l11_opy_.append({
                    bstack11l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᵪ"): commit.message.strip(),
                    bstack11l11_opy_ (u"ࠨࡵࡴࡧࡵࠦᵫ"): bstack1111lll1l1l_opy_
                })
            result[bstack11l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᵬ")] = list(bstack1111l1l1l1l_opy_)
            result[bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᵭ")] = bstack1111l1l1l11_opy_
            result[bstack11l11_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᵮ")] = bstack1111l11ll1l_opy_.committed_datetime.strftime(bstack11l11_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᵯ"))
            if (not result[bstack11l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᵰ")] or result[bstack11l11_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᵱ")].strip() == bstack11l11_opy_ (u"ࠨࠢᵲ")) and bstack1111l11ll1l_opy_.message:
                bstack1111l1llll1_opy_ = bstack1111l11ll1l_opy_.message.strip().splitlines()
                result[bstack11l11_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᵳ")] = bstack1111l1llll1_opy_[0] if bstack1111l1llll1_opy_ else bstack11l11_opy_ (u"ࠣࠤᵴ")
                if len(bstack1111l1llll1_opy_) > 2:
                    result[bstack11l11_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᵵ")] = bstack11l11_opy_ (u"ࠪࡠࡳ࠭ᵶ").join(bstack1111l1llll1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀࢃࠩ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥᵷ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111l111llll_opy_(result)
    ]
    return filtered_results
def _111l111llll_opy_(result):
    bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡎࡥ࡭ࡲࡨࡶࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡮ࡹࠠࡷࡣ࡯࡭ࡩࠦࠨ࡯ࡱࡱ࠱ࡪࡳࡰࡵࡻࠣࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡤࡲࡩࠦࡡࡶࡶ࡫ࡳࡷࡹࠩ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᵸ")
    return (
        isinstance(result.get(bstack11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᵹ"), None), list)
        and len(result[bstack11l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᵺ")]) > 0
        and isinstance(result.get(bstack11l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᵻ"), None), list)
        and len(result[bstack11l11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᵼ")]) > 0
    )
def _1111ll111l1_opy_(repo):
    bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡘࡷࡿࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡩࡧࠣࡦࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡴࡨࡴࡴࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡩࡣࡵࡨࡨࡵࡤࡦࡦࠣࡲࡦࡳࡥࡴࠢࡤࡲࡩࠦࡷࡰࡴ࡮ࠤࡼ࡯ࡴࡩࠢࡤࡰࡱࠦࡖࡄࡕࠣࡴࡷࡵࡶࡪࡦࡨࡶࡸ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡦࡷࡧ࡮ࡤࡪࠣ࡭࡫ࠦࡰࡰࡵࡶ࡭ࡧࡲࡥ࠭ࠢࡨࡰࡸ࡫ࠠࡏࡱࡱࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᵽ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111lll1111_opy_ = origin.refs[bstack11l11_opy_ (u"ࠫࡍࡋࡁࡅࠩᵾ")]
            target = bstack1111lll1111_opy_.reference.name
            if target.startswith(bstack11l11_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭ᵿ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11l11_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧᶀ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111l11lllll_opy_(commits):
    bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᶁ")
    bstack11111lll1ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11111llll11_opy_ in diff:
                        if bstack11111llll11_opy_.a_path:
                            bstack11111lll1ll_opy_.add(bstack11111llll11_opy_.a_path)
                        if bstack11111llll11_opy_.b_path:
                            bstack11111lll1ll_opy_.add(bstack11111llll11_opy_.b_path)
    except Exception:
        pass
    return list(bstack11111lll1ll_opy_)
def bstack111l1l111ll_opy_(bstack1111l11lll1_opy_):
    bstack1111l1ll1ll_opy_ = bstack11111llllll_opy_(bstack1111l11lll1_opy_)
    if bstack1111l1ll1ll_opy_ and bstack1111l1ll1ll_opy_ > bstack111ll11l1l1_opy_:
        bstack111l11llll1_opy_ = bstack1111l1ll1ll_opy_ - bstack111ll11l1l1_opy_
        bstack111l1l1lll1_opy_ = bstack1111l1111ll_opy_(bstack1111l11lll1_opy_[bstack11l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᶂ")], bstack111l11llll1_opy_)
        bstack1111l11lll1_opy_[bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᶃ")] = bstack111l1l1lll1_opy_
        logger.info(bstack11l11_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᶄ")
                    .format(bstack11111llllll_opy_(bstack1111l11lll1_opy_) / 1024))
    return bstack1111l11lll1_opy_
def bstack11111llllll_opy_(bstack11l1l11l_opy_):
    try:
        if bstack11l1l11l_opy_:
            bstack111l111l111_opy_ = json.dumps(bstack11l1l11l_opy_)
            bstack1111l11ll11_opy_ = sys.getsizeof(bstack111l111l111_opy_)
            return bstack1111l11ll11_opy_
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᶅ").format(e))
    return -1
def bstack1111l1111ll_opy_(field, bstack1111l1l11l1_opy_):
    try:
        bstack111l1l1l1ll_opy_ = len(bytes(bstack111lll1ll11_opy_, bstack11l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᶆ")))
        bstack11111ll1lll_opy_ = bytes(field, bstack11l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᶇ"))
        bstack111l11l111l_opy_ = len(bstack11111ll1lll_opy_)
        bstack1111l1lllll_opy_ = ceil(bstack111l11l111l_opy_ - bstack1111l1l11l1_opy_ - bstack111l1l1l1ll_opy_)
        if bstack1111l1lllll_opy_ > 0:
            bstack1111ll11lll_opy_ = bstack11111ll1lll_opy_[:bstack1111l1lllll_opy_].decode(bstack11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᶈ"), errors=bstack11l11_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᶉ")) + bstack111lll1ll11_opy_
            return bstack1111ll11lll_opy_
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᶊ").format(e))
    return field
def bstack11l1lllll1_opy_():
    env = os.environ
    if (bstack11l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᶋ") in env and len(env[bstack11l11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᶌ")]) > 0) or (
            bstack11l11_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᶍ") in env and len(env[bstack11l11_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᶎ")]) > 0):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᶏ"): bstack11l11_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤᶐ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᶑ"): env.get(bstack11l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᶒ")),
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᶓ"): env.get(bstack11l11_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢᶔ")),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᶕ"): env.get(bstack11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᶖ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠣࡅࡌࠦᶗ")) == bstack11l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᶘ") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧᶙ"))):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᶚ"): bstack11l11_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢᶛ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᶜ"): env.get(bstack11l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᶝ")),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᶞ"): env.get(bstack11l11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨᶟ")),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᶠ"): env.get(bstack11l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢᶡ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠧࡉࡉࠣᶢ")) == bstack11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᶣ") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᶤ"))):
        return {
            bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᶥ"): bstack11l11_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᶦ"),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᶧ"): env.get(bstack11l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦᶨ")),
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᶩ"): env.get(bstack11l11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᶪ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᶫ"): env.get(bstack11l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᶬ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡆࡍࠧᶭ")) == bstack11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᶮ") and env.get(bstack11l11_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᶯ")) == bstack11l11_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᶰ"):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᶱ"): bstack11l11_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᶲ"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᶳ"): None,
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶴ"): None,
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᶵ"): None
        }
    if env.get(bstack11l11_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᶶ")) and env.get(bstack11l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᶷ")):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᶸ"): bstack11l11_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᶹ"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᶺ"): env.get(bstack11l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᶻ")),
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᶼ"): None,
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶽ"): env.get(bstack11l11_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᶾ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠨࡃࡊࠤᶿ")) == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᷀") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢ᷁"))):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫᷂ࠢ"): bstack11l11_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤ᷃"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᷄"): env.get(bstack11l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣ᷅")),
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᷆"): None,
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᷇"): env.get(bstack11l11_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᷈"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡆࡍࠧ᷉")) == bstack11l11_opy_ (u"ࠥࡸࡷࡻࡥ᷊ࠣ") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢ᷋"))):
        return {
            bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᷌"): bstack11l11_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤ᷍"),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᷎ࠥ"): env.get(bstack11l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒ᷏ࠢ")),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨ᷐ࠦ"): env.get(bstack11l11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᷑")),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᷒"): env.get(bstack11l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᷓ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠨࡃࡊࠤᷔ")) == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᷕ") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᷖ"))):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᷗ"): bstack11l11_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᷘ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᷙ"): env.get(bstack11l11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᷚ")),
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᷛ"): env.get(bstack11l11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᷜ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᷝ"): env.get(bstack11l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᷞ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡇࡎࠨᷟ")) == bstack11l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᷠ") and bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᷡ"))):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᷢ"): bstack11l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᷣ"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᷤ"): env.get(bstack11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᷥ")),
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᷦ"): env.get(bstack11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᷧ")) or env.get(bstack11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᷨ")),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᷩ"): env.get(bstack11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᷪ"))
        }
    if bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᷫ"))):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᷬ"): bstack11l11_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᷭ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᷮ"): bstack11l11_opy_ (u"ࠧࢁࡽࡼࡿࠥᷯ").format(env.get(bstack11l11_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᷰ")), env.get(bstack11l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᷱ"))),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᷲ"): env.get(bstack11l11_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᷳ")),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᷴ"): env.get(bstack11l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᷵"))
        }
    if bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢ᷶"))):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᷷ࠦ"): bstack11l11_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤ᷸"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᷹ࠦ"): bstack11l11_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ᷺ࠣ").format(env.get(bstack11l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩ᷻")), env.get(bstack11l11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬ᷼")), env.get(bstack11l11_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ᷽࠭")), env.get(bstack11l11_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ᷾"))),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᷿"): env.get(bstack11l11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧḀ")),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣḁ"): env.get(bstack11l11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦḂ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧḃ")) and env.get(bstack11l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢḄ")):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦḅ"): bstack11l11_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤḆ"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦḇ"): bstack11l11_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧḈ").format(env.get(bstack11l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ḉ")), env.get(bstack11l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩḊ")), env.get(bstack11l11_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬḋ"))),
            bstack11l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣḌ"): env.get(bstack11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢḍ")),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢḎ"): env.get(bstack11l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤḏ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣḐ")), env.get(bstack11l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥḑ")), env.get(bstack11l11_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤḒ"))]):
        return {
            bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦḓ"): bstack11l11_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢḔ"),
            bstack11l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦḕ"): env.get(bstack11l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣḖ")),
            bstack11l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧḗ"): env.get(bstack11l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤḘ")),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦḙ"): env.get(bstack11l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦḚ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧḛ")):
        return {
            bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨḜ"): bstack11l11_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤḝ"),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨḞ"): env.get(bstack11l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨḟ")),
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢḠ"): env.get(bstack11l11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧḡ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨḢ"): env.get(bstack11l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨḣ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥḤ")) or env.get(bstack11l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧḥ")):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤḦ"): bstack11l11_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨḧ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤḨ"): env.get(bstack11l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦḩ")),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥḪ"): bstack11l11_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤḫ") if env.get(bstack11l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧḬ")) else None,
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥḭ"): env.get(bstack11l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥḮ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦḯ")), env.get(bstack11l11_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣḰ")), env.get(bstack11l11_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣḱ"))]):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢḲ"): bstack11l11_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤḳ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢḴ"): None,
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢḵ"): env.get(bstack11l11_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥḶ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨḷ"): env.get(bstack11l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥḸ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧḹ")):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣḺ"): bstack11l11_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢḻ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣḼ"): env.get(bstack11l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧḽ")),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤḾ"): bstack11l11_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤḿ").format(env.get(bstack11l11_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬṀ"))) if env.get(bstack11l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨṁ")) else None,
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥṂ"): env.get(bstack11l11_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢṃ"))
        }
    if bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢṄ"))):
        return {
            bstack11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧṅ"): bstack11l11_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤṆ"),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧṇ"): env.get(bstack11l11_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢṈ")),
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨṉ"): env.get(bstack11l11_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣṊ")),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧṋ"): env.get(bstack11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤṌ"))
        }
    if bstack1ll1l11lll_opy_(env.get(bstack11l11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤṍ"))):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢṎ"): bstack11l11_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦṏ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢṐ"): bstack11l11_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨṑ").format(env.get(bstack11l11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪṒ")), env.get(bstack11l11_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫṓ")), env.get(bstack11l11_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨṔ"))),
            bstack11l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦṕ"): env.get(bstack11l11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧṖ")),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥṗ"): env.get(bstack11l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧṘ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠨࡃࡊࠤṙ")) == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧṚ") and env.get(bstack11l11_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣṛ")) == bstack11l11_opy_ (u"ࠤ࠴ࠦṜ"):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣṝ"): bstack11l11_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦṞ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣṟ"): bstack11l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤṠ").format(env.get(bstack11l11_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫṡ"))),
            bstack11l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥṢ"): None,
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣṣ"): None,
        }
    if env.get(bstack11l11_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨṤ")):
        return {
            bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤṥ"): bstack11l11_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢṦ"),
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤṧ"): None,
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤṨ"): env.get(bstack11l11_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤṩ")),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣṪ"): env.get(bstack11l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤṫ"))
        }
    if any([env.get(bstack11l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢṬ")), env.get(bstack11l11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧṭ")), env.get(bstack11l11_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦṮ")), env.get(bstack11l11_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣṯ"))]):
        return {
            bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨṰ"): bstack11l11_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧṱ"),
            bstack11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨṲ"): None,
            bstack11l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨṳ"): env.get(bstack11l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨṴ")) or None,
            bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧṵ"): env.get(bstack11l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤṶ"), 0)
        }
    if env.get(bstack11l11_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨṷ")):
        return {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢṸ"): bstack11l11_opy_ (u"ࠥࡋࡴࡉࡄࠣṹ"),
            bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢṺ"): None,
            bstack11l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢṻ"): env.get(bstack11l11_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦṼ")),
            bstack11l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨṽ"): env.get(bstack11l11_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢṾ"))
        }
    if env.get(bstack11l11_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢṿ")):
        return {
            bstack11l11_opy_ (u"ࠥࡲࡦࡳࡥࠣẀ"): bstack11l11_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢẁ"),
            bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣẂ"): env.get(bstack11l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧẃ")),
            bstack11l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤẄ"): env.get(bstack11l11_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦẅ")),
            bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣẆ"): env.get(bstack11l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣẇ"))
        }
    return {bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥẈ"): None}
def get_host_info():
    return {
        bstack11l11_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢẉ"): platform.node(),
        bstack11l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣẊ"): platform.system(),
        bstack11l11_opy_ (u"ࠢࡵࡻࡳࡩࠧẋ"): platform.machine(),
        bstack11l11_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤẌ"): platform.version(),
        bstack11l11_opy_ (u"ࠤࡤࡶࡨ࡮ࠢẍ"): platform.architecture()[0]
    }
def bstack1l1l1l1lll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111l1l1ll1_opy_():
    if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫẎ")):
        return bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪẏ")
    return bstack11l11_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫẐ")
def bstack1111l111l11_opy_(driver):
    info = {
        bstack11l11_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬẑ"): driver.capabilities,
        bstack11l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫẒ"): driver.session_id,
        bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩẓ"): driver.capabilities.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧẔ"), None),
        bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬẕ"): driver.capabilities.get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬẖ"), None),
        bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧẗ"): driver.capabilities.get(bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬẘ"), None),
        bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪẙ"):driver.capabilities.get(bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪẚ"), None),
    }
    if bstack1111l1l1ll1_opy_() == bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨẛ"):
        if bstack11l1l1ll1_opy_():
            info[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫẜ")] = bstack11l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪẝ")
        elif driver.capabilities.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ẞ"), {}).get(bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪẟ"), False):
            info[bstack11l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨẠ")] = bstack11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬạ")
        else:
            info[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪẢ")] = bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬả")
    return info
def bstack11l1l1ll1_opy_():
    if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪẤ")):
        return True
    if bstack1ll1l11lll_opy_(os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ấ"), None)):
        return True
    return False
def bstack1111lllll11_opy_(bstack111l1l1l11l_opy_, url, response, headers=None, data=None):
    bstack11l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡂࡶ࡫࡯ࡨࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡯ࡳ࡬ࠦࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠰ࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡵࡺ࡫ࡳࡵࡡࡷࡽࡵ࡫࠺ࠡࡊࡗࡘࡕࠦ࡭ࡦࡶ࡫ࡳࡩࠦࠨࡈࡇࡗ࠰ࠥࡖࡏࡔࡖ࠯ࠤࡪࡺࡣ࠯ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡺࡸ࡬࠻ࠢࡕࡩࡶࡻࡥࡴࡶ࡙ࠣࡗࡒ࠯ࡦࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡱࡥ࡮ࡪࡩࡴࠡࡨࡵࡳࡲࠦࡲࡦࡳࡸࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡩࡦࡪࡥࡳࡵ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡮ࡥࡢࡦࡨࡶࡸࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡤࡸࡦࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡌࡖࡓࡓࠦࡤࡢࡶࡤࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡋࡵࡲ࡮ࡣࡷࡸࡪࡪࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠥࡽࡩࡵࡪࠣࡶࡪࡷࡵࡦࡵࡷࠤࡦࡴࡤࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠋࠢࠣࠤࠥࠨࠢࠣẦ")
    bstack111l11l11ll_opy_ = {
        bstack11l11_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣầ"): headers,
        bstack11l11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣẨ"): bstack111l1l1l11l_opy_.upper(),
        bstack11l11_opy_ (u"ࠤࡤ࡫ࡪࡴࡴࠣẩ"): None,
        bstack11l11_opy_ (u"ࠥࡩࡳࡪࡰࡰ࡫ࡱࡸࠧẪ"): url,
        bstack11l11_opy_ (u"ࠦ࡯ࡹ࡯࡯ࠤẫ"): data
    }
    try:
        bstack111l111ll1l_opy_ = response.json()
    except Exception:
        bstack111l111ll1l_opy_ = response.text
    bstack111l11ll11l_opy_ = {
        bstack11l11_opy_ (u"ࠧࡨ࡯ࡥࡻࠥẬ"): bstack111l111ll1l_opy_,
        bstack11l11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࡉ࡯ࡥࡧࠥậ"): response.status_code
    }
    return {
        bstack11l11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣẮ"): bstack111l11l11ll_opy_,
        bstack11l11_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥắ"): bstack111l11ll11l_opy_
    }
def bstack1l11l11ll1_opy_(bstack111l1l1l11l_opy_, url, data, config):
    headers = config.get(bstack11l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪẰ"), None)
    proxies = bstack1llll1l111_opy_(config, url)
    auth = config.get(bstack11l11_opy_ (u"ࠪࡥࡺࡺࡨࠨằ"), None)
    response = requests.request(
            bstack111l1l1l11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111lllll11_opy_(bstack111l1l1l11l_opy_, url, response, headers, data)
        bstack111111l11_opy_.debug(json.dumps(log_message, separators=(bstack11l11_opy_ (u"ࠫ࠱࠭Ẳ"), bstack11l11_opy_ (u"ࠬࡀࠧẳ"))))
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࢀࢃࠢẴ").format(e))
    return response
def bstack1l1l11111l_opy_(bstack1l11111ll1_opy_, size):
    bstack11l1l11l1l_opy_ = []
    while len(bstack1l11111ll1_opy_) > size:
        bstack1l11lllll1_opy_ = bstack1l11111ll1_opy_[:size]
        bstack11l1l11l1l_opy_.append(bstack1l11lllll1_opy_)
        bstack1l11111ll1_opy_ = bstack1l11111ll1_opy_[size:]
    bstack11l1l11l1l_opy_.append(bstack1l11111ll1_opy_)
    return bstack11l1l11l1l_opy_
def bstack1111l111lll_opy_(message, bstack1111lll11ll_opy_=False):
    os.write(1, bytes(message, bstack11l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ẵ")))
    os.write(1, bytes(bstack11l11_opy_ (u"ࠨ࡞ࡱࠫẶ"), bstack11l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨặ")))
    if bstack1111lll11ll_opy_:
        with open(bstack11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩẸ") + os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪẹ")] + bstack11l11_opy_ (u"ࠬ࠴࡬ࡰࡩࠪẺ"), bstack11l11_opy_ (u"࠭ࡡࠨẻ")) as f:
            f.write(message + bstack11l11_opy_ (u"ࠧ࡝ࡰࠪẼ"))
def bstack1l111lllll1_opy_():
    return os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫẽ")].lower() == bstack11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧẾ")
def bstack11l1lll11_opy_():
    return bstack111111l11l_opy_().replace(tzinfo=None).isoformat() + bstack11l11_opy_ (u"ࠪ࡞ࠬế")
def bstack111l11l1ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l11_opy_ (u"ࠫ࡟࠭Ề"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l11_opy_ (u"ࠬࡠࠧề")))).total_seconds() * 1000
def bstack111l111l1l1_opy_(timestamp):
    return bstack1111l1111l1_opy_(timestamp).isoformat() + bstack11l11_opy_ (u"࡚࠭ࠨỂ")
def bstack1111llllll1_opy_(bstack111l11ll1l1_opy_):
    date_format = bstack11l11_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬể")
    bstack1111l11l1ll_opy_ = datetime.datetime.strptime(bstack111l11ll1l1_opy_, date_format)
    return bstack1111l11l1ll_opy_.isoformat() + bstack11l11_opy_ (u"ࠨ࡜ࠪỄ")
def bstack111l1111l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩễ")
    else:
        return bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪỆ")
def bstack1ll1l11lll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l11_opy_ (u"ࠫࡹࡸࡵࡦࠩệ")
def bstack111l11l1l11_opy_(val):
    return val.__str__().lower() == bstack11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫỈ")
def error_handler(bstack1111ll1l1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111ll1l1ll_opy_ as e:
                print(bstack11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨỉ").format(func.__name__, bstack1111ll1l1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l1l11111_opy_(bstack1111ll1111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111ll1111l_opy_(cls, *args, **kwargs)
            except bstack1111ll1l1ll_opy_ as e:
                print(bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢỊ").format(bstack1111ll1111l_opy_.__name__, bstack1111ll1l1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l1l11111_opy_
    else:
        return decorator
def bstack1ll111l11_opy_(bstack1llll111111_opy_):
    if os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫị")) is not None:
        return bstack1ll1l11lll_opy_(os.getenv(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬỌ")))
    if bstack11l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧọ") in bstack1llll111111_opy_ and bstack111l11l1l11_opy_(bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨỎ")]):
        return False
    if bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧỏ") in bstack1llll111111_opy_ and bstack111l11l1l11_opy_(bstack1llll111111_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨỐ")]):
        return False
    return True
def bstack11lll1111l_opy_():
    try:
        from pytest_bdd import reporting
        bstack111l111l1ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢố"), None)
        return bstack111l111l1ll_opy_ is None or bstack111l111l1ll_opy_ == bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧỒ")
    except Exception as e:
        return False
def bstack1l1llll1ll_opy_(hub_url, CONFIG):
    if bstack111l1lll1_opy_() <= version.parse(bstack11l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩồ")):
        if hub_url:
            return bstack11l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦỔ") + hub_url + bstack11l11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣổ")
        return bstack1l1111ll1_opy_
    if hub_url:
        return bstack11l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢỖ") + hub_url + bstack11l11_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢỗ")
    return bstack11l111l1_opy_
def bstack1111l1ll1l1_opy_():
    return isinstance(os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭Ộ")), str)
def bstack11ll1lll11_opy_(url):
    return urlparse(url).hostname
def bstack1ll11lll_opy_(hostname):
    for bstack11ll11111l_opy_ in bstack1l11ll1lll_opy_:
        regex = re.compile(bstack11ll11111l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1111l11llll_opy_(bstack1111lllllll_opy_, file_name, logger):
    bstack1l1llll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠨࢀࠪộ")), bstack1111lllllll_opy_)
    try:
        if not os.path.exists(bstack1l1llll1l1_opy_):
            os.makedirs(bstack1l1llll1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠩࢁࠫỚ")), bstack1111lllllll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l11_opy_ (u"ࠪࡻࠬớ")):
                pass
            with open(file_path, bstack11l11_opy_ (u"ࠦࡼ࠱ࠢỜ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111ll11l_opy_.format(str(e)))
def bstack1111llll11l_opy_(file_name, key, value, logger):
    file_path = bstack1111l11llll_opy_(bstack11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬờ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1ll1l1_opy_ = json.load(open(file_path, bstack11l11_opy_ (u"࠭ࡲࡣࠩỞ")))
        else:
            bstack1l1ll1l1_opy_ = {}
        bstack1l1ll1l1_opy_[key] = value
        with open(file_path, bstack11l11_opy_ (u"ࠢࡸ࠭ࠥở")) as outfile:
            json.dump(bstack1l1ll1l1_opy_, outfile)
def bstack1l1111ll_opy_(file_name, logger):
    file_path = bstack1111l11llll_opy_(bstack11l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨỠ"), file_name, logger)
    bstack1l1ll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l11_opy_ (u"ࠩࡵࠫỡ")) as bstack1ll1l1ll1l_opy_:
            bstack1l1ll1l1_opy_ = json.load(bstack1ll1l1ll1l_opy_)
    return bstack1l1ll1l1_opy_
def bstack11l11llll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧỢ") + file_path + bstack11l11_opy_ (u"ࠫࠥ࠭ợ") + str(e))
def bstack111l1lll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l11_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢỤ")
def bstack1l1l1llll_opy_(config):
    if bstack11l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬụ") in config:
        del (config[bstack11l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ủ")])
        return False
    if bstack111l1lll1_opy_() < version.parse(bstack11l11_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧủ")):
        return False
    if bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨỨ")):
        return True
    if bstack11l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪứ") in config and config[bstack11l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫỪ")] is False:
        return False
    else:
        return True
def bstack1llllllll_opy_(args_list, bstack111l11111ll_opy_):
    index = -1
    for value in bstack111l11111ll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l111l1l11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l111l1l11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111ll11l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111ll11l1_opy_ = bstack1111ll11l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬừ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ử"), exception=exception)
    def bstack1lll1l11lll_opy_(self):
        if self.result != bstack11l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧử"):
            return None
        if isinstance(self.exception_type, str) and bstack11l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦỮ") in self.exception_type:
            return bstack11l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥữ")
        return bstack11l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦỰ")
    def bstack111l1l1ll11_opy_(self):
        if self.result != bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫự"):
            return None
        if self.bstack1111ll11l1_opy_:
            return self.bstack1111ll11l1_opy_
        return bstack1111lll111l_opy_(self.exception)
def bstack1111lll111l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11111lll11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll11l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11llllll_opy_(config, logger):
    try:
        import playwright
        bstack111l1l1l1l1_opy_ = playwright.__file__
        bstack1111ll1ll1l_opy_ = os.path.split(bstack111l1l1l1l1_opy_)
        bstack111l111111l_opy_ = bstack1111ll1ll1l_opy_[0] + bstack11l11_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨỲ")
        os.environ[bstack11l11_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩỳ")] = bstack111l11l11_opy_(config)
        with open(bstack111l111111l_opy_, bstack11l11_opy_ (u"ࠧࡳࠩỴ")) as f:
            bstack111l11l111_opy_ = f.read()
            bstack111l1l1l111_opy_ = bstack11l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧỵ")
            bstack11111lll111_opy_ = bstack111l11l111_opy_.find(bstack111l1l1l111_opy_)
            if bstack11111lll111_opy_ == -1:
              process = subprocess.Popen(bstack11l11_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨỶ"), shell=True, cwd=bstack1111ll1ll1l_opy_[0])
              process.wait()
              bstack11111lllll1_opy_ = bstack11l11_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪỷ")
              bstack1111ll11l11_opy_ = bstack11l11_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣỸ")
              bstack1111ll1ll11_opy_ = bstack111l11l111_opy_.replace(bstack11111lllll1_opy_, bstack1111ll11l11_opy_)
              with open(bstack111l111111l_opy_, bstack11l11_opy_ (u"ࠬࡽࠧỹ")) as f:
                f.write(bstack1111ll1ll11_opy_)
    except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
def bstack1l111l11l_opy_():
  try:
    bstack111l1l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭Ỻ"))
    bstack111l1111lll_opy_ = []
    if os.path.exists(bstack111l1l11ll1_opy_):
      with open(bstack111l1l11ll1_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
      os.remove(bstack111l1l11ll1_opy_)
    return bstack111l1111lll_opy_
  except:
    pass
  return []
def bstack111llll1_opy_(bstack1111lll1_opy_):
  try:
    bstack111l1111lll_opy_ = []
    bstack111l1l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧỻ"))
    if os.path.exists(bstack111l1l11ll1_opy_):
      with open(bstack111l1l11ll1_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
    bstack111l1111lll_opy_.append(bstack1111lll1_opy_)
    with open(bstack111l1l11ll1_opy_, bstack11l11_opy_ (u"ࠨࡹࠪỼ")) as f:
        json.dump(bstack111l1111lll_opy_, f)
  except:
    pass
def bstack11111l111_opy_(logger, bstack111l1l111l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬỽ"), bstack11l11_opy_ (u"ࠪࠫỾ"))
    if test_name == bstack11l11_opy_ (u"ࠫࠬỿ"):
        test_name = threading.current_thread().__dict__.get(bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫἀ"), bstack11l11_opy_ (u"࠭ࠧἁ"))
    bstack1111ll1l1l1_opy_ = bstack11l11_opy_ (u"ࠧ࠭ࠢࠪἂ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l1l111l1_opy_:
        bstack11lllll1l1_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨἃ"), bstack11l11_opy_ (u"ࠩ࠳ࠫἄ"))
        bstack11lll11l_opy_ = {bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨἅ"): test_name, bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪἆ"): bstack1111ll1l1l1_opy_, bstack11l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫἇ"): bstack11lllll1l1_opy_}
        bstack1111l11l1l1_opy_ = []
        bstack111l1l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬἈ"))
        if os.path.exists(bstack111l1l11lll_opy_):
            with open(bstack111l1l11lll_opy_) as f:
                bstack1111l11l1l1_opy_ = json.load(f)
        bstack1111l11l1l1_opy_.append(bstack11lll11l_opy_)
        with open(bstack111l1l11lll_opy_, bstack11l11_opy_ (u"ࠧࡸࠩἉ")) as f:
            json.dump(bstack1111l11l1l1_opy_, f)
    else:
        bstack11lll11l_opy_ = {bstack11l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ἂ"): test_name, bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨἋ"): bstack1111ll1l1l1_opy_, bstack11l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩἌ"): str(multiprocessing.current_process().name)}
        if bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨἍ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11lll11l_opy_)
  except Exception as e:
      logger.warn(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤἎ").format(e))
def bstack111111111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩἏ"))
    try:
      bstack111l11ll1ll_opy_ = []
      bstack11lll11l_opy_ = {bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬἐ"): test_name, bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧἑ"): error_message, bstack11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨἒ"): index}
      bstack111l11l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫἓ"))
      if os.path.exists(bstack111l11l1111_opy_):
          with open(bstack111l11l1111_opy_) as f:
              bstack111l11ll1ll_opy_ = json.load(f)
      bstack111l11ll1ll_opy_.append(bstack11lll11l_opy_)
      with open(bstack111l11l1111_opy_, bstack11l11_opy_ (u"ࠫࡼ࠭ἔ")) as f:
          json.dump(bstack111l11ll1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣἕ").format(e))
    return
  bstack111l11ll1ll_opy_ = []
  bstack11lll11l_opy_ = {bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ἖"): test_name, bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭἗"): error_message, bstack11l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧἘ"): index}
  bstack111l11l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪἙ"))
  lock_file = bstack111l11l1111_opy_ + bstack11l11_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩἚ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l11l1111_opy_):
          with open(bstack111l11l1111_opy_, bstack11l11_opy_ (u"ࠫࡷ࠭Ἓ")) as f:
              content = f.read().strip()
              if content:
                  bstack111l11ll1ll_opy_ = json.load(open(bstack111l11l1111_opy_))
      bstack111l11ll1ll_opy_.append(bstack11lll11l_opy_)
      with open(bstack111l11l1111_opy_, bstack11l11_opy_ (u"ࠬࡽࠧἜ")) as f:
          json.dump(bstack111l11ll1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨ࠼ࠣࡿࢂࠨἝ").format(e))
def bstack111ll11111_opy_(bstack111l111l11_opy_, name, logger):
  try:
    bstack11lll11l_opy_ = {bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ἞"): name, bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ἟"): bstack111l111l11_opy_, bstack11l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨἠ"): str(threading.current_thread()._name)}
    return bstack11lll11l_opy_
  except Exception as e:
    logger.warn(bstack11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢἡ").format(e))
  return
def bstack1111llll111_opy_():
    return platform.system() == bstack11l11_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬἢ")
def bstack11l1l1llll_opy_(bstack1111l11l11l_opy_, config, logger):
    bstack1111ll1l111_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111l11l11l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦἣ").format(e))
    return bstack1111ll1l111_opy_
def bstack1111l11111l_opy_(bstack111l11l1lll_opy_, bstack1111lll1ll1_opy_):
    bstack11111lll1l1_opy_ = version.parse(bstack111l11l1lll_opy_)
    bstack1111l1l111l_opy_ = version.parse(bstack1111lll1ll1_opy_)
    if bstack11111lll1l1_opy_ > bstack1111l1l111l_opy_:
        return 1
    elif bstack11111lll1l1_opy_ < bstack1111l1l111l_opy_:
        return -1
    else:
        return 0
def bstack111111l11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1111l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1111l1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll1l1ll1_opy_(options, framework, config, bstack111ll1ll1l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l11_opy_ (u"࠭ࡧࡦࡶࠪἤ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll1llllll_opy_ = caps.get(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨἥ"))
    bstack1111ll11ll1_opy_ = True
    bstack1ll11ll1l_opy_ = os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ἦ")]
    bstack1l1l111l1l1_opy_ = config.get(bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἧ"), False)
    if bstack1l1l111l1l1_opy_:
        bstack1ll1l11ll11_opy_ = config.get(bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪἨ"), {})
        bstack1ll1l11ll11_opy_[bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧἩ")] = os.getenv(bstack11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪἪ"))
        bstack11l11l1l1l1_opy_ = json.loads(os.getenv(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧἫ"), bstack11l11_opy_ (u"ࠧࡼࡿࠪἬ"))).get(bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩἭ"))
    if bstack111l11l1l11_opy_(caps.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨἮ"))) or bstack111l11l1l11_opy_(caps.get(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪἯ"))):
        bstack1111ll11ll1_opy_ = False
    if bstack1l1l1llll_opy_({bstack11l11_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦἰ"): bstack1111ll11ll1_opy_}):
        bstack1ll1llllll_opy_ = bstack1ll1llllll_opy_ or {}
        bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧἱ")] = bstack111l1111l1l_opy_(framework)
        bstack1ll1llllll_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨἲ")] = bstack1l111lllll1_opy_()
        bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪἳ")] = bstack1ll11ll1l_opy_
        bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪἴ")] = bstack111ll1ll1l_opy_
        if bstack1l1l111l1l1_opy_:
            bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἵ")] = bstack1l1l111l1l1_opy_
            bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪἶ")] = bstack1ll1l11ll11_opy_
            bstack1ll1llllll_opy_[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫἷ")][bstack11l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ἰ")] = bstack11l11l1l1l1_opy_
        if getattr(options, bstack11l11_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧἹ"), None):
            options.set_capability(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨἺ"), bstack1ll1llllll_opy_)
        else:
            options[bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩἻ")] = bstack1ll1llllll_opy_
    else:
        if getattr(options, bstack11l11_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪἼ"), None):
            options.set_capability(bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫἽ"), bstack111l1111l1l_opy_(framework))
            options.set_capability(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬἾ"), bstack1l111lllll1_opy_())
            options.set_capability(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧἿ"), bstack1ll11ll1l_opy_)
            options.set_capability(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧὀ"), bstack111ll1ll1l_opy_)
            if bstack1l1l111l1l1_opy_:
                options.set_capability(bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ὁ"), bstack1l1l111l1l1_opy_)
                options.set_capability(bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧὂ"), bstack1ll1l11ll11_opy_)
                options.set_capability(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩὃ"), bstack11l11l1l1l1_opy_)
        else:
            options[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫὄ")] = bstack111l1111l1l_opy_(framework)
            options[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬὅ")] = bstack1l111lllll1_opy_()
            options[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ὆")] = bstack1ll11ll1l_opy_
            options[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ὇")] = bstack111ll1ll1l_opy_
            if bstack1l1l111l1l1_opy_:
                options[bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ὀ")] = bstack1l1l111l1l1_opy_
                options[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧὉ")] = bstack1ll1l11ll11_opy_
                options[bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨὊ")][bstack11l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫὋ")] = bstack11l11l1l1l1_opy_
    return options
def bstack111l1l11l11_opy_(bstack1111l1lll1l_opy_, framework):
    bstack111ll1ll1l_opy_ = bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨὌ"))
    if bstack1111l1lll1l_opy_ and len(bstack1111l1lll1l_opy_.split(bstack11l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫὍ"))) > 1:
        ws_url = bstack1111l1lll1l_opy_.split(bstack11l11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ὎"))[0]
        if bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ὏") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111llll1l_opy_ = json.loads(urllib.parse.unquote(bstack1111l1lll1l_opy_.split(bstack11l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧὐ"))[1]))
            bstack11111llll1l_opy_ = bstack11111llll1l_opy_ or {}
            bstack1ll11ll1l_opy_ = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧὑ")]
            bstack11111llll1l_opy_[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫὒ")] = str(framework) + str(__version__)
            bstack11111llll1l_opy_[bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬὓ")] = bstack1l111lllll1_opy_()
            bstack11111llll1l_opy_[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧὔ")] = bstack1ll11ll1l_opy_
            bstack11111llll1l_opy_[bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧὕ")] = bstack111ll1ll1l_opy_
            bstack1111l1lll1l_opy_ = bstack1111l1lll1l_opy_.split(bstack11l11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ὖ"))[0] + bstack11l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧὗ") + urllib.parse.quote(json.dumps(bstack11111llll1l_opy_))
    return bstack1111l1lll1l_opy_
def bstack1ll1llll11_opy_():
    global bstack11llllll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11llllll11_opy_ = BrowserType.connect
    return bstack11llllll11_opy_
def bstack1l1lll1l_opy_(framework_name):
    global bstack11l1111ll1_opy_
    bstack11l1111ll1_opy_ = framework_name
    return framework_name
def bstack1l111lll_opy_(self, *args, **kwargs):
    global bstack11llllll11_opy_
    try:
        global bstack11l1111ll1_opy_
        if bstack11l11_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭὘") in kwargs:
            kwargs[bstack11l11_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧὙ")] = bstack111l1l11l11_opy_(
                kwargs.get(bstack11l11_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ὚"), None),
                bstack11l1111ll1_opy_
            )
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧὛ").format(str(e)))
    return bstack11llllll11_opy_(self, *args, **kwargs)
def bstack1111l1l11ll_opy_(bstack111l11111l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1llll1l111_opy_(bstack111l11111l1_opy_, bstack11l11_opy_ (u"ࠨࠢ὜"))
        if proxies and proxies.get(bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨὝ")):
            parsed_url = urlparse(proxies.get(bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ὞")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬὟ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ὠ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧὡ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨὢ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack111l111ll1_opy_(bstack111l11111l1_opy_):
    bstack1111ll1llll_opy_ = {
        bstack111lll1ll1l_opy_[bstack1111l1l1111_opy_]: bstack111l11111l1_opy_[bstack1111l1l1111_opy_]
        for bstack1111l1l1111_opy_ in bstack111l11111l1_opy_
        if bstack1111l1l1111_opy_ in bstack111lll1ll1l_opy_
    }
    bstack1111ll1llll_opy_[bstack11l11_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨὣ")] = bstack1111l1l11ll_opy_(bstack111l11111l1_opy_, bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢὤ")))
    bstack111l1l1111l_opy_ = [element.lower() for element in bstack111ll1ll1l1_opy_]
    bstack1111l111111_opy_(bstack1111ll1llll_opy_, bstack111l1l1111l_opy_)
    return bstack1111ll1llll_opy_
def bstack1111l111111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l11_opy_ (u"ࠣࠬ࠭࠮࠯ࠨὥ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111l111111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111l111111_opy_(item, keys)
def bstack1l11l11l11l_opy_():
    bstack111l11l1l1l_opy_ = [os.environ.get(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡌࡐࡊ࡙࡟ࡅࡋࡕࠦὦ")), os.path.join(os.path.expanduser(bstack11l11_opy_ (u"ࠥࢂࠧὧ")), bstack11l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫὨ")), os.path.join(bstack11l11_opy_ (u"ࠬ࠵ࡴ࡮ࡲࠪὩ"), bstack11l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ὢ"))]
    for path in bstack111l11l1l1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢὫ") + str(path) + bstack11l11_opy_ (u"ࠣࠩࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦὬ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l11_opy_ (u"ࠤࡊ࡭ࡻ࡯࡮ࡨࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠠࡧࡱࡵࠤࠬࠨὭ") + str(path) + bstack11l11_opy_ (u"ࠥࠫࠧὮ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦὯ") + str(path) + bstack11l11_opy_ (u"ࠧ࠭ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡷࠥࡺࡨࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴ࠰ࠥὰ"))
            else:
                logger.debug(bstack11l11_opy_ (u"ࠨࡃࡳࡧࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࠧࠣά") + str(path) + bstack11l11_opy_ (u"ࠢࠨࠢࡺ࡭ࡹ࡮ࠠࡸࡴ࡬ࡸࡪࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰ࠱ࠦὲ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l11_opy_ (u"ࠣࡑࡳࡩࡷࡧࡴࡪࡱࡱࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠠࡧࡱࡵࠤࠬࠨέ") + str(path) + bstack11l11_opy_ (u"ࠤࠪ࠲ࠧὴ"))
            return path
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡹࡵࠦࡦࡪ࡮ࡨࠤࠬࢁࡰࡢࡶ࡫ࢁࠬࡀࠠࠣή") + str(e) + bstack11l11_opy_ (u"ࠦࠧὶ"))
    logger.debug(bstack11l11_opy_ (u"ࠧࡇ࡬࡭ࠢࡳࡥࡹ࡮ࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠤί"))
    return None
@measure(event_name=EVENTS.bstack111lll111l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1lllll1l11l_opy_(binary_path, bstack1llll1lllll_opy_, bs_config):
    logger.debug(bstack11l11_opy_ (u"ࠨࡃࡶࡴࡵࡩࡳࡺࠠࡄࡎࡌࠤࡕࡧࡴࡩࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧὸ").format(binary_path))
    bstack1111lllll1l_opy_ = bstack11l11_opy_ (u"ࠧࠨό")
    bstack1111l111l1l_opy_ = {
        bstack11l11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ὺ"): __version__,
        bstack11l11_opy_ (u"ࠤࡲࡷࠧύ"): platform.system(),
        bstack11l11_opy_ (u"ࠥࡳࡸࡥࡡࡳࡥ࡫ࠦὼ"): platform.machine(),
        bstack11l11_opy_ (u"ࠦࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠤώ"): bstack11l11_opy_ (u"ࠬ࠶ࠧ὾"),
        bstack11l11_opy_ (u"ࠨࡳࡥ࡭ࡢࡰࡦࡴࡧࡶࡣࡪࡩࠧ὿"): bstack11l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᾀ")
    }
    bstack111l111l11l_opy_(bstack1111l111l1l_opy_)
    try:
        if binary_path:
            if bstack1111llll111_opy_():
                bstack1111l111l1l_opy_[bstack11l11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᾁ")] = subprocess.check_output([binary_path, bstack11l11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᾂ")]).strip().decode(bstack11l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᾃ"))
            else:
                bstack1111l111l1l_opy_[bstack11l11_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᾄ")] = subprocess.check_output([binary_path, bstack11l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᾅ")], stderr=subprocess.DEVNULL).strip().decode(bstack11l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᾆ"))
        response = requests.request(
            bstack11l11_opy_ (u"ࠧࡈࡇࡗࠫᾇ"),
            url=bstack11l111ll1_opy_(bstack111lll1l1ll_opy_),
            headers=None,
            auth=(bs_config[bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᾈ")], bs_config[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᾉ")]),
            json=None,
            params=bstack1111l111l1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l11_opy_ (u"ࠪࡹࡷࡲࠧᾊ") in data.keys() and bstack11l11_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᾋ") in data.keys():
            logger.debug(bstack11l11_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨᾌ").format(bstack1111l111l1l_opy_[bstack11l11_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᾍ")]))
            if bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪᾎ") in os.environ:
                logger.debug(bstack11l11_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦᾏ"))
                data[bstack11l11_opy_ (u"ࠩࡸࡶࡱ࠭ᾐ")] = os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭ᾑ")]
            bstack1111ll1l11l_opy_ = bstack1111llll1ll_opy_(data[bstack11l11_opy_ (u"ࠫࡺࡸ࡬ࠨᾒ")], bstack1llll1lllll_opy_)
            bstack1111lllll1l_opy_ = os.path.join(bstack1llll1lllll_opy_, bstack1111ll1l11l_opy_)
            os.chmod(bstack1111lllll1l_opy_, 0o777) # bstack1111ll111ll_opy_ permission
            return bstack1111lllll1l_opy_
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧᾓ").format(e))
    return binary_path
def bstack111l111l11l_opy_(bstack1111l111l1l_opy_):
    try:
        if bstack11l11_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᾔ") not in bstack1111l111l1l_opy_[bstack11l11_opy_ (u"ࠧࡰࡵࠪᾕ")].lower():
            return
        if os.path.exists(bstack11l11_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᾖ")):
            with open(bstack11l11_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᾗ"), bstack11l11_opy_ (u"ࠥࡶࠧᾘ")) as f:
                bstack1111l1l1lll_opy_ = {}
                for line in f:
                    if bstack11l11_opy_ (u"ࠦࡂࠨᾙ") in line:
                        key, value = line.rstrip().split(bstack11l11_opy_ (u"ࠧࡃࠢᾚ"), 1)
                        bstack1111l1l1lll_opy_[key] = value.strip(bstack11l11_opy_ (u"࠭ࠢ࡝ࠩࠪᾛ"))
                bstack1111l111l1l_opy_[bstack11l11_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᾜ")] = bstack1111l1l1lll_opy_.get(bstack11l11_opy_ (u"ࠣࡋࡇࠦᾝ"), bstack11l11_opy_ (u"ࠤࠥᾞ"))
        elif os.path.exists(bstack11l11_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᾟ")):
            bstack1111l111l1l_opy_[bstack11l11_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᾠ")] = bstack11l11_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬᾡ")
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣᾢ") + e)
@measure(event_name=EVENTS.bstack111ll1l1111_opy_, stage=STAGE.bstack111ll11l1_opy_)
def bstack1111llll1ll_opy_(bstack111l11lll11_opy_, bstack111l11lll1l_opy_):
    logger.debug(bstack11l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᾣ") + str(bstack111l11lll11_opy_) + bstack11l11_opy_ (u"ࠣࠤᾤ"))
    zip_path = os.path.join(bstack111l11lll1l_opy_, bstack11l11_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᾥ"))
    bstack1111ll1l11l_opy_ = bstack11l11_opy_ (u"ࠪࠫᾦ")
    with requests.get(bstack111l11lll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l11_opy_ (u"ࠦࡼࡨࠢᾧ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᾨ"))
    with zipfile.ZipFile(zip_path, bstack11l11_opy_ (u"࠭ࡲࠨᾩ")) as zip_ref:
        bstack1111l11l111_opy_ = zip_ref.namelist()
        if len(bstack1111l11l111_opy_) > 0:
            bstack1111ll1l11l_opy_ = bstack1111l11l111_opy_[0] # bstack111l1l11l1l_opy_ bstack111lll111ll_opy_ will be bstack1111l111ll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l11lll1l_opy_)
        logger.debug(bstack11l11_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᾪ") + str(bstack111l11lll1l_opy_) + bstack11l11_opy_ (u"ࠣࠩࠥᾫ"))
    os.remove(zip_path)
    return bstack1111ll1l11l_opy_
def get_cli_dir():
    bstack1111lll11l1_opy_ = bstack1l11l11l11l_opy_()
    if bstack1111lll11l1_opy_:
        bstack1llll1lllll_opy_ = os.path.join(bstack1111lll11l1_opy_, bstack11l11_opy_ (u"ࠤࡦࡰ࡮ࠨᾬ"))
        if not os.path.exists(bstack1llll1lllll_opy_):
            os.makedirs(bstack1llll1lllll_opy_, mode=0o777, exist_ok=True)
        return bstack1llll1lllll_opy_
    else:
        raise FileNotFoundError(bstack11l11_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᾭ"))
def bstack1lllll11lll_opy_(bstack1llll1lllll_opy_):
    bstack11l11_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᾮ")
    bstack1111ll11l1l_opy_ = [
        os.path.join(bstack1llll1lllll_opy_, f)
        for f in os.listdir(bstack1llll1lllll_opy_)
        if os.path.isfile(os.path.join(bstack1llll1lllll_opy_, f)) and f.startswith(bstack11l11_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᾯ"))
    ]
    if len(bstack1111ll11l1l_opy_) > 0:
        return max(bstack1111ll11l1l_opy_, key=os.path.getmtime) # get bstack111l111ll11_opy_ binary
    return bstack11l11_opy_ (u"ࠨࠢᾰ")
def bstack11l11ll11ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l111ll1l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l111ll1l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11l1llll_opy_(data, keys, default=None):
    bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡣࡩࡩࡱࡿࠠࡨࡧࡷࠤࡦࠦ࡮ࡦࡵࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡤࡸࡦࡀࠠࡕࡪࡨࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡷࡳࠥࡺࡲࡢࡸࡨࡶࡸ࡫࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡱࡥࡺࡵ࠽ࠤࡆࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠ࡬ࡧࡼࡷ࠴࡯࡮ࡥ࡫ࡦࡩࡸࠦࡲࡦࡲࡵࡩࡸ࡫࡮ࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡥࡧࡣࡸࡰࡹࡀࠠࡗࡣ࡯ࡹࡪࠦࡴࡰࠢࡵࡩࡹࡻࡲ࡯ࠢ࡬ࡪࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡳࡧࡷࡹࡷࡴ࠺ࠡࡖ࡫ࡩࠥࡼࡡ࡭ࡷࡨࠤࡦࡺࠠࡵࡪࡨࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡧࡴࡩ࠮ࠣࡳࡷࠦࡤࡦࡨࡤࡹࡱࡺࠠࡪࡨࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᾱ")
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
def bstack1l1l1111l1_opy_(bstack1111ll11111_opy_, key, value):
    bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡷࡳࡷ࡫ࠠࡄࡎࡌࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠥࡳࡡࡱࡲ࡬ࡲ࡬ࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡱ࡯࡟ࡦࡰࡹࡣࡻࡧࡲࡴࡡࡰࡥࡵࡀࠠࡅ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡌࡧࡼࠤ࡫ࡸ࡯࡮ࠢࡆࡐࡎࡥࡃࡂࡒࡖࡣ࡙ࡕ࡟ࡄࡑࡑࡊࡎࡍࠊࠡࠢࠣࠤࠥࠦࠠࠡࡸࡤࡰࡺ࡫࠺ࠡࡘࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࡬ࡪࡰࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠊࠡࠢࠣࠤࠧࠨࠢᾲ")
    if key in bstack1l11l11l1l_opy_:
        bstack1l1l1l1l11_opy_ = bstack1l11l11l1l_opy_[key]
        if isinstance(bstack1l1l1l1l11_opy_, list):
            for env_name in bstack1l1l1l1l11_opy_:
                bstack1111ll11111_opy_[env_name] = value
        else:
            bstack1111ll11111_opy_[bstack1l1l1l1l11_opy_] = value