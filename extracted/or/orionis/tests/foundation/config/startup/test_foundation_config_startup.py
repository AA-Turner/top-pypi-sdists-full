from dataclasses import is_dataclass
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.foundation.config.startup import Configuration
from orionis.foundation.config.app.entities.app import App
from orionis.foundation.config.auth.entities.auth import Auth
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.roots.paths import Paths
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.session.entities.session import Session
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigStartup(AsyncTestCase):
    """
    Test suite for the `Configuration` dataclass, validating its structure, initialization,
    type enforcement, mutability, equality, and dictionary conversion.

    Methods
    -------
    testConfigurationIsDataclass
        Verify that `Configuration` is a dataclass.
    testDefaultInitialization
        Ensure all fields of `Configuration` are initialized with their default factories and correct types.
    testAllSectionsHaveDefaultFactories
        Check that every field in `Configuration` has a callable default factory.
    testTypeValidationInPostInit
        Confirm that type validation and dictionary conversion occur in `__post_init__`,
        and that invalid types raise `OrionisIntegrityException`.
    testToDictReturnsCompleteDictionary
        Assert that `toDict()` returns a dictionary containing all configuration sections.
    testToDictReturnsNestedStructures
        Ensure that nested configuration sections are represented as dictionaries in `toDict()` output.
    testMetadataIsAccessible
        Validate that field metadata is accessible and contains required keys and types.
    testConfigurationIsMutable
        Check that attributes of `Configuration` can be modified after initialization.
    testConfigurationEquality
        Test equality comparison between `Configuration` instances, especially with differing keys.
    """

    def testConfigurationIsDataclass(self):
        """
        Verify that `Configuration` is implemented as a dataclass.

        Returns
        -------
        None
        """
        self.assertTrue(is_dataclass(Configuration))

    def testDefaultInitialization(self):
        """
        Ensure all fields of `Configuration` are initialized with their default factories
        and are instances of their respective entity classes.

        Returns
        -------
        None
        """
        config = Configuration()
        self.assertIsInstance(config, Configuration)
        self.assertIsInstance(config.app, App)
        self.assertIsInstance(config.auth, Auth)
        self.assertIsInstance(config.cache, Cache)
        self.assertIsInstance(config.cors, Cors)
        self.assertIsInstance(config.database, Database)
        self.assertIsInstance(config.filesystems, Filesystems)
        self.assertIsInstance(config.logging, Logging)
        self.assertIsInstance(config.mail, Mail)
        self.assertIsInstance(config.path, Paths)
        self.assertIsInstance(config.queue, Queue)
        self.assertIsInstance(config.session, Session)
        self.assertIsInstance(config.testing, Testing)

    def testAllSectionsHaveDefaultFactories(self):
        """
        Check that every field in `Configuration` has a callable default factory.

        Returns
        -------
        None
        """
        config = Configuration()
        for field in config.__dataclass_fields__.values():
            self.assertTrue(callable(field.default_factory),
                            f"Field {field.name} is missing default_factory")

    def testTypeValidationInPostInit(self):
        """
        Confirm that type validation and dictionary conversion occur in `__post_init__`.
        Validates that dictionaries are converted to entity instances and invalid types
        raise `OrionisIntegrityException`.

        Returns
        -------
        None
        """
        # Valid dict conversion
        config = Configuration(app={"name": "TestApp"})
        self.assertIsInstance(config.app, App)

        # Invalid types for each section should raise an exception
        sections = [
            ('app', 123),
            ('auth', 123),
            ('cache', 123),
            ('cors', 123),
            ('database', 123),
            ('filesystems', 123),
            ('logging', 123),
            ('mail', 123),
            ('path', 123),
            ('queue', 123),
            ('session', 123),
            ('testing', 123)
        ]
        for section_name, wrong_value in sections:
            with self.subTest(section=section_name):
                kwargs = {section_name: wrong_value}
                with self.assertRaises(OrionisIntegrityException):
                    Configuration(**kwargs)

    def testToDictReturnsCompleteDictionary(self):
        """
        Assert that `toDict()` returns a dictionary containing all configuration sections.

        Returns
        -------
        None
        """
        config = Configuration()
        config_dict = config.toDict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(set(config_dict.keys()), set(config.__dataclass_fields__.keys()))

    def testToDictReturnsNestedStructures(self):
        """
        Ensure that nested configuration sections are represented as dictionaries
        in the output of `toDict()`.

        Returns
        -------
        None
        """
        config = Configuration()
        config_dict = config.toDict()
        self.assertIsInstance(config_dict['app'], dict)
        self.assertIsInstance(config_dict['auth'], dict)
        self.assertIsInstance(config_dict['database'], dict)
        self.assertIsInstance(config_dict['path'], dict)

    def testMetadataIsAccessible(self):
        """
        Validate that field metadata is accessible and contains the 'description' key
        as a string and the 'default' key.

        Returns
        -------
        None
        """
        config = Configuration()
        for field in config.__dataclass_fields__.values():
            metadata = field.metadata
            self.assertIn('description', metadata)
            self.assertIsInstance(metadata['description'], str)
            self.assertIn('default', metadata)

    def testConfigurationIsMutable(self):
        """
        Check that attributes of `Configuration` can be modified after initialization.

        Returns
        -------
        None
        """
        config = Configuration()
        new_app = App()
        try:
            config.app = new_app
        except Exception as e:
            self.fail(f"Should be able to modify attributes, but got {type(e).__name__}")

    def testConfigurationEquality(self):
        """
        Test equality comparison between `Configuration` instances, ensuring that
        instances with differing keys are not considered equal.

        Returns
        -------
        None
        """
        # Ensure both configs have identical App objects, but their keys differ
        app_data = {"name": "TestApp"}
        config1 = Configuration(app=app_data)
        config2 = Configuration(app=app_data)
        # The key (e.g., a generated UUID or secret) will be different for each instance
        self.assertNotEqual(config1, config2)
