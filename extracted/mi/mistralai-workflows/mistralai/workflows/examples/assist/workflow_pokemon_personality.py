import asyncio

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)


@workflows.workflow.define(
    name="pokemon-personality-workflow",
    workflow_display_name="Pokemon Personality",
    workflow_description="Discover your personality based on your Pokemon preferences",
)
class PokemonPersonalityWorkflow(workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self) -> workflows_mistralai.ChatAssistantWorkflowOutput:
        favorite_item = workflows_mistralai.TodoListItem(
            title="Favorite pokémon", description="Choose your favorite Pokémon"
        )
        least_favorite_item = workflows_mistralai.TodoListItem(
            title="Least favorite pokémon", description="Choose your least favorite Pokémon"
        )
        favorite_type_item = workflows_mistralai.TodoListItem(
            title="Favorite type", description="Choose your favorite type"
        )
        confirmation_item = workflows_mistralai.TodoListItem(
            title="Confirmation", description="Ensure proper Pokemon selection"
        )
        analyze_item = workflows_mistralai.TodoListItem(
            title="Personality analyze",
            description="Who knew just two 'mons could tell so much about you?",
        )

        async with workflows_mistralai.TodoList(
            items=[favorite_item, least_favorite_item, favorite_type_item, confirmation_item, analyze_item]
        ) as todo_list:
            # Step 1: Ask for favorite pokemon
            async with favorite_item:
                await workflows_mistralai.send_assistant_message(
                    "Let's discover your Pokemon personality! First, tell me about your favorite Pokemon."
                )
                favorite = await self.wait_for_input(
                    workflows_mistralai.ChatInput(
                        "What is your favorite Pokémon?",
                        suggestions=[
                            [workflows_mistralai.TextChunk(text="Pikachu")],
                            [workflows_mistralai.TextChunk(text="Charizard")],
                            [workflows_mistralai.TextChunk(text="Gengar")],
                        ],
                    )
                )
                pokemon_name = favorite.message[0].text if favorite.message else ""
                logger.info("Received favorite Pokemon", pokemon=pokemon_name)

            # Step 2: Ask for least favorite pokemon
            async with least_favorite_item:
                await workflows_mistralai.send_assistant_message(
                    f"Great choice! {pokemon_name} says a lot about you. Now, which Pokemon do you like the least?"
                )
                least_favorite = await self.wait_for_input(
                    workflows_mistralai.ChatInput("What is your least favorite Pokémon?")
                )
                least_pokemon_name = least_favorite.message[0].text if least_favorite.message else ""
                logger.info("Received least favorite Pokemon", pokemon=least_pokemon_name)

                # Step 3: Ask for favourite pokemon type
            async with favorite_type_item:
                await workflows_mistralai.send_assistant_message("Ok! Now what about your favorite type?")
                favorite_type = await self.wait_for_input(
                    workflows_mistralai.ConfirmationInput(
                        options=[("normal", "Normal"), ("fire", "Fire"), ("water", "Water"), ("grass", "Grass")],
                        description="What is your favorite Pokemon type?",
                    )
                )
                favorite_type_name = favorite_type.choice if favorite_type.choice else ""

                await workflows_mistralai.send_assistant_message(
                    f"{favorite_type_name}, got it! Let's move on to the next step."
                )
                logger.info("Received least favorite Pokemon type", type=favorite_type_name)

            # Step 4: Confirmation step
            async with confirmation_item:
                confirmation = await self.wait_for_input(
                    workflows_mistralai.AcceptDeclineConfirmation(
                        description=f"Ready to analyze your personality based on {pokemon_name} and {least_pokemon_name}?",  # noqa: E501
                        accept_label="Yes, analyze my personality!",
                        decline_label="No",
                    )
                )
                logger.info("Received confirmation", choice=confirmation.choice)

            # Send different message based on confirmation status
            if workflows_mistralai.is_accepted(confirmation):
                await workflows_mistralai.send_assistant_message(
                    f"Excellent! Let me analyze your personality based on your love for {pokemon_name} "
                    f"and your feelings about {least_pokemon_name}..."
                )
            else:
                await workflows_mistralai.send_assistant_message(
                    "No worries! Come back when you're ready to discover your Pokemon personality."
                )
                return workflows_mistralai.ChatAssistantWorkflowOutput(
                    content=[workflows_mistralai.TextOutput(text="Session cancelled. See you next time!")]
                )

            # Step 4: Analyze personality
            # Remove the original analyze item and add a new "enjoy" item dynamically
            await todo_list.remove_item(analyze_item)
            enjoy_item = workflows_mistralai.TodoListItem(
                title="Enjoy your analysis",
                description="Sit back and enjoy your Pokemon personality profile!",
            )
            await todo_list.add_item(enjoy_item)

            # Manually control status
            await enjoy_item.set_status("in_progress")

            logger.info("Creating personality analysis agent")
            session = workflows_mistralai.RemoteSession(stream=True)

            personality_agent = workflows_mistralai.Agent(
                description="Pokemon personality analyst that creates fun personality profiles",
                instructions="""You are a fun and insightful personality analyst who specializes in understanding
people through their Pokemon preferences. When given a favorite Pokemon, least favorite Pokemon and favorite type,
you create an engaging personality analysis.

Write a short, engaging personality description (2-3 paragraphs) that:
1. Analyzes what the favorite Pokemon choice says about the person's values and personality
2. Analyzes what the least favorite Pokemon choice reveals about what they avoid or dislike
3. Synthesizes these insights into a cohesive personality profile

Be creative, fun, and positive while still being insightful!""",
                name="pokemon-personality-agent",
            )

            prompt = f"""Analyze this person's personality based on their Pokemon preferences:

Favorite Pokemon: {pokemon_name}
Least Favorite Pokemon: {least_pokemon_name}
Favorite Type: {favorite_type_name}

Please provide your personality analysis."""

            logger.info("Running personality agent", prompt=prompt)
            await workflows_mistralai.Runner.run(
                agent=personality_agent,
                inputs=prompt,
                session=session,
            )

            await enjoy_item.set_status("done")

        return workflows_mistralai.ChatAssistantWorkflowOutput(
            content=[workflows_mistralai.TextOutput(text="Come back for more Pokemon based Quiz another time!")]
        )


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([PokemonPersonalityWorkflow]))
