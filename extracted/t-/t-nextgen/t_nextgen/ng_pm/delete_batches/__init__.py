"""This module provides a function to delete batches from the database."""
from .delete_batches import delete_batches
from .delete_duplicates import DuplicateBatchDeleter

__all__ = ["delete_batches", "DuplicateBatchDeleter"]
