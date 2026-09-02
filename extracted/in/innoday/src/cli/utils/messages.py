"""Motivational messages shown in the CLI welcome banner.

Lives here rather than in a top-level ``src/ui`` package: ``cli/utils/banner.py``
is the only consumer, and a second directory called "ui" alongside the real
browser pages in ``src/routers/webui`` was a standing invitation to open the
wrong one.
"""

import random

# List of tech-focused motivational messages
MESSAGES = [
    "🚀 Time to turn coffee into code and dreams into reality!",
    "💡 Innovation is the outcome of a habit, not a random act.",
    "🎯 Small progress is still progress. Keep coding!",
    "🌟 Every bug you fix makes you a better developer.",
    "🔄 Continuous improvement is better than delayed perfection.",
    "🎨 Code is poetry waiting to be written.",
    "🧩 Complex problems are just simple problems in disguise.",
    "⚡ Your code can change someone's world today.",
    "🌈 The best code is the one that ships.",
    "🎭 Debug like a detective, code like an artist.",
    "🎵 Programming is music for the logical mind.",
    "🌱 Growth happens outside your comfort zone.",
    "🔥 Your determination is your superpower.",
    "🎪 Every line of code tells a story. Make it epic!",
    "🎲 Take risks, break things, learn, repeat.",
    "🏗️  Build whatever you want, whenever you want, for whoever you want!",
    "✨ Every day is an innovation day with InnoDay!",
]


def get_random_message() -> str:
    """Get a random motivational message"""
    return random.choice(MESSAGES)
