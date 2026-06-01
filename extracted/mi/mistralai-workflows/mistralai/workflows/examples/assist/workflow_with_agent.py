import asyncio
import contextlib

from mistralai.client.models import ChatCompletionChoice, TextChunk, UsageInfo, WebSearchTool
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow
from mistralai.workflows.plugins.mistralai import MCPSSEConfig, MCPStdioConfig
from mistralai.workflows.plugins.mistralai.session.local_session import LocalSession
from mistralai.workflows.plugins.mistralai.session.mock_session import MockSession

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)


# ===== Deal Desk Workflow Activities =====


class ParseDealResult(BaseModel):
    deal_type: str = Field(..., description="Type of deal (e.g., 'enterprise', 'startup', 'partnership')")
    amount: float = Field(..., description="Deal amount in USD")
    customer_name: str = Field(..., description="Customer name")
    region: str = Field(..., description="Geographic region")


class RiskResult(BaseModel):
    risk_score: float = Field(..., description="Risk score from 0-100")
    risk_factors: list[str] = Field(..., description="List of identified risk factors")


class ComplianceResult(BaseModel):
    compliant: bool = Field(..., description="Whether the deal is compliant")
    issues: list[str] = Field(..., description="List of compliance issues if any")
    required_approvals: list[str] = Field(..., description="Required approvals")


class ContractResult(BaseModel):
    contract_terms: str = Field(..., description="Generated contract terms")
    payment_schedule: str = Field(..., description="Payment schedule")


@workflows.activity()
async def parse_deal_document(document_text: str) -> ParseDealResult:
    """Parse a deal document and extract key information."""
    logger.info("Activity: Parsing deal document", doc_length=len(document_text))
    # Mock: extract deal info
    result = ParseDealResult(
        deal_type="enterprise",
        amount=500000.0,
        customer_name="Acme Corp",
        region="EU",
    )
    logger.info("Activity: Deal parsed", deal_type=result.deal_type, amount=result.amount)
    return result


@workflows.activity()
async def calculate_risk_score(deal_type: str, amount: float, customer_name: str, region: str) -> RiskResult:
    """Calculate financial risk score for a deal."""
    logger.info("Activity: Calculating risk score", deal_type=deal_type, amount=amount)
    # Mock: calculate risk based on amount and region
    risk_score = min(100.0, amount / 10000.0)
    risk_factors = []
    if amount > 100000:
        risk_factors.append("High value transaction")
    if region in ["APAC", "LATAM"]:
        risk_factors.append("Emerging market region")

    result = RiskResult(risk_score=risk_score, risk_factors=risk_factors)
    logger.info("Activity: Risk calculated", risk_score=result.risk_score, factors=len(result.risk_factors))
    return result


@workflows.activity()
async def check_compliance(deal_type: str, amount: float, region: str) -> ComplianceResult:
    """Check regulatory compliance for a deal."""
    logger.info("Activity: Checking compliance", region=region, amount=amount)
    # Mock: check compliance rules
    compliant = amount < 1000000  # Deals over 1M need extra review
    issues = []
    required_approvals = ["legal"]

    if not compliant:
        issues.append("Amount exceeds threshold for automatic approval")
        required_approvals.extend(["cfo", "ceo"])

    if region == "EU":
        required_approvals.append("gdpr_officer")

    result = ComplianceResult(
        compliant=compliant,
        issues=issues,
        required_approvals=required_approvals,
    )
    logger.info("Activity: Compliance checked", compliant=result.compliant, issues=len(result.issues))
    return result


@workflows.activity()
async def generate_contract_terms(deal_type: str, amount: float, customer_name: str) -> ContractResult:
    """Generate contract terms for an approved deal."""
    logger.info("Activity: Generating contract terms", customer=customer_name, amount=amount)
    # Mock: generate contract language
    result = ContractResult(
        contract_terms=f"Standard {deal_type} agreement for {customer_name}",
        payment_schedule="Net 30 with quarterly installments",
    )
    logger.info("Activity: Contract generated", customer=customer_name)
    return result


# ===== Finance Workflow =====


class GetInterestRateParams(BaseModel):
    year: int = Field(..., description="The year to get the interest rate for")


class GetInterestRateResult(BaseModel):
    interest_rate: float


@workflows.activity()
async def get_interest_rate(params: GetInterestRateParams) -> GetInterestRateResult:
    """Get the interest rate of the European central bank for a given year."""
    logger.info("Activity: Getting interest rate", year=params.year)
    # mock data, in reality you would call an API here
    result = GetInterestRateResult(interest_rate=1.62)
    logger.info("Activity: Interest rate retrieved", year=params.year, rate=result.interest_rate)
    return result


class FinanceAgentWorkflowParams(BaseModel):
    question: str = Field(..., description="The question to ask the finance agent")
    mock_session: bool = Field(default=False, description="Whether to use a mock session instead of a local session")


class FinanceAgentWorkflowResult(BaseModel):
    answer: str = Field(..., description="The answer to the question")


async def _mock_chat_complete(
    request: workflows_mistralai.ChatCompletionRequest,
) -> workflows_mistralai.ChatCompletionResponse:
    """Mock chat completion that returns a canned response."""
    return workflows_mistralai.ChatCompletionResponse(
        id="mock",
        object="chat.completion",
        model=request.model,
        created=0,
        usage=UsageInfo(prompt_tokens=0, completion_tokens=0, total_tokens=0),
        choices=[
            ChatCompletionChoice(
                index=0,
                message=workflows_mistralai.AssistantMessage(content="The ECB interest rate for 2024 is 1.62%."),
                finish_reason="stop",
            )
        ],
    )


@workflows.workflow.define(name="finance_agent_workflow")
class FinanceAgentWorkflow:
    @workflows.workflow.entrypoint
    async def entrypoint(self, params: FinanceAgentWorkflowParams) -> FinanceAgentWorkflowResult:
        logger.info("Workflow: Starting finance agent workflow", question=params.question)

        session: LocalSession
        if params.mock_session:
            session = MockSession(chat_complete_callback=_mock_chat_complete)
        else:
            session = LocalSession()

        logger.info("Workflow: Creating ECB interest rate agent")
        ecb_interest_rate_agent = workflows_mistralai.Agent(
            description="Agent to do research on the interest rate of the European central bank.",
            instructions="Use tools to get the interest rate for a given year.",
            name="ecb-interest-rate-agent",
            tools=[get_interest_rate],
        )

        logger.info("Workflow: Creating finance agent with handoff")
        finance_agent = workflows_mistralai.Agent(
            description="Agent used to answer financial related requests",
            name="finance-agent",
            handoffs=[ecb_interest_rate_agent],
        )

        logger.info("Workflow: Running agent with question", question=params.question)
        outputs = await workflows_mistralai.Runner.run(agent=finance_agent, inputs=params.question, session=session)

        str_output = "\n".join([output.text for output in outputs if isinstance(output, TextChunk)])
        logger.info("Workflow: Agent execution completed", output_length=len(str_output))

        return FinanceAgentWorkflowResult(answer=str_output)


class MCPToolsWorkflowParams(BaseModel):
    question: str = Field(..., description="The question to ask the agent with MCP tools")


class MCPToolsWorkflowResult(BaseModel):
    answer: str = Field(..., description="The answer from the agent using MCP tools")


@workflows.workflow.define(name="mcp_tools_workflow")
class MCPToolsWorkflow:
    @workflows.workflow.entrypoint
    async def entrypoint(self, question: str) -> MCPToolsWorkflowResult:
        """Workflow that uses an agent with MCP tools from a local stdio server."""
        logger.info("Workflow: Starting MCP tools workflow", question=question)

        # Create MCP config (serializable)
        logger.info("Workflow: Creating MCP stdio config")
        mcp_config = MCPStdioConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            name="server-everything",
        )

        # Create local session
        local_session = workflows_mistralai.RemoteSession()

        # Create agent with MCP config
        logger.info("Workflow: Creating agent with MCP config")
        agent = workflows_mistralai.Agent(
            description="Agent with access to MCP tools",
            name="mcp-agent",
            mcp_clients=[mcp_config],
        )

        # Run agent with question (MCP tools will be collected and added automatically)
        logger.info("Workflow: Running agent with question", question=question)
        outputs = await workflows_mistralai.Runner.run(
            agent=agent,
            inputs=question,
            session=local_session,
        )

        str_output = "\n".join([output.text for output in outputs if isinstance(output, TextChunk)])
        logger.info("Workflow: Agent execution completed", output_length=len(str_output))

        return MCPToolsWorkflowResult(answer=str_output)


class MCPSSEWorkflowParams(BaseModel):
    question: str = Field(..., description="The question to ask the agent with remote SSE MCP server")


class MCPSSEWorkflowResult(BaseModel):
    answer: str = Field(..., description="The answer from the agent using remote SSE MCP server")


@workflows.workflow.define(name="mcp_sse_workflow")
class MCPSSEWorkflow:
    @workflows.workflow.entrypoint
    async def entrypoint(self, question: str) -> MCPSSEWorkflowResult:
        """Workflow that uses an agent with remote SSE MCP server (no auth)."""
        logger.info("Workflow: Starting MCP SSE workflow", question=question)

        logger.info("Workflow: Creating MCP SSE config")
        mcp_config = MCPSSEConfig(
            url="https://demo-day.mcp.cloudflare.com/sse",
            timeout=60,
            name="cloudflare-demo",
        )

        remote_session = workflows_mistralai.RemoteSession()

        logger.info("Workflow: Creating agent with SSE MCP config")
        agent = workflows_mistralai.Agent(
            description="Agent with access to remote SSE MCP tools",
            name="sse-mcp-agent",
            mcp_clients=[mcp_config],
        )

        logger.info("Workflow: Running agent with question", question=question)
        outputs = await workflows_mistralai.Runner.run(
            agent=agent,
            inputs=question,
            session=remote_session,
        )

        str_output = "\n".join([output.text for output in outputs if isinstance(output, TextChunk)])
        logger.info("Workflow: Agent execution completed", output_length=len(str_output))

        return MCPSSEWorkflowResult(answer=str_output)


class DealDeskWorkflowParams(BaseModel):
    deal_request: str = Field(..., description="The deal request or document text to process")


class DealDeskWorkflowResult(BaseModel):
    answer: str = Field(..., description="The final decision and recommendation")


class WebSearchWorkflowParams(BaseModel):
    query: str = Field(..., description="Query to ask to the agent")


class WebSearchWorkflowResult(BaseModel):
    answer: str = Field(..., description="Output of the agent")


@workflows.workflow.define("web-search-workflow")
class WebSearchAgentWorkflow:
    @workflows.workflow.entrypoint
    async def entrypoint(self, query: str) -> WebSearchWorkflowResult:
        """Workflow that uses an agent with built-in tools."""
        logger.info("Workflow: Starting built-in tools workflow", query=query)
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Agent with web search tool",
            instructions="You must use the web search tool to answer user questions",
            name="web-search-agent",
            tools=[WebSearchTool()],
        )
        logger.info("Workflow: Running agent with question", question=query)
        outputs = await workflows_mistralai.Runner.run(agent=agent, inputs=query, session=session)

        answer = "\n".join([output.text for output in outputs if isinstance(output, TextChunk)])
        return WebSearchWorkflowResult(answer=answer)


@workflows.activity(retry_policy_max_attempts=1)
async def capitalize(name: str) -> dict:
    """Use this to capitalize a name."""
    return {"result": name.capitalize()}


@workflows.workflow.define("tool-return-dict-workflow")
class ToolReturnDictWorkflow:
    """Workflow that uses an agent with a tool returning a dict and not a BaseModel."""

    @workflows.workflow.entrypoint
    async def entrypoint(self) -> None:
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Agent that capitalizes names",
            instructions="Follow the user instructions",
            name="capitalize-agent",
            tools=[capitalize],
        )
        logger.info("Workflow: Running agent")
        await workflows_mistralai.Runner.run(agent=agent, inputs="Capitalize 'alice'", session=session)


@workflows.workflow.define("failing-tool-call-workflow")
class FailingToolCallWorkflow:
    @workflows.workflow.entrypoint
    async def entrypoint(self) -> None:
        session = workflows_mistralai.RemoteSession()

        class WebSearchParams(BaseModel):
            query: str

        class WebSearchResult(BaseModel):
            result: str

        @workflows.activity(retry_policy_max_attempts=1)
        async def do_web_search(params: WebSearchParams) -> WebSearchResult:
            raise ValueError("This is a test error")

        agent = workflows_mistralai.Agent(
            description="Agent with web search tool",
            instructions="Follow the user instructions",
            name="web-search-agent",
            tools=[do_web_search],
        )
        logger.info("Workflow: Running agent")
        with contextlib.suppress(Exception):
            await workflows_mistralai.Runner.run(
                agent=agent,
                inputs="Call do_web_search tool with query 'What is the weather today?'",
                session=session,
            )

        await workflows_mistralai.Runner.run(agent=agent, inputs="Say 'done'", session=session)


# TODO:
# @workflows.workflow.define(name="deal_desk_workflow")
# class DealDeskWorkflow:
#     @workflows.workflow.entrypoint
#     async def entrypoint(self, params: DealDeskWorkflowParams) -> DealDeskWorkflowResult:
#         """Complex multi-agent workflow demonstrating handoffs, activities, and conditional routing."""
#         logger.info("Workflow: Starting deal desk workflow", request_length=len(params.deal_request))

#         # Create agents in reverse dependency order (targets first, sources last)

#         # Terminal agents (no handoffs)
#         logger.info("Workflow: Creating negotiation agent")
#         negotiation_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to negotiate deal terms and generate contracts",
#             instructions=(
#                 "Use the generate_contract_terms tool to create contract terms. Provide a final recommendation."
#             ),
#             name="negotiation-agent",
#             tools=[generate_contract_terms],
#         )

#         logger.info("Workflow: Creating escalation agent")
#         escalation_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to escalate deals requiring human review",
#             instructions="Format an escalation report with all identified issues and required approvals.",
#             name="escalation-agent",
#         )

#         # Aggregator agent (hands off to negotiation or escalation)
#         logger.info("Workflow: Creating aggregator agent")
#         aggregator_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to synthesize risk and compliance findings",
#             instructions=(
#                 "Review risk and compliance analysis. "
#                 "If risk is acceptable and compliant, hand off to negotiation-agent. "
#                 "If issues found, hand off to escalation-agent."
#             ),
#             name="aggregator-agent",
#             handoffs=[negotiation_agent, escalation_agent],
#         )

#         # Sequential chain: compliance -> risk -> aggregator (no convergence)
#         logger.info("Workflow: Creating compliance agent")
#         compliance_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to check regulatory compliance",
#             instructions=(
#                 "Use check_compliance to verify regulatory requirements. "
#                 "Hand off results to aggregator-agent for final decision."
#             ),
#             name="compliance-agent",
#             tools=[check_compliance],
#             handoffs=[aggregator_agent],
#         )

#         logger.info("Workflow: Creating risk agent")
#         risk_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to analyze financial risk",
#             instructions=(
#                 "Use calculate_risk_score to assess deal risk. "
#                 "Hand off results to compliance-agent for compliance check."
#             ),
#             name="risk-agent",
#             tools=[calculate_risk_score],
#             handoffs=[compliance_agent],
#         )

#         # Intake agent (starting point)
#         logger.info("Workflow: Creating intake agent")
#         intake_agent = workflows_agents.Agent(
#             model="mistral-medium-2508",
#             description="Agent to intake and parse deal requests",
#             instructions=(
#                 "Parse the deal request using parse_deal_document tool. "
#                 "Extract key information and hand off to risk-agent for analysis."
#             ),
#             name="intake-agent",
#             tools=[parse_deal_document],
#             handoffs=[risk_agent],
#         )

#         # Run workflow with remote session
#         logger.info("Workflow: Running agent workflow starting with intake")
#         session = workflows_agents.RemoteSession()

#         outputs = await workflows_agents.Runner.run(
#             agent=intake_agent,
#             inputs=params.deal_request,
#             session=session,
#         )

#         # Extract text output
#         answer = "\n".join([output.text for output in outputs if isinstance(output, TextChunk)])
#         logger.info("Workflow: Deal desk workflow completed", output_length=len(answer))

#         return DealDeskWorkflowResult(answer=answer)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([FinanceAgentWorkflow, MCPToolsWorkflow, MCPSSEWorkflow, WebSearchAgentWorkflow]))
