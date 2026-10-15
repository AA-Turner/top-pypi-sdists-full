"""Deprecated module. Import ``Category``, ``CategorySummary``, and ``CategoriesClient`` from ``bitfab.categories`` instead."""

from bitfab.categories import (
    CATEGORIES_PATH,
    CategoriesClient,
    Category,
    CategorySummary,
)

AssertionCategory = Category
AssertionCategorySummary = CategorySummary
AssertionCategoriesClient = CategoriesClient

__all__ = [
    "CATEGORIES_PATH",
    "AssertionCategoriesClient",
    "AssertionCategory",
    "AssertionCategorySummary",
]
