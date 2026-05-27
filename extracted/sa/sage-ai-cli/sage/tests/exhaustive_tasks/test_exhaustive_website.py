import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

@pytest.mark.parametrize("prompt", [
    "Create a responsive advertising dashboard using React and Tailwind.",
    "Build a React Native feed with infinite scrolling.",
    "Develop a 2D physics engine in JavaScript for a browser game.",
    "Create a FastAPI backend with PostgreSQL and Redis caching.",
    "Write Terraform IaC to deploy a Node.js app to AWS ECS.",
    "Make a music video with moviepy that says 'I love you Lily'.",
    "Generate a professional SVG logo and PNG favicon.",
    "Synthesize a WAV audio file playing a C major chord.",
    "Combine generated audio and video into an MP4 music video.",
    "Write a complex Python script, a JSON config, and a YAML manifest.",
    "Open the Messages app on my Mac and prepare a text.",
    "Use osascript to change my system volume and toggle dark mode.",
    "Send a text message using the SMS bridge natively.",
    "Trigger an API call to Twilio to initiate a phone call."
])
def test_website_exhaustive_task(prompt):
    """Verify that the Website chat API handles the task correctly, returns exact output, and satisfies the rubric."""
    verify_website_with_rubric(prompt)
