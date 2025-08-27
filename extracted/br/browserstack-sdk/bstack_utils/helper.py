# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
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
from bstack_utils.constants import (bstack11lll1ll11_opy_, bstack1llll11ll_opy_, bstack11l1ll1l1_opy_,
                                    bstack11l1lll1111_opy_, bstack11ll1111111_opy_, bstack11l1lll1lll_opy_, bstack11l1ll1l111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l111l111_opy_, bstack1l1lll11_opy_
from bstack_utils.proxy import bstack1lll1llll1_opy_, bstack1llll1ll1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1l11111_opy_
from bstack_utils.bstack1l111l1ll1_opy_ import bstack1ll11l11l1_opy_
from browserstack_sdk._version import __version__
bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
logger = bstack1l1l11111_opy_.get_logger(__name__, bstack1l1l11111_opy_.bstack1lll11l111l_opy_())
def bstack11ll11llll1_opy_(config):
    return config[bstack1111lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᫽")]
def bstack11ll1l1l11l_opy_(config):
    return config[bstack1111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᫾")]
def bstack1l1lllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l111ll1l1_opy_(obj):
    values = []
    bstack11l1111111l_opy_ = re.compile(bstack1111lll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ᫿"), re.I)
    for key in obj.keys():
        if bstack11l1111111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111ll1llll1_opy_(config):
    tags = []
    tags.extend(bstack11l111ll1l1_opy_(os.environ))
    tags.extend(bstack11l111ll1l1_opy_(config))
    return tags
def bstack11l11ll1111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11111lll_opy_(bstack11l1111l111_opy_):
    if not bstack11l1111l111_opy_:
        return bstack1111lll_opy_ (u"ࠪࠫᬀ")
    return bstack1111lll_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᬁ").format(bstack11l1111l111_opy_.name, bstack11l1111l111_opy_.email)
def bstack11ll1ll1lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111l1ll1_opy_ = repo.common_dir
        info = {
            bstack1111lll_opy_ (u"ࠧࡹࡨࡢࠤᬂ"): repo.head.commit.hexsha,
            bstack1111lll_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᬃ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111lll_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᬄ"): repo.active_branch.name,
            bstack1111lll_opy_ (u"ࠣࡶࡤ࡫ࠧᬅ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111lll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᬆ"): bstack11l11111lll_opy_(repo.head.commit.committer),
            bstack1111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᬇ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111lll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᬈ"): bstack11l11111lll_opy_(repo.head.commit.author),
            bstack1111lll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᬉ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111lll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᬊ"): repo.head.commit.message,
            bstack1111lll_opy_ (u"ࠢࡳࡱࡲࡸࠧᬋ"): repo.git.rev_parse(bstack1111lll_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᬌ")),
            bstack1111lll_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᬍ"): bstack11l111l1ll1_opy_,
            bstack1111lll_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᬎ"): subprocess.check_output([bstack1111lll_opy_ (u"ࠦ࡬࡯ࡴࠣᬏ"), bstack1111lll_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᬐ"), bstack1111lll_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᬑ")]).strip().decode(
                bstack1111lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬒ")),
            bstack1111lll_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᬓ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111lll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᬔ"): repo.git.rev_list(
                bstack1111lll_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᬕ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l11l11lll_opy_ = []
        for remote in remotes:
            bstack111lllll11l_opy_ = {
                bstack1111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬖ"): remote.name,
                bstack1111lll_opy_ (u"ࠧࡻࡲ࡭ࠤᬗ"): remote.url,
            }
            bstack11l11l11lll_opy_.append(bstack111lllll11l_opy_)
        bstack111lll1llll_opy_ = {
            bstack1111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬘ"): bstack1111lll_opy_ (u"ࠢࡨ࡫ࡷࠦᬙ"),
            **info,
            bstack1111lll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᬚ"): bstack11l11l11lll_opy_
        }
        bstack111lll1llll_opy_ = bstack11l111ll11l_opy_(bstack111lll1llll_opy_)
        return bstack111lll1llll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᬛ").format(err))
        return {}
def bstack11l11ll1lll_opy_(bstack11l1l111l1l_opy_=None):
    bstack1111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡵࡧࡴࡩࡵࠣࡸࡴࠦࡥࡹࡶࡵࡥࡨࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡳࡱࡰ࠲ࠥࡊࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡩ࡯ࡣࡵࡵ࠯ࠤࡪࡧࡣࡩࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡤࠤ࡫ࡵ࡬ࡥࡧࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᬜ")
    if not bstack11l1l111l1l_opy_: # bstack111llllllll_opy_ for bstack11l111111l1_opy_-repo
        bstack11l1l111l1l_opy_ = [os.getcwd()]
    results = []
    for folder in bstack11l1l111l1l_opy_:
        try:
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1111lll_opy_ (u"ࠦࡵࡸࡉࡥࠤᬝ"): bstack1111lll_opy_ (u"ࠧࠨᬞ"),
                bstack1111lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᬟ"): [],
                bstack1111lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬠ"): [],
                bstack1111lll_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᬡ"): bstack1111lll_opy_ (u"ࠤࠥᬢ"),
                bstack1111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᬣ"): [],
                bstack1111lll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᬤ"): bstack1111lll_opy_ (u"ࠧࠨᬥ"),
                bstack1111lll_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᬦ"): bstack1111lll_opy_ (u"ࠢࠣᬧ"),
                bstack1111lll_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦᬨ"): bstack1111lll_opy_ (u"ࠤࠥᬩ")
            }
            bstack111ll1ll1l1_opy_ = repo.active_branch.name
            bstack11l111l1111_opy_ = repo.head.commit
            result[bstack1111lll_opy_ (u"ࠥࡴࡷࡏࡤࠣᬪ")] = bstack11l111l1111_opy_.hexsha
            bstack11l11lll111_opy_ = _11l111l1l1l_opy_(repo)
            logger.debug(bstack1111lll_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᬫ") + str(bstack11l11lll111_opy_) + bstack1111lll_opy_ (u"ࠧࠨᬬ"))
            if bstack11l11lll111_opy_:
                try:
                    bstack111ll1lll1l_opy_ = repo.git.diff(bstack1111lll_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᬭ"), bstack1llll1l1ll1_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᬮ")).split(bstack1111lll_opy_ (u"ࠨ࡞ࡱࠫᬯ"))
                    logger.debug(bstack1111lll_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᬰ") + str(bstack111ll1lll1l_opy_) + bstack1111lll_opy_ (u"ࠥࠦᬱ"))
                    result[bstack1111lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᬲ")] = [f.strip() for f in bstack111ll1lll1l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1llll1l1ll1_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᬳ")))
                except Exception:
                    logger.debug(bstack1111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨ᬴"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1111lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᬵ")] = _11l1l1111l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1111lll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᬶ")] = _11l1l1111l1_opy_(commits[:5])
            bstack111llll1lll_opy_ = set()
            bstack111lll11ll1_opy_ = []
            for commit in commits:
                logger.debug(bstack1111lll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᬷ") + str(commit.message) + bstack1111lll_opy_ (u"ࠥࠦᬸ"))
                bstack11l11ll1ll1_opy_ = commit.author.name if commit.author else bstack1111lll_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᬹ")
                bstack111llll1lll_opy_.add(bstack11l11ll1ll1_opy_)
                bstack111lll11ll1_opy_.append({
                    bstack1111lll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᬺ"): commit.message.strip(),
                    bstack1111lll_opy_ (u"ࠨࡵࡴࡧࡵࠦᬻ"): bstack11l11ll1ll1_opy_
                })
            result[bstack1111lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᬼ")] = list(bstack111llll1lll_opy_)
            result[bstack1111lll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᬽ")] = bstack111lll11ll1_opy_
            result[bstack1111lll_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᬾ")] = bstack11l111l1111_opy_.committed_datetime.strftime(bstack1111lll_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᬿ"))
            if (not result[bstack1111lll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᭀ")] or result[bstack1111lll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᭁ")].strip() == bstack1111lll_opy_ (u"ࠨࠢᭂ")) and bstack11l111l1111_opy_.message:
                bstack111lll1ll1l_opy_ = bstack11l111l1111_opy_.message.strip().splitlines()
                result[bstack1111lll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᭃ")] = bstack111lll1ll1l_opy_[0] if bstack111lll1ll1l_opy_ else bstack1111lll_opy_ (u"ࠣࠤ᭄")
                if len(bstack111lll1ll1l_opy_) > 2:
                    result[bstack1111lll_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᭅ")] = bstack1111lll_opy_ (u"ࠪࡠࡳ࠭ᭆ").join(bstack111lll1ll1l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀ࡬࡯࡭ࡦࡨࡶࢂ࠯࠺ࠡࠤᭇ") + str(err) + bstack1111lll_opy_ (u"ࠧࠨᭈ"))
    filtered_results = [
        r
        for r in results
        if _11l11111l11_opy_(r)
    ]
    return filtered_results
def _11l11111l11_opy_(result):
    bstack1111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡦ࡮ࡳࡩࡷࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡴࡷ࡯ࡸࠥ࡯ࡳࠡࡸࡤࡰ࡮ࡪࠠࠩࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠤ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠣࡥࡳࡪࠠࡢࡷࡷ࡬ࡴࡸࡳࠪ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᭉ")
    return (
        isinstance(result.get(bstack1111lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᭊ"), None), list)
        and len(result[bstack1111lll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᭋ")]) > 0
        and isinstance(result.get(bstack1111lll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᭌ"), None), list)
        and len(result[bstack1111lll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ᭍")]) > 0
    )
def _11l111l1l1l_opy_(repo):
    bstack1111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤ࡙ࡸࡹࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡪࡨࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡵࡩࡵࡵࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡪࡤࡶࡩࡩ࡯ࡥࡧࡧࠤࡳࡧ࡭ࡦࡵࠣࡥࡳࡪࠠࡸࡱࡵ࡯ࠥࡽࡩࡵࡪࠣࡥࡱࡲࠠࡗࡅࡖࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡷࡹ࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡮࡬ࠠࡱࡱࡶࡷ࡮ࡨ࡬ࡦ࠮ࠣࡩࡱࡹࡥࠡࡐࡲࡲࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ᭎")
    try:
        try:
            origin = repo.remotes.origin
            bstack111ll1lllll_opy_ = origin.refs[bstack1111lll_opy_ (u"ࠬࡎࡅࡂࡆࠪ᭏")]
            target = bstack111ll1lllll_opy_.reference.name
            if target.startswith(bstack1111lll_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧ᭐")):
                return target
        except Exception:
            pass
        if repo.heads:
            return repo.heads[0].name
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1111lll_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨ᭑")):
                    return ref.name
    except Exception:
        pass
    return None
def _11l1l1111l1_opy_(commits):
    bstack1111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡦࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ᭒")
    bstack111ll1lll1l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111ll1ll1ll_opy_ in diff:
                        if bstack111ll1ll1ll_opy_.a_path:
                            bstack111ll1lll1l_opy_.add(bstack111ll1ll1ll_opy_.a_path)
                        if bstack111ll1ll1ll_opy_.b_path:
                            bstack111ll1lll1l_opy_.add(bstack111ll1ll1ll_opy_.b_path)
    except Exception:
        pass
    return list(bstack111ll1lll1l_opy_)
def bstack11l111ll11l_opy_(bstack111lll1llll_opy_):
    bstack111lllllll1_opy_ = bstack11l11l1l1ll_opy_(bstack111lll1llll_opy_)
    if bstack111lllllll1_opy_ and bstack111lllllll1_opy_ > bstack11l1lll1111_opy_:
        bstack11l11l1l1l1_opy_ = bstack111lllllll1_opy_ - bstack11l1lll1111_opy_
        bstack11l11llll1l_opy_ = bstack11l111lllll_opy_(bstack111lll1llll_opy_[bstack1111lll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ᭓")], bstack11l11l1l1l1_opy_)
        bstack111lll1llll_opy_[bstack1111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ᭔")] = bstack11l11llll1l_opy_
        logger.info(bstack1111lll_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨ᭕")
                    .format(bstack11l11l1l1ll_opy_(bstack111lll1llll_opy_) / 1024))
    return bstack111lll1llll_opy_
def bstack11l11l1l1ll_opy_(bstack11l111ll11_opy_):
    try:
        if bstack11l111ll11_opy_:
            bstack11l111ll1ll_opy_ = json.dumps(bstack11l111ll11_opy_)
            bstack11l11lll1l1_opy_ = sys.getsizeof(bstack11l111ll1ll_opy_)
            return bstack11l11lll1l1_opy_
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧ᭖").format(e))
    return -1
def bstack11l111lllll_opy_(field, bstack11l111l1lll_opy_):
    try:
        bstack11l11l1ll11_opy_ = len(bytes(bstack11ll1111111_opy_, bstack1111lll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᭗")))
        bstack111lll1111l_opy_ = bytes(field, bstack1111lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᭘"))
        bstack11l11ll1l1l_opy_ = len(bstack111lll1111l_opy_)
        bstack11l1l111111_opy_ = ceil(bstack11l11ll1l1l_opy_ - bstack11l111l1lll_opy_ - bstack11l11l1ll11_opy_)
        if bstack11l1l111111_opy_ > 0:
            bstack111lll11111_opy_ = bstack111lll1111l_opy_[:bstack11l1l111111_opy_].decode(bstack1111lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᭙"), errors=bstack1111lll_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩ᭚")) + bstack11ll1111111_opy_
            return bstack111lll11111_opy_
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣ᭛").format(e))
    return field
def bstack1l111ll11l_opy_():
    env = os.environ
    if (bstack1111lll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ᭜") in env and len(env[bstack1111lll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ᭝")]) > 0) or (
            bstack1111lll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ᭞") in env and len(env[bstack1111lll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ᭟")]) > 0):
        return {
            bstack1111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭠"): bstack1111lll_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥ᭡"),
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭢"): env.get(bstack1111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ᭣")),
            bstack1111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭤"): env.get(bstack1111lll_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ᭥")),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᭦"): env.get(bstack1111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᭧"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠤࡆࡍࠧ᭨")) == bstack1111lll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᭩") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨ᭪"))):
        return {
            bstack1111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᭫"): bstack1111lll_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉ᭬ࠣ"),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᭭"): env.get(bstack1111lll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᭮")),
            bstack1111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᭯"): env.get(bstack1111lll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢ᭰")),
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᭱"): env.get(bstack1111lll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣ᭲"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠨࡃࡊࠤ᭳")) == bstack1111lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ᭴") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣ᭵"))):
        return {
            bstack1111lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭶"): bstack1111lll_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨ᭷"),
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭸"): env.get(bstack1111lll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧ᭹")),
            bstack1111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᭺"): env.get(bstack1111lll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᭻")),
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭼"): env.get(bstack1111lll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᭽"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠥࡇࡎࠨ᭾")) == bstack1111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᭿") and env.get(bstack1111lll_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᮀ")) == bstack1111lll_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᮁ"):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮂ"): bstack1111lll_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᮃ"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮄ"): None,
            bstack1111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮅ"): None,
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮆ"): None
        }
    if env.get(bstack1111lll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᮇ")) and env.get(bstack1111lll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᮈ")):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮉ"): bstack1111lll_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᮊ"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮋ"): env.get(bstack1111lll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᮌ")),
            bstack1111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮍ"): None,
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮎ"): env.get(bstack1111lll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᮏ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠢࡄࡋࠥᮐ")) == bstack1111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᮑ") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᮒ"))):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᮓ"): bstack1111lll_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᮔ"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮕ"): env.get(bstack1111lll_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᮖ")),
            bstack1111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮗ"): None,
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮘ"): env.get(bstack1111lll_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᮙ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠥࡇࡎࠨᮚ")) == bstack1111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤᮛ") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᮜ"))):
        return {
            bstack1111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᮝ"): bstack1111lll_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᮞ"),
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᮟ"): env.get(bstack1111lll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᮠ")),
            bstack1111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮡ"): env.get(bstack1111lll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᮢ")),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮣ"): env.get(bstack1111lll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᮤ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠢࡄࡋࠥᮥ")) == bstack1111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᮦ") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᮧ"))):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᮨ"): bstack1111lll_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᮩ"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᮪ࠣ"): env.get(bstack1111lll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎ᮫ࠥ")),
            bstack1111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮬ"): env.get(bstack1111lll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᮭ")),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮮ"): env.get(bstack1111lll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᮯ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠦࡈࡏࠢ᮰")) == bstack1111lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᮱") and bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ᮲"))):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᮳"): bstack1111lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ᮴"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᮵"): env.get(bstack1111lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᮶")),
            bstack1111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᮷"): env.get(bstack1111lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ᮸")) or env.get(bstack1111lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᮹")),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮺ"): env.get(bstack1111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᮻ"))
        }
    if bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᮼ"))):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᮽ"): bstack1111lll_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᮾ"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮿ"): bstack1111lll_opy_ (u"ࠨࡻࡾࡽࢀࠦᯀ").format(env.get(bstack1111lll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᯁ")), env.get(bstack1111lll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᯂ"))),
            bstack1111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᯃ"): env.get(bstack1111lll_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᯄ")),
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯅ"): env.get(bstack1111lll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᯆ"))
        }
    if bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᯇ"))):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᯈ"): bstack1111lll_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᯉ"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᯊ"): bstack1111lll_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᯋ").format(env.get(bstack1111lll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᯌ")), env.get(bstack1111lll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᯍ")), env.get(bstack1111lll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᯎ")), env.get(bstack1111lll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᯏ"))),
            bstack1111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᯐ"): env.get(bstack1111lll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᯑ")),
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᯒ"): env.get(bstack1111lll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᯓ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᯔ")) and env.get(bstack1111lll_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᯕ")):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᯖ"): bstack1111lll_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᯗ"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᯘ"): bstack1111lll_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᯙ").format(env.get(bstack1111lll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᯚ")), env.get(bstack1111lll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᯛ")), env.get(bstack1111lll_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᯜ"))),
            bstack1111lll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯝ"): env.get(bstack1111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᯞ")),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯟ"): env.get(bstack1111lll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᯠ"))
        }
    if any([env.get(bstack1111lll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᯡ")), env.get(bstack1111lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᯢ")), env.get(bstack1111lll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᯣ"))]):
        return {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᯤ"): bstack1111lll_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᯥ"),
            bstack1111lll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰ᯦ࠧ"): env.get(bstack1111lll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᯧ")),
            bstack1111lll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯨ"): env.get(bstack1111lll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᯩ")),
            bstack1111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯪ"): env.get(bstack1111lll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᯫ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᯬ")):
        return {
            bstack1111lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᯭ"): bstack1111lll_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᯮ"),
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᯯ"): env.get(bstack1111lll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᯰ")),
            bstack1111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯱ"): env.get(bstack1111lll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨ᯲")),
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ᯳ࠢ"): env.get(bstack1111lll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ᯴"))
        }
    if env.get(bstack1111lll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦ᯵")) or env.get(bstack1111lll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᯶")):
        return {
            bstack1111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᯷"): bstack1111lll_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ᯸"),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᯹"): env.get(bstack1111lll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᯺")),
            bstack1111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᯻"): bstack1111lll_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ᯼") if env.get(bstack1111lll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ᯽")) else None,
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᯾"): env.get(bstack1111lll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ᯿"))
        }
    if any([env.get(bstack1111lll_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᰀ")), env.get(bstack1111lll_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᰁ")), env.get(bstack1111lll_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᰂ"))]):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᰃ"): bstack1111lll_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᰄ"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰅ"): None,
            bstack1111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᰆ"): env.get(bstack1111lll_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᰇ")),
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰈ"): env.get(bstack1111lll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᰉ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᰊ")):
        return {
            bstack1111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰋ"): bstack1111lll_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᰌ"),
            bstack1111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰍ"): env.get(bstack1111lll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᰎ")),
            bstack1111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᰏ"): bstack1111lll_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᰐ").format(env.get(bstack1111lll_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᰑ"))) if env.get(bstack1111lll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᰒ")) else None,
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰓ"): env.get(bstack1111lll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᰔ"))
        }
    if bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᰕ"))):
        return {
            bstack1111lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᰖ"): bstack1111lll_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥᰗ"),
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᰘ"): env.get(bstack1111lll_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣᰙ")),
            bstack1111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᰚ"): env.get(bstack1111lll_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤᰛ")),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᰜ"): env.get(bstack1111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᰝ"))
        }
    if bstack11lll1111_opy_(env.get(bstack1111lll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥᰞ"))):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᰟ"): bstack1111lll_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧᰠ"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᰡ"): bstack1111lll_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢᰢ").format(env.get(bstack1111lll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫᰣ")), env.get(bstack1111lll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬᰤ")), env.get(bstack1111lll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩᰥ"))),
            bstack1111lll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᰦ"): env.get(bstack1111lll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨᰧ")),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᰨ"): env.get(bstack1111lll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨᰩ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠢࡄࡋࠥᰪ")) == bstack1111lll_opy_ (u"ࠣࡶࡵࡹࡪࠨᰫ") and env.get(bstack1111lll_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤᰬ")) == bstack1111lll_opy_ (u"ࠥ࠵ࠧᰭ"):
        return {
            bstack1111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰮ"): bstack1111lll_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧᰯ"),
            bstack1111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰰ"): bstack1111lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥᰱ").format(env.get(bstack1111lll_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬᰲ"))),
            bstack1111lll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰳ"): None,
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᰴ"): None,
        }
    if env.get(bstack1111lll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢᰵ")):
        return {
            bstack1111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰶ"): bstack1111lll_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹ᰷ࠣ"),
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᰸"): None,
            bstack1111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᰹"): env.get(bstack1111lll_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ᰺")),
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᰻"): env.get(bstack1111lll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᰼"))
        }
    if any([env.get(bstack1111lll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣ᰽")), env.get(bstack1111lll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ᰾")), env.get(bstack1111lll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧ᰿")), env.get(bstack1111lll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤ᱀"))]):
        return {
            bstack1111lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᱁"): bstack1111lll_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ᱂"),
            bstack1111lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᱃"): None,
            bstack1111lll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᱄"): env.get(bstack1111lll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᱅")) or None,
            bstack1111lll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᱆"): env.get(bstack1111lll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᱇"), 0)
        }
    if env.get(bstack1111lll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᱈")):
        return {
            bstack1111lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᱉"): bstack1111lll_opy_ (u"ࠦࡌࡵࡃࡅࠤ᱊"),
            bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᱋"): None,
            bstack1111lll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᱌"): env.get(bstack1111lll_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᱍ")),
            bstack1111lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱎ"): env.get(bstack1111lll_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣᱏ"))
        }
    if env.get(bstack1111lll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᱐")):
        return {
            bstack1111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᱑"): bstack1111lll_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ᱒"),
            bstack1111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᱓"): env.get(bstack1111lll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᱔")),
            bstack1111lll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᱕"): env.get(bstack1111lll_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ᱖")),
            bstack1111lll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᱗"): env.get(bstack1111lll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᱘"))
        }
    return {bstack1111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱙"): None}
def get_host_info():
    return {
        bstack1111lll_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣᱚ"): platform.node(),
        bstack1111lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤᱛ"): platform.system(),
        bstack1111lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᱜ"): platform.machine(),
        bstack1111lll_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᱝ"): platform.version(),
        bstack1111lll_opy_ (u"ࠥࡥࡷࡩࡨࠣᱞ"): platform.architecture()[0]
    }
def bstack11l11ll111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll1l1l11_opy_():
    if bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᱟ")):
        return bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᱠ")
    return bstack1111lll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬᱡ")
def bstack11l11l11l11_opy_(driver):
    info = {
        bstack1111lll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᱢ"): driver.capabilities,
        bstack1111lll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᱣ"): driver.session_id,
        bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᱤ"): driver.capabilities.get(bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᱥ"), None),
        bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᱦ"): driver.capabilities.get(bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᱧ"), None),
        bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᱨ"): driver.capabilities.get(bstack1111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᱩ"), None),
        bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫᱪ"):driver.capabilities.get(bstack1111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᱫ"), None),
    }
    if bstack111ll1l1l11_opy_() == bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᱬ"):
        if bstack11111l11_opy_():
            info[bstack1111lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᱭ")] = bstack1111lll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᱮ")
        elif driver.capabilities.get(bstack1111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᱯ"), {}).get(bstack1111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᱰ"), False):
            info[bstack1111lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᱱ")] = bstack1111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᱲ")
        else:
            info[bstack1111lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᱳ")] = bstack1111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᱴ")
    return info
def bstack11111l11_opy_():
    if bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᱵ")):
        return True
    if bstack11lll1111_opy_(os.environ.get(bstack1111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᱶ"), None)):
        return True
    return False
def bstack1l11l1l1_opy_(bstack111llll11l1_opy_, url, data, config):
    headers = config.get(bstack1111lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᱷ"), None)
    proxies = bstack1lll1llll1_opy_(config, url)
    auth = config.get(bstack1111lll_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᱸ"), None)
    response = requests.request(
            bstack111llll11l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lllll1ll_opy_(bstack11llll1l1l_opy_, size):
    bstack1l111llll_opy_ = []
    while len(bstack11llll1l1l_opy_) > size:
        bstack11llllll1l_opy_ = bstack11llll1l1l_opy_[:size]
        bstack1l111llll_opy_.append(bstack11llllll1l_opy_)
        bstack11llll1l1l_opy_ = bstack11llll1l1l_opy_[size:]
    bstack1l111llll_opy_.append(bstack11llll1l1l_opy_)
    return bstack1l111llll_opy_
def bstack111ll1l1ll1_opy_(message, bstack11l111lll1l_opy_=False):
    os.write(1, bytes(message, bstack1111lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᱹ")))
    os.write(1, bytes(bstack1111lll_opy_ (u"ࠪࡠࡳ࠭ᱺ"), bstack1111lll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᱻ")))
    if bstack11l111lll1l_opy_:
        with open(bstack1111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᱼ") + os.environ[bstack1111lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᱽ")] + bstack1111lll_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬ᱾"), bstack1111lll_opy_ (u"ࠨࡣࠪ᱿")) as f:
            f.write(message + bstack1111lll_opy_ (u"ࠩ࡟ࡲࠬᲀ"))
def bstack1l1lll11l1l_opy_():
    return os.environ[bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᲁ")].lower() == bstack1111lll_opy_ (u"ࠫࡹࡸࡵࡦࠩᲂ")
def bstack11l11ll1l1_opy_():
    return bstack111l1111ll_opy_().replace(tzinfo=None).isoformat() + bstack1111lll_opy_ (u"ࠬࡠࠧᲃ")
def bstack111llll1ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1111lll_opy_ (u"࡚࠭ࠨᲄ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1111lll_opy_ (u"࡛ࠧࠩᲅ")))).total_seconds() * 1000
def bstack11l11l1ll1l_opy_(timestamp):
    return bstack11l11ll1l11_opy_(timestamp).isoformat() + bstack1111lll_opy_ (u"ࠨ࡜ࠪᲆ")
def bstack11l1l111l11_opy_(bstack11l11111ll1_opy_):
    date_format = bstack1111lll_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧᲇ")
    bstack11l1111l1ll_opy_ = datetime.datetime.strptime(bstack11l11111ll1_opy_, date_format)
    return bstack11l1111l1ll_opy_.isoformat() + bstack1111lll_opy_ (u"ࠪ࡞ࠬᲈ")
def bstack11l11l1111l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᲉ")
    else:
        return bstack1111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᲊ")
def bstack11lll1111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1111lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᲋")
def bstack111ll1ll111_opy_(val):
    return val.__str__().lower() == bstack1111lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᲌")
def error_handler(bstack11l111111ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l111111ll_opy_ as e:
                print(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ᲍").format(func.__name__, bstack11l111111ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lllll111_opy_(bstack111lll111l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lll111l1_opy_(cls, *args, **kwargs)
            except bstack11l111111ll_opy_ as e:
                print(bstack1111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᲎").format(bstack111lll111l1_opy_.__name__, bstack11l111111ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lllll111_opy_
    else:
        return decorator
def bstack11l1111l1l_opy_(bstack11111lll1l_opy_):
    if os.getenv(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭᲏")) is not None:
        return bstack11lll1111_opy_(os.getenv(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᲐ")))
    if bstack1111lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᲑ") in bstack11111lll1l_opy_ and bstack111ll1ll111_opy_(bstack11111lll1l_opy_[bstack1111lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᲒ")]):
        return False
    if bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᲓ") in bstack11111lll1l_opy_ and bstack111ll1ll111_opy_(bstack11111lll1l_opy_[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᲔ")]):
        return False
    return True
def bstack1l111lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack111llll1l11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤᲕ"), None)
        return bstack111llll1l11_opy_ is None or bstack111llll1l11_opy_ == bstack1111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᲖ")
    except Exception as e:
        return False
def bstack11ll11llll_opy_(hub_url, CONFIG):
    if bstack1l1l1ll111_opy_() <= version.parse(bstack1111lll_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᲗ")):
        if hub_url:
            return bstack1111lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᲘ") + hub_url + bstack1111lll_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥᲙ")
        return bstack1llll11ll_opy_
    if hub_url:
        return bstack1111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᲚ") + hub_url + bstack1111lll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᲛ")
    return bstack11l1ll1l1_opy_
def bstack111ll1l1lll_opy_():
    return isinstance(os.getenv(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᲜ")), str)
def bstack111ll11ll_opy_(url):
    return urlparse(url).hostname
def bstack1l1lll1111_opy_(hostname):
    for bstack1lll11ll1_opy_ in bstack11lll1ll11_opy_:
        regex = re.compile(bstack1lll11ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111ll1_opy_(bstack11l111l1l11_opy_, file_name, logger):
    bstack111lllll_opy_ = os.path.join(os.path.expanduser(bstack1111lll_opy_ (u"ࠪࢂࠬᲝ")), bstack11l111l1l11_opy_)
    try:
        if not os.path.exists(bstack111lllll_opy_):
            os.makedirs(bstack111lllll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111lll_opy_ (u"ࠫࢃ࠭Პ")), bstack11l111l1l11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111lll_opy_ (u"ࠬࡽࠧᲟ")):
                pass
            with open(file_path, bstack1111lll_opy_ (u"ࠨࡷࠬࠤᲠ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l111l111_opy_.format(str(e)))
def bstack11l11111l1l_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111ll1_opy_(bstack1111lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᲡ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l111l1l11_opy_ = json.load(open(file_path, bstack1111lll_opy_ (u"ࠨࡴࡥࠫᲢ")))
        else:
            bstack1l111l1l11_opy_ = {}
        bstack1l111l1l11_opy_[key] = value
        with open(file_path, bstack1111lll_opy_ (u"ࠤࡺ࠯ࠧᲣ")) as outfile:
            json.dump(bstack1l111l1l11_opy_, outfile)
def bstack1l111l1l_opy_(file_name, logger):
    file_path = bstack11l1l111ll1_opy_(bstack1111lll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᲤ"), file_name, logger)
    bstack1l111l1l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111lll_opy_ (u"ࠫࡷ࠭Ქ")) as bstack1l111lll1_opy_:
            bstack1l111l1l11_opy_ = json.load(bstack1l111lll1_opy_)
    return bstack1l111l1l11_opy_
def bstack111lll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᲦ") + file_path + bstack1111lll_opy_ (u"࠭ࠠࠨᲧ") + str(e))
def bstack1l1l1ll111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111lll_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᲨ")
def bstack1lll1l1l_opy_(config):
    if bstack1111lll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᲩ") in config:
        del (config[bstack1111lll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᲪ")])
        return False
    if bstack1l1l1ll111_opy_() < version.parse(bstack1111lll_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᲫ")):
        return False
    if bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᲬ")):
        return True
    if bstack1111lll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᲭ") in config and config[bstack1111lll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭Ხ")] is False:
        return False
    else:
        return True
def bstack111ll11l1_opy_(args_list, bstack111lll1l11l_opy_):
    index = -1
    for value in bstack111lll1l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1llllll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1llllll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll111ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll111ll_opy_ = bstack111ll111ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1111lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᲯ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᲰ"), exception=exception)
    def bstack111111ll1l_opy_(self):
        if self.result != bstack1111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᲱ"):
            return None
        if isinstance(self.exception_type, str) and bstack1111lll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᲲ") in self.exception_type:
            return bstack1111lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᲳ")
        return bstack1111lll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᲴ")
    def bstack111lll11l11_opy_(self):
        if self.result != bstack1111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ჵ"):
            return None
        if self.bstack111ll111ll_opy_:
            return self.bstack111ll111ll_opy_
        return bstack111lll1ll11_opy_(self.exception)
def bstack111lll1ll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111lll11l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l11l1l1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1111l11l_opy_(config, logger):
    try:
        import playwright
        bstack11l11l11ll1_opy_ = playwright.__file__
        bstack111ll1l1l1l_opy_ = os.path.split(bstack11l11l11ll1_opy_)
        bstack11l11lll11l_opy_ = bstack111ll1l1l1l_opy_[0] + bstack1111lll_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᲶ")
        os.environ[bstack1111lll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᲷ")] = bstack1llll1ll1_opy_(config)
        with open(bstack11l11lll11l_opy_, bstack1111lll_opy_ (u"ࠩࡵࠫᲸ")) as f:
            bstack1l1ll1l1l1_opy_ = f.read()
            bstack11l11llll11_opy_ = bstack1111lll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᲹ")
            bstack11l111l11l1_opy_ = bstack1l1ll1l1l1_opy_.find(bstack11l11llll11_opy_)
            if bstack11l111l11l1_opy_ == -1:
              process = subprocess.Popen(bstack1111lll_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᲺ"), shell=True, cwd=bstack111ll1l1l1l_opy_[0])
              process.wait()
              bstack11l11111111_opy_ = bstack1111lll_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬ᲻")
              bstack11l1l1111ll_opy_ = bstack1111lll_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥ᲼")
              bstack11l11l1l111_opy_ = bstack1l1ll1l1l1_opy_.replace(bstack11l11111111_opy_, bstack11l1l1111ll_opy_)
              with open(bstack11l11lll11l_opy_, bstack1111lll_opy_ (u"ࠧࡸࠩᲽ")) as f:
                f.write(bstack11l11l1l111_opy_)
    except Exception as e:
        logger.error(bstack1l1lll11_opy_.format(str(e)))
def bstack11ll111l11_opy_():
  try:
    bstack11l1111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᲾ"))
    bstack111lllll1ll_opy_ = []
    if os.path.exists(bstack11l1111l11l_opy_):
      with open(bstack11l1111l11l_opy_) as f:
        bstack111lllll1ll_opy_ = json.load(f)
      os.remove(bstack11l1111l11l_opy_)
    return bstack111lllll1ll_opy_
  except:
    pass
  return []
def bstack1l1ll111_opy_(bstack111l11ll1_opy_):
  try:
    bstack111lllll1ll_opy_ = []
    bstack11l1111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᲿ"))
    if os.path.exists(bstack11l1111l11l_opy_):
      with open(bstack11l1111l11l_opy_) as f:
        bstack111lllll1ll_opy_ = json.load(f)
    bstack111lllll1ll_opy_.append(bstack111l11ll1_opy_)
    with open(bstack11l1111l11l_opy_, bstack1111lll_opy_ (u"ࠪࡻࠬ᳀")) as f:
        json.dump(bstack111lllll1ll_opy_, f)
  except:
    pass
def bstack1ll11111l_opy_(logger, bstack11l111llll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1111lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ᳁"), bstack1111lll_opy_ (u"ࠬ࠭᳂"))
    if test_name == bstack1111lll_opy_ (u"࠭ࠧ᳃"):
        test_name = threading.current_thread().__dict__.get(bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭᳄"), bstack1111lll_opy_ (u"ࠨࠩ᳅"))
    bstack111ll1ll11l_opy_ = bstack1111lll_opy_ (u"ࠩ࠯ࠤࠬ᳆").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l111llll1_opy_:
        bstack1111ll11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᳇"), bstack1111lll_opy_ (u"ࠫ࠵࠭᳈"))
        bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᳉"): test_name, bstack1111lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᳊"): bstack111ll1ll11l_opy_, bstack1111lll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᳋"): bstack1111ll11_opy_}
        bstack11l1l11111l_opy_ = []
        bstack11l11l11111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ᳌"))
        if os.path.exists(bstack11l11l11111_opy_):
            with open(bstack11l11l11111_opy_) as f:
                bstack11l1l11111l_opy_ = json.load(f)
        bstack11l1l11111l_opy_.append(bstack1ll1lll1_opy_)
        with open(bstack11l11l11111_opy_, bstack1111lll_opy_ (u"ࠩࡺࠫ᳍")) as f:
            json.dump(bstack11l1l11111l_opy_, f)
    else:
        bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᳎"): test_name, bstack1111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᳏"): bstack111ll1ll11l_opy_, bstack1111lll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᳐"): str(multiprocessing.current_process().name)}
        if bstack1111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ᳑") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1lll1_opy_)
  except Exception as e:
      logger.warn(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᳒").format(e))
def bstack11lll111l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡲ࡯ࡤ࡭ࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡺࡹࡩ࡯ࡩࠣࡦࡦࡹࡩࡤࠢࡩ࡭ࡱ࡫ࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠫ᳓"))
    try:
      bstack11l111l11ll_opy_ = []
      bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠩࡱࡥࡲ࡫᳔ࠧ"): test_name, bstack1111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ᳕ࠩ"): error_message, bstack1111lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺ᳖ࠪ"): index}
      bstack11l11l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ᳗࠭"))
      if os.path.exists(bstack11l11l111ll_opy_):
          with open(bstack11l11l111ll_opy_) as f:
              bstack11l111l11ll_opy_ = json.load(f)
      bstack11l111l11ll_opy_.append(bstack1ll1lll1_opy_)
      with open(bstack11l11l111ll_opy_, bstack1111lll_opy_ (u"࠭ࡷࠨ᳘")) as f:
          json.dump(bstack11l111l11ll_opy_, f)
    except Exception as e:
      logger.warn(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿ᳙ࠥ").format(e))
    return
  bstack11l111l11ll_opy_ = []
  bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭᳚"): test_name, bstack1111lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᳛"): error_message, bstack1111lll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹ᳜ࠩ"): index}
  bstack11l11l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲ᳝ࠬ"))
  lock_file = bstack11l11l111ll_opy_ + bstack1111lll_opy_ (u"ࠬ࠴࡬ࡰࡥ࡮᳞ࠫ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l11l111ll_opy_):
          with open(bstack11l11l111ll_opy_, bstack1111lll_opy_ (u"࠭ࡲࠨ᳟")) as f:
              content = f.read().strip()
              if content:
                  bstack11l111l11ll_opy_ = json.load(open(bstack11l11l111ll_opy_))
      bstack11l111l11ll_opy_.append(bstack1ll1lll1_opy_)
      with open(bstack11l11l111ll_opy_, bstack1111lll_opy_ (u"ࠧࡸࠩ᳠")) as f:
          json.dump(bstack11l111l11ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡬ࡩ࡭ࡧࠣࡰࡴࡩ࡫ࡪࡰࡪ࠾ࠥࢁࡽࠣ᳡").format(e))
def bstack1lll111lll_opy_(bstack1ll111l1l1_opy_, name, logger):
  try:
    bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠩࡱࡥࡲ࡫᳢ࠧ"): name, bstack1111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳ᳣ࠩ"): bstack1ll111l1l1_opy_, bstack1111lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺ᳤ࠪ"): str(threading.current_thread()._name)}
    return bstack1ll1lll1_opy_
  except Exception as e:
    logger.warn(bstack1111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᳥").format(e))
  return
def bstack111llllll1l_opy_():
    return platform.system() == bstack1111lll_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹ᳦ࠧ")
def bstack1l11lll1_opy_(bstack111lll11lll_opy_, config, logger):
    bstack111lll1l1ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111lll11lll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ᳧").format(e))
    return bstack111lll1l1ll_opy_
def bstack11l111ll111_opy_(bstack111llll111l_opy_, bstack11l11l11l1l_opy_):
    bstack11l111lll11_opy_ = version.parse(bstack111llll111l_opy_)
    bstack111llll1111_opy_ = version.parse(bstack11l11l11l1l_opy_)
    if bstack11l111lll11_opy_ > bstack111llll1111_opy_:
        return 1
    elif bstack11l111lll11_opy_ < bstack111llll1111_opy_:
        return -1
    else:
        return 0
def bstack111l1111ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11ll1l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11lllll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l11llll_opy_(options, framework, config, bstack11111ll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1111lll_opy_ (u"ࠨࡩࡨࡸ᳨ࠬ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1ll11l_opy_ = caps.get(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᳩ"))
    bstack11l1111l1l1_opy_ = True
    bstack1l1l1ll1l_opy_ = os.environ[bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᳪ")]
    bstack1ll11ll1lll_opy_ = config.get(bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᳫ"), False)
    if bstack1ll11ll1lll_opy_:
        bstack1ll1llll1l1_opy_ = config.get(bstack1111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᳬ"), {})
        bstack1ll1llll1l1_opy_[bstack1111lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯᳭ࠩ")] = os.getenv(bstack1111lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᳮ"))
        bstack11ll1l1l1l1_opy_ = json.loads(os.getenv(bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᳯ"), bstack1111lll_opy_ (u"ࠩࡾࢁࠬᳰ"))).get(bstack1111lll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᳱ"))
    if bstack111ll1ll111_opy_(caps.get(bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᳲ"))) or bstack111ll1ll111_opy_(caps.get(bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᳳ"))):
        bstack11l1111l1l1_opy_ = False
    if bstack1lll1l1l_opy_({bstack1111lll_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ᳴"): bstack11l1111l1l1_opy_}):
        bstack11l1ll11l_opy_ = bstack11l1ll11l_opy_ or {}
        bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᳵ")] = bstack11l11lllll1_opy_(framework)
        bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᳶ")] = bstack1l1lll11l1l_opy_()
        bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᳷")] = bstack1l1l1ll1l_opy_
        bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᳸")] = bstack11111ll1_opy_
        if bstack1ll11ll1lll_opy_:
            bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᳹")] = bstack1ll11ll1lll_opy_
            bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᳺ")] = bstack1ll1llll1l1_opy_
            bstack11l1ll11l_opy_[bstack1111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᳻")][bstack1111lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᳼")] = bstack11ll1l1l1l1_opy_
        if getattr(options, bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᳽"), None):
            options.set_capability(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᳾"), bstack11l1ll11l_opy_)
        else:
            options[bstack1111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᳿")] = bstack11l1ll11l_opy_
    else:
        if getattr(options, bstack1111lll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᴀ"), None):
            options.set_capability(bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᴁ"), bstack11l11lllll1_opy_(framework))
            options.set_capability(bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᴂ"), bstack1l1lll11l1l_opy_())
            options.set_capability(bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᴃ"), bstack1l1l1ll1l_opy_)
            options.set_capability(bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᴄ"), bstack11111ll1_opy_)
            if bstack1ll11ll1lll_opy_:
                options.set_capability(bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴅ"), bstack1ll11ll1lll_opy_)
                options.set_capability(bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴆ"), bstack1ll1llll1l1_opy_)
                options.set_capability(bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ࠱ࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᴇ"), bstack11ll1l1l1l1_opy_)
        else:
            options[bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᴈ")] = bstack11l11lllll1_opy_(framework)
            options[bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᴉ")] = bstack1l1lll11l1l_opy_()
            options[bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᴊ")] = bstack1l1l1ll1l_opy_
            options[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᴋ")] = bstack11111ll1_opy_
            if bstack1ll11ll1lll_opy_:
                options[bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴌ")] = bstack1ll11ll1lll_opy_
                options[bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴍ")] = bstack1ll1llll1l1_opy_
                options[bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᴎ")][bstack1111lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᴏ")] = bstack11ll1l1l1l1_opy_
    return options
def bstack11l11l1l11l_opy_(bstack11l11l111l1_opy_, framework):
    bstack11111ll1_opy_ = bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣᴐ"))
    if bstack11l11l111l1_opy_ and len(bstack11l11l111l1_opy_.split(bstack1111lll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᴑ"))) > 1:
        ws_url = bstack11l11l111l1_opy_.split(bstack1111lll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᴒ"))[0]
        if bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᴓ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1111ll1l_opy_ = json.loads(urllib.parse.unquote(bstack11l11l111l1_opy_.split(bstack1111lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴔ"))[1]))
            bstack11l1111ll1l_opy_ = bstack11l1111ll1l_opy_ or {}
            bstack1l1l1ll1l_opy_ = os.environ[bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᴕ")]
            bstack11l1111ll1l_opy_[bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᴖ")] = str(framework) + str(__version__)
            bstack11l1111ll1l_opy_[bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᴗ")] = bstack1l1lll11l1l_opy_()
            bstack11l1111ll1l_opy_[bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᴘ")] = bstack1l1l1ll1l_opy_
            bstack11l1111ll1l_opy_[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᴙ")] = bstack11111ll1_opy_
            bstack11l11l111l1_opy_ = bstack11l11l111l1_opy_.split(bstack1111lll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᴚ"))[0] + bstack1111lll_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᴛ") + urllib.parse.quote(json.dumps(bstack11l1111ll1l_opy_))
    return bstack11l11l111l1_opy_
def bstack1l1ll11ll1_opy_():
    global bstack1lll111l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll111l_opy_ = BrowserType.connect
    return bstack1lll111l_opy_
def bstack1llllll11l_opy_(framework_name):
    global bstack1l11l1l11_opy_
    bstack1l11l1l11_opy_ = framework_name
    return framework_name
def bstack1l111llll1_opy_(self, *args, **kwargs):
    global bstack1lll111l_opy_
    try:
        global bstack1l11l1l11_opy_
        if bstack1111lll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᴜ") in kwargs:
            kwargs[bstack1111lll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᴝ")] = bstack11l11l1l11l_opy_(
                kwargs.get(bstack1111lll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᴞ"), None),
                bstack1l11l1l11_opy_
            )
    except Exception as e:
        logger.error(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢᴟ").format(str(e)))
    return bstack1lll111l_opy_(self, *args, **kwargs)
def bstack11l11l1lll1_opy_(bstack111llllll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll1llll1_opy_(bstack111llllll11_opy_, bstack1111lll_opy_ (u"ࠣࠤᴠ"))
        if proxies and proxies.get(bstack1111lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᴡ")):
            parsed_url = urlparse(proxies.get(bstack1111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᴢ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1111lll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧᴣ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1111lll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨᴤ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1111lll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᴥ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1111lll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪᴦ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1lll1ll_opy_(bstack111llllll11_opy_):
    bstack111ll1lll11_opy_ = {
        bstack11l1ll1l111_opy_[bstack111lll1l111_opy_]: bstack111llllll11_opy_[bstack111lll1l111_opy_]
        for bstack111lll1l111_opy_ in bstack111llllll11_opy_
        if bstack111lll1l111_opy_ in bstack11l1ll1l111_opy_
    }
    bstack111ll1lll11_opy_[bstack1111lll_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᴧ")] = bstack11l11l1lll1_opy_(bstack111llllll11_opy_, bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᴨ")))
    bstack11l11ll11l1_opy_ = [element.lower() for element in bstack11l1lll1lll_opy_]
    bstack111lllll1l1_opy_(bstack111ll1lll11_opy_, bstack11l11ll11l1_opy_)
    return bstack111ll1lll11_opy_
def bstack111lllll1l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1111lll_opy_ (u"ࠥ࠮࠯࠰ࠪࠣᴩ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111lllll1l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111lllll1l1_opy_(item, keys)
def bstack1l1ll1lll11_opy_():
    bstack111lll1lll1_opy_ = [os.environ.get(bstack1111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡎࡒࡅࡔࡡࡇࡍࡗࠨᴪ")), os.path.join(os.path.expanduser(bstack1111lll_opy_ (u"ࠧࢄࠢᴫ")), bstack1111lll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᴬ")), os.path.join(bstack1111lll_opy_ (u"ࠧ࠰ࡶࡰࡴࠬᴭ"), bstack1111lll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᴮ"))]
    for path in bstack111lll1lll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1111lll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᴯ") + str(path) + bstack1111lll_opy_ (u"ࠥࠫࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨᴰ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1111lll_opy_ (u"ࠦࡌ࡯ࡶࡪࡰࡪࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࠧࠣᴱ") + str(path) + bstack1111lll_opy_ (u"ࠧ࠭ࠢᴲ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1111lll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࠬࠨᴳ") + str(path) + bstack1111lll_opy_ (u"ࠢࠨࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡬ࡦࡹࠠࡵࡪࡨࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡩࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶ࠲ࠧᴴ"))
            else:
                logger.debug(bstack1111lll_opy_ (u"ࠣࡅࡵࡩࡦࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࠩࠥᴵ") + str(path) + bstack1111lll_opy_ (u"ࠤࠪࠤࡼ࡯ࡴࡩࠢࡺࡶ࡮ࡺࡥࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲ࠳ࠨᴶ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1111lll_opy_ (u"ࠥࡓࡵ࡫ࡲࡢࡶ࡬ࡳࡳࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥࠢࡩࡳࡷࠦࠧࠣᴷ") + str(path) + bstack1111lll_opy_ (u"ࠦࠬ࠴ࠢᴸ"))
            return path
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡻࡰࠡࡨ࡬ࡰࡪࠦࠧࡼࡲࡤࡸ࡭ࢃࠧ࠻ࠢࠥᴹ") + str(e) + bstack1111lll_opy_ (u"ࠨࠢᴺ"))
    logger.debug(bstack1111lll_opy_ (u"ࠢࡂ࡮࡯ࠤࡵࡧࡴࡩࡵࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠦᴻ"))
    return None
@measure(event_name=EVENTS.bstack11l1lll1l11_opy_, stage=STAGE.bstack11111lll_opy_)
def bstack1lll1l11ll1_opy_(binary_path, bstack1lll11l1111_opy_, bs_config):
    logger.debug(bstack1111lll_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵࠢࡆࡐࡎࠦࡐࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࢀࢃࠢᴼ").format(binary_path))
    bstack11l11ll11ll_opy_ = bstack1111lll_opy_ (u"ࠩࠪᴽ")
    bstack11l111l111l_opy_ = {
        bstack1111lll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᴾ"): __version__,
        bstack1111lll_opy_ (u"ࠦࡴࡹࠢᴿ"): platform.system(),
        bstack1111lll_opy_ (u"ࠧࡵࡳࡠࡣࡵࡧ࡭ࠨᵀ"): platform.machine(),
        bstack1111lll_opy_ (u"ࠨࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠦᵁ"): bstack1111lll_opy_ (u"ࠧ࠱ࠩᵂ"),
        bstack1111lll_opy_ (u"ࠣࡵࡧ࡯ࡤࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠢᵃ"): bstack1111lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᵄ")
    }
    bstack111ll1l11ll_opy_(bstack11l111l111l_opy_)
    try:
        if binary_path:
            bstack11l111l111l_opy_[bstack1111lll_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᵅ")] = subprocess.check_output([binary_path, bstack1111lll_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᵆ")]).strip().decode(bstack1111lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᵇ"))
        response = requests.request(
            bstack1111lll_opy_ (u"࠭ࡇࡆࡖࠪᵈ"),
            url=bstack1ll11l11l1_opy_(bstack11l1lllll11_opy_),
            headers=None,
            auth=(bs_config[bstack1111lll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᵉ")], bs_config[bstack1111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᵊ")]),
            json=None,
            params=bstack11l111l111l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1111lll_opy_ (u"ࠩࡸࡶࡱ࠭ᵋ") in data.keys() and bstack1111lll_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡧࡣࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᵌ") in data.keys():
            logger.debug(bstack1111lll_opy_ (u"ࠦࡓ࡫ࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡨࡩ࡯ࡣࡵࡽ࠱ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧᵍ").format(bstack11l111l111l_opy_[bstack1111lll_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᵎ")]))
            if bstack1111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩᵏ") in os.environ:
                logger.debug(bstack1111lll_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡦࡹࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠣ࡭ࡸࠦࡳࡦࡶࠥᵐ"))
                data[bstack1111lll_opy_ (u"ࠨࡷࡵࡰࠬᵑ")] = os.environ[bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᵒ")]
            bstack11l1111ll11_opy_ = bstack111ll1l11l1_opy_(data[bstack1111lll_opy_ (u"ࠪࡹࡷࡲࠧᵓ")], bstack1lll11l1111_opy_)
            bstack11l11ll11ll_opy_ = os.path.join(bstack1lll11l1111_opy_, bstack11l1111ll11_opy_)
            os.chmod(bstack11l11ll11ll_opy_, 0o777) # bstack11l11l1llll_opy_ permission
            return bstack11l11ll11ll_opy_
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡘࡊࡋࠡࡽࢀࠦᵔ").format(e))
    return binary_path
def bstack111ll1l11ll_opy_(bstack11l111l111l_opy_):
    try:
        if bstack1111lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᵕ") not in bstack11l111l111l_opy_[bstack1111lll_opy_ (u"࠭࡯ࡴࠩᵖ")].lower():
            return
        if os.path.exists(bstack1111lll_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡵࡳ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᵗ")):
            with open(bstack1111lll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᵘ"), bstack1111lll_opy_ (u"ࠤࡵࠦᵙ")) as f:
                bstack11l11lll1ll_opy_ = {}
                for line in f:
                    if bstack1111lll_opy_ (u"ࠥࡁࠧᵚ") in line:
                        key, value = line.rstrip().split(bstack1111lll_opy_ (u"ࠦࡂࠨᵛ"), 1)
                        bstack11l11lll1ll_opy_[key] = value.strip(bstack1111lll_opy_ (u"ࠬࠨ࡜ࠨࠩᵜ"))
                bstack11l111l111l_opy_[bstack1111lll_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭ᵝ")] = bstack11l11lll1ll_opy_.get(bstack1111lll_opy_ (u"ࠢࡊࡆࠥᵞ"), bstack1111lll_opy_ (u"ࠣࠤᵟ"))
        elif os.path.exists(bstack1111lll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡢ࡮ࡳ࡭ࡳ࡫࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣᵠ")):
            bstack11l111l111l_opy_[bstack1111lll_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪᵡ")] = bstack1111lll_opy_ (u"ࠫࡦࡲࡰࡪࡰࡨࠫᵢ")
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡪࡩࡴࡶࡵࡳࠥࡵࡦࠡ࡮࡬ࡲࡺࡾࠢᵣ") + e)
@measure(event_name=EVENTS.bstack11l1llll1ll_opy_, stage=STAGE.bstack11111lll_opy_)
def bstack111ll1l11l1_opy_(bstack11l11ll111l_opy_, bstack111llll11ll_opy_):
    logger.debug(bstack1111lll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࡀࠠࠣᵤ") + str(bstack11l11ll111l_opy_) + bstack1111lll_opy_ (u"ࠢࠣᵥ"))
    zip_path = os.path.join(bstack111llll11ll_opy_, bstack1111lll_opy_ (u"ࠣࡦࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࡤ࡬ࡩ࡭ࡧ࠱ࡾ࡮ࡶࠢᵦ"))
    bstack11l1111ll11_opy_ = bstack1111lll_opy_ (u"ࠩࠪᵧ")
    with requests.get(bstack11l11ll111l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1111lll_opy_ (u"ࠥࡻࡧࠨᵨ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1111lll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽ࠳ࠨᵩ"))
    with zipfile.ZipFile(zip_path, bstack1111lll_opy_ (u"ࠬࡸࠧᵪ")) as zip_ref:
        bstack11l1111llll_opy_ = zip_ref.namelist()
        if len(bstack11l1111llll_opy_) > 0:
            bstack11l1111ll11_opy_ = bstack11l1111llll_opy_[0] # bstack111llll1l1l_opy_ bstack11l1l1llll1_opy_ will be bstack111lll1l1l1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111llll11ll_opy_)
        logger.debug(bstack1111lll_opy_ (u"ࠨࡆࡪ࡮ࡨࡷࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡪࡾࡴࡳࡣࡦࡸࡪࡪࠠࡵࡱࠣࠫࠧᵫ") + str(bstack111llll11ll_opy_) + bstack1111lll_opy_ (u"ࠢࠨࠤᵬ"))
    os.remove(zip_path)
    return bstack11l1111ll11_opy_
def get_cli_dir():
    bstack111lll111ll_opy_ = bstack1l1ll1lll11_opy_()
    if bstack111lll111ll_opy_:
        bstack1lll11l1111_opy_ = os.path.join(bstack111lll111ll_opy_, bstack1111lll_opy_ (u"ࠣࡥ࡯࡭ࠧᵭ"))
        if not os.path.exists(bstack1lll11l1111_opy_):
            os.makedirs(bstack1lll11l1111_opy_, mode=0o777, exist_ok=True)
        return bstack1lll11l1111_opy_
    else:
        raise FileNotFoundError(bstack1111lll_opy_ (u"ࠤࡑࡳࠥࡽࡲࡪࡶࡤࡦࡱ࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠧᵮ"))
def bstack1ll1l1ll11l_opy_(bstack1lll11l1111_opy_):
    bstack1111lll_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡱࠤࡦࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠧࠨࠢᵯ")
    bstack11l11llllll_opy_ = [
        os.path.join(bstack1lll11l1111_opy_, f)
        for f in os.listdir(bstack1lll11l1111_opy_)
        if os.path.isfile(os.path.join(bstack1lll11l1111_opy_, f)) and f.startswith(bstack1111lll_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼ࠱ࠧᵰ"))
    ]
    if len(bstack11l11llllll_opy_) > 0:
        return max(bstack11l11llllll_opy_, key=os.path.getmtime) # get bstack11l1111lll1_opy_ binary
    return bstack1111lll_opy_ (u"ࠧࠨᵱ")
def bstack11ll1lll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll1l11lll1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l11lll1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll11l1l_opy_(data, keys, default=None):
    bstack1111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡢࡨࡨࡰࡾࠦࡧࡦࡶࠣࡥࠥࡴࡥࡴࡶࡨࡨࠥࡼࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡣࡷࡥ࠿ࠦࡔࡩࡧࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡶࡲࠤࡹࡸࡡࡷࡧࡵࡷࡪ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡰ࡫ࡹࡴ࠼ࠣࡅࠥࡲࡩࡴࡶࠣࡳ࡫ࠦ࡫ࡦࡻࡶ࠳࡮ࡴࡤࡪࡥࡨࡷࠥࡸࡥࡱࡴࡨࡷࡪࡴࡴࡪࡰࡪࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩ࡫ࡦࡢࡷ࡯ࡸ࠿ࠦࡖࡢ࡮ࡸࡩࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡲࡦࡶࡸࡶࡳࡀࠠࡕࡪࡨࠤࡻࡧ࡬ࡶࡧࠣࡥࡹࠦࡴࡩࡧࠣࡲࡪࡹࡴࡦࡦࠣࡴࡦࡺࡨ࠭ࠢࡲࡶࠥࡪࡥࡧࡣࡸࡰࡹࠦࡩࡧࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᵲ")
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