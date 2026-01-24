# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
bstack1l1111_opy_ (u"ࠢࠣࠤࠍࡔࡾࡺࡥࡴࡶࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡮ࡥ࡭ࡲࡨࡶࠥࡻࡳࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࠤࡵࡿࡴࡦࡵࡷࠤ࡭ࡵ࡯࡬ࡵ࠱ࠎࠧࠨࠢႵ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llllll1l1l_opy_(bstack1llllll11l1_opy_=None, bstack1lllllll1l1_opy_=None):
    bstack1l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡅࡲࡰࡱ࡫ࡣࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡷࡩࡸࡺࡳࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠧࡴࠢ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤࡆࡖࡉࡴ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡧࡲࡨࡵࠣࠬࡱ࡯ࡳࡵ࠮ࠣࡳࡵࡺࡩࡰࡰࡤࡰ࠮ࡀࠠࡄࡱࡰࡴࡱ࡫ࡴࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡴࡾࡺࡥࡴࡶࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࡥ࡯ࡹࡩ࡯࡮ࡨࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥ࡬࡬ࡢࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡡ࡬ࡧࡶࠤࡵࡸࡥࡤࡧࡧࡩࡳࡩࡥࠡࡱࡹࡩࡷࠦࡴࡦࡵࡷࡣࡵࡧࡴࡩࡵࠣ࡭࡫ࠦࡢࡰࡶ࡫ࠤࡦࡸࡥࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡴࡦࡺࡨࡴࠢࠫࡰ࡮ࡹࡴࠡࡱࡵࠤࡸࡺࡲ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡔࡦࡵࡷࠤ࡫࡯࡬ࡦࠪࡶ࠭࠴ࡪࡩࡳࡧࡦࡸࡴࡸࡹࠩ࡫ࡨࡷ࠮ࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡪࡷࡵ࡭࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡇࡦࡴࠠࡣࡧࠣࡥࠥࡹࡩ࡯ࡩ࡯ࡩࠥࡶࡡࡵࡪࠣࡷࡹࡸࡩ࡯ࡩࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡣࡷ࡬ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡋࡪࡲࡴࡸࡥࡥࠢ࡬ࡪࠥࡺࡥࡴࡶࡢࡥࡷ࡭ࡳࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡯ࡴࡩࠢ࡮ࡩࡾࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡵࡸࡧࡨ࡫ࡳࡴࠢࠫࡦࡴࡵ࡬ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡦࡳࡺࡴࡴࠡࠪ࡬ࡲࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠ࡯ࡱࡧࡩ࡮ࡪࡳࠡࠪ࡯࡭ࡸࡺࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥ࡫ࡲࡳࡱࡵࠤ࠭ࡹࡴࡳࠫࠍࠤࠥࠦࠠࠣࠤࠥႶ")
    try:
        bstack1lllllll11l_opy_ = os.getenv(bstack1l1111_opy_ (u"ࠤࡓ࡝࡙ࡋࡓࡕࡡࡆ࡙ࡗࡘࡅࡏࡖࡢࡘࡊ࡙ࡔࠣႷ")) is not None
        if bstack1llllll11l1_opy_ is not None:
            args = list(bstack1llllll11l1_opy_)
        elif bstack1lllllll1l1_opy_ is not None:
            if isinstance(bstack1lllllll1l1_opy_, str):
                args = [bstack1lllllll1l1_opy_]
            elif isinstance(bstack1lllllll1l1_opy_, list):
                args = list(bstack1lllllll1l1_opy_)
            else:
                args = [bstack1l1111_opy_ (u"ࠥ࠲ࠧႸ")]
        else:
            args = [bstack1l1111_opy_ (u"ࠦ࠳ࠨႹ")]
        if bstack1lllllll11l_opy_:
            return _1lllllll111_opy_(args)
        bstack1llllll111l_opy_ = args + [
            bstack1l1111_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨႺ"),
            bstack1l1111_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢႻ")
        ]
        class bstack1llllll1lll_opy_:
            bstack1l1111_opy_ (u"ࠢࠣࠤࡓࡽࡹ࡫ࡳࡵࠢࡳࡰࡺ࡭ࡩ࡯ࠢࡷ࡬ࡦࡺࠠࡤࡣࡳࡸࡺࡸࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨࠥࡺࡥࡴࡶࠣ࡭ࡹ࡫࡭ࡴ࠰ࠥࠦࠧႼ")
            def __init__(self):
                self.bstack1lllll1llll_opy_ = []
                self.test_files = set()
                self.bstack1llllll11ll_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1l1111_opy_ (u"ࠣࠤࠥࡌࡴࡵ࡫ࠡࡥࡤࡰࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠰ࠥࠦࠧႽ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1lllll1llll_opy_.append(nodeid)
                        if bstack1l1111_opy_ (u"ࠤ࠽࠾ࠧႾ") in nodeid:
                            file_path = nodeid.split(bstack1l1111_opy_ (u"ࠥ࠾࠿ࠨႿ"), 1)[0]
                            if file_path.endswith(bstack1l1111_opy_ (u"ࠫ࠳ࡶࡹࠨჀ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1llllll11ll_opy_ = str(e)
        collector = bstack1llllll1lll_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llllll111l_opy_, plugins=[collector])
        if collector.bstack1llllll11ll_opy_:
            return {bstack1l1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨჁ"): False, bstack1l1111_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧჂ"): 0, bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣჃ"): [], bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧჄ"): [], bstack1l1111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣჅ"): bstack1l1111_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ჆").format(collector.bstack1llllll11ll_opy_)}
        return {
            bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧჇ"): True,
            bstack1l1111_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦ჈"): len(collector.bstack1lllll1llll_opy_),
            bstack1l1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢ჉"): collector.bstack1lllll1llll_opy_,
            bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦ჊"): sorted(collector.test_files),
            bstack1l1111_opy_ (u"ࠣࡧࡻ࡭ࡹࡥࡣࡰࡦࡨࠦ჋"): exit_code
        }
    except Exception as e:
        return {bstack1l1111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ჌"): False, bstack1l1111_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤჍ"): 0, bstack1l1111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧ჎"): [], bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤ჏"): [], bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧა"): bstack1l1111_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧბ").format(e)}
def _1lllllll111_opy_(args):
    bstack1l1111_opy_ (u"ࠣࠤࠥࡍࡸࡵ࡬ࡢࡶࡨࡨࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡧࠤ࡮ࡴࠠࡢࠢࡶࡩࡵࡧࡲࡢࡶࡨࠤࡕࡿࡴࡩࡱࡱࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࡺ࡯ࠡࡣࡹࡳ࡮ࡪࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡻࡷࡩࡸࡺࠠࡪࡵࡶࡹࡪࡹ࠮ࠣࠤࠥგ")
    bstack1llllll1111_opy_ = [sys.executable, bstack1l1111_opy_ (u"ࠤ࠰ࡱࠧდ"), bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥე"), bstack1l1111_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧვ"), bstack1l1111_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨზ")]
    bstack1llllll1ll1_opy_ = [a for a in args if a not in (bstack1l1111_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢთ"), bstack1l1111_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣი"), bstack1l1111_opy_ (u"ࠣ࠯ࡴࠦკ"))]
    cmd = bstack1llllll1111_opy_ + bstack1llllll1ll1_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1lllll1llll_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1l1111_opy_ (u"ࠤࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨლ") in line.lower():
                continue
            if bstack1l1111_opy_ (u"ࠥ࠾࠿ࠨმ") in line:
                bstack1lllll1llll_opy_.append(line)
                file_path = line.split(bstack1l1111_opy_ (u"ࠦ࠿ࡀࠢნ"), 1)[0]
                if file_path.endswith(bstack1l1111_opy_ (u"ࠬ࠴ࡰࡺࠩო")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1l1111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢპ"): success,
            bstack1l1111_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨჟ"): len(bstack1lllll1llll_opy_),
            bstack1l1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤრ"): bstack1lllll1llll_opy_,
            bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨს"): sorted(test_files),
            bstack1l1111_opy_ (u"ࠥࡩࡽ࡯ࡴࡠࡥࡲࡨࡪࠨტ"): proc.returncode,
            bstack1l1111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥუ"): None if success else bstack1l1111_opy_ (u"࡙ࠧࡵࡣࡲࡵࡳࡨ࡫ࡳࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࠨࡦࡺ࡬ࡸࠥࢁࡽࠪࠤფ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1l1111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢქ"): False, bstack1l1111_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨღ"): 0, bstack1l1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤყ"): [], bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨშ"): [], bstack1l1111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤჩ"): bstack1l1111_opy_ (u"ࠦࡘࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣც").format(e)}