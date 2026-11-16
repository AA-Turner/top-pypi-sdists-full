"""Bounded GPU observations shared by serving requests and rollout capture."""

from .trace import GpuTrace

__all__ = ["GpuTrace"]
