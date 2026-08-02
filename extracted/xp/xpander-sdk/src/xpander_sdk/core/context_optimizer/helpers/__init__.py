"""Pure helpers extracted from context_optimizer.py.

These modules hold logic that is conceptually orthogonal to the optimizer
class — secret redaction, XML safety, tool-result repr unwrapping,
recent-actions block rendering, message chunking. Keep helpers stateless
so they remain easy to test in isolation.
"""
