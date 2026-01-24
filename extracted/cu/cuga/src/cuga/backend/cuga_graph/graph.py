from typing import Optional

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from cuga.backend.cuga_graph.nodes.browser.action_agent.action_agent import ActionAgent
from cuga.backend.cuga_graph.nodes.api.api_code_planner_agent.api_code_planner_agent import (
    APICodePlannerAgent,
)
from cuga.backend.cuga_graph.nodes.api.api_planner_agent.api_planner_agent import APIPlannerAgent
from cuga.backend.cuga_graph.nodes.api.code_agent.code_agent import CodeAgent
from cuga.backend.cuga_graph.nodes.api.shortlister_agent.shortlister_agent import ShortlisterAgent
from cuga.backend.cuga_graph.nodes.answer.final_answer_agent.final_answer_agent import FinalAnswerAgent
from cuga.backend.cuga_graph.nodes.browser.action import ActionNode
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.analyze_task import TaskAnalyzer
from cuga.backend.cuga_graph.nodes.api.api_code_agent import ApiCoder
from cuga.backend.cuga_graph.nodes.api.api_code_planner import ApiCodePlanner
from cuga.backend.cuga_graph.nodes.api.api_planner import ApiPlanner
from cuga.backend.cuga_graph.nodes.api.api_shortlister import ApiShortlister
from cuga.backend.cuga_graph.nodes.chat.chat import ChatNode
from cuga.backend.cuga_graph.nodes.answer.final_answer import FinalAnswerNode
from cuga.backend.cuga_graph.nodes.human_in_the_loop.suggest_actions import SuggestHumanActions
from cuga.backend.cuga_graph.nodes.human_in_the_loop.wait_for_response import WaitForResponse
from cuga.backend.cuga_graph.nodes.shared.interrupt_tool_node import InterruptToolNode
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.plan_controller import PlanControllerNode
from cuga.backend.cuga_graph.nodes.browser.browser_planner import PlannerNode
from cuga.backend.cuga_graph.nodes.browser.qa_agent_node import QaNode
from cuga.backend.cuga_graph.nodes.save_reuse.save_reuse_node import SaveReuseNode
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.task_decomposition import TaskDecompositionNode
from cuga.backend.cuga_graph.state.agent_state import AgentState
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.plan_controller_agent.plan_controller_agent import (
    PlanControllerAgent,
)
from cuga.backend.cuga_graph.nodes.browser.browser_planner_agent.browser_planner_agent import (
    BrowserPlannerAgent,
)
from cuga.backend.cuga_graph.nodes.browser.qa_agent.qa_agent import QaAgent
from cuga.backend.cuga_graph.nodes.save_reuse.save_reuse_agent.reuse_agent import ReuseAgent
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.task_analyzer_agent.task_analyzer_agent import (
    TaskAnalyzerAgent,
)
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.task_decomposition_agent.task_decomposition_agent import (
    TaskDecompositionAgent,
)
from cuga.backend.cuga_graph.nodes.cuga_lite.cuga_lite_node import CugaLiteNode
from cuga.backend.cuga_graph.nodes.cuga_lite.cuga_lite_graph import (
    create_cuga_lite_graph,
)
from cuga.backend.cuga_graph.nodes.cuga_lite.combined_tool_provider import CombinedToolProvider
from cuga.backend.cuga_graph.nodes.cuga_lite.tool_provider_interface import ToolProviderInterface
from cuga.backend.cuga_graph.policy.configurable import PolicyConfigurable
from cuga.backend.llm.models import LLMManager
from cuga.config import settings


class DynamicAgentGraph:
    def __init__(
        self,
        configurations,
        langfuse_handler=None,
        policy_system: Optional[PolicyConfigurable] = None,
        tool_provider: Optional[ToolProviderInterface] = None,
    ):
        self.task_decomposition_agent = TaskDecompositionNode(TaskDecompositionAgent.create())
        self.plan_controller_agent = PlanControllerNode(PlanControllerAgent.create())
        self.final_answer_agent = FinalAnswerNode(FinalAnswerAgent.create())
        self.planner = PlannerNode(BrowserPlannerAgent.create())
        self.followup = SuggestHumanActions()
        self.followup_response = WaitForResponse()
        self.reuse = SaveReuseNode(ReuseAgent.create())
        self.chat: Optional[ChatNode] = None
        self.qa = QaNode(QaAgent.create())
        self.interrupt_tool_node = InterruptToolNode()
        self.task_analyzer = TaskAnalyzer(TaskAnalyzerAgent.create())
        self.action_agent = ActionNode(ActionAgent.create())
        self.api_code_planner = ApiCodePlanner(APICodePlannerAgent.create())
        self.api_planner = ApiPlanner(APIPlannerAgent.create())
        self.api_shortlister = ApiShortlister(ShortlisterAgent.create())
        self.api_coder = ApiCoder(CodeAgent.create())
        self.cuga_lite = CugaLiteNode(langfuse_handler=langfuse_handler)
        self.langfuse_handler = langfuse_handler
        self.policy_system = policy_system or PolicyConfigurable.get_instance()
        self.tool_provider = tool_provider
        self.graph = None

    async def build_graph(self):
        graph = StateGraph(AgentState)
        await self.add_nodes(graph)
        self.add_edges(graph)

        # Compile with policy_system in configurable
        self.graph = graph.compile(
            checkpointer=MemorySaver(),
            interrupt_after=[self.action_agent.action_agent.name, self.interrupt_tool_node.name],
        )

        # Store policy_system for passing to config
        self._policy_system = self.policy_system

    def get_config_with_policy(self, base_config: dict = None) -> dict:
        """
        Get config dict with policy_system included in configurable.

        Args:
            base_config: Base configuration dict to merge with

        Returns:
            Config dict with policy_system in configurable
        """
        config = base_config or {}
        if "configurable" not in config:
            config["configurable"] = {}

        config["configurable"]["policy_system"] = self.policy_system
        return config

    async def add_nodes(self, graph):
        self.chat = await ChatNode.create()
        graph.add_node(
            self.chat.chat_agent.name,
            self.chat.node,
        )
        graph.add_node(
            self.task_decomposition_agent.task_decomposition_agent.name,
            self.task_decomposition_agent.node,
        )
        graph.add_node(self.followup.name, self.followup.node)
        graph.add_node(self.followup_response.name, self.followup_response.node)
        graph.add_node(self.reuse.name, self.reuse.node)
        graph.add_node(self.planner.browser_planner_agent.name, self.planner.node)
        graph.add_node(self.action_agent.action_agent.name, self.action_agent.node)
        graph.add_node(self.plan_controller_agent.plan_controller_agent.name, self.plan_controller_agent.node)
        graph.add_node(self.final_answer_agent.final_answer_agent.name, self.final_answer_agent.node)
        graph.add_node(self.qa.qa_agent.name, self.qa.node)
        graph.add_node(self.task_analyzer.name, self.task_analyzer.node)
        graph.add_node(self.interrupt_tool_node.name, self.interrupt_tool_node.node)
        graph.add_node(self.api_code_planner.agent.name, self.api_code_planner.node)
        graph.add_node(self.api_shortlister.agent.name, self.api_shortlister.node)
        graph.add_node(self.api_coder.agent.name, self.api_coder.node)
        graph.add_node(self.api_planner.agent.name, self.api_planner.node)

        # Add CugaLite entry node
        graph.add_node(self.cuga_lite.name, self.cuga_lite.node)

        # Create and add CugaLite subgraph
        # Use provided tool provider or create default CombinedToolProvider
        tool_provider = self.tool_provider or CombinedToolProvider()
        await tool_provider.initialize()

        # Get apps for apps_list
        apps = await tool_provider.get_apps()
        apps_list = [app.name for app in apps] if apps else None

        # Initialize LLM
        llm_manager = LLMManager()
        model_config = settings.agent.code.model.copy()
        model_config["streaming"] = False
        model = llm_manager.get_model(model_config)

        # Create the CugaLite subgraph (tools will be fetched dynamically from tool_provider)
        # Note: This subgraph is created at build time (before any invocation).
        # The policy_system is NOT passed here because it's accessed at runtime via
        # config["configurable"]["policy_system"]. When the main graph invokes this
        # subgraph node, LangGraph automatically passes the config down to the subgraph's
        # nodes (prepare_tools_and_apps), where PolicyEnactment.check_and_enact() extracts it.
        cuga_lite_subgraph = create_cuga_lite_graph(
            model=model,
            prompt=None,  # Will be created dynamically from state
            tool_provider=tool_provider,
            apps_list=apps_list,
            callbacks=[self.langfuse_handler] if self.langfuse_handler else None,
        )

        # Compile and add as a subgraph node
        # The compiled subgraph will receive config from parent graph at runtime
        compiled_cuga_lite_subgraph = cuga_lite_subgraph.compile()
        graph.add_node("CugaLiteSubgraph", compiled_cuga_lite_subgraph)

        # Add callback node to process results after subgraph
        graph.add_node("CugaLiteCallback", self.cuga_lite.callback_node)

    def add_edges(self, graph):
        graph.add_edge(START, self.chat.chat_agent.name)
        graph.add_edge(
            self.task_decomposition_agent.task_decomposition_agent.name,
            self.plan_controller_agent.plan_controller_agent.name,
        )
        graph.add_edge(self.interrupt_tool_node.name, self.plan_controller_agent.plan_controller_agent.name)
        graph.add_edge(self.qa.qa_agent.name, self.planner.browser_planner_agent.name)
        graph.add_edge(self.final_answer_agent.final_answer_agent.name, END)
        graph.add_edge(self.action_agent.action_agent.name, self.planner.browser_planner_agent.name)

        # CugaLite subgraph flow: CugaLiteSubgraph -> CugaLiteCallback
        graph.add_edge("CugaLiteSubgraph", "CugaLiteCallback")
