# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
bstack11l1l11_opy_ (u"ࠣࠤࠥࠎࡕࡿࡴࡦࡵࡷࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡨࡦ࡮ࡳࡩࡷࠦࡵࡴ࡫ࡱ࡫ࠥࡪࡩࡳࡧࡦࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡮࡯ࡰ࡭ࡶ࠲ࠏࠨࠢࠣᄑ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lllll11111_opy_(bstack1lllll11ll1_opy_=None, bstack1lllll1l1ll_opy_=None):
    bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡆࡳࡱࡲࡥࡤࡶࠣࡴࡾࡺࡥࡴࡶࠣࡸࡪࡹࡴࡴࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠨࡵࠣ࡭ࡳࡺࡥࡳࡰࡤࡰࠥࡇࡐࡊࡵ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡡࡳࡩࡶࠤ࠭ࡲࡩࡴࡶ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࡅࡲࡱࡵࡲࡥࡵࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡿࡴࡦࡵࡷࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡪࡰࡦࡰࡺࡪࡩ࡯ࡩࠣࡴࡦࡺࡨࡴࠢࡤࡲࡩࠦࡦ࡭ࡣࡪࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡢ࡭ࡨࡷࠥࡶࡲࡦࡥࡨࡨࡪࡴࡣࡦࠢࡲࡺࡪࡸࠠࡵࡧࡶࡸࡤࡶࡡࡵࡪࡶࠤ࡮࡬ࠠࡣࡱࡷ࡬ࠥࡧࡲࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡵࡧࡴࡩࡵࠣࠬࡱ࡯ࡳࡵࠢࡲࡶࠥࡹࡴࡳ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࡕࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠫࡷ࠮࠵ࡤࡪࡴࡨࡧࡹࡵࡲࡺࠪ࡬ࡩࡸ࠯ࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤ࡫ࡸ࡯࡮࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧ࡮ࠡࡤࡨࠤࡦࠦࡳࡪࡰࡪࡰࡪࠦࡰࡢࡶ࡫ࠤࡸࡺࡲࡪࡰࡪࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡌ࡫ࡳࡵࡲࡦࡦࠣ࡭࡫ࠦࡴࡦࡵࡷࡣࡦࡸࡧࡴࠢ࡬ࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡩࡵࡪࠣ࡯ࡪࡿࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡶࡹࡨࡩࡥࡴࡵࠣࠬࡧࡵ࡯࡭ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡧࡴࡻ࡮ࡵࠢࠫ࡭ࡳࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡰࡲࡨࡪ࡯ࡤࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡥࡳࡴࡲࡶࠥ࠮ࡳࡵࡴࠬࠎࠥࠦࠠࠡࠤࠥࠦᄒ")
    try:
        bstack1lllll1111l_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠥࡔ࡞࡚ࡅࡔࡖࡢࡇ࡚ࡘࡒࡆࡐࡗࡣ࡙ࡋࡓࡕࠤᄓ")) is not None
        if bstack1lllll11ll1_opy_ is not None:
            args = list(bstack1lllll11ll1_opy_)
        elif bstack1lllll1l1ll_opy_ is not None:
            if isinstance(bstack1lllll1l1ll_opy_, str):
                args = [bstack1lllll1l1ll_opy_]
            elif isinstance(bstack1lllll1l1ll_opy_, list):
                args = list(bstack1lllll1l1ll_opy_)
            else:
                args = [bstack11l1l11_opy_ (u"ࠦ࠳ࠨᄔ")]
        else:
            args = [bstack11l1l11_opy_ (u"ࠧ࠴ࠢᄕ")]
        if bstack1lllll1111l_opy_:
            return _1lllll111ll_opy_(args)
        bstack1lllll1l11l_opy_ = args + [
            bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢᄖ"),
            bstack11l1l11_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣᄗ")
        ]
        class bstack1lllll111l1_opy_:
            bstack11l1l11_opy_ (u"ࠣࠤࠥࡔࡾࡺࡥࡴࡶࠣࡴࡱࡻࡧࡪࡰࠣࡸ࡭ࡧࡴࠡࡥࡤࡴࡹࡻࡲࡦࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠦࡴࡦࡵࡷࠤ࡮ࡺࡥ࡮ࡵ࠱ࠦࠧࠨᄘ")
            def __init__(self):
                self.bstack1lllll1l1l1_opy_ = []
                self.test_files = set()
                self.bstack1lllll11l1l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack11l1l11_opy_ (u"ࠤࠥࠦࡍࡵ࡯࡬ࠢࡦࡥࡱࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡨ࡬ࡲ࡮ࡹࡨࡦࡦ࠱ࠦࠧࠨᄙ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lllll1l1l1_opy_.append(nodeid)
                        if bstack11l1l11_opy_ (u"ࠥ࠾࠿ࠨᄚ") in nodeid:
                            file_path = nodeid.split(bstack11l1l11_opy_ (u"ࠦ࠿ࡀࠢᄛ"), 1)[0]
                            if file_path.endswith(bstack11l1l11_opy_ (u"ࠬ࠴ࡰࡺࠩᄜ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll11l1l_opy_ = str(e)
        collector = bstack1lllll111l1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lllll1l11l_opy_, plugins=[collector])
        if collector.bstack1lllll11l1l_opy_:
            return {bstack11l1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᄝ"): False, bstack11l1l11_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨᄞ"): 0, bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤᄟ"): [], bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨᄠ"): [], bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᄡ"): bstack11l1l11_opy_ (u"ࠦࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᄢ").format(collector.bstack1lllll11l1l_opy_)}
        return {
            bstack11l1l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄣ"): True,
            bstack11l1l11_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᄤ"): len(collector.bstack1lllll1l1l1_opy_),
            bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᄥ"): collector.bstack1lllll1l1l1_opy_,
            bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᄦ"): sorted(collector.test_files),
            bstack11l1l11_opy_ (u"ࠤࡨࡼ࡮ࡺ࡟ࡤࡱࡧࡩࠧᄧ"): exit_code
        }
    except Exception as e:
        return {bstack11l1l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄨ"): False, bstack11l1l11_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄩ"): 0, bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄪ"): [], bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᄫ"): [], bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᄬ"): bstack11l1l11_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᄭ").format(e)}
def _1lllll111ll_opy_(args):
    bstack11l1l11_opy_ (u"ࠤࠥࠦࡎࡹ࡯࡭ࡣࡷࡩࡩࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡽ࡫ࡣࡶࡶࡨࡨࠥ࡯࡮ࠡࡣࠣࡷࡪࡶࡡࡳࡣࡷࡩࠥࡖࡹࡵࡪࡲࡲࠥࡶࡲࡰࡥࡨࡷࡸࠦࡴࡰࠢࡤࡺࡴ࡯ࡤࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡼࡸࡪࡹࡴࠡ࡫ࡶࡷࡺ࡫ࡳ࠯ࠤࠥࠦᄮ")
    bstack1lllll11l11_opy_ = [sys.executable, bstack11l1l11_opy_ (u"ࠥ࠱ࡲࠨᄯ"), bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᄰ"), bstack11l1l11_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨᄱ"), bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢᄲ")]
    bstack1lllll11lll_opy_ = [a for a in args if a not in (bstack11l1l11_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣᄳ"), bstack11l1l11_opy_ (u"ࠣ࠯࠰ࡵࡺ࡯ࡥࡵࠤᄴ"), bstack11l1l11_opy_ (u"ࠤ࠰ࡵࠧᄵ"))]
    cmd = bstack1lllll11l11_opy_ + bstack1lllll11lll_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lllll1l1l1_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack11l1l11_opy_ (u"ࠥࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᄶ") in line.lower():
                continue
            if bstack11l1l11_opy_ (u"ࠦ࠿ࡀࠢᄷ") in line:
                bstack1lllll1l1l1_opy_.append(line)
                file_path = line.split(bstack11l1l11_opy_ (u"ࠧࡀ࠺ࠣᄸ"), 1)[0]
                if file_path.endswith(bstack11l1l11_opy_ (u"࠭࠮ࡱࡻࠪᄹ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack11l1l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᄺ"): success,
            bstack11l1l11_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢᄻ"): len(bstack1lllll1l1l1_opy_),
            bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥᄼ"): bstack1lllll1l1l1_opy_,
            bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢᄽ"): sorted(test_files),
            bstack11l1l11_opy_ (u"ࠦࡪࡾࡩࡵࡡࡦࡳࡩ࡫ࠢᄾ"): proc.returncode,
            bstack11l1l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᄿ"): None if success else bstack11l1l11_opy_ (u"ࠨࡓࡶࡤࡳࡶࡴࡩࡥࡴࡵࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࠩࡧࡻ࡭ࡹࠦࡻࡾࠫࠥᅀ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack11l1l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᅁ"): False, bstack11l1l11_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢᅂ"): 0, bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥᅃ"): [], bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢᅄ"): [], bstack11l1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᅅ"): bstack11l1l11_opy_ (u"࡙ࠧࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᅆ").format(e)}