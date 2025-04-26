r"""Define the main errors of the object factory package."""

from __future__ import annotations

__all__ = [
    "AbstractClassFactoryError",
    "AbstractFactoryTypeError",
    "FactoryError",
    "IncorrectObjectFactoryError",
    "InvalidAttributeRegistryError",
    "InvalidNameFactoryError",
    "UnregisteredObjectFactoryError",
]


class FactoryError(Exception):
    r"""Define an exception that can be used to catch all the factory
    errors."""


class UnregisteredObjectFactoryError(FactoryError):
    r"""Define an exception that is raised when you try to initialize or
    unregister an object which is not registered to the factory."""


class IncorrectObjectFactoryError(FactoryError):
    r"""Define an exception that is raised when you try to register an
    object which cannot be registered."""


class AbstractClassFactoryError(FactoryError):
    r"""Define an exception that is raised when you try to initialize an
    abstract class."""


class InvalidNameFactoryError(FactoryError):
    r"""Define an exception that is raised when you try to use an
    invalid name to register an object to a factory."""


###########################
#     AbstractFactory     #
###########################


class AbstractFactoryTypeError(FactoryError):
    r"""Define an exception that is raised when an object does not of
    type ``AbstractFactory``."""


####################
#     Registry     #
####################


class InvalidAttributeRegistryError(FactoryError):
    r"""Define an exception that is raised when you try to access a non
    Registry object in the registry."""
