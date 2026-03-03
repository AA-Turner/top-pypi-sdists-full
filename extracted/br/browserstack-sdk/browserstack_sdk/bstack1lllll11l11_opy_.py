# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
bstack11ll111_opy_ (u"ࠦࠧࠨࠊࡑࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡫ࡩࡱࡶࡥࡳࠢࡸࡷ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡪࡲࡳࡰࡹ࠮ࠋࠤࠥࠦᄍ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1lllll1l11l_opy_(bstack1lllll111l1_opy_=None, bstack1lllll11l1l_opy_=None):
    bstack11ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡࡃࡓࡍࡸ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡩࡰࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡥࡰ࡫ࡳࠡࡲࡵࡩࡨ࡫ࡤࡦࡰࡦࡩࠥࡵࡶࡦࡴࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࡪࡨࠣࡦࡴࡺࡨࠡࡣࡵࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࠨ࡭࡫ࡶࡸࠥࡵࡲࠡࡵࡷࡶ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡘࡪࡹࡴࠡࡨ࡬ࡰࡪ࠮ࡳࠪ࠱ࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠭࡯ࡥࡴࠫࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡧࡴࡲࡱ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡱࠤࡧ࡫ࠠࡢࠢࡶ࡭ࡳ࡭࡬ࡦࠢࡳࡥࡹ࡮ࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡏࡧ࡯ࡱࡵࡩࡩࠦࡩࡧࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹ࡬ࡸ࡭ࠦ࡫ࡦࡻࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡹࡵࡤࡥࡨࡷࡸࠦࠨࡣࡱࡲࡰ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡣࡰࡷࡱࡸࠥ࠮ࡩ࡯ࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡳࡵࡤࡦ࡫ࡧࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡨࡶࡷࡵࡲࠡࠪࡶࡸࡷ࠯ࠊࠡࠢࠣࠤࠧࠨࠢᄎ")
    try:
        bstack1lllll1111l_opy_ = os.getenv(bstack11ll111_opy_ (u"ࠨࡐ࡚ࡖࡈࡗ࡙ࡥࡃࡖࡔࡕࡉࡓ࡚࡟ࡕࡇࡖࡘࠧᄏ")) is not None
        if bstack1lllll111l1_opy_ is not None:
            args = list(bstack1lllll111l1_opy_)
        elif bstack1lllll11l1l_opy_ is not None:
            if isinstance(bstack1lllll11l1l_opy_, str):
                args = [bstack1lllll11l1l_opy_]
            elif isinstance(bstack1lllll11l1l_opy_, list):
                args = list(bstack1lllll11l1l_opy_)
            else:
                args = [bstack11ll111_opy_ (u"ࠢ࠯ࠤᄐ")]
        else:
            args = [bstack11ll111_opy_ (u"ࠣ࠰ࠥᄑ")]
        if bstack1lllll1111l_opy_:
            return _1lllll111ll_opy_(args)
        bstack1lllll1l1l1_opy_ = args + [
            bstack11ll111_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥᄒ"),
            bstack11ll111_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦᄓ")
        ]
        class bstack1lllll1l111_opy_:
            bstack11ll111_opy_ (u"ࠦࠧࠨࡐࡺࡶࡨࡷࡹࠦࡰ࡭ࡷࡪ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡰࡵࡷࡵࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡷࡩࡸࡺࠠࡪࡶࡨࡱࡸ࠴ࠢࠣࠤᄔ")
            def __init__(self):
                self.bstack1lllll11111_opy_ = []
                self.test_files = set()
                self.bstack1lllll11ll1_opy_ = None
            def pytest_collection_finish(self, session):
                bstack11ll111_opy_ (u"ࠧࠨࠢࡉࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠴ࠢࠣࠤᄕ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lllll11111_opy_.append(nodeid)
                        if bstack11ll111_opy_ (u"ࠨ࠺࠻ࠤᄖ") in nodeid:
                            file_path = nodeid.split(bstack11ll111_opy_ (u"ࠢ࠻࠼ࠥᄗ"), 1)[0]
                            if file_path.endswith(bstack11ll111_opy_ (u"ࠨ࠰ࡳࡽࠬᄘ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll11ll1_opy_ = str(e)
        collector = bstack1lllll1l111_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1lllll1l1l1_opy_, plugins=[collector])
        if collector.bstack1lllll11ll1_opy_:
            return {bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᄙ"): False, bstack11ll111_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤᄚ"): 0, bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧᄛ"): [], bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤᄜ"): [], bstack11ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᄝ"): bstack11ll111_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᄞ").format(collector.bstack1lllll11ll1_opy_)}
        return {
            bstack11ll111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᄟ"): True,
            bstack11ll111_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣᄠ"): len(collector.bstack1lllll11111_opy_),
            bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦᄡ"): collector.bstack1lllll11111_opy_,
            bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣᄢ"): sorted(collector.test_files),
            bstack11ll111_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣᄣ"): exit_code
        }
    except Exception as e:
        return {bstack11ll111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᄤ"): False, bstack11ll111_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨᄥ"): 0, bstack11ll111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤᄦ"): [], bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨᄧ"): [], bstack11ll111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᄨ"): bstack11ll111_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᄩ").format(e)}
def _1lllll111ll_opy_(args):
    bstack11ll111_opy_ (u"ࠧࠨࠢࡊࡵࡲࡰࡦࡺࡥࡥࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡤࠡ࡫ࡱࠤࡦࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡿࡴࡦࡵࡷࠤ࡮ࡹࡳࡶࡧࡶ࠲ࠧࠨࠢᄪ")
    bstack1llll1lllll_opy_ = [sys.executable, bstack11ll111_opy_ (u"ࠨ࠭࡮ࠤᄫ"), bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᄬ"), bstack11ll111_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤᄭ"), bstack11ll111_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥᄮ")]
    bstack1lllll11lll_opy_ = [a for a in args if a not in (bstack11ll111_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦᄯ"), bstack11ll111_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧᄰ"), bstack11ll111_opy_ (u"ࠧ࠳ࡱࠣᄱ"))]
    cmd = bstack1llll1lllll_opy_ + bstack1lllll11lll_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lllll11111_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack11ll111_opy_ (u"ࠨࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᄲ") in line.lower():
                continue
            if bstack11ll111_opy_ (u"ࠢ࠻࠼ࠥᄳ") in line:
                bstack1lllll11111_opy_.append(line)
                file_path = line.split(bstack11ll111_opy_ (u"ࠣ࠼࠽ࠦᄴ"), 1)[0]
                if file_path.endswith(bstack11ll111_opy_ (u"ࠩ࠱ࡴࡾ࠭ᄵ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack11ll111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄶ"): success,
            bstack11ll111_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄷ"): len(bstack1lllll11111_opy_),
            bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄸ"): bstack1lllll11111_opy_,
            bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᄹ"): sorted(test_files),
            bstack11ll111_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥᄺ"): proc.returncode,
            bstack11ll111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᄻ"): None if success else bstack11ll111_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࡪࡾࡩࡵࠢࡾࢁ࠮ࠨᄼ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack11ll111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄽ"): False, bstack11ll111_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄾ"): 0, bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄿ"): [], bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᅀ"): [], bstack11ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᅁ"): bstack11ll111_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᅂ").format(e)}