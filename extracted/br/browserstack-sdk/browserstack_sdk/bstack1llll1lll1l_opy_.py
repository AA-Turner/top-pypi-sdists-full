# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࡒࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡬ࡪࡲࡰࡦࡴࠣࡹࡸ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡳࡴࡱࡳ࠯ࠌࠥࠦࠧᄕ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lllll11l11_opy_(bstack1lllll1111l_opy_=None, bstack1lllll111ll_opy_=None):
    bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡰ࡮࡯ࡩࡨࡺࠠࡱࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࡸࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠬࡹࠠࡪࡰࡷࡩࡷࡴࡡ࡭ࠢࡄࡔࡎࡹ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡲࡼࡸࡪࡹࡴࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡣ࡭ࡷࡧ࡭ࡳ࡭ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡪࡱࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘࡦࡱࡥࡴࠢࡳࡶࡪࡩࡥࡥࡧࡱࡧࡪࠦ࡯ࡷࡧࡵࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡ࡫ࡩࠤࡧࡵࡴࡩࠢࡤࡶࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࠩ࡮࡬ࡷࡹࠦ࡯ࡳࠢࡶࡸࡷ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤ࡙࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠨࡴࠫ࠲ࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠮ࡩࡦࡵࠬࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡨࡵࡳࡲ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡲࠥࡨࡥࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡴࡦࡺࡨࠡࡵࡷࡶ࡮ࡴࡧࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡉࡨࡰࡲࡶࡪࡪࠠࡪࡨࠣࡸࡪࡹࡴࡠࡣࡵ࡫ࡸࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺ࡭ࡹ࡮ࠠ࡬ࡧࡼࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡳࡶࡥࡦࡩࡸࡹࠠࠩࡤࡲࡳࡱ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡤࡱࡸࡲࡹࠦࠨࡪࡰࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡴ࡯ࡥࡧ࡬ࡨࡸࠦࠨ࡭࡫ࡶࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡩࡷࡸ࡯ࡳࠢࠫࡷࡹࡸࠩࠋࠢࠣࠤࠥࠨࠢࠣᄖ")
    try:
        bstack1lllll11111_opy_ = os.getenv(bstack1lll1l_opy_ (u"ࠢࡑ࡛ࡗࡉࡘ࡚࡟ࡄࡗࡕࡖࡊࡔࡔࡠࡖࡈࡗ࡙ࠨᄗ")) is not None
        if bstack1lllll1111l_opy_ is not None:
            args = list(bstack1lllll1111l_opy_)
        elif bstack1lllll111ll_opy_ is not None:
            if isinstance(bstack1lllll111ll_opy_, str):
                args = [bstack1lllll111ll_opy_]
            elif isinstance(bstack1lllll111ll_opy_, list):
                args = list(bstack1lllll111ll_opy_)
            else:
                args = [bstack1lll1l_opy_ (u"ࠣ࠰ࠥᄘ")]
        else:
            args = [bstack1lll1l_opy_ (u"ࠤ࠱ࠦᄙ")]
        if bstack1lllll11111_opy_:
            return _1lllll111l1_opy_(args)
        bstack1llll1lll11_opy_ = args + [
            bstack1lll1l_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦᄚ"),
            bstack1lll1l_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧᄛ")
        ]
        class bstack1lllll11ll1_opy_:
            bstack1lll1l_opy_ (u"ࠧࠨࠢࡑࡻࡷࡩࡸࡺࠠࡱ࡮ࡸ࡫࡮ࡴࠠࡵࡪࡤࡸࠥࡩࡡࡱࡶࡸࡶࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡸࡪࡹࡴࠡ࡫ࡷࡩࡲࡹ࠮ࠣࠤࠥᄜ")
            def __init__(self):
                self.bstack1llll1lllll_opy_ = []
                self.test_files = set()
                self.bstack1lllll11l1l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1lll1l_opy_ (u"ࠨࠢࠣࡊࡲࡳࡰࠦࡣࡢ࡮࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠮ࠣࠤࠥᄝ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llll1lllll_opy_.append(nodeid)
                        if bstack1lll1l_opy_ (u"ࠢ࠻࠼ࠥᄞ") in nodeid:
                            file_path = nodeid.split(bstack1lll1l_opy_ (u"ࠣ࠼࠽ࠦᄟ"), 1)[0]
                            if file_path.endswith(bstack1lll1l_opy_ (u"ࠩ࠱ࡴࡾ࠭ᄠ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll11l1l_opy_ = str(e)
        collector = bstack1lllll11ll1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llll1lll11_opy_, plugins=[collector])
        if collector.bstack1lllll11l1l_opy_:
            return {bstack1lll1l_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄡ"): False, bstack1lll1l_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄢ"): 0, bstack1lll1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄣ"): [], bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᄤ"): [], bstack1lll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᄥ"): bstack1lll1l_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᄦ").format(collector.bstack1lllll11l1l_opy_)}
        return {
            bstack1lll1l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᄧ"): True,
            bstack1lll1l_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᄨ"): len(collector.bstack1llll1lllll_opy_),
            bstack1lll1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᄩ"): collector.bstack1llll1lllll_opy_,
            bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᄪ"): sorted(collector.test_files),
            bstack1lll1l_opy_ (u"ࠨࡥࡹ࡫ࡷࡣࡨࡵࡤࡦࠤᄫ"): exit_code
        }
    except Exception as e:
        return {bstack1lll1l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᄬ"): False, bstack1lll1l_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢᄭ"): 0, bstack1lll1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥᄮ"): [], bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢᄯ"): [], bstack1lll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᄰ"): bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᄱ").format(e)}
def _1lllll111l1_opy_(args):
    bstack1lll1l_opy_ (u"ࠨࠢࠣࡋࡶࡳࡱࡧࡴࡦࡦࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡺࡨࡧࡺࡺࡥࡥࠢ࡬ࡲࠥࡧࠠࡴࡧࡳࡥࡷࡧࡴࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡳࡶࡴࡩࡥࡴࡵࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡴࡥࡴࡶࡨࡨࠥࡶࡹࡵࡧࡶࡸࠥ࡯ࡳࡴࡷࡨࡷ࠳ࠨࠢࠣᄲ")
    bstack1llll1ll1ll_opy_ = [sys.executable, bstack1lll1l_opy_ (u"ࠢ࠮࡯ࠥᄳ"), bstack1lll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᄴ"), bstack1lll1l_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥᄵ"), bstack1lll1l_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦᄶ")]
    bstack1llll1llll1_opy_ = [a for a in args if a not in (bstack1lll1l_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧᄷ"), bstack1lll1l_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨᄸ"), bstack1lll1l_opy_ (u"ࠨ࠭ࡲࠤᄹ"))]
    cmd = bstack1llll1ll1ll_opy_ + bstack1llll1llll1_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llll1lllll_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1lll1l_opy_ (u"ࠢࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦᄺ") in line.lower():
                continue
            if bstack1lll1l_opy_ (u"ࠣ࠼࠽ࠦᄻ") in line:
                bstack1llll1lllll_opy_.append(line)
                file_path = line.split(bstack1lll1l_opy_ (u"ࠤ࠽࠾ࠧᄼ"), 1)[0]
                if file_path.endswith(bstack1lll1l_opy_ (u"ࠪ࠲ࡵࡿࠧᄽ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1lll1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᄾ"): success,
            bstack1lll1l_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᄿ"): len(bstack1llll1lllll_opy_),
            bstack1lll1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᅀ"): bstack1llll1lllll_opy_,
            bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᅁ"): sorted(test_files),
            bstack1lll1l_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦᅂ"): proc.returncode,
            bstack1lll1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᅃ"): None if success else bstack1lll1l_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭࡫ࡸࡪࡶࠣࡿࢂ࠯ࠢᅄ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1lll1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᅅ"): False, bstack1lll1l_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᅆ"): 0, bstack1lll1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᅇ"): [], bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᅈ"): [], bstack1lll1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᅉ"): bstack1lll1l_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᅊ").format(e)}