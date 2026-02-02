# Auto-generated, do not edit directly. Run `make generate_strategy_info` to update.

import enum

from pydantic import BaseModel


class StrategyName(str, enum.Enum):
    NATURAL_EDIT_CLAUDE_3_7_XML = "NATURAL_EDIT_CLAUDE_3_7_XML"
    READ_ONLY = "READ_ONLY"
    NATURAL_EDIT_CLAUDE_3_7_XML_WITH_STEPS = "NATURAL_EDIT_CLAUDE_3_7_XML_WITH_STEPS"
    NATURAL_EDIT_CLAUDE_3_7_FUNCTION_CALLING = (
        "NATURAL_EDIT_CLAUDE_3_7_FUNCTION_CALLING"
    )
    SEARCH_REPLACE_FUNCTION_CALLING = "SEARCH_REPLACE_FUNCTION_CALLING"
    FULL_FILE_REWRITE = "FULL_FILE_REWRITE"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    RAW_GPT = "RAW_GPT"
    NATURAL_EDIT = "NATURAL_EDIT"
    AGENT = "AGENT"
    AGENT_STEP = "AGENT_STEP"
    DATABASE = "DATABASE"
    DATABASE_AGENT = "DATABASE_AGENT"
    DATABASE_AGENT_STEP = "DATABASE_AGENT_STEP"
    REVIEW_FILES = "REVIEW_FILES"
    EXPLORE_CODEBASE = "EXPLORE_CODEBASE"
    GENERATE_REVIEW = "GENERATE_REVIEW"
    CUSTOM_STEP = "CUSTOM_STEP"


class StrategyInfo(BaseModel):
    strategy_name: StrategyName
    display_name: str
    description: str
    disabled: bool
    display_order: int
    is_agentic: bool


STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT_CLAUDE_3_7_XML,
        display_name="Natural Edit Claude 3.7 XML",
        description="A natural file editing strategy that uses Claude 3.7 XML.",
        disabled=False,
        display_order=-1,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.READ_ONLY,
        display_name="Read Only",
        description="A strategy that allows you to read the codebase.",
        disabled=False,
        display_order=-1,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT_CLAUDE_3_7_XML_WITH_STEPS,
        display_name="Natural Edit Claude 3.7 XML with Steps",
        description="A natural file editing strategy that uses Claude 3.7 XML with steps.",
        disabled=True,
        display_order=0,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT_CLAUDE_3_7_FUNCTION_CALLING,
        display_name="Natural Edit Claude 3.7 Function Calling",
        description="A natural file editing strategy that uses Claude 3.7 Function Calling.",
        disabled=True,
        display_order=0,
        is_agentic=True,
    ),
    StrategyInfo(
        strategy_name=StrategyName.SEARCH_REPLACE_FUNCTION_CALLING,
        display_name="Search Replace Function Calling",
        description="A search replace strategy that uses Function Calling.",
        disabled=True,
        display_order=0,
        is_agentic=True,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=2,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FUNCTION_CALLING,
        display_name="Function Calling",
        description="Using native function calling.",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.RAW_GPT,
        display_name="Raw GPT",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT,
        display_name="Natural Edit",
        description="Deprecated",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.AGENT,
        display_name="Agent",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=True,
    ),
    StrategyInfo(
        strategy_name=StrategyName.AGENT_STEP,
        display_name="Agent Step",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.DATABASE,
        display_name="Database",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.DATABASE_AGENT,
        display_name="Database Agent",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=True,
    ),
    StrategyInfo(
        strategy_name=StrategyName.DATABASE_AGENT_STEP,
        display_name="Database Agent Step",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.REVIEW_FILES,
        display_name="Review Files",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.EXPLORE_CODEBASE,
        display_name="Explore Codebase",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.GENERATE_REVIEW,
        display_name="Generate Review",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.CUSTOM_STEP,
        display_name="Custom Step",
        description="No description",
        disabled=True,
        display_order=99,
        is_agentic=False,
    ),
]


ENABLED_STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT_CLAUDE_3_7_XML,
        display_name="Natural Edit Claude 3.7 XML",
        description="A natural file editing strategy that uses Claude 3.7 XML.",
        disabled=False,
        display_order=-1,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.READ_ONLY,
        display_name="Read Only",
        description="A strategy that allows you to read the codebase.",
        disabled=False,
        display_order=-1,
        is_agentic=False,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=2,
        is_agentic=False,
    ),
]
