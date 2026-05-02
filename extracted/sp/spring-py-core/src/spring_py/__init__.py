"""
Spring-Py: A Python implementation of Spring Framework IoC container
"""

from .annotation import Component, Configuration, Bean, Autowired, Service, RestController
from .scanner import ComponentScanner, scan_components
from .container import Container, BeanInfo
from .context import ApplicationContext
from .global_context import (
    initialize_context, 
    get_context, 
    get_bean, 
    is_context_initialized,
    get_all_controllers,
)
from .application import SpringApplication, SpringBootApplication

__version__ = "0.1.3"
__all__ = [
    "Component", "Configuration", "Bean", "Autowired", "Service", "RestController"
    "ComponentScanner", "scan_components",
    "Container", "BeanInfo",
    "ApplicationContext",
    "initialize_context", "get_context", "get_bean", "is_context_initialized", "get_all_controllers",
    "SpringApplication", "SpringBootApplication"
]
