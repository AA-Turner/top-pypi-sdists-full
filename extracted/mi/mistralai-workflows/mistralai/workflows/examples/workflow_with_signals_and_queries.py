import asyncio
from typing import List

import pydantic
from temporalio import workflow as temporal_workflow

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.logging import Env, LogFormat, LogLevel, setup_logging

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class AppConfig(pydantic.BaseModel):
    env: Env = Env.DEV
    temporal_server_url: str = "localhost:7233"
    temporal_namespace: str = "default"
    log_format: str = "console"
    log_level: str = "DEBUG"
    app_version: str = "local_test"


class Empty(pydantic.BaseModel):
    pass


class GameWorkflowParams(pydantic.BaseModel):
    initial_player_name: str | None = "AnonPlayer"
    max_riddles: int = 2


class SetNameSignalInput(pydantic.BaseModel):
    new_name: str


class SubmitAnswerSignalInput(pydantic.BaseModel):
    answer: str


class GameWorkflowResult(pydantic.BaseModel):
    final_score: int
    player_name: str
    game_log: List[str]
    message: str


class GameStatusQueryResponse(pydantic.BaseModel):
    player_name: str
    current_riddle: str | None
    riddles_solved: int
    score: int
    game_over: bool
    log_preview: List[str]


class Riddle(pydantic.BaseModel):
    question: str
    correct_answer: str


# --- Activities  ---


@workflows.activity()
async def fetch_next_riddle_activity(solved_count: int) -> Riddle:
    logger.info("activity: fetching riddle", solved_count=solved_count)
    await asyncio.sleep(0.1)
    riddles_db = [
        Riddle(
            question="I have cities, but no houses. I have mountains, but no trees. I have water, \
                but no fish. What am I?",
            correct_answer="map",
        ),
        Riddle(question="What has an eye, but cannot see?", correct_answer="needle"),
        Riddle(question="What is full of holes but still holds water?", correct_answer="sponge"),
    ]
    if solved_count < len(riddles_db):
        return riddles_db[solved_count]
    # Return an empty riddle instead of None to satisfy type checking
    return Riddle(question="No more riddles available", correct_answer="")


# --- Workflow  ---


@workflows.workflow.define(
    name="example-interactive-game-workflow",
    workflow_description="A simple interactive riddle game driven by signals and queries.",
)
class InteractiveGameWorkflow:
    def __init__(self) -> None:
        self.player_name: str = "PlayerUnset"
        self.current_riddle_text: str | None = None
        self.current_riddle_answer: str | None = None
        self.riddles_solved_count: int = 0
        self.score: int = 0
        self.game_over: bool = False
        self.game_log: List[str] = []
        self.max_riddles_to_win: int = 1

        # For wait_for_condition
        self._action_occurred: bool = False

    def _add_log(self, message: str) -> None:
        timestamp = temporal_workflow.now().isoformat()
        entry = f"{timestamp} - {message}"
        self.game_log.append(entry)
        logger.info(f"GameLog[{self.player_name}]: {message}")

    async def _load_new_riddle(self) -> None:
        riddle_data = await fetch_next_riddle_activity(self.riddles_solved_count)

        # Check if the returned riddle is the empty placeholder
        if riddle_data.correct_answer:
            self.current_riddle_text = riddle_data.question
            self.current_riddle_answer = riddle_data.correct_answer
            self._add_log(f"New riddle presented: {self.current_riddle_text}")
        else:
            self._add_log("No more riddles available!")
            self.current_riddle_text = None
            if self.riddles_solved_count >= self.max_riddles_to_win:
                self._add_log(f"Congratulations {self.player_name}! You solved all riddles!")
                self.game_over = True

    async def _run_impl(
        self, initial_player_name: str | None = "AnonPlayer", max_riddles: int = 2
    ) -> GameWorkflowResult:
        self.player_name = initial_player_name or "Hero"
        self.max_riddles_to_win = max_riddles
        self._add_log(f"Game started for {self.player_name}. Solve {self.max_riddles_to_win} riddle(s) to win.")

        await self._load_new_riddle()

        if self.current_riddle_text is None and self.riddles_solved_count < self.max_riddles_to_win:
            self._add_log("Failed to load initial riddle. Ending game.")
            self.game_over = True

        while not self.game_over:
            self._add_log(
                f"Waiting for player action (current riddle: {'...' if self.current_riddle_text else 'None'})..."
            )
            await workflows.workflow.wait_condition(lambda: self._action_occurred)

            # AND RESET THE FLAG:
            self._action_occurred = False

            if self.game_over:  # A signal might have ended the game
                break

            # Check if we need a new riddle (e.g., after a correct answer processed by a signal)
            # This logic is a bit simplified; signal handlers might directly call _load_new_riddle
            # or set a flag that this loop checks. For now, assume signals update state,
            # and if a riddle was solved, current_riddle_text might be None.
            if self.current_riddle_text is None and not self.game_over:
                self._add_log("Current riddle solved or became unavailable, attempting to load next.")
                await self._load_new_riddle()
                if (
                    self.current_riddle_text is None and not self.game_over
                ):  # Still no riddle and not game over (e.g. no more riddles but not enough solved)
                    self._add_log("No more riddles to solve, but not enough solved to win. Game over.")
                    self.game_over = True

        final_message = f"Game Over! Thanks for playing, {self.player_name}."
        if self.riddles_solved_count >= self.max_riddles_to_win:
            final_message = f"YOU WON, {self.player_name}! You solved {self.riddles_solved_count} riddle(s)!"
        self._add_log(final_message)

        return GameWorkflowResult(
            final_score=self.score, player_name=self.player_name, game_log=self.game_log, message=final_message
        )

    @workflows.workflow.entrypoint
    async def run(self, initial_player_name: str | None = "AnonPlayer", max_riddles: int = 2) -> GameWorkflowResult:
        return await self._run_impl(initial_player_name, max_riddles)

    async def _set_name_signal_impl(self, new_name: str) -> None:
        self._add_log(f"Name change requested from '{self.player_name}' to '{new_name}'.")
        self.player_name = new_name
        self._action_occurred = True  # Notify the main loop

    @workflows.workflow.signal(name="set_name", description="Sets the player's name.")
    async def set_name_signal(self, new_name: str) -> None:
        await self._set_name_signal_impl(new_name)

    async def _submit_answer_signal_impl(self, answer: str) -> None:
        if self.game_over:
            self._add_log(f"Answer '{answer}' submitted, but game is already over.")
            self._action_occurred = True
            return

        if not self.current_riddle_text or not self.current_riddle_answer:
            self._add_log(f"Answer '{answer}' submitted, but no active riddle.")
            self._action_occurred = True
            return

        self._add_log(f"Player '{self.player_name}' answered '{answer}' for riddle: '{self.current_riddle_text}'.")
        if answer.lower().strip() == self.current_riddle_answer.lower().strip():
            self.score += 10
            self.riddles_solved_count += 1
            self._add_log(f"Correct! Score: {self.score}. Riddles solved: {self.riddles_solved_count}.")
            self.current_riddle_text = None  # Mark as solved, run loop will try to load next
            if self.riddles_solved_count >= self.max_riddles_to_win:
                self._add_log(f"Victory condition met with {self.riddles_solved_count} riddles solved!")
                self.game_over = True
        else:
            self.score -= 1  # Penalty for wrong answer
            self._add_log(f"Incorrect. Score: {self.score}.")
            # Could add attempts logic here too

        self._action_occurred = True  # Notify the main loop

    @workflows.workflow.signal(name="submit_answer", description="Submits an answer to the current riddle.")
    async def submit_answer_signal(self, answer: str) -> None:
        await self._submit_answer_signal_impl(answer)

    async def _force_end_game_signal_impl(self) -> None:
        self._add_log(f"Game force-ended by signal for player {self.player_name}.")
        self.game_over = True
        self._action_occurred = True

    @workflows.workflow.signal(name="force_end_game", description="Ends the game immediately.")
    async def force_end_game_signal(self) -> None:  # No input needed
        await self._force_end_game_signal_impl()

    def _get_status_query_impl(self) -> GameStatusQueryResponse:
        # Create a preview of the log (handle empty case gracefully)
        log_preview = self.game_log[-5:] if len(self.game_log) > 0 else []

        return GameStatusQueryResponse(
            player_name=self.player_name,
            current_riddle=self.current_riddle_text,
            riddles_solved=self.riddles_solved_count,
            score=self.score,
            game_over=self.game_over,
            log_preview=log_preview,  # Last 5 log entries
        )

    @workflows.workflow.query(name="get_status", description="Gets the current game status.")
    def get_status_query(self) -> GameStatusQueryResponse:
        return self._get_status_query_impl()

    def _get_riddle_by_index_query_impl(self, index: int) -> str | None:
        riddles = [
            "I have cities, but no houses...",
            "What has an eye, but cannot see?",
            "What is full of holes but still holds water?",
        ]
        if 0 <= index < len(riddles):
            return riddles[index]
        return None

    @workflows.workflow.query(name="get_riddle_by_index", description="Gets a riddle by its index.")
    def get_riddle_by_index_query(self, index: int) -> str | None:
        return self._get_riddle_by_index_query_impl(index)

    @workflows.workflow.query(name="search_logs", description="Searches the game log for entries containing the term.")
    def search_logs_query(self, search_term: str) -> List[str]:
        return [entry for entry in self.game_log if search_term.lower() in entry.lower()]


# --- Main for local worker (optional, good for quick testing) ---

if __name__ == "__main__":
    app_cfg = AppConfig()
    setup_logging(
        log_format=LogFormat(app_cfg.log_format),
        log_level=LogLevel(app_cfg.log_level),
        app_version=app_cfg.app_version,
    )
    asyncio.run(workflows.run_worker([InteractiveGameWorkflow]))
