from cuga.backend.activity_tracker.tracker import ActivityTracker, Step
from cuga.backend.cuga_graph.nodes.shared.base_agent import create_partial
from cuga.backend.cuga_graph.nodes.shared.base_node import BaseNode
from cuga.backend.cuga_graph.state.agent_state import AgentState
from cuga.backend.cuga_graph.nodes.task_decomposition_planning.location_resolver_agent.location_resolver_agent import (
    LocationResolverAgent,
)
from langchain_core.messages import AIMessage

tracker = ActivityTracker()


class LocationSolver(BaseNode):
    def __init__(self, agent: LocationResolverAgent):
        super().__init__()
        self.name = "LocationResolver"
        self.agent = agent
        self.node = create_partial(
            LocationSolver.node_handler,
            agent=self.agent,
            name=self.name,
        )

    @staticmethod
    async def node_handler(state: AgentState, agent: LocationResolverAgent, name: str) -> AgentState:
        res: AIMessage = await agent.run(state.input)
        state.sender = name
        if res.content:
            tracker.collect_step(Step(name=name, data=res.content))
            state.task_analyzer_output.resolved_intent = res.content
        return state
        # if attrs.requires_location_search:
        #     return Command(update=state.model_dump(),goto="LocationResolverAgent")
        # else:
        #     return Command(update=state.model_dump(),goto="TaskDecompositionAgent")
