# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
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
from unittest import result
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1lllll_opy_, bstack11ll1ll11_opy_, bstack11lllll1ll_opy_,
                                    bstack11l1ll1ll1l_opy_, bstack11l1ll111l1_opy_, bstack11l1ll1l1l1_opy_, bstack11l1l11ll11_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l11l111ll_opy_, bstack11l11llll1_opy_
from bstack_utils.proxy import bstack1llll11lll_opy_, bstack11l1l1ll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1lll1llll_opy_
from bstack_utils.bstack1l1lll11l_opy_ import bstack11ll11111_opy_
from browserstack_sdk._version import __version__
bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
logger = bstack1lll1llll_opy_.get_logger(__name__, bstack1lll1llll_opy_.bstack1lll1l1ll1l_opy_())
def bstack11ll1ll11l1_opy_(config):
    return config[bstack1ll11ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᬆ")]
def bstack11ll1ll1l11_opy_(config):
    return config[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᬇ")]
def bstack11l111l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll11l1l1_opy_(obj):
    values = []
    bstack111ll1l1l1l_opy_ = re.compile(bstack1ll11ll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᬈ"), re.I)
    for key in obj.keys():
        if bstack111ll1l1l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l111l1l11_opy_(config):
    tags = []
    tags.extend(bstack111ll11l1l1_opy_(os.environ))
    tags.extend(bstack111ll11l1l1_opy_(config))
    return tags
def bstack111ll1l1lll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111llll1l1l_opy_(bstack111lllllll1_opy_):
    if not bstack111lllllll1_opy_:
        return bstack1ll11ll_opy_ (u"ࠬ࠭ᬉ")
    return bstack1ll11ll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᬊ").format(bstack111lllllll1_opy_.name, bstack111lllllll1_opy_.email)
def bstack11ll1ll1l1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111lll11111_opy_ = repo.common_dir
        info = {
            bstack1ll11ll_opy_ (u"ࠢࡴࡪࡤࠦᬋ"): repo.head.commit.hexsha,
            bstack1ll11ll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᬌ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll11ll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᬍ"): repo.active_branch.name,
            bstack1ll11ll_opy_ (u"ࠥࡸࡦ࡭ࠢᬎ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᬏ"): bstack111llll1l1l_opy_(repo.head.commit.committer),
            bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᬐ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᬑ"): bstack111llll1l1l_opy_(repo.head.commit.author),
            bstack1ll11ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᬒ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll11ll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᬓ"): repo.head.commit.message,
            bstack1ll11ll_opy_ (u"ࠤࡵࡳࡴࡺࠢᬔ"): repo.git.rev_parse(bstack1ll11ll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᬕ")),
            bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᬖ"): bstack111lll11111_opy_,
            bstack1ll11ll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᬗ"): subprocess.check_output([bstack1ll11ll_opy_ (u"ࠨࡧࡪࡶࠥᬘ"), bstack1ll11ll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᬙ"), bstack1ll11ll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᬚ")]).strip().decode(
                bstack1ll11ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᬛ")),
            bstack1ll11ll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᬜ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᬝ"): repo.git.rev_list(
                bstack1ll11ll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᬞ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11ll11l1_opy_ = []
        for remote in remotes:
            bstack111lll1l11l_opy_ = {
                bstack1ll11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬟ"): remote.name,
                bstack1ll11ll_opy_ (u"ࠢࡶࡴ࡯ࠦᬠ"): remote.url,
            }
            bstack11l11ll11l1_opy_.append(bstack111lll1l11l_opy_)
        bstack111ll1l111l_opy_ = {
            bstack1ll11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᬡ"): bstack1ll11ll_opy_ (u"ࠤࡪ࡭ࡹࠨᬢ"),
            **info,
            bstack1ll11ll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᬣ"): bstack11l11ll11l1_opy_
        }
        bstack111ll1l111l_opy_ = bstack111lll11l1l_opy_(bstack111ll1l111l_opy_)
        return bstack111ll1l111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᬤ").format(err))
        return {}
def bstack111ll111l11_opy_(bstack111ll1llll1_opy_=None):
    bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࡤࡰࡱࡿࠠࡧࡱࡵࡱࡦࡺࡴࡦࡦࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡵࡴࡧࠣࡧࡦࡹࡥࡴࠢࡩࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫ࡵ࡬ࡥࡧࡵࠤ࡮ࡴࠠࡵࡪࡨࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡦࡰ࡮ࡧࡩࡷࠦࡰࡢࡶ࡫ࡷࠥࡺ࡯ࠡࡧࡻࡸࡷࡧࡣࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡵࡳࡲ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡡ࡯ࡴ࠰ࡪࡩࡹࡩࡷࡥࠪࠬࡡ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡤࡪࡥࡷࡷ࠱ࠦࡥࡢࡥ࡫ࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡦࠦࡦࡰ࡮ࡧࡩࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᬥ")
    if not bstack111ll1llll1_opy_: # bstack11l111ll11l_opy_ for bstack111ll11ll1l_opy_-repo
        bstack111ll1llll1_opy_ = [os.getcwd()]
    results = []
    for folder in bstack111ll1llll1_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll11ll_opy_ (u"ࠨࡰࡳࡋࡧࠦᬦ"): bstack1ll11ll_opy_ (u"ࠢࠣᬧ"),
                bstack1ll11ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬨ"): [],
                bstack1ll11ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᬩ"): [],
                bstack1ll11ll_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᬪ"): bstack1ll11ll_opy_ (u"ࠦࠧᬫ"),
                bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᬬ"): [],
                bstack1ll11ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᬭ"): bstack1ll11ll_opy_ (u"ࠢࠣᬮ"),
                bstack1ll11ll_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣᬯ"): bstack1ll11ll_opy_ (u"ࠤࠥᬰ"),
                bstack1ll11ll_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨᬱ"): bstack1ll11ll_opy_ (u"ࠦࠧᬲ")
            }
            bstack111lll111l1_opy_ = repo.active_branch.name
            bstack11l111l1111_opy_ = repo.head.commit
            result[bstack1ll11ll_opy_ (u"ࠧࡶࡲࡊࡦࠥᬳ")] = bstack11l111l1111_opy_.hexsha
            bstack111llllllll_opy_ = _111ll1l11l1_opy_(repo)
            logger.debug(bstack1ll11ll_opy_ (u"ࠨࡂࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠿᬴ࠦࠢ") + str(bstack111llllllll_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣᬵ"))
            if bstack111llllllll_opy_:
                try:
                    bstack11l111l11ll_opy_ = repo.git.diff(bstack1ll11ll_opy_ (u"ࠣ࠯࠰ࡲࡦࡳࡥ࠮ࡱࡱࡰࡾࠨᬶ"), bstack1lll111ll1l_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨᬷ")).split(bstack1ll11ll_opy_ (u"ࠪࡠࡳ࠭ᬸ"))
                    logger.debug(bstack1ll11ll_opy_ (u"ࠦࡈ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡧ࡫ࡴࡸࡧࡨࡲࠥࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠥࡧ࡮ࡥࠢࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠿ࠦࠢᬹ") + str(bstack11l111l11ll_opy_) + bstack1ll11ll_opy_ (u"ࠧࠨᬺ"))
                    result[bstack1ll11ll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᬻ")] = [f.strip() for f in bstack11l111l11ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll111ll1l_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᬼ")))
                except Exception:
                    logger.debug(bstack1ll11ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠱ࠤࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡲࡦࡥࡨࡲࡹࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠣᬽ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll11ll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᬾ")] = _111lll1ll11_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᬿ")] = _111lll1ll11_opy_(commits[:5])
            bstack11l11l1l111_opy_ = set()
            bstack11l111111l1_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll11ll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲ࡯ࡴ࠻ࠢࠥᭀ") + str(commit.message) + bstack1ll11ll_opy_ (u"ࠧࠨᭁ"))
                bstack11l11111l11_opy_ = commit.author.name if commit.author else bstack1ll11ll_opy_ (u"ࠨࡕ࡯࡭ࡱࡳࡼࡴࠢᭂ")
                bstack11l11l1l111_opy_.add(bstack11l11111l11_opy_)
                bstack11l111111l1_opy_.append({
                    bstack1ll11ll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᭃ"): commit.message.strip(),
                    bstack1ll11ll_opy_ (u"ࠣࡷࡶࡩࡷࠨ᭄"): bstack11l11111l11_opy_
                })
            result[bstack1ll11ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᭅ")] = list(bstack11l11l1l111_opy_)
            result[bstack1ll11ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᭆ")] = bstack11l111111l1_opy_
            result[bstack1ll11ll_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᭇ")] = bstack11l111l1111_opy_.committed_datetime.strftime(bstack1ll11ll_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࠢᭈ"))
            if (not result[bstack1ll11ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᭉ")] or result[bstack1ll11ll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᭊ")].strip() == bstack1ll11ll_opy_ (u"ࠣࠤᭋ")) and bstack11l111l1111_opy_.message:
                bstack11l111l1l1l_opy_ = bstack11l111l1111_opy_.message.strip().splitlines()
                result[bstack1ll11ll_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᭌ")] = bstack11l111l1l1l_opy_[0] if bstack11l111l1l1l_opy_ else bstack1ll11ll_opy_ (u"ࠥࠦ᭍")
                if len(bstack11l111l1l1l_opy_) > 2:
                    result[bstack1ll11ll_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ᭎")] = bstack1ll11ll_opy_ (u"ࠬࡢ࡮ࠨ᭏").join(bstack11l111l1l1l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤ࠭࡬࡯࡭ࡦࡨࡶ࠿ࠦࡻࡧࡱ࡯ࡨࡪࡸࡽࠪ࠼ࠣࠦ᭐") + str(err) + bstack1ll11ll_opy_ (u"ࠢࠣ᭑"))
    filtered_results = [
        r
        for r in results
        if _11l11111l1l_opy_(r)
    ]
    return filtered_results
def _11l11111l1l_opy_(result):
    bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡨࡰࡵ࡫ࡲࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡶࡹࡱࡺࠠࡪࡵࠣࡺࡦࡲࡩࡥࠢࠫࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠦࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠥࡧ࡮ࡥࠢࡤࡹࡹ࡮࡯ࡳࡵࠬ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭒")
    return (
        isinstance(result.get(bstack1ll11ll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ᭓"), None), list)
        and len(result[bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ᭔")]) > 0
        and isinstance(result.get(bstack1ll11ll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧ᭕"), None), list)
        and len(result[bstack1ll11ll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨ᭖")]) > 0
    )
def _111ll1l11l1_opy_(repo):
    bstack1ll11ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡷ࡫ࡰࡰࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣ࡬ࡦࡸࡤࡤࡱࡧࡩࡩࠦ࡮ࡢ࡯ࡨࡷࠥࡧ࡮ࡥࠢࡺࡳࡷࡱࠠࡸ࡫ࡷ࡬ࠥࡧ࡬࡭࡙ࠢࡇࡘࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡪࡥࡧࡣࡸࡰࡹࠦࡢࡳࡣࡱࡧ࡭ࠦࡩࡧࠢࡳࡳࡸࡹࡩࡣ࡮ࡨ࠰ࠥ࡫࡬ࡴࡧࠣࡒࡴࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ᭗")
    try:
        try:
            origin = repo.remotes.origin
            bstack11l111lllll_opy_ = origin.refs[bstack1ll11ll_opy_ (u"ࠧࡉࡇࡄࡈࠬ᭘")]
            target = bstack11l111lllll_opy_.reference.name
            if target.startswith(bstack1ll11ll_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ᭙")):
                return target
        except Exception:
            pass
        if repo.heads:
            return repo.heads[0].name
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll11ll_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ᭚")):
                    return ref.name
    except Exception:
        pass
    return None
def _111lll1ll11_opy_(commits):
    bstack1ll11ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡡࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ᭛")
    bstack11l111l11ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11l111lll11_opy_ in diff:
                        if bstack11l111lll11_opy_.a_path:
                            bstack11l111l11ll_opy_.add(bstack11l111lll11_opy_.a_path)
                        if bstack11l111lll11_opy_.b_path:
                            bstack11l111l11ll_opy_.add(bstack11l111lll11_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l111l11ll_opy_)
def bstack111lll11l1l_opy_(bstack111ll1l111l_opy_):
    bstack11l111lll1l_opy_ = bstack11l11ll1111_opy_(bstack111ll1l111l_opy_)
    if bstack11l111lll1l_opy_ and bstack11l111lll1l_opy_ > bstack11l1ll1ll1l_opy_:
        bstack111lll1lll1_opy_ = bstack11l111lll1l_opy_ - bstack11l1ll1ll1l_opy_
        bstack111llllll1l_opy_ = bstack111ll11111l_opy_(bstack111ll1l111l_opy_[bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᭜")], bstack111lll1lll1_opy_)
        bstack111ll1l111l_opy_[bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨ᭝")] = bstack111llllll1l_opy_
        logger.info(bstack1ll11ll_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣ᭞")
                    .format(bstack11l11ll1111_opy_(bstack111ll1l111l_opy_) / 1024))
    return bstack111ll1l111l_opy_
def bstack11l11ll1111_opy_(bstack1l1lllll1_opy_):
    try:
        if bstack1l1lllll1_opy_:
            bstack11l111l1ll1_opy_ = json.dumps(bstack1l1lllll1_opy_)
            bstack11l11l11l11_opy_ = sys.getsizeof(bstack11l111l1ll1_opy_)
            return bstack11l11l11l11_opy_
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢ᭟").format(e))
    return -1
def bstack111ll11111l_opy_(field, bstack11l11111ll1_opy_):
    try:
        bstack11l11l1l1l1_opy_ = len(bytes(bstack11l1ll111l1_opy_, bstack1ll11ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᭠")))
        bstack111ll111l1l_opy_ = bytes(field, bstack1ll11ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᭡"))
        bstack11l111111ll_opy_ = len(bstack111ll111l1l_opy_)
        bstack11l11l1111l_opy_ = ceil(bstack11l111111ll_opy_ - bstack11l11111ll1_opy_ - bstack11l11l1l1l1_opy_)
        if bstack11l11l1111l_opy_ > 0:
            bstack111ll1ll1ll_opy_ = bstack111ll111l1l_opy_[:bstack11l11l1111l_opy_].decode(bstack1ll11ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᭢"), errors=bstack1ll11ll_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫ᭣")) + bstack11l1ll111l1_opy_
            return bstack111ll1ll1ll_opy_
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥ᭤").format(e))
    return field
def bstack1l1llll111_opy_():
    env = os.environ
    if (bstack1ll11ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᭥") in env and len(env[bstack1ll11ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ᭦")]) > 0) or (
            bstack1ll11ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᭧") in env and len(env[bstack1ll11ll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ᭨")]) > 0):
        return {
            bstack1ll11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭩"): bstack1ll11ll_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧ᭪"),
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭫"): env.get(bstack1ll11ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᭬")),
            bstack1ll11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᭭"): env.get(bstack1ll11ll_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥ᭮")),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭯"): env.get(bstack1ll11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᭰"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠦࡈࡏࠢ᭱")) == bstack1ll11ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᭲") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣ᭳"))):
        return {
            bstack1ll11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭴"): bstack1ll11ll_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥ᭵"),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭶"): env.get(bstack1ll11ll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᭷")),
            bstack1ll11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭸"): env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤ᭹")),
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᭺"): env.get(bstack1ll11ll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥ᭻"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠣࡅࡌࠦ᭼")) == bstack1ll11ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᭽") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥ᭾"))):
        return {
            bstack1ll11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭿"): bstack1ll11ll_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣᮀ"),
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᮁ"): env.get(bstack1ll11ll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢᮂ")),
            bstack1ll11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮃ"): env.get(bstack1ll11ll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᮄ")),
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮅ"): env.get(bstack1ll11ll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮆ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡉࠣᮇ")) == bstack1ll11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᮈ") and env.get(bstack1ll11ll_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣᮉ")) == bstack1ll11ll_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥᮊ"):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮋ"): bstack1ll11ll_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧᮌ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮍ"): None,
            bstack1ll11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮎ"): None,
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᮏ"): None
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥᮐ")) and env.get(bstack1ll11ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦᮑ")):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮒ"): bstack1ll11ll_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨᮓ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮔ"): env.get(bstack1ll11ll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥᮕ")),
            bstack1ll11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮖ"): None,
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮗ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮘ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡍࠧᮙ")) == bstack1ll11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᮚ") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠦࡉࡘࡏࡏࡇࠥᮛ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᮜ"): bstack1ll11ll_opy_ (u"ࠨࡄࡳࡱࡱࡩࠧᮝ"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᮞ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦᮟ")),
            bstack1ll11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮠ"): None,
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮡ"): env.get(bstack1ll11ll_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᮢ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡉࠣᮣ")) == bstack1ll11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᮤ") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥᮥ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᮦ"): bstack1ll11ll_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩࠧᮧ"),
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮨ"): env.get(bstack1ll11ll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎࠥᮩ")),
            bstack1ll11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᮪ࠢ"): env.get(bstack1ll11ll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈ᮫ࠦ")),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮬ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇࠦᮭ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡍࠧᮮ")) == bstack1ll11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᮯ") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢ᮰"))):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᮱"): bstack1ll11ll_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ᮲"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᮳"): env.get(bstack1ll11ll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧ᮴")),
            bstack1ll11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᮵"): env.get(bstack1ll11ll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᮶")),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᮷"): env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣ᮸"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠨࡃࡊࠤ᮹")) == bstack1ll11ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᮺ") and bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᮻ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮼ"): bstack1ll11ll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨᮽ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮾ"): env.get(bstack1ll11ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᮿ")),
            bstack1ll11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯀ"): env.get(bstack1ll11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤᯁ")) or env.get(bstack1ll11ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᯂ")),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯃ"): env.get(bstack1ll11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᯄ"))
        }
    if bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᯅ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯆ"): bstack1ll11ll_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᯇ"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯈ"): bstack1ll11ll_opy_ (u"ࠣࡽࢀࡿࢂࠨᯉ").format(env.get(bstack1ll11ll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᯊ")), env.get(bstack1ll11ll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᯋ"))),
            bstack1ll11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯌ"): env.get(bstack1ll11ll_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᯍ")),
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯎ"): env.get(bstack1ll11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᯏ"))
        }
    if bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᯐ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᯑ"): bstack1ll11ll_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᯒ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᯓ"): bstack1ll11ll_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᯔ").format(env.get(bstack1ll11ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᯕ")), env.get(bstack1ll11ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᯖ")), env.get(bstack1ll11ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᯗ")), env.get(bstack1ll11ll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᯘ"))),
            bstack1ll11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯙ"): env.get(bstack1ll11ll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᯚ")),
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᯛ"): env.get(bstack1ll11ll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᯜ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᯝ")) and env.get(bstack1ll11ll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᯞ")):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᯟ"): bstack1ll11ll_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᯠ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᯡ"): bstack1ll11ll_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᯢ").format(env.get(bstack1ll11ll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᯣ")), env.get(bstack1ll11ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᯤ")), env.get(bstack1ll11ll_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᯥ"))),
            bstack1ll11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨ᯦ࠦ"): env.get(bstack1ll11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᯧ")),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯨ"): env.get(bstack1ll11ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᯩ"))
        }
    if any([env.get(bstack1ll11ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᯪ")), env.get(bstack1ll11ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᯫ")), env.get(bstack1ll11ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᯬ"))]):
        return {
            bstack1ll11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᯭ"): bstack1ll11ll_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᯮ"),
            bstack1ll11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᯯ"): env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᯰ")),
            bstack1ll11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯱ"): env.get(bstack1ll11ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈ᯲ࠧ")),
            bstack1ll11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ᯳ࠢ"): env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᯴"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ᯵")):
        return {
            bstack1ll11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᯶"): bstack1ll11ll_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧ᯷"),
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᯸"): env.get(bstack1ll11ll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤ᯹")),
            bstack1ll11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᯺"): env.get(bstack1ll11ll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣ᯻")),
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᯼"): env.get(bstack1ll11ll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᯽"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨ᯾")) or env.get(bstack1ll11ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣ᯿")):
        return {
            bstack1ll11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰀ"): bstack1ll11ll_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᰁ"),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰂ"): env.get(bstack1ll11ll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᰃ")),
            bstack1ll11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᰄ"): bstack1ll11ll_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᰅ") if env.get(bstack1ll11ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᰆ")) else None,
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᰇ"): env.get(bstack1ll11ll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᰈ"))
        }
    if any([env.get(bstack1ll11ll_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᰉ")), env.get(bstack1ll11ll_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᰊ")), env.get(bstack1ll11ll_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᰋ"))]):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰌ"): bstack1ll11ll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᰍ"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᰎ"): None,
            bstack1ll11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰏ"): env.get(bstack1ll11ll_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᰐ")),
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰑ"): env.get(bstack1ll11ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᰒ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᰓ")):
        return {
            bstack1ll11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᰔ"): bstack1ll11ll_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᰕ"),
            bstack1ll11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᰖ"): env.get(bstack1ll11ll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᰗ")),
            bstack1ll11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰘ"): bstack1ll11ll_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᰙ").format(env.get(bstack1ll11ll_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᰚ"))) if env.get(bstack1ll11ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᰛ")) else None,
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᰜ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᰝ"))
        }
    if bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᰞ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᰟ"): bstack1ll11ll_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᰠ"),
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰡ"): env.get(bstack1ll11ll_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᰢ")),
            bstack1ll11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰣ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᰤ")),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰥ"): env.get(bstack1ll11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᰦ"))
        }
    if bstack1l1l1llll1_opy_(env.get(bstack1ll11ll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᰧ"))):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰨ"): bstack1ll11ll_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᰩ"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᰪ"): bstack1ll11ll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᰫ").format(env.get(bstack1ll11ll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᰬ")), env.get(bstack1ll11ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᰭ")), env.get(bstack1ll11ll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᰮ"))),
            bstack1ll11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰯ"): env.get(bstack1ll11ll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᰰ")),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᰱ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᰲ"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡍࠧᰳ")) == bstack1ll11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᰴ") and env.get(bstack1ll11ll_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᰵ")) == bstack1ll11ll_opy_ (u"ࠧ࠷ࠢᰶ"):
        return {
            bstack1ll11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᰷ࠦ"): bstack1ll11ll_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢ᰸"),
            bstack1ll11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᰹"): bstack1ll11ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧ᰺").format(env.get(bstack1ll11ll_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧ᰻"))),
            bstack1ll11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᰼"): None,
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᰽"): None,
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤ᰾")):
        return {
            bstack1ll11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᰿"): bstack1ll11ll_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥ᱀"),
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱁"): None,
            bstack1ll11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᱂"): env.get(bstack1ll11ll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧ᱃")),
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱄"): env.get(bstack1ll11ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᱅"))
        }
    if any([env.get(bstack1ll11ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥ᱆")), env.get(bstack1ll11ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣ᱇")), env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢ᱈")), env.get(bstack1ll11ll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦ᱉"))]):
        return {
            bstack1ll11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᱊"): bstack1ll11ll_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣ᱋"),
            bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᱌"): None,
            bstack1ll11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᱍ"): env.get(bstack1ll11ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᱎ")) or None,
            bstack1ll11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᱏ"): env.get(bstack1ll11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᱐"), 0)
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᱑")):
        return {
            bstack1ll11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᱒"): bstack1ll11ll_opy_ (u"ࠨࡇࡰࡅࡇࠦ᱓"),
            bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᱔"): None,
            bstack1ll11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᱕"): env.get(bstack1ll11ll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᱖")),
            bstack1ll11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᱗"): env.get(bstack1ll11ll_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥ᱘"))
        }
    if env.get(bstack1ll11ll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᱙")):
        return {
            bstack1ll11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱚ"): bstack1ll11ll_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᱛ"),
            bstack1ll11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱜ"): env.get(bstack1ll11ll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᱝ")),
            bstack1ll11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᱞ"): env.get(bstack1ll11ll_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᱟ")),
            bstack1ll11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᱠ"): env.get(bstack1ll11ll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᱡ"))
        }
    return {bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᱢ"): None}
def get_host_info():
    return {
        bstack1ll11ll_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᱣ"): platform.node(),
        bstack1ll11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᱤ"): platform.system(),
        bstack1ll11ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᱥ"): platform.machine(),
        bstack1ll11ll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᱦ"): platform.version(),
        bstack1ll11ll_opy_ (u"ࠧࡧࡲࡤࡪࠥᱧ"): platform.architecture()[0]
    }
def bstack111111ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111llll1lll_opy_():
    if bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᱨ")):
        return bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᱩ")
    return bstack1ll11ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᱪ")
def bstack11l111l111l_opy_(driver):
    info = {
        bstack1ll11ll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᱫ"): driver.capabilities,
        bstack1ll11ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᱬ"): driver.session_id,
        bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᱭ"): driver.capabilities.get(bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᱮ"), None),
        bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᱯ"): driver.capabilities.get(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱰ"), None),
        bstack1ll11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᱱ"): driver.capabilities.get(bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᱲ"), None),
        bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᱳ"):driver.capabilities.get(bstack1ll11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᱴ"), None),
    }
    if bstack111llll1lll_opy_() == bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᱵ"):
        if bstack11ll11ll1l_opy_():
            info[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᱶ")] = bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᱷ")
        elif driver.capabilities.get(bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᱸ"), {}).get(bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᱹ"), False):
            info[bstack1ll11ll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᱺ")] = bstack1ll11ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᱻ")
        else:
            info[bstack1ll11ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᱼ")] = bstack1ll11ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᱽ")
    return info
def bstack11ll11ll1l_opy_():
    if bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᱾")):
        return True
    if bstack1l1l1llll1_opy_(os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᱿"), None)):
        return True
    return False
def bstack1lllll1111_opy_(bstack11l11l1ll11_opy_, url, data, config):
    headers = config.get(bstack1ll11ll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᲀ"), None)
    proxies = bstack1llll11lll_opy_(config, url)
    auth = config.get(bstack1ll11ll_opy_ (u"ࠪࡥࡺࡺࡨࠨᲁ"), None)
    response = requests.request(
            bstack11l11l1ll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1l11l11_opy_(bstack1l1ll1ll11_opy_, size):
    bstack1l1ll1111_opy_ = []
    while len(bstack1l1ll1ll11_opy_) > size:
        bstack11l11l11_opy_ = bstack1l1ll1ll11_opy_[:size]
        bstack1l1ll1111_opy_.append(bstack11l11l11_opy_)
        bstack1l1ll1ll11_opy_ = bstack1l1ll1ll11_opy_[size:]
    bstack1l1ll1111_opy_.append(bstack1l1ll1ll11_opy_)
    return bstack1l1ll1111_opy_
def bstack111llll111l_opy_(message, bstack11l1111l1ll_opy_=False):
    os.write(1, bytes(message, bstack1ll11ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᲂ")))
    os.write(1, bytes(bstack1ll11ll_opy_ (u"ࠬࡢ࡮ࠨᲃ"), bstack1ll11ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᲄ")))
    if bstack11l1111l1ll_opy_:
        with open(bstack1ll11ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ᲅ") + os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᲆ")] + bstack1ll11ll_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧᲇ"), bstack1ll11ll_opy_ (u"ࠪࡥࠬᲈ")) as f:
            f.write(message + bstack1ll11ll_opy_ (u"ࠫࡡࡴࠧᲉ"))
def bstack1l1l1lll111_opy_():
    return os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᲊ")].lower() == bstack1ll11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᲋")
def bstack11l1l1l1l1_opy_():
    return bstack111l1l11ll_opy_().replace(tzinfo=None).isoformat() + bstack1ll11ll_opy_ (u"࡛ࠧࠩ᲌")
def bstack11l11l111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll11ll_opy_ (u"ࠨ࡜ࠪ᲍"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll11ll_opy_ (u"ࠩ࡝ࠫ᲎")))).total_seconds() * 1000
def bstack11l11ll11ll_opy_(timestamp):
    return bstack11l11l1l11l_opy_(timestamp).isoformat() + bstack1ll11ll_opy_ (u"ࠪ࡞ࠬ᲏")
def bstack111ll1l1111_opy_(bstack111ll11llll_opy_):
    date_format = bstack1ll11ll_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᲐ")
    bstack111llll1l11_opy_ = datetime.datetime.strptime(bstack111ll11llll_opy_, date_format)
    return bstack111llll1l11_opy_.isoformat() + bstack1ll11ll_opy_ (u"ࠬࡠࠧᲑ")
def bstack111lll1l111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Გ")
    else:
        return bstack1ll11ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᲓ")
def bstack1l1l1llll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll11ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ე")
def bstack111ll11l1ll_opy_(val):
    return val.__str__().lower() == bstack1ll11ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᲕ")
def error_handler(bstack111llll11l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111llll11l1_opy_ as e:
                print(bstack1ll11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᲖ").format(func.__name__, bstack111llll11l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111ll1l1l11_opy_(bstack111lllll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lllll11l_opy_(cls, *args, **kwargs)
            except bstack111llll11l1_opy_ as e:
                print(bstack1ll11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᲗ").format(bstack111lllll11l_opy_.__name__, bstack111llll11l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111ll1l1l11_opy_
    else:
        return decorator
def bstack11l1lll1ll_opy_(bstack11111l11ll_opy_):
    if os.getenv(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᲘ")) is not None:
        return bstack1l1l1llll1_opy_(os.getenv(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᲙ")))
    if bstack1ll11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᲚ") in bstack11111l11ll_opy_ and bstack111ll11l1ll_opy_(bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲛ")]):
        return False
    if bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᲜ") in bstack11111l11ll_opy_ and bstack111ll11l1ll_opy_(bstack11111l11ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᲝ")]):
        return False
    return True
def bstack1llll1l11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11ll1l11_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦᲞ"), None)
        return bstack11l11ll1l11_opy_ is None or bstack11l11ll1l11_opy_ == bstack1ll11ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᲟ")
    except Exception as e:
        return False
def bstack11lll111l1_opy_(hub_url, CONFIG):
    if bstack1l11111111_opy_() <= version.parse(bstack1ll11ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭Რ")):
        if hub_url:
            return bstack1ll11ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᲡ") + hub_url + bstack1ll11ll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᲢ")
        return bstack11ll1ll11_opy_
    if hub_url:
        return bstack1ll11ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᲣ") + hub_url + bstack1ll11ll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᲤ")
    return bstack11lllll1ll_opy_
def bstack111llll1111_opy_():
    return isinstance(os.getenv(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᲥ")), str)
def bstack1111111l_opy_(url):
    return urlparse(url).hostname
def bstack1l1l1l11l_opy_(hostname):
    for bstack1ll111l1l_opy_ in bstack1l1lllll_opy_:
        regex = re.compile(bstack1ll111l1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11l1llll_opy_(bstack11l1111111l_opy_, file_name, logger):
    bstack1l1111lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠬࢄࠧᲦ")), bstack11l1111111l_opy_)
    try:
        if not os.path.exists(bstack1l1111lll1_opy_):
            os.makedirs(bstack1l1111lll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"࠭ࡾࠨᲧ")), bstack11l1111111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll11ll_opy_ (u"ࠧࡸࠩᲨ")):
                pass
            with open(file_path, bstack1ll11ll_opy_ (u"ࠣࡹ࠮ࠦᲩ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11l111ll_opy_.format(str(e)))
def bstack11l11l11l1l_opy_(file_name, key, value, logger):
    file_path = bstack11l11l1llll_opy_(bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᲪ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack111l111l1_opy_ = json.load(open(file_path, bstack1ll11ll_opy_ (u"ࠪࡶࡧ࠭Ძ")))
        else:
            bstack111l111l1_opy_ = {}
        bstack111l111l1_opy_[key] = value
        with open(file_path, bstack1ll11ll_opy_ (u"ࠦࡼ࠱ࠢᲬ")) as outfile:
            json.dump(bstack111l111l1_opy_, outfile)
def bstack1lll1lll1l_opy_(file_name, logger):
    file_path = bstack11l11l1llll_opy_(bstack1ll11ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᲭ"), file_name, logger)
    bstack111l111l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll11ll_opy_ (u"࠭ࡲࠨᲮ")) as bstack1l11ll11_opy_:
            bstack111l111l1_opy_ = json.load(bstack1l11ll11_opy_)
    return bstack111l111l1_opy_
def bstack1l111l11ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᲯ") + file_path + bstack1ll11ll_opy_ (u"ࠨࠢࠪᲰ") + str(e))
def bstack1l11111111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll11ll_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᲱ")
def bstack1l11l1llll_opy_(config):
    if bstack1ll11ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᲲ") in config:
        del (config[bstack1ll11ll_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᲳ")])
        return False
    if bstack1l11111111_opy_() < version.parse(bstack1ll11ll_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᲴ")):
        return False
    if bstack1l11111111_opy_() >= version.parse(bstack1ll11ll_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᲵ")):
        return True
    if bstack1ll11ll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᲶ") in config and config[bstack1ll11ll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᲷ")] is False:
        return False
    else:
        return True
def bstack1l11ll1l1_opy_(args_list, bstack11l11111lll_opy_):
    index = -1
    for value in bstack11l11111lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1ll1111_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1ll1111_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll1l1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll1l1l1_opy_ = bstack111ll1l1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll11ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᲸ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᲹ"), exception=exception)
    def bstack111111l11l_opy_(self):
        if self.result != bstack1ll11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲺ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll11ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ᲻") in self.exception_type:
            return bstack1ll11ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᲼")
        return bstack1ll11ll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᲽ")
    def bstack111lll1111l_opy_(self):
        if self.result != bstack1ll11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᲾ"):
            return None
        if self.bstack111ll1l1l1_opy_:
            return self.bstack111ll1l1l1_opy_
        return bstack11l111llll1_opy_(self.exception)
def bstack11l111llll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l1ll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1111l1l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l111ll111_opy_(config, logger):
    try:
        import playwright
        bstack111lll11l11_opy_ = playwright.__file__
        bstack111lll1l1ll_opy_ = os.path.split(bstack111lll11l11_opy_)
        bstack111lll1llll_opy_ = bstack111lll1l1ll_opy_[0] + bstack1ll11ll_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬᲿ")
        os.environ[bstack1ll11ll_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭᳀")] = bstack11l1l1ll1l_opy_(config)
        with open(bstack111lll1llll_opy_, bstack1ll11ll_opy_ (u"ࠫࡷ࠭᳁")) as f:
            bstack11lll11l11_opy_ = f.read()
            bstack111ll1ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ᳂")
            bstack11l1111l111_opy_ = bstack11lll11l11_opy_.find(bstack111ll1ll1l1_opy_)
            if bstack11l1111l111_opy_ == -1:
              process = subprocess.Popen(bstack1ll11ll_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥ᳃"), shell=True, cwd=bstack111lll1l1ll_opy_[0])
              process.wait()
              bstack111ll1ll11l_opy_ = bstack1ll11ll_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ᳄")
              bstack11l1111ll11_opy_ = bstack1ll11ll_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ᳅")
              bstack111llll1ll1_opy_ = bstack11lll11l11_opy_.replace(bstack111ll1ll11l_opy_, bstack11l1111ll11_opy_)
              with open(bstack111lll1llll_opy_, bstack1ll11ll_opy_ (u"ࠩࡺࠫ᳆")) as f:
                f.write(bstack111llll1ll1_opy_)
    except Exception as e:
        logger.error(bstack11l11llll1_opy_.format(str(e)))
def bstack11ll11l1l_opy_():
  try:
    bstack111ll111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪ᳇"))
    bstack11l1111ll1l_opy_ = []
    if os.path.exists(bstack111ll111ll1_opy_):
      with open(bstack111ll111ll1_opy_) as f:
        bstack11l1111ll1l_opy_ = json.load(f)
      os.remove(bstack111ll111ll1_opy_)
    return bstack11l1111ll1l_opy_
  except:
    pass
  return []
def bstack1l1l11lll1_opy_(bstack111l1l11l_opy_):
  try:
    bstack11l1111ll1l_opy_ = []
    bstack111ll111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫ᳈"))
    if os.path.exists(bstack111ll111ll1_opy_):
      with open(bstack111ll111ll1_opy_) as f:
        bstack11l1111ll1l_opy_ = json.load(f)
    bstack11l1111ll1l_opy_.append(bstack111l1l11l_opy_)
    with open(bstack111ll111ll1_opy_, bstack1ll11ll_opy_ (u"ࠬࡽࠧ᳉")) as f:
        json.dump(bstack11l1111ll1l_opy_, f)
  except:
    pass
def bstack1ll1l11l_opy_(logger, bstack11l11ll111l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ᳊"), bstack1ll11ll_opy_ (u"ࠧࠨ᳋"))
    if test_name == bstack1ll11ll_opy_ (u"ࠨࠩ᳌"):
        test_name = threading.current_thread().__dict__.get(bstack1ll11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ᳍"), bstack1ll11ll_opy_ (u"ࠪࠫ᳎"))
    bstack111lll1l1l1_opy_ = bstack1ll11ll_opy_ (u"ࠫ࠱ࠦࠧ᳏").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11ll111l_opy_:
        bstack11llll111l_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᳐"), bstack1ll11ll_opy_ (u"࠭࠰ࠨ᳑"))
        bstack11llll1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᳒"): test_name, bstack1ll11ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᳓"): bstack111lll1l1l1_opy_, bstack1ll11ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᳔"): bstack11llll111l_opy_}
        bstack11l111ll111_opy_ = []
        bstack111lll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯᳕ࠩ"))
        if os.path.exists(bstack111lll1ll1l_opy_):
            with open(bstack111lll1ll1l_opy_) as f:
                bstack11l111ll111_opy_ = json.load(f)
        bstack11l111ll111_opy_.append(bstack11llll1ll1_opy_)
        with open(bstack111lll1ll1l_opy_, bstack1ll11ll_opy_ (u"ࠫࡼ᳖࠭")) as f:
            json.dump(bstack11l111ll111_opy_, f)
    else:
        bstack11llll1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠬࡴࡡ࡮ࡧ᳗ࠪ"): test_name, bstack1ll11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳘ࠬ"): bstack111lll1l1l1_opy_, bstack1ll11ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ᳙࠭"): str(multiprocessing.current_process().name)}
        if bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ᳚") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llll1ll1_opy_)
  except Exception as e:
      logger.warn(bstack1ll11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ᳛").format(e))
def bstack1l1ll1l11l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ᳜࠭"))
    try:
      bstack111ll111lll_opy_ = []
      bstack11llll1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦ᳝ࠩ"): test_name, bstack1ll11ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵ᳞ࠫ"): error_message, bstack1ll11ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᳟ࠬ"): index}
      bstack111ll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ᳠"))
      if os.path.exists(bstack111ll1111l1_opy_):
          with open(bstack111ll1111l1_opy_) as f:
              bstack111ll111lll_opy_ = json.load(f)
      bstack111ll111lll_opy_.append(bstack11llll1ll1_opy_)
      with open(bstack111ll1111l1_opy_, bstack1ll11ll_opy_ (u"ࠨࡹࠪ᳡")) as f:
          json.dump(bstack111ll111lll_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁ᳢ࠧ").format(e))
    return
  bstack111ll111lll_opy_ = []
  bstack11llll1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᳣"): test_name, bstack1ll11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴ᳤ࠪ"): error_message, bstack1ll11ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻ᳥ࠫ"): index}
  bstack111ll1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll11ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴ᳦ࠧ"))
  lock_file = bstack111ll1111l1_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ᳧࠭")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111ll1111l1_opy_):
          with open(bstack111ll1111l1_opy_, bstack1ll11ll_opy_ (u"ࠨࡴ᳨ࠪ")) as f:
              content = f.read().strip()
              if content:
                  bstack111ll111lll_opy_ = json.load(open(bstack111ll1111l1_opy_))
      bstack111ll111lll_opy_.append(bstack11llll1ll1_opy_)
      with open(bstack111ll1111l1_opy_, bstack1ll11ll_opy_ (u"ࠩࡺࠫᳩ")) as f:
          json.dump(bstack111ll111lll_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࡀࠠࡼࡿࠥᳪ").format(e))
def bstack11l11l1l1_opy_(bstack1lll1lll11_opy_, name, logger):
  try:
    bstack11llll1ll1_opy_ = {bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᳫ"): name, bstack1ll11ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᳬ"): bstack1lll1lll11_opy_, bstack1ll11ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ᳭ࠬ"): str(threading.current_thread()._name)}
    return bstack11llll1ll1_opy_
  except Exception as e:
    logger.warn(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᳮ").format(e))
  return
def bstack11l1111l11l_opy_():
    return platform.system() == bstack1ll11ll_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩᳯ")
def bstack1ll1ll1lll_opy_(bstack11l1111lll1_opy_, config, logger):
    bstack111ll1lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1111lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣᳰ").format(e))
    return bstack111ll1lllll_opy_
def bstack111lllll111_opy_(bstack111llll11ll_opy_, bstack111ll1l1ll1_opy_):
    bstack111lll11lll_opy_ = version.parse(bstack111llll11ll_opy_)
    bstack11l111l1lll_opy_ = version.parse(bstack111ll1l1ll1_opy_)
    if bstack111lll11lll_opy_ > bstack11l111l1lll_opy_:
        return 1
    elif bstack111lll11lll_opy_ < bstack11l111l1lll_opy_:
        return -1
    else:
        return 0
def bstack111l1l11ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l1l11l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll1lll11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l11l1ll_opy_(options, framework, config, bstack1l1l1111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll11ll_opy_ (u"ࠪ࡫ࡪࡺࠧᳱ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l11l11l_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᳲ"))
    bstack111ll11lll1_opy_ = True
    bstack11ll11l11_opy_ = os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᳳ")]
    bstack1ll11l1lll1_opy_ = config.get(bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᳴"), False)
    if bstack1ll11l1lll1_opy_:
        bstack1lll11l1111_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᳵ"), {})
        bstack1lll11l1111_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᳶ")] = os.getenv(bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᳷"))
        bstack11ll11ll11l_opy_ = json.loads(os.getenv(bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ᳸"), bstack1ll11ll_opy_ (u"ࠫࢀࢃࠧ᳹"))).get(bstack1ll11ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᳺ"))
    if bstack111ll11l1ll_opy_(caps.get(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬ᳻"))) or bstack111ll11l1ll_opy_(caps.get(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧ᳼"))):
        bstack111ll11lll1_opy_ = False
    if bstack1l11l1llll_opy_({bstack1ll11ll_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣ᳽"): bstack111ll11lll1_opy_}):
        bstack1l1l11l11l_opy_ = bstack1l1l11l11l_opy_ or {}
        bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᳾")] = bstack111ll1lll11_opy_(framework)
        bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᳿")] = bstack1l1l1lll111_opy_()
        bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᴀ")] = bstack11ll11l11_opy_
        bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᴁ")] = bstack1l1l1111l_opy_
        if bstack1ll11l1lll1_opy_:
            bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴂ")] = bstack1ll11l1lll1_opy_
            bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᴃ")] = bstack1lll11l1111_opy_
            bstack1l1l11l11l_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᴄ")][bstack1ll11ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᴅ")] = bstack11ll11ll11l_opy_
        if getattr(options, bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫᴆ"), None):
            options.set_capability(bstack1ll11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᴇ"), bstack1l1l11l11l_opy_)
        else:
            options[bstack1ll11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴈ")] = bstack1l1l11l11l_opy_
    else:
        if getattr(options, bstack1ll11ll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᴉ"), None):
            options.set_capability(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᴊ"), bstack111ll1lll11_opy_(framework))
            options.set_capability(bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᴋ"), bstack1l1l1lll111_opy_())
            options.set_capability(bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᴌ"), bstack11ll11l11_opy_)
            options.set_capability(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᴍ"), bstack1l1l1111l_opy_)
            if bstack1ll11l1lll1_opy_:
                options.set_capability(bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴎ"), bstack1ll11l1lll1_opy_)
                options.set_capability(bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᴏ"), bstack1lll11l1111_opy_)
                options.set_capability(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᴐ"), bstack11ll11ll11l_opy_)
        else:
            options[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᴑ")] = bstack111ll1lll11_opy_(framework)
            options[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᴒ")] = bstack1l1l1lll111_opy_()
            options[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᴓ")] = bstack11ll11l11_opy_
            options[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᴔ")] = bstack1l1l1111l_opy_
            if bstack1ll11l1lll1_opy_:
                options[bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴕ")] = bstack1ll11l1lll1_opy_
                options[bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᴖ")] = bstack1lll11l1111_opy_
                options[bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᴗ")][bstack1ll11ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᴘ")] = bstack11ll11ll11l_opy_
    return options
def bstack111lllll1ll_opy_(bstack111ll11ll11_opy_, framework):
    bstack1l1l1111l_opy_ = bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥᴙ"))
    if bstack111ll11ll11_opy_ and len(bstack111ll11ll11_opy_.split(bstack1ll11ll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᴚ"))) > 1:
        ws_url = bstack111ll11ll11_opy_.split(bstack1ll11ll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴛ"))[0]
        if bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᴜ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111lll111ll_opy_ = json.loads(urllib.parse.unquote(bstack111ll11ll11_opy_.split(bstack1ll11ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴝ"))[1]))
            bstack111lll111ll_opy_ = bstack111lll111ll_opy_ or {}
            bstack11ll11l11_opy_ = os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᴞ")]
            bstack111lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᴟ")] = str(framework) + str(__version__)
            bstack111lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᴠ")] = bstack1l1l1lll111_opy_()
            bstack111lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᴡ")] = bstack11ll11l11_opy_
            bstack111lll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᴢ")] = bstack1l1l1111l_opy_
            bstack111ll11ll11_opy_ = bstack111ll11ll11_opy_.split(bstack1ll11ll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᴣ"))[0] + bstack1ll11ll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴤ") + urllib.parse.quote(json.dumps(bstack111lll111ll_opy_))
    return bstack111ll11ll11_opy_
def bstack1ll1l1lll1_opy_():
    global bstack11l1l111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1l111_opy_ = BrowserType.connect
    return bstack11l1l111_opy_
def bstack11ll1l1ll1_opy_(framework_name):
    global bstack11l1lll1l1_opy_
    bstack11l1lll1l1_opy_ = framework_name
    return framework_name
def bstack11111111l_opy_(self, *args, **kwargs):
    global bstack11l1l111_opy_
    try:
        global bstack11l1lll1l1_opy_
        if bstack1ll11ll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᴥ") in kwargs:
            kwargs[bstack1ll11ll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᴦ")] = bstack111lllll1ll_opy_(
                kwargs.get(bstack1ll11ll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᴧ"), None),
                bstack11l1lll1l1_opy_
            )
    except Exception as e:
        logger.error(bstack1ll11ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᴨ").format(str(e)))
    return bstack11l1l111_opy_(self, *args, **kwargs)
def bstack11l11111111_opy_(bstack11l11ll1l1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1llll11lll_opy_(bstack11l11ll1l1l_opy_, bstack1ll11ll_opy_ (u"ࠥࠦᴩ"))
        if proxies and proxies.get(bstack1ll11ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᴪ")):
            parsed_url = urlparse(proxies.get(bstack1ll11ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᴫ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll11ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᴬ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll11ll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᴭ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᴮ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll11ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᴯ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1llll1l1l_opy_(bstack11l11ll1l1l_opy_):
    bstack111ll11l11l_opy_ = {
        bstack11l1l11ll11_opy_[bstack111lll11ll1_opy_]: bstack11l11ll1l1l_opy_[bstack111lll11ll1_opy_]
        for bstack111lll11ll1_opy_ in bstack11l11ll1l1l_opy_
        if bstack111lll11ll1_opy_ in bstack11l1l11ll11_opy_
    }
    bstack111ll11l11l_opy_[bstack1ll11ll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᴰ")] = bstack11l11111111_opy_(bstack11l11ll1l1l_opy_, bstack1l111111l1_opy_.get_property(bstack1ll11ll_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᴱ")))
    bstack11l11l111l1_opy_ = [element.lower() for element in bstack11l1ll1l1l1_opy_]
    bstack111ll1ll111_opy_(bstack111ll11l11l_opy_, bstack11l11l111l1_opy_)
    return bstack111ll11l11l_opy_
def bstack111ll1ll111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll11ll_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᴲ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111ll1ll111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111ll1ll111_opy_(item, keys)
def bstack1l1l1lll1l1_opy_():
    bstack11l11l11111_opy_ = [os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣᴳ")), os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠢࡿࠤᴴ")), bstack1ll11ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᴵ")), os.path.join(bstack1ll11ll_opy_ (u"ࠩ࠲ࡸࡲࡶࠧᴶ"), bstack1ll11ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᴷ"))]
    for path in bstack11l11l11111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll11ll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦᴸ") + str(path) + bstack1ll11ll_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣᴹ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll11ll_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥᴺ") + str(path) + bstack1ll11ll_opy_ (u"ࠢࠨࠤᴻ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll11ll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣᴼ") + str(path) + bstack1ll11ll_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢᴽ"))
            else:
                logger.debug(bstack1ll11ll_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧᴾ") + str(path) + bstack1ll11ll_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣᴿ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll11ll_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥᵀ") + str(path) + bstack1ll11ll_opy_ (u"ࠨࠧ࠯ࠤᵁ"))
            return path
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧᵂ") + str(e) + bstack1ll11ll_opy_ (u"ࠣࠤᵃ"))
    logger.debug(bstack1ll11ll_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨᵄ"))
    return None
@measure(event_name=EVENTS.bstack11l1ll11lll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack1lll1ll11ll_opy_(binary_path, bstack1lll1ll1l11_opy_, bs_config):
    logger.debug(bstack1ll11ll_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤᵅ").format(binary_path))
    bstack111lllll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬᵆ")
    bstack11l1111llll_opy_ = {
        bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᵇ"): __version__,
        bstack1ll11ll_opy_ (u"ࠨ࡯ࡴࠤᵈ"): platform.system(),
        bstack1ll11ll_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣᵉ"): platform.machine(),
        bstack1ll11ll_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᵊ"): bstack1ll11ll_opy_ (u"ࠩ࠳ࠫᵋ"),
        bstack1ll11ll_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤᵌ"): bstack1ll11ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᵍ")
    }
    bstack11l111l11l1_opy_(bstack11l1111llll_opy_)
    try:
        if binary_path:
            bstack11l1111llll_opy_[bstack1ll11ll_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᵎ")] = subprocess.check_output([binary_path, bstack1ll11ll_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᵏ")]).strip().decode(bstack1ll11ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᵐ"))
        response = requests.request(
            bstack1ll11ll_opy_ (u"ࠨࡉࡈࡘࠬᵑ"),
            url=bstack11ll11111_opy_(bstack11l1l1ll1l1_opy_),
            headers=None,
            auth=(bs_config[bstack1ll11ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᵒ")], bs_config[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᵓ")]),
            json=None,
            params=bstack11l1111llll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll11ll_opy_ (u"ࠫࡺࡸ࡬ࠨᵔ") in data.keys() and bstack1ll11ll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᵕ") in data.keys():
            logger.debug(bstack1ll11ll_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᵖ").format(bstack11l1111llll_opy_[bstack1ll11ll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵗ")]))
            if bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫᵘ") in os.environ:
                logger.debug(bstack1ll11ll_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠥ࡯ࡳࠡࡵࡨࡸࠧᵙ"))
                data[bstack1ll11ll_opy_ (u"ࠪࡹࡷࡲࠧᵚ")] = os.environ[bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᵛ")]
            bstack11l11l1l1ll_opy_ = bstack111ll1111ll_opy_(data[bstack1ll11ll_opy_ (u"ࠬࡻࡲ࡭ࠩᵜ")], bstack1lll1ll1l11_opy_)
            bstack111lllll1l1_opy_ = os.path.join(bstack1lll1ll1l11_opy_, bstack11l11l1l1ll_opy_)
            os.chmod(bstack111lllll1l1_opy_, 0o777) # bstack11l111ll1ll_opy_ permission
            return bstack111lllll1l1_opy_
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᵝ").format(e))
    return binary_path
def bstack11l111l11l1_opy_(bstack11l1111llll_opy_):
    try:
        if bstack1ll11ll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᵞ") not in bstack11l1111llll_opy_[bstack1ll11ll_opy_ (u"ࠨࡱࡶࠫᵟ")].lower():
            return
        if os.path.exists(bstack1ll11ll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᵠ")):
            with open(bstack1ll11ll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᵡ"), bstack1ll11ll_opy_ (u"ࠦࡷࠨᵢ")) as f:
                bstack11l11l1lll1_opy_ = {}
                for line in f:
                    if bstack1ll11ll_opy_ (u"ࠧࡃࠢᵣ") in line:
                        key, value = line.rstrip().split(bstack1ll11ll_opy_ (u"ࠨ࠽ࠣᵤ"), 1)
                        bstack11l11l1lll1_opy_[key] = value.strip(bstack1ll11ll_opy_ (u"ࠧࠣ࡞ࠪࠫᵥ"))
                bstack11l1111llll_opy_[bstack1ll11ll_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᵦ")] = bstack11l11l1lll1_opy_.get(bstack1ll11ll_opy_ (u"ࠤࡌࡈࠧᵧ"), bstack1ll11ll_opy_ (u"ࠥࠦᵨ"))
        elif os.path.exists(bstack1ll11ll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᵩ")):
            bstack11l1111llll_opy_[bstack1ll11ll_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬᵪ")] = bstack1ll11ll_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭ᵫ")
    except Exception as e:
        logger.debug(bstack1ll11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤᵬ") + e)
@measure(event_name=EVENTS.bstack11l1lll111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
def bstack111ll1111ll_opy_(bstack11l11l11ll1_opy_, bstack11l1111l1l1_opy_):
    logger.debug(bstack1ll11ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᵭ") + str(bstack11l11l11ll1_opy_) + bstack1ll11ll_opy_ (u"ࠤࠥᵮ"))
    zip_path = os.path.join(bstack11l1111l1l1_opy_, bstack1ll11ll_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᵯ"))
    bstack11l11l1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠫࠬᵰ")
    with requests.get(bstack11l11l11ll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll11ll_opy_ (u"ࠧࡽࡢࠣᵱ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣᵲ"))
    with zipfile.ZipFile(zip_path, bstack1ll11ll_opy_ (u"ࠧࡳࠩᵳ")) as zip_ref:
        bstack111ll1lll1l_opy_ = zip_ref.namelist()
        if len(bstack111ll1lll1l_opy_) > 0:
            bstack11l11l1l1ll_opy_ = bstack111ll1lll1l_opy_[0] # bstack111ll11l111_opy_ bstack11l1l1ll111_opy_ will be bstack11l111ll1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1111l1l1_opy_)
        logger.debug(bstack1ll11ll_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᵴ") + str(bstack11l1111l1l1_opy_) + bstack1ll11ll_opy_ (u"ࠤࠪࠦᵵ"))
    os.remove(zip_path)
    return bstack11l11l1l1ll_opy_
def get_cli_dir():
    bstack111llllll11_opy_ = bstack1l1l1lll1l1_opy_()
    if bstack111llllll11_opy_:
        bstack1lll1ll1l11_opy_ = os.path.join(bstack111llllll11_opy_, bstack1ll11ll_opy_ (u"ࠥࡧࡱ࡯ࠢᵶ"))
        if not os.path.exists(bstack1lll1ll1l11_opy_):
            os.makedirs(bstack1lll1ll1l11_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1ll1l11_opy_
    else:
        raise FileNotFoundError(bstack1ll11ll_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢᵷ"))
def bstack1llll11111l_opy_(bstack1lll1ll1l11_opy_):
    bstack1ll11ll_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤᵸ")
    bstack111ll1l11ll_opy_ = [
        os.path.join(bstack1lll1ll1l11_opy_, f)
        for f in os.listdir(bstack1lll1ll1l11_opy_)
        if os.path.isfile(os.path.join(bstack1lll1ll1l11_opy_, f)) and f.startswith(bstack1ll11ll_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢᵹ"))
    ]
    if len(bstack111ll1l11ll_opy_) > 0:
        return max(bstack111ll1l11ll_opy_, key=os.path.getmtime) # get bstack11l11l11lll_opy_ binary
    return bstack1ll11ll_opy_ (u"ࠢࠣᵺ")
def bstack11ll11l1111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1111ll11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1111ll11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1111lllll_opy_(data, keys, default=None):
    bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡤࡪࡪࡲࡹࠡࡩࡨࡸࠥࡧࠠ࡯ࡧࡶࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡥࡹࡧ࠺ࠡࡖ࡫ࡩࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶࠣࡸࡴࠦࡴࡳࡣࡹࡩࡷࡹࡥ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡫ࡦࡻࡶ࠾ࠥࡇࠠ࡭࡫ࡶࡸࠥࡵࡦࠡ࡭ࡨࡽࡸ࠵ࡩ࡯ࡦ࡬ࡧࡪࡹࠠࡳࡧࡳࡶࡪࡹࡥ࡯ࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡦࡨࡤࡹࡱࡺ࠺ࠡࡘࡤࡰࡺ࡫ࠠࡵࡱࠣࡶࡪࡺࡵࡳࡰࠣ࡭࡫ࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡴࡨࡸࡺࡸ࡮࠻ࠢࡗ࡬ࡪࠦࡶࡢ࡮ࡸࡩࠥࡧࡴࠡࡶ࡫ࡩࠥࡴࡥࡴࡶࡨࡨࠥࡶࡡࡵࡪ࠯ࠤࡴࡸࠠࡥࡧࡩࡥࡺࡲࡴࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᵻ")
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