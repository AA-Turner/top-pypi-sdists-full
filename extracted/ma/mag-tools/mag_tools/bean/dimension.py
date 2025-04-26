from dataclasses import dataclass, field
from typing import Optional

from mag_tools.bean.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils
from mag_tools.utils.data.value_utils import ValueUtils


@dataclass
class Dimension(BaseData):
    nx: Optional[int] = field(default=None, metadata={
        'min': 10,
        'max': 9999,
        'description': '行数'})
    ny: Optional[int] = field(default=None, metadata={
        'min': 10,
        'max': 9999,
        'description': '列数'})
    nz: Optional[int] = field(default=None, metadata={
        'min': 10,
        'max': 9999,
        'description': '层数'})
    ngrid: Optional[int] = field(default=None, metadata={'description': '总网格数'})

    @classmethod
    def from_block(cls, block_lines):
        if block_lines is None or len(block_lines) < 1:
            return None

        block_lines = [StringUtils.pick_head(line, '#') if '#' in line else line for line in block_lines]

        block_lines = ListUtils.trim(block_lines)

        return cls.__from_text(' '.join(block_lines))

    def to_block(self):
        if self.nx is not None and self.ny is not None and self.nz is not None and self.ngrid is not None:
            return []

        lines = ['DIMENS', self.__to_text()]
        return lines

    @property
    def size(self):
        if self.nx is not None and self.ny is not None and self.nz is not None:
            return self.nx * self.ny * self.nz
        else:
            return self.ngrid

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.nx, self.ny, self.nz

    @classmethod
    def random_generate(cls):
        dimens = cls()
        dimens.set_random_value('nx', 10000)
        dimens.set_random_value('ny', 1000)
        dimens.set_random_value('nz', 100)
        return dimens

    @classmethod
    def __from_text(cls, text):
        if not text:
            return None

        numbers = ValueUtils.pick_numbers(text)
        nx = numbers[0] if len(numbers) == 3 else None
        ny = numbers[1] if len(numbers) == 3 else None
        nz = numbers[2] if len(numbers) == 3 else None
        ngrid = numbers[0] if len(numbers) == 1 else None
        return cls(nx=nx, ny=ny, nz=nz, ngrid=ngrid)

    def __to_text(self):
        if self.nx and self.ny and self.nz:
            return f' {self.nx} {self.ny} {self.nz}'
        elif self.ngrid:
            return f' {self.ngrid}'