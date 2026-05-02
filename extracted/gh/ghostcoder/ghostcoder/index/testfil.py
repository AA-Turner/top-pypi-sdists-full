
import logging
# ...


class CodeBlock(BaseModel):
    # ...
    merge_history: List[MergeAction] = []
    children: List["CodeBlock"] = []
    parent: Optional["CodeBlock"] = None
    # ...

    def insert_child(self, index: int, child: "CodeBlock"):
        if index == 0 and self.children[0].pre_lines == 0:
            self.children[0].pre_lines = 1

        self.children.insert(index, child)
        child.parent = self

    def insert_children(self, index: int, children: List["CodeBlock"]):
        for child in children:
            self.insert_child(index, child)
            index += 1
    # ...

    def find_next_matching_child_block(self, children_start, other_child_block):
        i = children_start
        while i < len(self.children):
            check_original_block = self.children[i]
            if (check_original_block.content
                    and check_original_block.content == other_child_block.content
                    and check_original_block.type == other_child_block.type):
                return i
            i += 1
        return None
    # ...

    def find_next_commented_out(self, start):
        i = start
        while i < len(self.children):
            if self.children[i].type == CodeBlockType.COMMENTED_OUT_CODE:
                return i
            i += 1
        return None
    # ...

    def most_similar_block(self,
                           other_block: "CodeBlock",
                           start_original: int):
        """Naive solution for finding similar blocks."""
        # TODO: Check identifier and parameters

        max_similarity = 0
        max_i = None

        i = start_original
        while i < len(self.children):
            if self.children[i].type == other_block.type:
                common_chars = sum(
                    c1 == c2 for c1, c2 in zip(self.children[i].content, other_block.content))
                if common_chars > max_similarity:
                    max_similarity = common_chars
                    max_i = i
            i += 1
        return max_i

    def find_matching_pairs(self, other_block: "CodeBlock") -> List[Tuple["CodeBlock", "CodeBlock"]]:
        matching_pairs = []

        for child_block in other_block.children:
            if child_block.type in NON_CODE_BLOCKS:
                continue
            matching_children = self.find_blocks_with_identifier(child_block.identifier)
            if len(matching_children) == 1:
                logging.debug(f"Found matching child block `{child_block.identifier}` in `{self.identifier}`")
                matching_pairs.append((matching_children[0], child_block))
            else:
                return []

        return matching_pairs

    def find_nested_matching_pairs(self, other_block: "CodeBlock") -> List[Tuple["CodeBlock", "CodeBlock"]]:
        for child_block in self.children:
            matching_children = child_block.find_matching_pairs(other_block)
            if matching_children:
                return matching_children

            matching_children = child_block.find_nested_matching_pairs(other_block)
            if matching_children:
                return matching_children

        return []
    # ...

    def _merge(self, updated_block: "CodeBlock"):
        logging.debug(f"Merging block `{self.type.value}: {self.identifier}` ({len(self.children)} children) with "
                      f"`{updated_block.type.value}: {updated_block.identifier}` ({len(updated_block.children)} children)")

        # Just replace if there are no code blocks in original block
        if len(self.children) == 0 or all(child.type in NON_CODE_BLOCKS for child in self.children):
            self.children = updated_block.children
            self.merge_history.append(MergeAction(action="replace_non_code_blocks"))

        # Find and replace if all children are matching
        update_pairs = self.find_matching_pairs(updated_block)
        if update_pairs:
            self.merge_history.append(
                MergeAction(action="all_children_match", original_block=self, updated_block=updated_block))

            for original_child, updated_child in update_pairs:
                original_child._merge(updated_child)

            return

        # Replace if block is complete
        if updated_block.is_complete():
            self.children = updated_block.children
            self.merge_history.append(MergeAction(action="replace_complete", original_block=self, updated_block=updated_block))

        self._merge_block_by_block(updated_block)

    def _merge_block_by_block(self, updated_block: "CodeBlock"):
        i = 0
        j = 0
        while j < len(updated_block.children):
            if i >= len(self.children):
                self.children.extend(updated_block.children[j:])
                return

            original_block_child = self.children[i]
            updated_block_child = updated_block.children[j]

            if original_block_child == updated_block_child:
                original_block_child.merge_history.append(MergeAction(action="is_same"))
                i += 1
                j += 1
            elif updated_block_child.type == CodeBlockType.COMMENTED_OUT_CODE:
                j += 1
                orig_next, update_next = self.find_next_matching_block(updated_block, i, j)

                for commented_out_child in self.children[i:orig_next]:
                    commented_out_child.merge_history.append(MergeAction(action="commented_out", original_block=commented_out_child, updated_block=None))

                i = orig_next
                if update_next > j:
                    #  Clean up commented out code at the end
                    last_updated_child = updated_block.children[update_next-1]
                    if last_updated_child.type == CodeBlockType.COMMENTED_OUT_CODE:
                        update_next -= 1

                    self.children[i:i] = updated_block.children[j:update_next]
                    i += update_next - j

                j = update_next
            elif (original_block_child.content == updated_block_child.content and
                  original_block_child.children and updated_block_child.children):
                original_block_child._merge(updated_block_child)
                i += 1
                j += 1
            elif original_block_child.content == updated_block_child.content:
                self.children[i] = updated_block_child
                i += 1
                j += 1
            elif updated_block_child:
                # we expect to update a block when the updated block is incomplete
                # and will try the find the most similar block.
                if not updated_block_child.is_complete():
                    similar_original_block = self.most_similar_block(updated_block_child, i)
                    logging.debug(f"Updated block with definition `{updated_block_child.content}` is not complete")
                    if similar_original_block == i:
                        self.merge_history.append(
                            MergeAction(action="replace_similar", original_block=original_block_child,
                                        updated_block=updated_block_child))

                        original_block_child = CodeBlock(
                            content=updated_block_child.content,
                            identifier=updated_block_child.identifier,
                            pre_code=updated_block_child.pre_code,
                            type=updated_block_child.type,
                            parent=self.parent,
                            children=original_block_child.children
                        )

                        self.children[i] = original_block_child

                        logging.debug(
                            f"Will replace similar original block definition: `{original_block_child.content}`")
                        original_block_child._merge(updated_block_child)
                        i += 1
                        j += 1

                        continue
                    elif not similar_original_block:
                        logging.debug(f"No most similar original block found to `{original_block_child.content}")
                    else:
                        logging.debug(f"Expected most similar original block to be `{original_block_child.content}, "
                                      f"but was {self.children[similar_original_block].content}`")

                next_original_match = self.find_next_matching_child_block(i, updated_block_child)
                next_updated_match = updated_block.find_next_matching_child_block(j, original_block_child)
                next_commented_out = updated_block.find_next_commented_out(j)

                if next_original_match:
                    self.merge_history.append(
                        MergeAction(action="next_original_match_replace", original_block=self.children[next_original_match],
                                    updated_block=updated_block_child))

                    # if it's not on the first level we expect the blocks to be replaced
                    self.children = self.children[:i] + self.children[next_original_match:]
                elif next_commented_out is not None and (
                        not next_updated_match or next_commented_out < next_updated_match):
                    # if there is commented out code after the updated block,
                    # we will insert the lines before the commented out block in the original block
                    self.merge_history.append(
                        MergeAction(action="next_commented_out_insert",
                                    original_block=original_block_child,
                                    updated_block=updated_block.children[next_commented_out]))

                    self.insert_children(i, updated_block.children[j:next_commented_out])
                    i += next_commented_out - j
                    j = next_commented_out
                elif next_updated_match:
                    # if there is a match in the updated block, we expect this to be an addition
                    # and insert the lines before in the original block
                    self.merge_history.append(
                        MergeAction(action="next_original_match_insert",
                                    original_block=original_block_child,
                                    updated_block=updated_block.children[next_updated_match]))

                    self.insert_children(i, updated_block.children[j:next_updated_match])
                    diff = next_updated_match - j
                    i += diff
                    j = next_updated_match
                else:
                    self.children.pop(i)
            else:
                self.insert_child(i, updated_block_child)
                j += 1
                i += 1
    # ...
# ...