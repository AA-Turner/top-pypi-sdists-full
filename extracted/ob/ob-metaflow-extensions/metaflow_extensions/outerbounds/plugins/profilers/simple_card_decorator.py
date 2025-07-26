from datetime import datetime
from metaflow.decorators import StepDecorator
from ..card_utilities.injector import CardDecoratorInjector


class DynamicCardAppendDecorator(StepDecorator):
    """
    A simple decorator that demonstrates using CardDecoratorInjector
    to inject a card and render simple markdown content.
    """

    name = "test_append_card"

    defaults = {
        "title": "Simple Card",
        "message": "Hello from DynamicCardAppendDecorator!",
        "show_timestamp": True,
        "refresh_interval": 5,
    }

    CARD_ID = "simple_card"

    def step_init(
        self, flow, graph, step_name, decorators, environment, flow_datastore, logger
    ):
        """Initialize the decorator and inject the card."""
        self.deco_injector = CardDecoratorInjector()
        self.deco_injector.attach_card_decorator(
            flow,
            step_name,
            self.CARD_ID,
            "blank",
            refresh_interval=self.attributes["refresh_interval"],
        )

    def task_decorate(
        self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context
    ):
        """Decorate the step function to add card content."""
        from metaflow import current
        from metaflow.cards import Markdown

        # Create the card content
        title = self.attributes["title"]
        message = self.attributes["message"]
        show_timestamp = self.attributes["show_timestamp"]

        # Add title to the card
        current.card[self.CARD_ID].append(Markdown(f"# {title}"))

        # Add message to the card
        current.card[self.CARD_ID].append(Markdown(f"**Message:** {message}"))

        # Add timestamp if requested
        if show_timestamp:
            timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
            current.card[self.CARD_ID].append(Markdown(f"**Created at:** {timestamp}"))

        # Add step information
        current.card[self.CARD_ID].append(Markdown(f"**Step:** `{current.pathspec}`"))

        # Add a simple divider
        current.card[self.CARD_ID].append(Markdown("---"))

        # Add some dynamic content that shows this is working
        current.card[self.CARD_ID].append(
            Markdown("**Status:** Card successfully injected! 🎉")
        )

        def wrapped_step_func():
            """Execute the original step function."""
            try:
                # Before execution
                current.card[self.CARD_ID].append(
                    Markdown("**Execution:** Step started...")
                )
                current.card[self.CARD_ID].refresh()

                # Execute the original step
                step_func()

                # After execution
                current.card[self.CARD_ID].append(
                    Markdown("**Execution:** Step completed successfully! ✅")
                )
                current.card[self.CARD_ID].refresh()

            except Exception as e:
                # Handle errors
                current.card[self.CARD_ID].append(
                    Markdown(f"**Error:** Step failed with error: `{str(e)}` ❌")
                )
                current.card[self.CARD_ID].refresh()
                raise

        return wrapped_step_func
