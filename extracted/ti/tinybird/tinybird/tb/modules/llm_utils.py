import re
from typing import List


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""


def parse_xml(text: str, tag: str) -> List[str]:
    """
    Parses the text for the specified XML tag and returns a list of the contents of each tag.
    """
    return re.findall(f"<{tag}.*?>(.*?)</{tag}>", text, re.DOTALL)


def generate(llm_call, task: str, feedback: str = "") -> tuple[str, str]:
    """Generate and improve a solution based on feedback."""
    task = f"<task>\n{task}\n</task>"
    full_prompt = (
        f"{generator_prompt}\n<feedback>\n{feedback}\n</feedback>\n{task}"
        if feedback
        else f"{generator_prompt}\n{task}"
    )
    response = llm_call(full_prompt)
    thoughts = extract_xml(response, "thoughts")
    result = extract_xml(response, "response")

    return thoughts, result


def evaluate(llm_call, content: str, task: str) -> tuple[str, str]:
    """Evaluate if a solution meets requirements."""
    full_prompt = f"{evaluator_prompt}\n<original_task>\n{task}\n</original_task>\n<content_to_evaluate>\n{content}\n</content_to_evaluate>"
    response = llm_call(full_prompt)
    evaluation = extract_xml(response, "evaluation")
    feedback = extract_xml(response, "feedback")

    return evaluation, feedback


def loop(llm_call, task: str) -> str:
    """Keep generating and evaluating until requirements are met."""
    memory = []
    chain_of_thought = []

    thoughts, result = generate(llm_call, task)
    memory.append(result)
    chain_of_thought.append({"thoughts": thoughts, "result": result})

    attempts = 0
    while True:
        if attempts > 5:
            raise Exception("Failed to generate a valid solution")

        evaluation, feedback = evaluate(llm_call, result, task)
        if evaluation == "PASS":
            return result

        context = "\n".join(
            [
                "Previous attempts:",
                *[f"- {m}" for m in memory],
                f"\nFeedback: {feedback}",
            ]
        )

        thoughts, result = generate(llm_call, task, context)
        memory.append(result)
        chain_of_thought.append({"thoughts": thoughts, "result": result})

        attempts += 1


evaluator_prompt = """
Evaluate this following code implementation for code correctness taking into account the user prompt and the instructions provided.

You should be evaluating only and not attemping to solve the task.
Only output "PASS" if all criteria are met and the code won't fail at runtime.
Output your evaluation concisely in the following format:

<evaluation>PASS or FAIL</evaluation>
<feedback>
[What is wrong with the code and how to fix it]
</feedback>
"""

generator_prompt = """
Your goal is to complete the task based on <task> tag. If there are feedback
from your previous generations, you should reflect on them to solve the task.
All xml tags MUST be closed.

Add the following tag to the requested response:

<thoughts>
[Your understanding of the task and feedback and how you plan to solve it]
</thoughts>
"""
