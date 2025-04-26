import re
from typing import Any, Optional

class ListUtils:
    @staticmethod
    def split(input_list: list[Any], num_per_group: int):
        """
        将一个列表切分为包含 N 个元素的多个子列表

        :param input_list: 要切分的列表
        :param num_per_group: 每个子列表包含的元素数量
        :return: 包含多个子列表的列表
        """
        return [input_list[i:i + num_per_group] for i in range(0, len(input_list), num_per_group)]

    @staticmethod
    def split_by_keyword(lines: list[str], keyword: Optional[str] = None, at_head: bool = True)-> list[list[str]]:
        """
        根据关键字或空行将字符串数组切分成若干块。

        参数：
        :param lines: 字符串数组
        :param keyword: 关键字,为None或空时表示按空行分隔
        :param at_head: 关键字是否在块的首行
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        if keyword is None or keyword == '':
            return ListUtils.split_by_empty_line(lines)

        blocks = []
        current_block = []

        for line in lines:
            if keyword in line:
                if not at_head:
                    current_block.append(line)

                # 遇到关键字行时，如块内容不为空，则表示该块结束；如为空，则表示开始
                if current_block:
                    blocks.append(current_block)
                    current_block = []

                if at_head:
                    current_block.append(line)
            else:
                current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks

    @staticmethod
    def split_by_keywords(lines: list[str], keywords: list[str]) -> dict[str, list[str]]:
        segments = {keyword: [] for keyword in keywords}
        current_keyword = None

        for line in lines:
            if line in keywords:
                current_keyword = line
            segments[current_keyword].append(line)

        return segments

    @staticmethod
    def split_by_boundary(lines: list[str], keyword_map: dict[str, tuple[Optional[str], Optional[str]]]) -> dict[
        str, list[str]]:
        text = "\n".join(lines)
        segments = {segment_name: [] for segment_name in keyword_map}

        # 构建正则表达式模式
        keyword_patterns = {segment_name: re.escape(segment_name) for segment_name in keyword_map}
        for segment_name, (begin_keyword, end_keyword) in keyword_map.items():
            if begin_keyword is None and end_keyword is None:
                # 处理没有分界线的情况
                keywords = [keyword for keyword in keyword_map.keys()]
                return ListUtils.split_by_keywords(lines, keywords)
            else:
                # 处理有分界线的情况
                pattern = rf"{keyword_patterns[segment_name]}\n{re.escape(begin_keyword)}.*?\n{re.escape(end_keyword)}"
                matches = re.finditer(pattern, text, re.DOTALL)

                for match in matches:
                    block_lines = match.group().split("\n")
                    segments[segment_name].extend(block_lines)

        # 处理 BASE 段
        base_pattern = re.escape("BASE")
        base_matches = list(re.finditer(base_pattern, text))
        if base_matches:
            base_start = base_matches[0].start()
            next_keyword_start = min(
                (match.start() for match in re.finditer("|".join(keyword_patterns.values()), text) if
                 match.start() > base_start), default=len(text))
            segments["BASE"] = text[base_start:next_keyword_start].strip().split("\n")

        return segments

    @staticmethod
    def trim(lines: list[str]) -> list[str]:
        """
        去掉字符串数组的起始和结尾的空行
        :param lines: 字符串数组
        :return: 去掉空行后的字符串数组
        """
        # 去掉起始的空行
        while lines and lines[0].strip() == '':
            lines.pop(0)

        # 去掉结尾的空行
        while lines and lines[-1].strip() == '':
            lines.pop()

        return lines

    @staticmethod
    def pick_line_by_keyword(lines: list[str], keyword: str) -> str:
        return next((line for line in lines if keyword in line), None)

    @staticmethod
    def pick_line_by_any_keyword(lines: list[str], keywords: list[str]) -> Optional[str]:
        return next((line for line in lines if any(keyword in line for keyword in keywords)), None)

    @staticmethod
    def pick_block_include_keyword(lines: list[str], keyword: str) -> list[str]:
        """
        根据关键字查找并返回所有匹配的行
        :param lines: 待查找的行列表
        :param keyword: 查找的关键字
        :return: 包含关键字的所有行
        """
        return [line for line in lines if keyword in line]

    @staticmethod
    def pick_block_include_keywords(lines: list[str], keywords: list[str]) -> Optional[list[str]]:
        """
        从提供的文本行中挑选出包含任意一个关键字的行。
        :param lines: 一个包含多行文本的列表。
        :param keywords: 一个包含关键字的列表。
        """
        matching_lines = [line for line in lines if any(keyword in line for keyword in keywords)]
        return matching_lines if matching_lines else []

    @staticmethod
    def pick_block_by_keyword(lines: list[str], keyword: str, count: int = 1) -> Optional[list[str]]:
        idx = next((i for i, line in enumerate(lines) if keyword in line), None)
        if idx is not None and idx + count <= len(lines):
            return lines[idx:idx + count]
        return None

    @staticmethod
    def pick_head(lines: list[str], keyword: str) -> list[str]:
        if not keyword:
            idx = next((index for index, line in enumerate(lines) if not line.strip()), None)
        else:
            idx: Optional[int] = next((index for index, line in enumerate(lines) if keyword in line), None)
        return lines[:idx] if idx is not None else []

    @staticmethod
    def pick_tail(lines: list[str], keyword: str) -> list[str]:
        if not keyword:
            idx = next((index for index, line in enumerate(lines) if not line.strip()), None)
        else:
            idx: Optional[int] = next((index for index, line in enumerate(lines) if keyword in line), None)
        return lines[idx:] if idx is not None else []

    @staticmethod
    def pick_block(lines: list[str], begin_keyword: str, end_keyword: str) -> list[str]:
        if begin_keyword:
            start_index: Optional[int] = next((i for i, line in enumerate(lines) if begin_keyword in line.strip()), None)
        else:
            start_index: Optional[int] = next((i for i, line in enumerate(lines) if not line.strip()), None)

        if start_index is None:
            return []

        if end_keyword:
            end_index: Optional[int] = next((i for i, line in enumerate(lines) if end_keyword in line.strip() and i > start_index), None)
        else:
            end_index: Optional[int] = next((i for i, line in enumerate(lines) if not line.strip() and i > start_index), None)
        return lines[start_index:end_index+1] if start_index is not None and end_index is not None else []

    @staticmethod
    def find(lines: list[str], keyword: str) -> Optional[int]:
        return next((i for i, line in enumerate(lines) if keyword in line), None)

    @staticmethod
    def remove_by_keyword(lines: list[str], keyword: str) -> list[str]:
        return [line for line in lines if keyword not in line]

    @staticmethod
    def remove_by_header(lines: list[str], keyword: str) -> list[str]:
        return [line for line in lines if not line.startswith(keyword)]

    @staticmethod
    def clear_empty(lines: list[Any]) -> list[Any]:
        new_lines = []
        for line in lines:
            if isinstance(line, str):
                if line.strip():
                    new_lines.append(line)
            elif isinstance(line, list):
                if len(line) > 0:
                    new_lines.extend(ListUtils.clear_empty(line))
            elif isinstance(line, dict):
                if len(line) > 0:
                    new_lines.extend(line.values())
            elif isinstance(line, set):
                if len(line):
                    new_lines.extend(line)
            elif isinstance(line, tuple):
                if len(line):
                    new_lines.extend(line)
            elif line is not None:
                new_lines.append(line)

        return new_lines

    @staticmethod
    def split_by_empty_line(lines: list[str]) -> list[list[str]]:
        """
        根据空行将字符串数组切分成若干块，并删除空行。

        参数：
        :param lines: 字符串数组
        :return: 切分后的块列表，每个块是一个字符串数组
        """
        blocks = []
        current_block = []

        for line in lines:
            if line.strip() == '':
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks