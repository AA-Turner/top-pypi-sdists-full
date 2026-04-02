from seshat.general.transformer_story.base import BaseChallenge, Approach
from seshat.transformer.aggregator.field import FieldAggregator
from seshat.transformer.deriver import Tagger
from seshat.transformer.deriver.branch_classifier import BranchClassifier
from seshat.transformer.merger import NestedKeyMerger, Merger

from seshat.transformer.pipeline.branch import Branch
from seshat.transformer.trimmer import LowTransactionTrimmer, InclusionTrimmer


class FilterSFrameBasedOnExistenceInAnotherSFrame(BaseChallenge):
    goal = (
        "There are two SFrames. We want to either remove or keep rows in the main SFrame "
        "based on whether corresponding keys exist in another SFrame. "
        "For example, if we have an SFrame containing top contract addresses, we may want "
        "to keep only the transactions associated with them."
    )
    approaches = [
        Approach(
            "Using Merger",
            involved_transformers={
                Merger: (
                    "Use Merger to join the main SFrame with the reference SFrame using a shared key. "
                    "Set `merge_how='inner'` to keep only matching rows (equivalent to `exclude=False`), "
                    "or `merge_how='left'` followed by filtering out nulls to remove matching rows "
                    "(equivalent to `exclude=True`). "
                    "This method simulates InclusionTrimmer behavior using join logic."
                )
            },
        ),
        Approach(
            "Using InclusionTrimmer",
            involved_transformers={
                InclusionTrimmer: (
                    "InclusionTrimmer is designed specifically for this use case. "
                    "It checks whether the specified column values exist in another SFrame "
                    "and keeps or removes rows accordingly."
                )
            },
        ),
    ]
    criteria = (
        "It is generally recommended to use InclusionTrimmer, which is specifically designed "
        "for this purpose. Although Merger can produce the same result, it requires the correct "
        "configuration of `right_schema` to ensure that unnecessary columns are not appended "
        "to the input SFrame."
    )


class SelectTopK(BaseChallenge):
    goal = (
        "We have a dataset and want to compute a metric, keeping only the rows "
        "that meet a threshold based on that metric."
    )
    approaches = [
        Approach(
            "For Ethereum transactions when the selection is based on transaction count",
            involved_transformers={
                LowTransactionTrimmer: (
                    "LowTransactionTrimmer is designed for Ethereum transaction data. "
                    "It identifies top addresses based on transaction count and keeps "
                    "only the transactions related to those addresses. "
                    "However, it is limited to filtering based on transaction count only."
                )
            },
        ),
        Approach(
            "Compute a complex metric and select rows that satisfy the condition in a general way",
            involved_transformers={
                FieldAggregator: (
                    "FieldAggregator can be used to compute the desired metric. "
                    "While other methods could also be used to calculate metrics, "
                    "FieldAggregator is commonly used in most scenarios."
                ),
                Merger: (
                    "After computing the metric, Merger can be used to filter "
                    "and retain rows that meet the desired condition."
                ),
                InclusionTrimmer: (
                    "InclusionTrimmer can also be used as an alternative method "
                    "to filter rows based on the computed metric."
                ),
            },
        ),
    ]
    criteria = (
        "LowTransactionTrimmer is a simpler solution when working with cryptocurrency "
        "transaction data and filtering based solely on transaction count. "
        "However, for more complex scenarios, a combination of FieldAggregator, Merger, "
        "or InclusionTrimmer is preferred. These allow you to compute advanced metrics, "
        "create new features, and apply flexible filtering logic."
    )


class ProcessDataBasedOnGroupingCriteria(BaseChallenge):
    goal = (
        "Process data differently based on grouping criteria (timestamp ranges, categories, etc.). "
        "After processing each group separately, merge results back into a single SFrame."
    )
    approaches = [
        Approach(
            "Using Tagger + BranchClassifier + Branch + NestedKeyMerger pattern",
            involved_transformers={
                Tagger: (
                    "Use Tagger to create classification labels based on filters (e.g., timestamp ranges). "
                    "Tagger applies multiple filters and attaches labels to rows that pass each filter. "
                    "This creates the column that BranchClassifier will use for grouping."
                ),
                BranchClassifier: (
                    "Split data into groups based on the labeled column from Tagger. "
                    "Each unique label creates a separate SFrame with a key matching the label."
                ),
                Branch: (
                    "Apply different pipelines to each group. The `pipe_map` keys must match "
                    "the group keys generated by BranchClassifier."
                ),
                NestedKeyMerger: (
                    "Merge results back into a single SFrame. NestedKeyMerger searches for a specific "
                    "key (typically 'default') in the nested GroupSFrame structure and merges all frames."
                ),
            },
        ),
    ]
    criteria = (
        "Use Tagger + BranchClassifier + Branch + NestedKeyMerger when processing data differently "
        "by grouping criteria. Workflow: Tagger (label) → BranchClassifier (split) → Branch (process) → "
        "NestedKeyMerger (combine). Common for timestamp-based grouping (e.g., 'last_day', 'last_week') "
        "or category-based processing. Can be nested for hierarchical grouping."
    )
