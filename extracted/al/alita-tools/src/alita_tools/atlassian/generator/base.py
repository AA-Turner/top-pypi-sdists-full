from typing import Any
import traceback
import logging
from .code_validator import CodeRequirementValidator

logger = logging.getLogger(__name__)

PLAN_CODE_PROMPT = """
# Role
You are Python developer tasked to create code to solve user's question.

# Goal 
Generate python code based on given user request.

# Requirements
* Carefully understand user's request and list core featured required to be covered with code.
* Pay attention to authentication if any (select proper one based on available data).
* Build the solution based on existing API libraries.
* Try to make it as flexible as possible.
* It is expected that required data (like url, authentication, etc.) is already filled in - use it directly in code.
* IMPORTANT: Avoid using __main__ or __name__ == "__main__" in the code.
* IMPORTANT: Pay attention to authentication selection if any: i.e. user passed token only (username is missed or empty) 
then it might be bearer or authentication via PAT, etc., if username exists then it mostly basic, etc.
* IMPORTANT: Finally, generated code has to return result of its execution.
* TESTING: generated code should contain simple healthcheck that verifies if the code works as expected or 
throws exception that can be handled futher

# Output
* generated executable code with the corresponding imports.
* return code only.

<user_request>
{task}
</user_request>

At the end, declare "result" variable as a dictionary of type and value.
"""

class CodeGenerator:
    def __init__(self, llm: Any):
        self.llm = llm
        self._code_validator = CodeRequirementValidator()

    def generate_code(self, prompt: str, error_trace:str = None) -> str:
        """
        Generates code using a given LLM and performs validation and cleaning steps.

        Args:
            prompt (BasePrompt): The prompt to guide code generation.
            error_trace (str): Optional error trace from previous attempts.

        Returns:
            str: The final cleaned and validated code.

        Raises:
            Exception: If any step fails during the process.
        """
        try:
            logger.debug(f"Using Prompt: {prompt}")
            prompt = PLAN_CODE_PROMPT.format(task=prompt)
            if error_trace:
                prompt += f"\n Last time you failed to generate the code <ErrorTrace>{error_trace}</ErrorTrace>"
            messages = [
                {"role": "user",  "content": [{"type": "text", "text": prompt}]}
            ]
            # Generate the code
            code = self.llm.invoke(messages).content
            return self.validate_and_clean_code(code)

        except Exception as e:
            error_message = f"An error occurred during code generation: {e}"
            stack_trace = traceback.format_exc()
            logger.debug(error_message)
            logger.debug(f"Stack Trace:\n{stack_trace}")
            raise e

    def validate_and_clean_code(self, code: str) -> str:
        # Validate code requirements
        logger.debug("Validating code requirements...")
        code = self._code_validator.clean_code(code)
        if not self._code_validator.validate(code):
            raise ValueError("Code validation failed due to unmet requirements.")
        logger.debug("Code validation successful.")

        # Clean the code
        # logger.debug("Cleaning the generated code...")
        # return self._code_cleaner.clean_code(code)
        return code