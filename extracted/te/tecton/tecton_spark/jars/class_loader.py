import os
import shutil
import tempfile
import threading
from importlib import resources
from pathlib import Path

from py4j.java_gateway import JavaObject
from pyspark import SparkContext


# Environment variables for the jar path. It is only used for integration tests because in local integration tests the
# file is not accessible via the resources.path. We need to access it via the Bazel runfiles.
_UDF_JAR_PATH = os.environ.get("UDF_JAR_PATH_FOR_INTEGRATION_TEST")


class SingletonResourceJarClassLoader:
    """Wraps a Java ClassLoader with its classpath set to a JAR.
    Additionally, upon initialization the JAR file is added to the SparkContext JARs, which will cause it to be added
    to the class path of executors. This is so that e.g. UDFs loaded from this class loader on the driver will be able
    to find their classes on the executors during deserialization.
    """

    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls, jar: Path) -> None:
        with cls._init_lock:
            if not cls._instance:
                cls._instance = super(SingletonResourceJarClassLoader, cls).__new__(cls)
                cls._instance._initialize(jar)
            return cls._instance

    def _initialize(self, jar: Path) -> None:
        self._jar = tempfile.NamedTemporaryFile()
        shutil.copyfile(jar, self._jar.name)
        self._lock = threading.Lock()
        self._loader = None

    def get_loader(self, sc: SparkContext) -> JavaObject:
        """Lazily initializes and returns the ClassLoader object."""
        with self._lock:
            if not self._loader:
                gateway = sc._gateway
                # This tells Spark to ship the JAR to the executors and add it to the class path.
                sc._jsc.addJar(self._jar.name)
                jvm = gateway.jvm
                URL = jvm.java.net.URL
                URLClassLoader = jvm.java.net.URLClassLoader
                url_array = gateway.new_array(URL, 1)
                url_array[0] = URL(f"file://{self._jar.name}")
                self._loader = URLClassLoader(url_array)
            return self._loader

    def load_class(self, sc: SparkContext, class_name: str) -> JavaObject:
        """Loads and initializes the class"""
        return sc._gateway.jvm.java.lang.Class.forName(class_name, True, self.get_loader(sc))


def get_or_create_udf_jar_class_loader():
    if _UDF_JAR_PATH:
        return SingletonResourceJarClassLoader(Path(_UDF_JAR_PATH))
    else:
        with resources.path("tecton_spark.jars", "tecton-udfs-spark-3.jar") as p:
            return SingletonResourceJarClassLoader(p)
