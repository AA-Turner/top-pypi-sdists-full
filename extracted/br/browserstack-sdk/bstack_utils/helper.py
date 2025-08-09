# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
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
from bstack_utils.constants import (bstack1l1l111ll_opy_, bstack1l11l11ll_opy_, bstack1ll11ll1ll_opy_,
                                    bstack11l1ll1l1l1_opy_, bstack11l1lll11ll_opy_, bstack11l1lll111l_opy_, bstack11l1ll1111l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll111111_opy_, bstack111l11111_opy_
from bstack_utils.proxy import bstack1ll1lll11l_opy_, bstack1ll1l1111_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1111111_opy_
from bstack_utils.bstack11ll1lllll_opy_ import bstack1111l1l11_opy_
from browserstack_sdk._version import __version__
bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
logger = bstack1l1111111_opy_.get_logger(__name__, bstack1l1111111_opy_.bstack1lll11lll1l_opy_())
def bstack11ll1lll11l_opy_(config):
    return config[bstack11l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᫰")]
def bstack11lll111111_opy_(config):
    return config[bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ᫱")]
def bstack11l11l1111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11l1ll11_opy_(obj):
    values = []
    bstack111lll1111l_opy_ = re.compile(bstack11l1_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ᫲"), re.I)
    for key in obj.keys():
        if bstack111lll1111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11ll1l11_opy_(config):
    tags = []
    tags.extend(bstack11l11l1ll11_opy_(os.environ))
    tags.extend(bstack11l11l1ll11_opy_(config))
    return tags
def bstack11l11ll1l1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11l1l1l1_opy_(bstack11l111ll11l_opy_):
    if not bstack11l111ll11l_opy_:
        return bstack11l1_opy_ (u"ࠫࠬ᫳")
    return bstack11l1_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨ᫴").format(bstack11l111ll11l_opy_.name, bstack11l111ll11l_opy_.email)
def bstack11lll11l11l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l11l1llll_opy_ = repo.common_dir
        info = {
            bstack11l1_opy_ (u"ࠨࡳࡩࡣࠥ᫵"): repo.head.commit.hexsha,
            bstack11l1_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥ᫶"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣ᫷"): repo.active_branch.name,
            bstack11l1_opy_ (u"ࠤࡷࡥ࡬ࠨ᫸"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨ᫹"): bstack11l11l1l1l1_opy_(repo.head.commit.committer),
            bstack11l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧ᫺"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧ᫻"): bstack11l11l1l1l1_opy_(repo.head.commit.author),
            bstack11l1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦ᫼"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᫽"): repo.head.commit.message,
            bstack11l1_opy_ (u"ࠣࡴࡲࡳࡹࠨ᫾"): repo.git.rev_parse(bstack11l1_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦ᫿")),
            bstack11l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᬀ"): bstack11l11l1llll_opy_,
            bstack11l1_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᬁ"): subprocess.check_output([bstack11l1_opy_ (u"ࠧ࡭ࡩࡵࠤᬂ"), bstack11l1_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᬃ"), bstack11l1_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᬄ")]).strip().decode(
                bstack11l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᬅ")),
            bstack11l1_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᬆ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᬇ"): repo.git.rev_list(
                bstack11l1_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᬈ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lllll111_opy_ = []
        for remote in remotes:
            bstack111ll1ll1ll_opy_ = {
                bstack11l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬉ"): remote.name,
                bstack11l1_opy_ (u"ࠨࡵࡳ࡮ࠥᬊ"): remote.url,
            }
            bstack111lllll111_opy_.append(bstack111ll1ll1ll_opy_)
        bstack11l11ll1lll_opy_ = {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬋ"): bstack11l1_opy_ (u"ࠣࡩ࡬ࡸࠧᬌ"),
            **info,
            bstack11l1_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᬍ"): bstack111lllll111_opy_
        }
        bstack11l11ll1lll_opy_ = bstack11l1l11l111_opy_(bstack11l11ll1lll_opy_)
        return bstack11l11ll1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᬎ").format(err))
        return {}
def bstack111ll1ll11l_opy_(bstack111lll1lll1_opy_=None):
    bstack11l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࡣ࡯ࡰࡾࠦࡦࡰࡴࡰࡥࡹࡺࡥࡥࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡻࡳࡦࠢࡦࡥࡸ࡫ࡳࠡࡨࡲࡶࠥ࡫ࡡࡤࡪࠣࡪࡴࡲࡤࡦࡴࠣ࡭ࡳࠦࡴࡩࡧࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥ࡬࡯࡭ࡦࡨࡶࠥࡶࡡࡵࡪࡶࠤࡹࡵࠠࡦࡺࡷࡶࡦࡩࡴࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡴࡲࡱ࠳ࠦࡄࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡠࡵࡳ࠯ࡩࡨࡸࡨࡽࡤࠩࠫࡠ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡲࡩࡴࡶ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡪࡩࡤࡶࡶ࠰ࠥ࡫ࡡࡤࡪࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡥࠥ࡬࡯࡭ࡦࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᬏ")
    if bstack111lll1lll1_opy_ is None:
        bstack111lll1lll1_opy_ = [os.getcwd()]
    results = []
    for folder in bstack111lll1lll1_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11l1_opy_ (u"ࠧࡶࡲࡊࡦࠥᬐ"): bstack11l1_opy_ (u"ࠨࠢᬑ"),
                bstack11l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬒ"): [],
                bstack11l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᬓ"): [],
                bstack11l1_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᬔ"): bstack11l1_opy_ (u"ࠥࠦᬕ"),
                bstack11l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᬖ"): [],
                bstack11l1_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᬗ"): bstack11l1_opy_ (u"ࠨࠢᬘ"),
                bstack11l1_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢᬙ"): bstack11l1_opy_ (u"ࠣࠤᬚ"),
                bstack11l1_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧᬛ"): bstack11l1_opy_ (u"ࠥࠦᬜ")
            }
            bstack11l11111l11_opy_ = repo.active_branch.name
            bstack111lllll1l1_opy_ = repo.head.commit
            result[bstack11l1_opy_ (u"ࠦࡵࡸࡉࡥࠤᬝ")] = bstack111lllll1l1_opy_.hexsha
            bstack11l11l11111_opy_ = _11l11111lll_opy_(repo)
            logger.debug(bstack11l1_opy_ (u"ࠧࡈࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠾ࠥࠨᬞ") + str(bstack11l11l11111_opy_) + bstack11l1_opy_ (u"ࠨࠢᬟ"))
            if bstack11l11l11111_opy_:
                try:
                    bstack11l111111l1_opy_ = repo.git.diff(bstack11l1_opy_ (u"ࠢ࠮࠯ࡱࡥࡲ࡫࠭ࡰࡰ࡯ࡽࠧᬠ"), bstack1lll1lll111_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᬡ")).split(bstack11l1_opy_ (u"ࠩ࡟ࡲࠬᬢ"))
                    logger.debug(bstack11l1_opy_ (u"ࠥࡇ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡦࡪࡺࡷࡦࡧࡱࠤࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀࠤࡦࡴࡤࠡࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀ࠾ࠥࠨᬣ") + str(bstack11l111111l1_opy_) + bstack11l1_opy_ (u"ࠦࠧᬤ"))
                    result[bstack11l1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᬥ")] = [f.strip() for f in bstack11l111111l1_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll1lll111_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥᬦ")))
                except Exception:
                    logger.debug(bstack11l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡨࡲࡢࡰࡦ࡬ࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠰ࠣࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥࡸࡥࡤࡧࡱࡸࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠢᬧ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬨ")] = _111ll1ll1l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11l1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᬩ")] = _111ll1ll1l1_opy_(commits[:5])
            bstack111ll1lll1l_opy_ = set()
            bstack111llll1111_opy_ = []
            for commit in commits:
                logger.debug(bstack11l1_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱ࡮ࡺ࠺ࠡࠤᬪ") + str(commit.message) + bstack11l1_opy_ (u"ࠦࠧᬫ"))
                bstack11l11l111l1_opy_ = commit.author.name if commit.author else bstack11l1_opy_ (u"࡛ࠧ࡮࡬ࡰࡲࡻࡳࠨᬬ")
                bstack111ll1lll1l_opy_.add(bstack11l11l111l1_opy_)
                bstack111llll1111_opy_.append({
                    bstack11l1_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᬭ"): commit.message.strip(),
                    bstack11l1_opy_ (u"ࠢࡶࡵࡨࡶࠧᬮ"): bstack11l11l111l1_opy_
                })
            result[bstack11l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᬯ")] = list(bstack111ll1lll1l_opy_)
            result[bstack11l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥᬰ")] = bstack111llll1111_opy_
            result[bstack11l1_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᬱ")] = bstack111lllll1l1_opy_.committed_datetime.strftime(bstack11l1_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩࠨᬲ"))
            if (not result[bstack11l1_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᬳ")] or result[bstack11l1_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫᬴ࠢ")].strip() == bstack11l1_opy_ (u"ࠢࠣᬵ")) and bstack111lllll1l1_opy_.message:
                bstack11l11l1l1ll_opy_ = bstack111lllll1l1_opy_.message.strip().split(bstack11l1_opy_ (u"ࠨ࡞ࡱࠫᬶ"))
                result[bstack11l1_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᬷ")] = bstack11l11l1l1ll_opy_[0] if bstack11l11l1l1ll_opy_ else bstack11l1_opy_ (u"ࠥࠦᬸ")
                if len(bstack11l11l1l1ll_opy_) > 2:
                    result[bstack11l1_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦᬹ")] = bstack11l1_opy_ (u"ࠬࡢ࡮ࠨᬺ").join(bstack11l11l1l1ll_opy_[2:]).strip()
            results.append(result)
        except git.InvalidGitRepositoryError:
            results.append({
                bstack11l1_opy_ (u"ࠨࡰࡳࡋࡧࠦᬻ"): bstack11l1_opy_ (u"ࠢࠣᬼ"),
                bstack11l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬽ"): [],
                bstack11l1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᬾ"): [],
                bstack11l1_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᬿ"): bstack11l1_opy_ (u"ࠦࠧᭀ"),
                bstack11l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᭁ"): [],
                bstack11l1_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᭂ"): bstack11l1_opy_ (u"ࠢࠣᭃ"),
                bstack11l1_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮᭄ࠣ"): bstack11l1_opy_ (u"ࠤࠥᭅ"),
                bstack11l1_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨᭆ"): bstack11l1_opy_ (u"ࠦࠧᭇ")
            })
        except Exception as err:
            logger.error(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࠬ࡫ࡵ࡬ࡥࡧࡵ࠾ࠥࢁࡦࡰ࡮ࡧࡩࡷࢃࠩ࠻ࠢࠥᭈ") + str(err) + bstack11l1_opy_ (u"ࠨࠢᭉ"))
            results.append({
                bstack11l1_opy_ (u"ࠢࡱࡴࡌࡨࠧᭊ"): bstack11l1_opy_ (u"ࠣࠤᭋ"),
                bstack11l1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᭌ"): [],
                bstack11l1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ᭍"): [],
                bstack11l1_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦ᭎"): bstack11l1_opy_ (u"ࠧࠨ᭏"),
                bstack11l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢ᭐"): [],
                bstack11l1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣ᭑"): bstack11l1_opy_ (u"ࠣࠤ᭒"),
                bstack11l1_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤ᭓"): bstack11l1_opy_ (u"ࠥࠦ᭔"),
                bstack11l1_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢ᭕"): bstack11l1_opy_ (u"ࠧࠨ᭖")
            })
    return results
def _11l11111lll_opy_(repo):
    bstack11l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࠭ࡳࡡࡪࡰ࠯ࠤࡲࡧࡳࡵࡧࡵ࠰ࠥࡪࡥࡷࡧ࡯ࡳࡵ࠲ࠠࡦࡶࡦ࠲࠮ࠐࠠࠡࠢࠣࠦࠧࠨ᭗")
    try:
        bstack11l1l1111l1_opy_ = [bstack11l1_opy_ (u"ࠧ࡮ࡣ࡬ࡲࠬ᭘"), bstack11l1_opy_ (u"ࠨ࡯ࡤࡷࡹ࡫ࡲࠨ᭙"), bstack11l1_opy_ (u"ࠩࡧࡩࡻ࡫࡬ࡰࡲࠪ᭚"), bstack11l1_opy_ (u"ࠪࡨࡪࡼࠧ᭛")]
        for branch_name in bstack11l1l1111l1_opy_:
            try:
                repo.heads[branch_name]
                return branch_name
            except IndexError:
                try:
                    repo.remotes.origin.refs[branch_name]
                    return bstack11l1_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱ࠳ࢀࢃࠢ᭜").format(branch_name)
                except (AttributeError, IndexError):
                    continue
    except Exception:
        pass
    return None
def _111ll1ll1l1_opy_(commits):
    bstack11l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡣࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᭝")
    bstack11l111111l1_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack11l111l1l1l_opy_ in diff:
                        if bstack11l111l1l1l_opy_.a_path:
                            bstack11l111111l1_opy_.add(bstack11l111l1l1l_opy_.a_path)
                        if bstack11l111l1l1l_opy_.b_path:
                            bstack11l111111l1_opy_.add(bstack11l111l1l1l_opy_.b_path)
    except Exception:
        pass
    return list(bstack11l111111l1_opy_)
def bstack11l1l11l111_opy_(bstack11l11ll1lll_opy_):
    bstack11l111l11ll_opy_ = bstack11l1111l1l1_opy_(bstack11l11ll1lll_opy_)
    if bstack11l111l11ll_opy_ and bstack11l111l11ll_opy_ > bstack11l1ll1l1l1_opy_:
        bstack11l1111ll1l_opy_ = bstack11l111l11ll_opy_ - bstack11l1ll1l1l1_opy_
        bstack11l1l11111l_opy_ = bstack11l11lll11l_opy_(bstack11l11ll1lll_opy_[bstack11l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᭞")], bstack11l1111ll1l_opy_)
        bstack11l11ll1lll_opy_[bstack11l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᭟")] = bstack11l1l11111l_opy_
        logger.info(bstack11l1_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ᭠")
                    .format(bstack11l1111l1l1_opy_(bstack11l11ll1lll_opy_) / 1024))
    return bstack11l11ll1lll_opy_
def bstack11l1111l1l1_opy_(bstack1111lll11_opy_):
    try:
        if bstack1111lll11_opy_:
            bstack111llllll1l_opy_ = json.dumps(bstack1111lll11_opy_)
            bstack11l11lll1l1_opy_ = sys.getsizeof(bstack111llllll1l_opy_)
            return bstack11l11lll1l1_opy_
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ᭡").format(e))
    return -1
def bstack11l11lll11l_opy_(field, bstack111llll1ll1_opy_):
    try:
        bstack11l11llll11_opy_ = len(bytes(bstack11l1lll11ll_opy_, bstack11l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᭢")))
        bstack111llll1lll_opy_ = bytes(field, bstack11l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᭣"))
        bstack11l111lllll_opy_ = len(bstack111llll1lll_opy_)
        bstack11l11l1lll1_opy_ = ceil(bstack11l111lllll_opy_ - bstack111llll1ll1_opy_ - bstack11l11llll11_opy_)
        if bstack11l11l1lll1_opy_ > 0:
            bstack11l1l111l11_opy_ = bstack111llll1lll_opy_[:bstack11l11l1lll1_opy_].decode(bstack11l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᭤"), errors=bstack11l1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭᭥")) + bstack11l1lll11ll_opy_
            return bstack11l1l111l11_opy_
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧ᭦").format(e))
    return field
def bstack1lllll11l_opy_():
    env = os.environ
    if (bstack11l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᭧") in env and len(env[bstack11l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ᭨")]) > 0) or (
            bstack11l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᭩") in env and len(env[bstack11l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᭪")]) > 0):
        return {
            bstack11l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᭫"): bstack11l1_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹ᭬ࠢ"),
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᭭"): env.get(bstack11l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᭮")),
            bstack11l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭯"): env.get(bstack11l1_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᭰")),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭱"): env.get(bstack11l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᭲"))
        }
    if env.get(bstack11l1_opy_ (u"ࠨࡃࡊࠤ᭳")) == bstack11l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ᭴") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᭵"))):
        return {
            bstack11l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭶"): bstack11l1_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᭷"),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭸"): env.get(bstack11l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᭹")),
            bstack11l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᭺"): env.get(bstack11l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᭻")),
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭼"): env.get(bstack11l1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ᭽"))
        }
    if env.get(bstack11l1_opy_ (u"ࠥࡇࡎࠨ᭾")) == bstack11l1_opy_ (u"ࠦࡹࡸࡵࡦࠤ᭿") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧᮀ"))):
        return {
            bstack11l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮁ"): bstack11l1_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥᮂ"),
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮃ"): env.get(bstack11l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤᮄ")),
            bstack11l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮅ"): env.get(bstack11l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᮆ")),
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮇ"): env.get(bstack11l1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᮈ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠢࡄࡋࠥᮉ")) == bstack11l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᮊ") and env.get(bstack11l1_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥᮋ")) == bstack11l1_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧᮌ"):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮍ"): bstack11l1_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢᮎ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᮏ"): None,
            bstack11l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮐ"): None,
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮑ"): None
        }
    if env.get(bstack11l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧᮒ")) and env.get(bstack11l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᮓ")):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮔ"): bstack11l1_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣᮕ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᮖ"): env.get(bstack11l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧᮗ")),
            bstack11l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮘ"): None,
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮙ"): env.get(bstack11l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᮚ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠦࡈࡏࠢᮛ")) == bstack11l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᮜ") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᮝ"))):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮞ"): bstack11l1_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢᮟ"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮠ"): env.get(bstack11l1_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᮡ")),
            bstack11l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮢ"): None,
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮣ"): env.get(bstack11l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᮤ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠢࡄࡋࠥᮥ")) == bstack11l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᮦ") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᮧ"))):
        return {
            bstack11l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᮨ"): bstack11l1_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᮩ"),
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᮪ࠣ"): env.get(bstack11l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐ᮫ࠧ")),
            bstack11l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮬ"): env.get(bstack11l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᮭ")),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮮ"): env.get(bstack11l1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᮯ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠦࡈࡏࠢ᮰")) == bstack11l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᮱") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ᮲"))):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᮳"): bstack11l1_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ᮴"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᮵"): env.get(bstack11l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢ᮶")),
            bstack11l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᮷"): env.get(bstack11l1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᮸")),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᮹"): env.get(bstack11l1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᮺ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠣࡅࡌࠦᮻ")) == bstack11l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᮼ") and bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᮽ"))):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮾ"): bstack11l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᮿ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯀ"): env.get(bstack11l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᯁ")),
            bstack11l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᯂ"): env.get(bstack11l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᯃ")) or env.get(bstack11l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᯄ")),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯅ"): env.get(bstack11l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᯆ"))
        }
    if bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᯇ"))):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᯈ"): bstack11l1_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᯉ"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᯊ"): bstack11l1_opy_ (u"ࠥࡿࢂࢁࡽࠣᯋ").format(env.get(bstack11l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᯌ")), env.get(bstack11l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᯍ"))),
            bstack11l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯎ"): env.get(bstack11l1_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᯏ")),
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᯐ"): env.get(bstack11l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᯑ"))
        }
    if bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᯒ"))):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯓ"): bstack11l1_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᯔ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯕ"): bstack11l1_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᯖ").format(env.get(bstack11l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᯗ")), env.get(bstack11l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᯘ")), env.get(bstack11l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᯙ")), env.get(bstack11l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᯚ"))),
            bstack11l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᯛ"): env.get(bstack11l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᯜ")),
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᯝ"): env.get(bstack11l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᯞ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᯟ")) and env.get(bstack11l1_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᯠ")):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯡ"): bstack11l1_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᯢ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯣ"): bstack11l1_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᯤ").format(env.get(bstack11l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᯥ")), env.get(bstack11l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ᯦࡚ࠧ")), env.get(bstack11l1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᯧ"))),
            bstack11l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯨ"): env.get(bstack11l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᯩ")),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯪ"): env.get(bstack11l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᯫ"))
        }
    if any([env.get(bstack11l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᯬ")), env.get(bstack11l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᯭ")), env.get(bstack11l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᯮ"))]):
        return {
            bstack11l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯯ"): bstack11l1_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᯰ"),
            bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯱ"): env.get(bstack11l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᯲")),
            bstack11l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧ᯳ࠥ"): env.get(bstack11l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᯴")),
            bstack11l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᯵"): env.get(bstack11l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᯶"))
        }
    if env.get(bstack11l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ᯷")):
        return {
            bstack11l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᯸"): bstack11l1_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢ᯹"),
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᯺"): env.get(bstack11l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ᯻")),
            bstack11l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᯼"): env.get(bstack11l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ᯽")),
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᯾"): env.get(bstack11l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᯿"))
        }
    if env.get(bstack11l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣᰀ")) or env.get(bstack11l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᰁ")):
        return {
            bstack11l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᰂ"): bstack11l1_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦᰃ"),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᰄ"): env.get(bstack11l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᰅ")),
            bstack11l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰆ"): bstack11l1_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢᰇ") if env.get(bstack11l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᰈ")) else None,
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰉ"): env.get(bstack11l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣᰊ"))
        }
    if any([env.get(bstack11l1_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤᰋ")), env.get(bstack11l1_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᰌ")), env.get(bstack11l1_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᰍ"))]):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰎ"): bstack11l1_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢᰏ"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰐ"): None,
            bstack11l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰑ"): env.get(bstack11l1_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣᰒ")),
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰓ"): env.get(bstack11l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᰔ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥᰕ")):
        return {
            bstack11l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᰖ"): bstack11l1_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧᰗ"),
            bstack11l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰘ"): env.get(bstack11l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᰙ")),
            bstack11l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰚ"): bstack11l1_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢᰛ").format(env.get(bstack11l1_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪᰜ"))) if env.get(bstack11l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦᰝ")) else None,
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰞ"): env.get(bstack11l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᰟ"))
        }
    if bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧᰠ"))):
        return {
            bstack11l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰡ"): bstack11l1_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢᰢ"),
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᰣ"): env.get(bstack11l1_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧᰤ")),
            bstack11l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰥ"): env.get(bstack11l1_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨᰦ")),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰧ"): env.get(bstack11l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᰨ"))
        }
    if bstack1ll1l11111_opy_(env.get(bstack11l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢᰩ"))):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰪ"): bstack11l1_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤᰫ"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᰬ"): bstack11l1_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦᰭ").format(env.get(bstack11l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨᰮ")), env.get(bstack11l1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩᰯ")), env.get(bstack11l1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ᰰ"))),
            bstack11l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰱ"): env.get(bstack11l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥᰲ")),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰳ"): env.get(bstack11l1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥᰴ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠦࡈࡏࠢᰵ")) == bstack11l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᰶ") and env.get(bstack11l1_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ᰷")) == bstack11l1_opy_ (u"ࠢ࠲ࠤ᰸"):
        return {
            bstack11l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᰹"): bstack11l1_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ᰺"),
            bstack11l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᰻"): bstack11l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ᰼").format(env.get(bstack11l1_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩ᰽"))),
            bstack11l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᰾"): None,
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᰿"): None,
        }
    if env.get(bstack11l1_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ᱀")):
        return {
            bstack11l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᱁"): bstack11l1_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ᱂"),
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᱃"): None,
            bstack11l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᱄"): env.get(bstack11l1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ᱅")),
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᱆"): env.get(bstack11l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᱇"))
        }
    if any([env.get(bstack11l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ᱈")), env.get(bstack11l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ᱉")), env.get(bstack11l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ᱊")), env.get(bstack11l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ᱋"))]):
        return {
            bstack11l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᱌"): bstack11l1_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥᱍ"),
            bstack11l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᱎ"): None,
            bstack11l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᱏ"): env.get(bstack11l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᱐")) or None,
            bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᱑"): env.get(bstack11l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᱒"), 0)
        }
    if env.get(bstack11l1_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᱓")):
        return {
            bstack11l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱔"): bstack11l1_opy_ (u"ࠣࡉࡲࡇࡉࠨ᱕"),
            bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᱖"): None,
            bstack11l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᱗"): env.get(bstack11l1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᱘")),
            bstack11l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱙"): env.get(bstack11l1_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧᱚ"))
        }
    if env.get(bstack11l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᱛ")):
        return {
            bstack11l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᱜ"): bstack11l1_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧᱝ"),
            bstack11l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᱞ"): env.get(bstack11l1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᱟ")),
            bstack11l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᱠ"): env.get(bstack11l1_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᱡ")),
            bstack11l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᱢ"): env.get(bstack11l1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᱣ"))
        }
    return {bstack11l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᱤ"): None}
def get_host_info():
    return {
        bstack11l1_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧᱥ"): platform.node(),
        bstack11l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨᱦ"): platform.system(),
        bstack11l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᱧ"): platform.machine(),
        bstack11l1_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᱨ"): platform.version(),
        bstack11l1_opy_ (u"ࠢࡢࡴࡦ࡬ࠧᱩ"): platform.architecture()[0]
    }
def bstack1l1l11l1l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11l11ll1_opy_():
    if bstack1l1llll1l_opy_.get_property(bstack11l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᱪ")):
        return bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᱫ")
    return bstack11l1_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩᱬ")
def bstack111ll1lll11_opy_(driver):
    info = {
        bstack11l1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᱭ"): driver.capabilities,
        bstack11l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩᱮ"): driver.session_id,
        bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᱯ"): driver.capabilities.get(bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᱰ"), None),
        bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᱱ"): driver.capabilities.get(bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱲ"), None),
        bstack11l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬᱳ"): driver.capabilities.get(bstack11l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᱴ"), None),
        bstack11l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᱵ"):driver.capabilities.get(bstack11l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱶ"), None),
    }
    if bstack11l11l11ll1_opy_() == bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᱷ"):
        if bstack1l11l11lll_opy_():
            info[bstack11l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᱸ")] = bstack11l1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᱹ")
        elif driver.capabilities.get(bstack11l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᱺ"), {}).get(bstack11l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᱻ"), False):
            info[bstack11l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᱼ")] = bstack11l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᱽ")
        else:
            info[bstack11l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᱾")] = bstack11l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᱿")
    return info
def bstack1l11l11lll_opy_():
    if bstack1l1llll1l_opy_.get_property(bstack11l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᲀ")):
        return True
    if bstack1ll1l11111_opy_(os.environ.get(bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᲁ"), None)):
        return True
    return False
def bstack1l11l1l1l1_opy_(bstack11l11lllll1_opy_, url, data, config):
    headers = config.get(bstack11l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᲂ"), None)
    proxies = bstack1ll1lll11l_opy_(config, url)
    auth = config.get(bstack11l1_opy_ (u"ࠬࡧࡵࡵࡪࠪᲃ"), None)
    response = requests.request(
            bstack11l11lllll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll1111l_opy_(bstack11lllll1_opy_, size):
    bstack1llll1l111_opy_ = []
    while len(bstack11lllll1_opy_) > size:
        bstack11111l1l_opy_ = bstack11lllll1_opy_[:size]
        bstack1llll1l111_opy_.append(bstack11111l1l_opy_)
        bstack11lllll1_opy_ = bstack11lllll1_opy_[size:]
    bstack1llll1l111_opy_.append(bstack11lllll1_opy_)
    return bstack1llll1l111_opy_
def bstack111llll1l11_opy_(message, bstack11l11l1111l_opy_=False):
    os.write(1, bytes(message, bstack11l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᲄ")))
    os.write(1, bytes(bstack11l1_opy_ (u"ࠧ࡝ࡰࠪᲅ"), bstack11l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᲆ")))
    if bstack11l11l1111l_opy_:
        with open(bstack11l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨᲇ") + os.environ[bstack11l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᲈ")] + bstack11l1_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩᲉ"), bstack11l1_opy_ (u"ࠬࡧࠧᲊ")) as f:
            f.write(message + bstack11l1_opy_ (u"࠭࡜࡯ࠩ᲋"))
def bstack1l1ll111l1l_opy_():
    return os.environ[bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ᲌")].lower() == bstack11l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᲍")
def bstack1l1l11lll_opy_():
    return bstack111l1ll11l_opy_().replace(tzinfo=None).isoformat() + bstack11l1_opy_ (u"ࠩ࡝ࠫ᲎")
def bstack111lll11l11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1_opy_ (u"ࠪ࡞ࠬ᲏"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1_opy_ (u"ࠫ࡟࠭Ა")))).total_seconds() * 1000
def bstack11l111l111l_opy_(timestamp):
    return bstack111llll11l1_opy_(timestamp).isoformat() + bstack11l1_opy_ (u"ࠬࡠࠧᲑ")
def bstack11l1111llll_opy_(bstack11l111l1lll_opy_):
    date_format = bstack11l1_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫᲒ")
    bstack11l111lll1l_opy_ = datetime.datetime.strptime(bstack11l111l1lll_opy_, date_format)
    return bstack11l111lll1l_opy_.isoformat() + bstack11l1_opy_ (u"࡛ࠧࠩᲓ")
def bstack11l11lll1ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᲔ")
    else:
        return bstack11l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᲕ")
def bstack1ll1l11111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᲖ")
def bstack111llllllll_opy_(val):
    return val.__str__().lower() == bstack11l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᲗ")
def error_handler(bstack111lll111ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111lll111ll_opy_ as e:
                print(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᲘ").format(func.__name__, bstack111lll111ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11l111ll_opy_(bstack11l1l111111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l111111_opy_(cls, *args, **kwargs)
            except bstack111lll111ll_opy_ as e:
                print(bstack11l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᲙ").format(bstack11l1l111111_opy_.__name__, bstack111lll111ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11l111ll_opy_
    else:
        return decorator
def bstack111l1llll_opy_(bstack11111ll1l1_opy_):
    if os.getenv(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᲚ")) is not None:
        return bstack1ll1l11111_opy_(os.getenv(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᲛ")))
    if bstack11l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ნ") in bstack11111ll1l1_opy_ and bstack111llllllll_opy_(bstack11111ll1l1_opy_[bstack11l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲝ")]):
        return False
    if bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Პ") in bstack11111ll1l1_opy_ and bstack111llllllll_opy_(bstack11111ll1l1_opy_[bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᲟ")]):
        return False
    return True
def bstack1l1l11l111_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11llll1l_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨᲠ"), None)
        return bstack11l11llll1l_opy_ is None or bstack11l11llll1l_opy_ == bstack11l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᲡ")
    except Exception as e:
        return False
def bstack1llll1l11_opy_(hub_url, CONFIG):
    if bstack1lll1l111_opy_() <= version.parse(bstack11l1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᲢ")):
        if hub_url:
            return bstack11l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᲣ") + hub_url + bstack11l1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᲤ")
        return bstack1l11l11ll_opy_
    if hub_url:
        return bstack11l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᲥ") + hub_url + bstack11l1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᲦ")
    return bstack1ll11ll1ll_opy_
def bstack111ll1llll1_opy_():
    return isinstance(os.getenv(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬᲧ")), str)
def bstack1ll11111ll_opy_(url):
    return urlparse(url).hostname
def bstack11ll11l11l_opy_(hostname):
    for bstack1llll11ll1_opy_ in bstack1l1l111ll_opy_:
        regex = re.compile(bstack1llll11ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l111l1l11_opy_(bstack11l11ll1111_opy_, file_name, logger):
    bstack1l1lll1111_opy_ = os.path.join(os.path.expanduser(bstack11l1_opy_ (u"ࠧࡿࠩᲨ")), bstack11l11ll1111_opy_)
    try:
        if not os.path.exists(bstack1l1lll1111_opy_):
            os.makedirs(bstack1l1lll1111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1_opy_ (u"ࠨࢀࠪᲩ")), bstack11l11ll1111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1_opy_ (u"ࠩࡺࠫᲪ")):
                pass
            with open(file_path, bstack11l1_opy_ (u"ࠥࡻ࠰ࠨᲫ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll111111_opy_.format(str(e)))
def bstack11l11l1l11l_opy_(file_name, key, value, logger):
    file_path = bstack11l111l1l11_opy_(bstack11l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᲬ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l111l1l1l_opy_ = json.load(open(file_path, bstack11l1_opy_ (u"ࠬࡸࡢࠨᲭ")))
        else:
            bstack1l111l1l1l_opy_ = {}
        bstack1l111l1l1l_opy_[key] = value
        with open(file_path, bstack11l1_opy_ (u"ࠨࡷࠬࠤᲮ")) as outfile:
            json.dump(bstack1l111l1l1l_opy_, outfile)
def bstack11lll11ll1_opy_(file_name, logger):
    file_path = bstack11l111l1l11_opy_(bstack11l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᲯ"), file_name, logger)
    bstack1l111l1l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1_opy_ (u"ࠨࡴࠪᲰ")) as bstack1llllll1l_opy_:
            bstack1l111l1l1l_opy_ = json.load(bstack1llllll1l_opy_)
    return bstack1l111l1l1l_opy_
def bstack1l11lllll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭Ჱ") + file_path + bstack11l1_opy_ (u"ࠪࠤࠬᲲ") + str(e))
def bstack1lll1l111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨᲳ")
def bstack11lll1111_opy_(config):
    if bstack11l1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᲴ") in config:
        del (config[bstack11l1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᲵ")])
        return False
    if bstack1lll1l111_opy_() < version.parse(bstack11l1_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭Ჶ")):
        return False
    if bstack1lll1l111_opy_() >= version.parse(bstack11l1_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧᲷ")):
        return True
    if bstack11l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᲸ") in config and config[bstack11l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᲹ")] is False:
        return False
    else:
        return True
def bstack1lllllll11_opy_(args_list, bstack11l1111111l_opy_):
    index = -1
    for value in bstack11l1111111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1ll1ll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1ll1ll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll11ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll11ll1_opy_ = bstack111ll11ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᲺ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᲻"), exception=exception)
    def bstack11111l111l_opy_(self):
        if self.result != bstack11l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᲼"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᲽ") in self.exception_type:
            return bstack11l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᲾ")
        return bstack11l1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᲿ")
    def bstack11l11l11lll_opy_(self):
        if self.result != bstack11l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᳀"):
            return None
        if self.bstack111ll11ll1_opy_:
            return self.bstack111ll11ll1_opy_
        return bstack111lll1ll11_opy_(self.exception)
def bstack111lll1ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l1111ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll11l11ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lll1l1ll_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1ll1l_opy_ = playwright.__file__
        bstack11l11ll11l1_opy_ = os.path.split(bstack11l11l1ll1l_opy_)
        bstack111llll111l_opy_ = bstack11l11ll11l1_opy_[0] + bstack11l1_opy_ (u"ࠫ࠴ࡪࡲࡪࡸࡨࡶ࠴ࡶࡡࡤ࡭ࡤ࡫ࡪ࠵࡬ࡪࡤ࠲ࡧࡱ࡯࠯ࡤ࡮࡬࠲࡯ࡹࠧ᳁")
        os.environ[bstack11l1_opy_ (u"ࠬࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠨ᳂")] = bstack1ll1l1111_opy_(config)
        with open(bstack111llll111l_opy_, bstack11l1_opy_ (u"࠭ࡲࠨ᳃")) as f:
            bstack11ll111lll_opy_ = f.read()
            bstack111lll1l111_opy_ = bstack11l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭᳄")
            bstack111ll1l1lll_opy_ = bstack11ll111lll_opy_.find(bstack111lll1l111_opy_)
            if bstack111ll1l1lll_opy_ == -1:
              process = subprocess.Popen(bstack11l1_opy_ (u"ࠣࡰࡳࡱࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠧ᳅"), shell=True, cwd=bstack11l11ll11l1_opy_[0])
              process.wait()
              bstack111lll111l1_opy_ = bstack11l1_opy_ (u"ࠩࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺࠢ࠼ࠩ᳆")
              bstack11l11llllll_opy_ = bstack11l1_opy_ (u"ࠥࠦࠧࠦ࡜ࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࡡࠨ࠻ࠡࡥࡲࡲࡸࡺࠠࡼࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴࠥࢃࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪ࠭ࡀࠦࡩࡧࠢࠫࡴࡷࡵࡣࡦࡵࡶ࠲ࡪࡴࡶ࠯ࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜࠭ࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠩࠫ࠾ࠤࠧࠨࠢ᳇")
              bstack111lll11ll1_opy_ = bstack11ll111lll_opy_.replace(bstack111lll111l1_opy_, bstack11l11llllll_opy_)
              with open(bstack111llll111l_opy_, bstack11l1_opy_ (u"ࠫࡼ࠭᳈")) as f:
                f.write(bstack111lll11ll1_opy_)
    except Exception as e:
        logger.error(bstack111l11111_opy_.format(str(e)))
def bstack11lll1ll1_opy_():
  try:
    bstack11l11ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲ࠮࡫ࡵࡲࡲࠬ᳉"))
    bstack111lll1l11l_opy_ = []
    if os.path.exists(bstack11l11ll1ll1_opy_):
      with open(bstack11l11ll1ll1_opy_) as f:
        bstack111lll1l11l_opy_ = json.load(f)
      os.remove(bstack11l11ll1ll1_opy_)
    return bstack111lll1l11l_opy_
  except:
    pass
  return []
def bstack1ll111l1ll_opy_(bstack1l1lll11_opy_):
  try:
    bstack111lll1l11l_opy_ = []
    bstack11l11ll1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭᳊"))
    if os.path.exists(bstack11l11ll1ll1_opy_):
      with open(bstack11l11ll1ll1_opy_) as f:
        bstack111lll1l11l_opy_ = json.load(f)
    bstack111lll1l11l_opy_.append(bstack1l1lll11_opy_)
    with open(bstack11l11ll1ll1_opy_, bstack11l1_opy_ (u"ࠧࡸࠩ᳋")) as f:
        json.dump(bstack111lll1l11l_opy_, f)
  except:
    pass
def bstack111111ll1_opy_(logger, bstack111lll11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ᳌"), bstack11l1_opy_ (u"ࠩࠪ᳍"))
    if test_name == bstack11l1_opy_ (u"ࠪࠫ᳎"):
        test_name = threading.current_thread().__dict__.get(bstack11l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡆࡩࡪ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠪ᳏"), bstack11l1_opy_ (u"ࠬ࠭᳐"))
    bstack111llll11ll_opy_ = bstack11l1_opy_ (u"࠭ࠬࠡࠩ᳑").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111lll11lll_opy_:
        bstack111111lll_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᳒"), bstack11l1_opy_ (u"ࠨ࠲ࠪ᳓"))
        bstack1ll1l1llll_opy_ = {bstack11l1_opy_ (u"ࠩࡱࡥࡲ࡫᳔ࠧ"): test_name, bstack11l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ᳕ࠩ"): bstack111llll11ll_opy_, bstack11l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺ᳖ࠪ"): bstack111111lll_opy_}
        bstack11l111l1111_opy_ = []
        bstack11l1l111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱ᳗ࠫ"))
        if os.path.exists(bstack11l1l111l1l_opy_):
            with open(bstack11l1l111l1l_opy_) as f:
                bstack11l111l1111_opy_ = json.load(f)
        bstack11l111l1111_opy_.append(bstack1ll1l1llll_opy_)
        with open(bstack11l1l111l1l_opy_, bstack11l1_opy_ (u"࠭ࡷࠨ᳘")) as f:
            json.dump(bstack11l111l1111_opy_, f)
    else:
        bstack1ll1l1llll_opy_ = {bstack11l1_opy_ (u"ࠧ࡯ࡣࡰࡩ᳙ࠬ"): test_name, bstack11l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᳚"): bstack111llll11ll_opy_, bstack11l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᳛"): str(multiprocessing.current_process().name)}
        if bstack11l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ᳜ࠧ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1l1llll_opy_)
  except Exception as e:
      logger.warn(bstack11l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡰࡺࡶࡨࡷࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽ᳝ࠣ").format(e))
def bstack11l111ll11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧ࡯ࡳࡨࡱࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡣࡣࡶ࡭ࡨࠦࡦࡪ࡮ࡨࠤࡴࡶࡥࡳࡣࡷ࡭ࡴࡴࡳࠨ᳞"))
    try:
      bstack111lll1l1ll_opy_ = []
      bstack1ll1l1llll_opy_ = {bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨ᳟ࠫ"): test_name, bstack11l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᳠"): error_message, bstack11l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᳡"): index}
      bstack111lll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰ᳢ࠪ"))
      if os.path.exists(bstack111lll1l1l1_opy_):
          with open(bstack111lll1l1l1_opy_) as f:
              bstack111lll1l1ll_opy_ = json.load(f)
      bstack111lll1l1ll_opy_.append(bstack1ll1l1llll_opy_)
      with open(bstack111lll1l1l1_opy_, bstack11l1_opy_ (u"ࠪࡻ᳣ࠬ")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack11l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃ᳤ࠢ").format(e))
    return
  bstack111lll1l1ll_opy_ = []
  bstack1ll1l1llll_opy_ = {bstack11l1_opy_ (u"ࠬࡴࡡ࡮ࡧ᳥ࠪ"): test_name, bstack11l1_opy_ (u"࠭ࡥࡳࡴࡲࡶ᳦ࠬ"): error_message, bstack11l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ᳧࠭"): index}
  bstack111lll1l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯᳨ࠩ"))
  lock_file = bstack111lll1l1l1_opy_ + bstack11l1_opy_ (u"ࠩ࠱ࡰࡴࡩ࡫ࠨᳩ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111lll1l1l1_opy_):
          with open(bstack111lll1l1l1_opy_, bstack11l1_opy_ (u"ࠪࡶࠬᳪ")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1l1ll_opy_ = json.load(open(bstack111lll1l1l1_opy_))
      bstack111lll1l1ll_opy_.append(bstack1ll1l1llll_opy_)
      with open(bstack111lll1l1l1_opy_, bstack11l1_opy_ (u"ࠫࡼ࠭ᳫ")) as f:
          json.dump(bstack111lll1l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡩ࡭ࡱ࡫ࠠ࡭ࡱࡦ࡯࡮ࡴࡧ࠻ࠢࡾࢁࠧᳬ").format(e))
def bstack11llll11_opy_(bstack1l1l1ll11_opy_, name, logger):
  try:
    bstack1ll1l1llll_opy_ = {bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨ᳭ࠫ"): name, bstack11l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᳮ"): bstack1l1l1ll11_opy_, bstack11l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᳯ"): str(threading.current_thread()._name)}
    return bstack1ll1l1llll_opy_
  except Exception as e:
    logger.warn(bstack11l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᳰ").format(e))
  return
def bstack11l11l11l1l_opy_():
    return platform.system() == bstack11l1_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫᳱ")
def bstack111111l11_opy_(bstack111llllll11_opy_, config, logger):
    bstack111ll1lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111llllll11_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᳲ").format(e))
    return bstack111ll1lllll_opy_
def bstack11l11l1l111_opy_(bstack11l111ll1ll_opy_, bstack111lllll1ll_opy_):
    bstack11l1l111ll1_opy_ = version.parse(bstack11l111ll1ll_opy_)
    bstack11l11ll11ll_opy_ = version.parse(bstack111lllll1ll_opy_)
    if bstack11l1l111ll1_opy_ > bstack11l11ll11ll_opy_:
        return 1
    elif bstack11l1l111ll1_opy_ < bstack11l11ll11ll_opy_:
        return -1
    else:
        return 0
def bstack111l1ll11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111llll11l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l111lll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l11111ll_opy_(options, framework, config, bstack1llll1111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1_opy_ (u"ࠬ࡭ࡥࡵࠩᳳ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1111lll_opy_ = caps.get(bstack11l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᳴"))
    bstack11l111l11l1_opy_ = True
    bstack11l111llll_opy_ = os.environ[bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᳵ")]
    bstack1ll11l1l1ll_opy_ = config.get(bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᳶ"), False)
    if bstack1ll11l1l1ll_opy_:
        bstack1llll11ll11_opy_ = config.get(bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳷"), {})
        bstack1llll11ll11_opy_[bstack11l1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭᳸")] = os.getenv(bstack11l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᳹"))
        bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᳺ"), bstack11l1_opy_ (u"࠭ࡻࡾࠩ᳻"))).get(bstack11l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᳼"))
    if bstack111llllllll_opy_(caps.get(bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧ᳽"))) or bstack111llllllll_opy_(caps.get(bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ᳾"))):
        bstack11l111l11l1_opy_ = False
    if bstack11lll1111_opy_({bstack11l1_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ᳿"): bstack11l111l11l1_opy_}):
        bstack1l1111lll_opy_ = bstack1l1111lll_opy_ or {}
        bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᴀ")] = bstack11l1l111lll_opy_(framework)
        bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᴁ")] = bstack1l1ll111l1l_opy_()
        bstack1l1111lll_opy_[bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᴂ")] = bstack11l111llll_opy_
        bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᴃ")] = bstack1llll1111l_opy_
        if bstack1ll11l1l1ll_opy_:
            bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴄ")] = bstack1ll11l1l1ll_opy_
            bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴅ")] = bstack1llll11ll11_opy_
            bstack1l1111lll_opy_[bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᴆ")][bstack11l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᴇ")] = bstack11ll1l1ll11_opy_
        if getattr(options, bstack11l1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ᴈ"), None):
            options.set_capability(bstack11l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴉ"), bstack1l1111lll_opy_)
        else:
            options[bstack11l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᴊ")] = bstack1l1111lll_opy_
    else:
        if getattr(options, bstack11l1_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᴋ"), None):
            options.set_capability(bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᴌ"), bstack11l1l111lll_opy_(framework))
            options.set_capability(bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᴍ"), bstack1l1ll111l1l_opy_())
            options.set_capability(bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᴎ"), bstack11l111llll_opy_)
            options.set_capability(bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᴏ"), bstack1llll1111l_opy_)
            if bstack1ll11l1l1ll_opy_:
                options.set_capability(bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴐ"), bstack1ll11l1l1ll_opy_)
                options.set_capability(bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴑ"), bstack1llll11ll11_opy_)
                options.set_capability(bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ࠮ࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᴒ"), bstack11ll1l1ll11_opy_)
        else:
            options[bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᴓ")] = bstack11l1l111lll_opy_(framework)
            options[bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᴔ")] = bstack1l1ll111l1l_opy_()
            options[bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᴕ")] = bstack11l111llll_opy_
            options[bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᴖ")] = bstack1llll1111l_opy_
            if bstack1ll11l1l1ll_opy_:
                options[bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴗ")] = bstack1ll11l1l1ll_opy_
                options[bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴘ")] = bstack1llll11ll11_opy_
                options[bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᴙ")][bstack11l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᴚ")] = bstack11ll1l1ll11_opy_
    return options
def bstack11l1111l11l_opy_(bstack111lll11l1l_opy_, framework):
    bstack1llll1111l_opy_ = bstack1l1llll1l_opy_.get_property(bstack11l1_opy_ (u"ࠥࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡑࡔࡒࡈ࡚ࡉࡔࡠࡏࡄࡔࠧᴛ"))
    if bstack111lll11l1l_opy_ and len(bstack111lll11l1l_opy_.split(bstack11l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᴜ"))) > 1:
        ws_url = bstack111lll11l1l_opy_.split(bstack11l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᴝ"))[0]
        if bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᴞ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l111l1ll1_opy_ = json.loads(urllib.parse.unquote(bstack111lll11l1l_opy_.split(bstack11l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᴟ"))[1]))
            bstack11l111l1ll1_opy_ = bstack11l111l1ll1_opy_ or {}
            bstack11l111llll_opy_ = os.environ[bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᴠ")]
            bstack11l111l1ll1_opy_[bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᴡ")] = str(framework) + str(__version__)
            bstack11l111l1ll1_opy_[bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᴢ")] = bstack1l1ll111l1l_opy_()
            bstack11l111l1ll1_opy_[bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᴣ")] = bstack11l111llll_opy_
            bstack11l111l1ll1_opy_[bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᴤ")] = bstack1llll1111l_opy_
            bstack111lll11l1l_opy_ = bstack111lll11l1l_opy_.split(bstack11l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᴥ"))[0] + bstack11l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᴦ") + urllib.parse.quote(json.dumps(bstack11l111l1ll1_opy_))
    return bstack111lll11l1l_opy_
def bstack11llll1ll1_opy_():
    global bstack1ll1l1lll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1l1lll_opy_ = BrowserType.connect
    return bstack1ll1l1lll_opy_
def bstack1ll1l11l1_opy_(framework_name):
    global bstack1l111l1111_opy_
    bstack1l111l1111_opy_ = framework_name
    return framework_name
def bstack11ll1l1l11_opy_(self, *args, **kwargs):
    global bstack1ll1l1lll_opy_
    try:
        global bstack1l111l1111_opy_
        if bstack11l1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᴧ") in kwargs:
            kwargs[bstack11l1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᴨ")] = bstack11l1111l11l_opy_(
                kwargs.get(bstack11l1_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᴩ"), None),
                bstack1l111l1111_opy_
            )
    except Exception as e:
        logger.error(bstack11l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᴪ").format(str(e)))
    return bstack1ll1l1lll_opy_(self, *args, **kwargs)
def bstack11l11ll111l_opy_(bstack11l111111ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll1lll11l_opy_(bstack11l111111ll_opy_, bstack11l1_opy_ (u"ࠧࠨᴫ"))
        if proxies and proxies.get(bstack11l1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᴬ")):
            parsed_url = urlparse(proxies.get(bstack11l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᴭ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᴮ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᴯ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᴰ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᴱ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1ll1l1_opy_(bstack11l111111ll_opy_):
    bstack11l11l11l11_opy_ = {
        bstack11l1ll1111l_opy_[bstack11l1111l1ll_opy_]: bstack11l111111ll_opy_[bstack11l1111l1ll_opy_]
        for bstack11l1111l1ll_opy_ in bstack11l111111ll_opy_
        if bstack11l1111l1ll_opy_ in bstack11l1ll1111l_opy_
    }
    bstack11l11l11l11_opy_[bstack11l1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᴲ")] = bstack11l11ll111l_opy_(bstack11l111111ll_opy_, bstack1l1llll1l_opy_.get_property(bstack11l1_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᴳ")))
    bstack11l11111l1l_opy_ = [element.lower() for element in bstack11l1lll111l_opy_]
    bstack111ll1ll111_opy_(bstack11l11l11l11_opy_, bstack11l11111l1l_opy_)
    return bstack11l11l11l11_opy_
def bstack111ll1ll111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᴴ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111ll1ll111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111ll1ll111_opy_(item, keys)
def bstack1l1llll1111_opy_():
    bstack111lll1llll_opy_ = [os.environ.get(bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡋࡏࡉࡘࡥࡄࡊࡔࠥᴵ")), os.path.join(os.path.expanduser(bstack11l1_opy_ (u"ࠤࢁࠦᴶ")), bstack11l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᴷ")), os.path.join(bstack11l1_opy_ (u"ࠫ࠴ࡺ࡭ࡱࠩᴸ"), bstack11l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᴹ"))]
    for path in bstack111lll1llll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᴺ") + str(path) + bstack11l1_opy_ (u"ࠢࠨࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥᴻ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1_opy_ (u"ࠣࡉ࡬ࡺ࡮ࡴࡧࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸࠦࡦࡰࡴࠣࠫࠧᴼ") + str(path) + bstack11l1_opy_ (u"ࠤࠪࠦᴽ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᴾ") + str(path) + bstack11l1_opy_ (u"ࠦࠬࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳ࠯ࠤᴿ"))
            else:
                logger.debug(bstack11l1_opy_ (u"ࠧࡉࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥ࠭ࠢᵀ") + str(path) + bstack11l1_opy_ (u"ࠨࠧࠡࡹ࡬ࡸ࡭ࠦࡷࡳ࡫ࡷࡩࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯࠰ࠥᵁ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1_opy_ (u"ࠢࡐࡲࡨࡶࡦࡺࡩࡰࡰࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩࠦࡦࡰࡴࠣࠫࠧᵂ") + str(path) + bstack11l1_opy_ (u"ࠣࠩ࠱ࠦᵃ"))
            return path
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡸࡴࠥ࡬ࡩ࡭ࡧࠣࠫࢀࡶࡡࡵࡪࢀࠫ࠿ࠦࠢᵄ") + str(e) + bstack11l1_opy_ (u"ࠥࠦᵅ"))
    logger.debug(bstack11l1_opy_ (u"ࠦࡆࡲ࡬ࠡࡲࡤࡸ࡭ࡹࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠣᵆ"))
    return None
@measure(event_name=EVENTS.bstack11ll1111l11_opy_, stage=STAGE.bstack11lll1l1_opy_)
def bstack1lll11l1lll_opy_(binary_path, bstack1ll1l1ll11l_opy_, bs_config):
    logger.debug(bstack11l1_opy_ (u"ࠧࡉࡵࡳࡴࡨࡲࡹࠦࡃࡍࡋࠣࡔࡦࡺࡨࠡࡨࡲࡹࡳࡪ࠺ࠡࡽࢀࠦᵇ").format(binary_path))
    bstack11l11111ll1_opy_ = bstack11l1_opy_ (u"࠭ࠧᵈ")
    bstack11l11111111_opy_ = {
        bstack11l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵉ"): __version__,
        bstack11l1_opy_ (u"ࠣࡱࡶࠦᵊ"): platform.system(),
        bstack11l1_opy_ (u"ࠤࡲࡷࡤࡧࡲࡤࡪࠥᵋ"): platform.machine(),
        bstack11l1_opy_ (u"ࠥࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᵌ"): bstack11l1_opy_ (u"ࠫ࠵࠭ᵍ"),
        bstack11l1_opy_ (u"ࠧࡹࡤ࡬ࡡ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠦᵎ"): bstack11l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᵏ")
    }
    bstack111lllllll1_opy_(bstack11l11111111_opy_)
    try:
        if binary_path:
            bstack11l11111111_opy_[bstack11l1_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵐ")] = subprocess.check_output([binary_path, bstack11l1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᵑ")]).strip().decode(bstack11l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᵒ"))
        response = requests.request(
            bstack11l1_opy_ (u"ࠪࡋࡊ࡚ࠧᵓ"),
            url=bstack1111l1l11_opy_(bstack11l1ll111l1_opy_),
            headers=None,
            auth=(bs_config[bstack11l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᵔ")], bs_config[bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᵕ")]),
            json=None,
            params=bstack11l11111111_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1_opy_ (u"࠭ࡵࡳ࡮ࠪᵖ") in data.keys() and bstack11l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᵗ") in data.keys():
            logger.debug(bstack11l1_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤᵘ").format(bstack11l11111111_opy_[bstack11l1_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᵙ")]))
            if bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭ᵚ") in os.environ:
                logger.debug(bstack11l1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢᵛ"))
                data[bstack11l1_opy_ (u"ࠬࡻࡲ࡭ࠩᵜ")] = os.environ[bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩᵝ")]
            bstack11l1111ll11_opy_ = bstack111llll1l1l_opy_(data[bstack11l1_opy_ (u"ࠧࡶࡴ࡯ࠫᵞ")], bstack1ll1l1ll11l_opy_)
            bstack11l11111ll1_opy_ = os.path.join(bstack1ll1l1ll11l_opy_, bstack11l1111ll11_opy_)
            os.chmod(bstack11l11111ll1_opy_, 0o777) # bstack11l1111lll1_opy_ permission
            return bstack11l11111ll1_opy_
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣᵟ").format(e))
    return binary_path
def bstack111lllllll1_opy_(bstack11l11111111_opy_):
    try:
        if bstack11l1_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨᵠ") not in bstack11l11111111_opy_[bstack11l1_opy_ (u"ࠪࡳࡸ࠭ᵡ")].lower():
            return
        if os.path.exists(bstack11l1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᵢ")):
            with open(bstack11l1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢᵣ"), bstack11l1_opy_ (u"ࠨࡲࠣᵤ")) as f:
                bstack11l111lll11_opy_ = {}
                for line in f:
                    if bstack11l1_opy_ (u"ࠢ࠾ࠤᵥ") in line:
                        key, value = line.rstrip().split(bstack11l1_opy_ (u"ࠣ࠿ࠥᵦ"), 1)
                        bstack11l111lll11_opy_[key] = value.strip(bstack11l1_opy_ (u"ࠩࠥࡠࠬ࠭ᵧ"))
                bstack11l11111111_opy_[bstack11l1_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪᵨ")] = bstack11l111lll11_opy_.get(bstack11l1_opy_ (u"ࠦࡎࡊࠢᵩ"), bstack11l1_opy_ (u"ࠧࠨᵪ"))
        elif os.path.exists(bstack11l1_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᵫ")):
            bstack11l11111111_opy_[bstack11l1_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᵬ")] = bstack11l1_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨᵭ")
    except Exception as e:
        logger.debug(bstack11l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦᵮ") + e)
@measure(event_name=EVENTS.bstack11l1ll1l1ll_opy_, stage=STAGE.bstack11lll1l1_opy_)
def bstack111llll1l1l_opy_(bstack11l111ll111_opy_, bstack111lllll11l_opy_):
    logger.debug(bstack11l1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧᵯ") + str(bstack11l111ll111_opy_) + bstack11l1_opy_ (u"ࠦࠧᵰ"))
    zip_path = os.path.join(bstack111lllll11l_opy_, bstack11l1_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦᵱ"))
    bstack11l1111ll11_opy_ = bstack11l1_opy_ (u"࠭ࠧᵲ")
    with requests.get(bstack11l111ll111_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1_opy_ (u"ࠢࡸࡤࠥᵳ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥᵴ"))
    with zipfile.ZipFile(zip_path, bstack11l1_opy_ (u"ࠩࡵࠫᵵ")) as zip_ref:
        bstack111lll11111_opy_ = zip_ref.namelist()
        if len(bstack111lll11111_opy_) > 0:
            bstack11l1111ll11_opy_ = bstack111lll11111_opy_[0] # bstack111lll1ll1l_opy_ bstack11l1ll1l111_opy_ will be bstack11l1111l111_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111lllll11l_opy_)
        logger.debug(bstack11l1_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤᵶ") + str(bstack111lllll11l_opy_) + bstack11l1_opy_ (u"ࠦࠬࠨᵷ"))
    os.remove(zip_path)
    return bstack11l1111ll11_opy_
def get_cli_dir():
    bstack11l11lll111_opy_ = bstack1l1llll1111_opy_()
    if bstack11l11lll111_opy_:
        bstack1ll1l1ll11l_opy_ = os.path.join(bstack11l11lll111_opy_, bstack11l1_opy_ (u"ࠧࡩ࡬ࡪࠤᵸ"))
        if not os.path.exists(bstack1ll1l1ll11l_opy_):
            os.makedirs(bstack1ll1l1ll11l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l1ll11l_opy_
    else:
        raise FileNotFoundError(bstack11l1_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤᵹ"))
def bstack1llll1l1111_opy_(bstack1ll1l1ll11l_opy_):
    bstack11l1_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦᵺ")
    bstack11l111ll1l1_opy_ = [
        os.path.join(bstack1ll1l1ll11l_opy_, f)
        for f in os.listdir(bstack1ll1l1ll11l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l1ll11l_opy_, f)) and f.startswith(bstack11l1_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤᵻ"))
    ]
    if len(bstack11l111ll1l1_opy_) > 0:
        return max(bstack11l111ll1l1_opy_, key=os.path.getmtime) # get bstack11l111llll1_opy_ binary
    return bstack11l1_opy_ (u"ࠤࠥᵼ")
def bstack11ll1ll1lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111ll1l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111ll1l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l111l11ll_opy_(data, keys, default=None):
    bstack11l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᵽ")
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