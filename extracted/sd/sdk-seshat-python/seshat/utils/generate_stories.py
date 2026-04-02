import shutil
from pathlib import Path
from typing import Type, Optional

import simplejson as json

from seshat import transformer
from seshat.general import transformer_story
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    BaseChallenge,
    Describable,
)
from seshat.utils.find_classes import find_classes


class StoryGenerator:
    def _get_doc(self, target: Type[Describable]):
        docs = []
        for d in find_classes((transformer, transformer_story), target):
            try:
                docs.append(d().generate_doc())
            except Exception:
                import traceback

                print(f"ERROR generating doc for {d}:")
                print(f"  Class: {d}")
                traceback.print_exc()
                raise
        return docs

    def _get_doc_hierarchical(self, target: Type[Describable]):
        story_classes = find_classes((transformer, transformer_story), target)
        transformer_to_story = {}
        for story_cls in story_classes:
            if hasattr(story_cls, "transformer"):
                transformer_to_story[story_cls.transformer] = story_cls

        all_transformers = set(transformer_to_story.keys())
        used = set()

        def build_node(transformer_cls):
            used.add(transformer_cls)

            node = {
                "class_name": transformer_cls.__name__,
                "path": transformer_cls.__module__,
                "story": transformer_to_story[transformer_cls]().generate_doc(),
            }

            # Find children: direct subclasses not yet used
            children = []
            for child_cls in all_transformers:
                if child_cls not in used and transformer_cls in child_cls.__bases__:
                    children.append(build_node(child_cls))

            if children:
                node["children"] = children

            return node

        # Find roots: classes with no parent in our set
        roots = []
        for transformer_cls in all_transformers:
            if transformer_cls not in used:
                has_parent = any(
                    base in all_transformers for base in transformer_cls.__bases__
                )
                if not has_parent:
                    roots.append(build_node(transformer_cls))

        return roots

    def generate(self, hierarchical: bool = True):
        transformers = (
            self._get_doc_hierarchical(BaseTransformerStory)
            if hierarchical
            else self._get_doc(BaseTransformerStory)
        )
        return json.dumps(
            {
                "transformers": transformers,
                "challenges": self._get_doc(BaseChallenge),
            },
            indent=4,
            default=str,
            ignore_nan=True,
        )


def generate_story(file_path: Optional[Path] = None, hierarchical: bool = True):
    """
    Generate story files. Works both in build process and after build.

    Args:
        file_path: Optional output path for the story file. If None, only saves to seshat_dir.
        hierarchical: If True, generate hierarchical format, else flat format.
    """
    seshat_dir = Path(__file__).parent.parent

    # Determine pre-generated file name
    filename = "_story-hierarchical.json" if hierarchical else "_story.json"
    pre_generated_file = seshat_dir / filename

    # Generate if doesn't exist
    if not pre_generated_file.exists():
        print(f"Generating {'hierarchical' if hierarchical else 'flat'} story...")
        generator = StoryGenerator()
        result = generator.generate(hierarchical=hierarchical)
        pre_generated_file.write_text(result)
        print(f"Story written to {pre_generated_file}")
        return

    # Copy to file_path if provided and different from source
    if file_path and file_path.resolve() != pre_generated_file.resolve():
        shutil.copy2(pre_generated_file, file_path)
    print(f"Story written to {file_path or pre_generated_file}")


if __name__ == "__main__":
    # Generate both hierarchical and flat formats
    generate_story(hierarchical=True)
    generate_story(hierarchical=False)
