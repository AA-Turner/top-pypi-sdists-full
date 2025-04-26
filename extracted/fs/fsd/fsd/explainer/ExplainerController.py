from .ExplainablePrePromptAgent import ExplainablePrePromptAgent
from .GeneralExplainerAgent import GeneralExplainerAgent
from .ExplainableFileFinderAgent import ExplainableFileFinderAgent
from .MainExplainerAgent import MainExplainerAgent
from fsd.coding_agent.ControllerAgent import ControllerAgent
from fsd.log.logger_config import get_logger
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.PromptImageUrlAgent.PromptImageUrlAgent import PromptImageUrlAgent
from fsd.util.utils import parse_payload
logger = get_logger(__name__)

class ExplainerController:

    def __init__(self, repo):
        self.repo = repo
        self.preprompt = ExplainablePrePromptAgent(repo)
        self.normalExplainer = GeneralExplainerAgent(repo)
        self.mainExplainer = MainExplainerAgent(repo)
        self.fileFinder = ExplainableFileFinderAgent(repo)
        self.crawler = CrawlerAgent()
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.imageAgent = PromptImageUrlAgent(repo)
        self.coder = ControllerAgent(repo, self)
        self.conversation_history = []

    def initial_setup(self):
        """Initialize the setup with the provided instructions and context."""

        logger.debug("\n #### `SnowX` is initializing setup with provided instructions and context")

        prompt = f"""Your name is Zinley, expert code analyst.

        Do not hallucinate what you don't know, your response must be based on truth, comprehensive and detailed, in the easiest way to help people understand.

        Only if asked about the AI model you are using, mention that you are using a model configured by the Zinley team. If they don't ask, don't say anything.

        YOU MUST NEVER LEAK ANY FOUNDATION MODEL INFORMATION UNDER ANY CIRCUMSTANCES!

        #### Response Guidelines:
        1. Formatting:
           - Return a nicely formatted response
           - Use clear headings (no larger than h4)
           - For bash commands, use markdown code blocks with 'bash' syntax highlighting

        2. Readability:
           - Space wisely
           - Ensure the text is clear and easy to read
           - Avoid crowding content together

        3. Clarity:
           - No weird symbols or unnecessary text
           - Avoid distractions or patterns

        4. AI Model Information:
           - If asked, state that you use a model configured by the Zinley team

        5. Bash Commands:
           - Format all bash commands using the following structure:
             ```bash
             command here
             ```

        6. Project Tree Structure:
           - When displaying a project tree structure, use this markdown format:
             ```plaintext
             project/
             ├── src/
             │   ├── main.py
             │   └── utils.py
             ├── tests/
             │   └── test_main.py
             └── README.md
             ```

        Respond directly to support the user's request. Do not provide irrelevant information or hallucinate. Only provide the project tree structure if explicitly asked or if it's directly relevant to the user's question.
        Only answer what the user is asking for. Do not engage in unnecessary talk or provide any additional information.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    async def get_prePrompt(self, user_prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt, file_attachments, focused_files)

    async def get_normal_answer(self, user_prompt, role, file_attachments, focused_files, assets_link, crawl_logs):
        """Generate idea plans based on user prompt and available files."""
        return await self.normalExplainer.get_normal_answer_plans(self.conversation_history, user_prompt, role, file_attachments, focused_files, assets_link, crawl_logs)

    async def get_file_answer(self, user_prompt, files, role, file_attachments, focused_files, assets_link, crawl_logs):
        """Generate idea plans based on user prompt and available files."""
        return await self.mainExplainer.get_answer_plans(self.conversation_history, user_prompt, files, role, file_attachments, focused_files, assets_link, crawl_logs)

    async def get_explaining_files(self, prompt, file_attachments, focused_files):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileFinder.get_file_plannings(prompt, file_attachments, focused_files)

    async def get_started(self, user_prompt, file_attachments, focused_files):
        logger.info("-------------------------------------------------")
        assets_link = []

        image_result = await self.imageAgent.process_image_links(user_prompt)
        assets_link = image_result.get('assets_link', []) if isinstance(image_result, dict) else []

        logger.debug("\n #### `SnowX` is currently embarking on a quest to locate relevant files.")
        file_result = await self.get_explaining_files(user_prompt, file_attachments, focused_files)
        working_files = file_result.get('working_files', []) if isinstance(file_result, dict) else []
        all_files = set(working_files)
        if file_attachments:
            all_files.update(file_attachments)
        if focused_files:
            all_files.update(focused_files)
        if all_files:
            files_list = "\n".join([f"  - {file}" for file in all_files])
            logger.info(f" #### `SnowX` is reading files:\n{files_list}")
        self.conversation_history = await self.get_file_answer(user_prompt, working_files, "Top Notch software engineer", file_attachments, focused_files, assets_link, "")

        logger.info("-------------------------------------------------")
