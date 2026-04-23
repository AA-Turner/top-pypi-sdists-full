#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Filter which jars from ``snowpark_connect_deps_1`` and ``snowpark_connect_deps_2``
are added to the server-side JVM classpath at startup.

Rationale
---------
Those two PyPI packages ship the full Spark 3.5.6 distribution plus its
transitive dependencies (Scala toolchain, Hadoop client, MLlib math, Kryo,
Hive, Kubernetes, Streaming, ...).

Of those 57 jars, only **6** are ever uploaded to the Snowflake session
stage for Scala UDF execution (``resources_initializer._upload_scala_2_12/13_jars``):
``spark-sql``, ``spark-connect-client-jvm``, ``spark-common-utils``,
``sas-scala-udf``, ``json4s-ast``, and ``scala-reflect``. The remaining
51 jars are not uploaded and are not needed by any stage-side Scala UDF.

On the SCOS server itself, only a narrow set of classes is loaded via
JPype (the SQL parser, ``StructType``, exception types, a few
``scala-library`` helpers). The rest of the jars are pure dead weight on
the server classpath and bloat the JVM's start-up footprint.

This module pins, by **exact filename**, the jars that the SCOS server
JVM does not need at runtime. It is a pure classpath filter; the on-demand
upload path in ``resources_initializer.py`` (which looks up jars by exact
name) is not affected, and the jars themselves still ship in the deps wheels.

Skippable jars (``_CLASSPATH_DROP_JARS``)
-----------------------------------------
29 jars, ~21.26 MB, never loaded by the SCOS server hot path. Verified by
CI (PR #3685) -- removing any of these from the classpath leaves every
required test green.

  Spark modules not exercised by SCOS:
    * spark-streaming_2.12-3.5.6.jar           (1.07 MB) -- no streaming
    * spark-kubernetes_2.12-3.5.6.jar          (0.51 MB) -- no cluster mgr
    * spark-hive_2.12-3.5.6.jar                (0.69 MB) -- Snowflake catalog
    * spark-network-shuffle_2.12-3.5.6.jar     (0.17 MB) -- no ext shuffle
    * spark-kvstore_2.12-3.5.6.jar             (0.08 MB) -- history server
    * spark-sketch_2.12-3.5.6.jar              (0.03 MB) -- BloomFilter unused
    * spark-sql-api_2.12-3.5.6.jar             (1.69 MB) -- 100% duplicate of
                                                            spark-connect-client-jvm

  Scala toolchain bits not used at runtime:
    * scala-compiler-2.12.18.jar              (10.47 MB) -- no runtime scalac
    * scala-xml_2.12-2.1.0.jar                 (0.44 MB) -- only used by
                                                            scala-compiler /
                                                            spark-hive

  MLlib / stats math (no MLlib on SCOS):
    * commons-math3-3.6.1.jar                  (2.11 MB)

  Hive metastore JDBC connection pool (no Hive):
    * commons-dbcp-1.4.jar                     (0.15 MB)
    * commons-pool-1.5.4.jar                   (0.09 MB)

  ``spark-submit`` CLI argument parsing (SCOS is not spark-submit):
    * commons-cli-1.5.0.jar                    (0.06 MB)

  Log4j 1.x compatibility shims (all runtime logging goes through log4j2):
    * log4j-1.2-api-2.20.0.jar                 (0.33 MB)
    * jackson-dataformat-yaml-2.15.2.jar       (0.05 MB) -- log4j2 YAML cfg

  Legacy Apache Commons (distinct from commons-collections4 / commons-lang3
  which we keep). Only referenced by the unused Hive/Hadoop stack:
    * commons-collections-3.2.2.jar            (0.56 MB)
    * commons-lang-2.6.jar                     (0.27 MB)

  Jackson 1.x (org.codehaus.jackson). SCOS / Spark use Jackson 2.x:
    * jackson-core-asl-1.9.13.jar              (0.22 MB)

  json4s native parser (SCOS path uses the Jackson backend):
    * json4s-native_2.12-3.7.0-M11.jar         (0.09 MB)

  SLF4J -> log4j2 binding (SLF4J falls back to a NOP provider when missing):
    * log4j-slf4j2-impl-2.20.0.jar             (0.03 MB)

  Scala collection-compat polyfill (zero bytecode references in any kept jar;
  all kept jars target Scala 2.12 natively):
    * scala-collection-compat_2.12-2.7.0.jar   (0.24 MB)

  Scala parser combinators (Spark 3.5 SQL parsing is ANTLR4; JsonPathParser
  is only instantiated during plan evaluation, never triggered by SCOS):
    * scala-parser-combinators_2.12-2.3.0.jar  (0.18 MB)

  Janino JVM compiler (WholeStageCodegen / CodeGenerator only; SCOS has no
  Spark executors and never JIT-compiles physical plans):
    * commons-compiler-3.1.9.jar               (0.17 MB)

  Spark I/O and RPC encryption (only loaded when
  spark.network.crypto.enabled / spark.io.encryption.enabled is set;
  SCOS does not enable either):
    * commons-crypto-1.1.0.jar                 (0.16 MB)

  Apache Commons Compress (bzip2/XZ/Zstd codecs; CompressionCodec companion
  defers instantiation until data is actually read/written; SCOS never
  reads or writes compressed RDD/shuffle data):
    * commons-compress-1.26.0.jar              (1.03 MB)

  Apache Commons IO (only referenced by Driver/executor operational classes
  -- DiskStore, DriverLogger, HDFSBackedStateStoreProvider -- none reachable
  from the SCOS JPype seed classes):
    * commons-io-2.16.1.jar                    (0.49 MB)

  Apache Commons Collections 4 (only BroadcastManager and
  StageDataWrapperSerializer in spark-core reference it; SCOS has no
  SparkContext / broadcast variables):
    * commons-collections4-4.4.jar             (0.72 MB)

  Apache Commons Logging / JCL (only JettyLogHandler in spark-core; Jetty
  web UI is never started in SCOS; SLF4J's JCL bridge already replaces
  the JCL API in the shaded bundle):
    * commons-logging-1.1.3.jar                (0.06 MB)

  Jackson Java-8 date/time module (ObjectMapperFactory in
  spark-connect-client-jvm registers JavaTimeModule only inside a factory
  method body; not accessed in the normal SCOS gRPC hot path):
    * jackson-datatype-jsr310-2.15.2.jar       (0.12 MB)

Jars required ONLY by ``execute_jar`` (``_EXECUTE_JAR_ONLY_JARS``)
-----------------------------------------------------------------
2 jars, ~20.57 MB, irrelevant to the gRPC server hot path but required by
``tools/snowpark-connect-execute-jar`` -> ``server.execute_jar()``, which
runs a customer Java/Scala Spark application *inside* the SCOS JVM.

  * spark-connect-client-jvm_2.12-3.5.6.jar  (20.55 MB)
      Routes ``SparkSession.builder().getOrCreate()`` through Spark
      Connect's gRPC client. Without it, the customer's Scala app falls
      back to constructing a classic ``SparkContext`` which requires
      ``hadoop-client-runtime`` (not shipped) and dies with
      ``NoClassDefFoundError: org.apache.hadoop.shaded.org.apache.commons.
      configuration2.Configuration``.

  * spark-tags_2.12-3.5.6.jar                 (0.01 MB)
      Marker jar for Spark developer-API annotations (``@DeveloperApi`` /
      ``@Unstable`` / ``@Experimental``). The JVM tolerates missing RUNTIME
      annotations, but ``scala.reflect``'s pickled-symbol reader does not:
      when the customer's Scala app calls
      ``SparkSession.builder().getOrCreate()``, scala-reflect deserializes
      Spark's pickled Scala signature metadata and needs every annotation
      class referenced there to resolve. Dropping this jar raises
      ``java.lang.AssertionError: unsafe symbol Unstable (child of package
      annotation) in runtime reflection universe``.

These are kept on the default classpath today for safety. A follow-up can
add a lazy-load hook inside ``execute_jar()`` to include them only when
that entry point is invoked, freeing ~20 MB of JVM class metadata on the
normal server hot path.

Intentionally NOT skipped
-------------------------
These jars were flagged as drop candidates but confirmed necessary by
CI gate runs or Codex bytecode analysis (noted per entry):

  * json4s-{core,jackson,scalap}_2.12 -- Spark references
    ``org.json4s.jackson.JsonMethods`` when building error messages /
    parse trees. (json4s-ast is also kept; ``resources_initializer``
    uploads it explicitly for Scala UDFs.) CI run 24586132218.

  * hadoop-client-api -- ``SQLConf.<clinit>`` pulls
    ``org.apache.hadoop.fs.FSDataInputStream``. CI run 24586132218.

  * spark-network-common_2.12 -- ``SQLConf.bytesConf(...)`` references
    ``org.apache.spark.network.util.ByteUnit``. Defensive keep (would
    have failed in the same CI run as hadoop-client-api).

  * kryo-shaded -- catalyst expression / aggregate classes declare
    ``implements KryoSerializable``; the JVM verifies the interface symbol
    at class-load time even though SCOS never serializes anything.
    CI run 24587234263.

  * commons-codec-1.16.1 -- ``AstBuilder.visitBitStringLiteral()`` calls
    ``Hex.decodeHex()`` for SQL hex literals (``X'ABCD'``). Even though
    this is an invokestatic (lazy per JVM §5.4.3), SCOS exposes SQL
    parsing and any query using a hex/bit-string literal would fail at
    runtime. Codex bytecode review (PR #3685).

  * jackson-module-scala_2.12 -- ``DefaultScalaModule$`` is referenced at
    class-load time, not just in method bodies. CI run 24656500830
    surfaced ``NoClassDefFoundError: com/fasterxml/jackson/module/scala/
    DefaultScalaModule$`` across multiple tests, cascading into
    ``Could not initialize class SparkThrowableHelper$``.

  * commons-text-1.10.0 -- ``Like`` and ``RLike`` expression classes in
    ``spark-catalyst`` reference ``StringEscapeUtils`` directly. LIKE /
    RLIKE are common SQL operators exercised throughout the test suite.
    Codex bytecode review (PR #3685).

  * scala-reflect-2.12.18.jar -- ``Literal$.<clinit>`` fails to complete
    without it. CI run on PR #3685 trial-drop commit raised
    ``NoClassDefFoundError: Could not initialize class
    org.apache.spark.sql.catalyst.expressions.Literal$`` across
    ``DatasetFilterWhereTest`` and ``DatasetSelectTest`` (any test that
    evaluates a string expression via ``filter()`` / ``where()`` /
    ``selectExpr()``). ``Literal$`` companion object references
    ``scala.reflect`` types in its static initializer, not just inside
    TypeTag-parametrized method bodies.

Kill switch
-----------
Set ``SCOS_JVM_CLASSPATH_FULL=1`` in the environment to disable filtering
and restore the previous behaviour of loading every jar from both packages.

Version-bump policy
-------------------
Entries below are pinned to **exact filenames** (with version suffix), so
a Spark or transitive-dependency upgrade in the deps packages will simply
stop matching and the affected jars will silently re-enter the classpath.
``filter_classpath_jars()`` emits a WARNING when an entry no longer
matches any shipped jar so the drift is visible in server startup logs.
"""

from __future__ import annotations

import os
from pathlib import Path

from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_FULL_CLASSPATH_ENV = "SCOS_JVM_CLASSPATH_FULL"

# Exact jar filenames excluded from the SCOS server JVM classpath.
# See module docstring for size, category, and rationale per entry.
_CLASSPATH_DROP_JARS: frozenset[str] = frozenset(
    {
        # Spark modules not exercised by the SCOS server JVM.
        "spark-streaming_2.12-3.5.6.jar",
        "spark-kubernetes_2.12-3.5.6.jar",
        "spark-hive_2.12-3.5.6.jar",
        "spark-network-shuffle_2.12-3.5.6.jar",
        "spark-kvstore_2.12-3.5.6.jar",
        "spark-sketch_2.12-3.5.6.jar",
        "spark-sql-api_2.12-3.5.6.jar",
        # Scala toolchain bits only used for runtime compilation / XML.
        "scala-compiler-2.12.18.jar",
        "scala-xml_2.12-2.1.0.jar",
        # MLlib / stats math (no MLlib on SCOS).
        "commons-math3-3.6.1.jar",
        # Hive metastore JDBC connection pool (no Hive).
        "commons-dbcp-1.4.jar",
        "commons-pool-1.5.4.jar",
        # ``spark-submit`` CLI argument parsing (SCOS is not spark-submit).
        "commons-cli-1.5.0.jar",
        # Log4j 1.x compatibility shims; runtime logging goes through log4j2.
        "log4j-1.2-api-2.20.0.jar",
        "jackson-dataformat-yaml-2.15.2.jar",
        # Legacy Apache Commons; commons-collections4 / commons-lang3 are kept.
        "commons-collections-3.2.2.jar",
        "commons-lang-2.6.jar",
        # Jackson 1.x; SCOS / Spark use Jackson 2.x.
        "jackson-core-asl-1.9.13.jar",
        # json4s native parser; SCOS path uses the Jackson backend.
        "json4s-native_2.12-3.7.0-M11.jar",
        # SLF4J -> log4j2 binding; SLF4J falls back to NOP when missing.
        "log4j-slf4j2-impl-2.20.0.jar",
        # Scala collection-compat polyfill; zero references in any kept jar.
        "scala-collection-compat_2.12-2.7.0.jar",
        # Scala parser combinators; Spark 3.5 SQL parsing is ANTLR4.
        # JsonPathParser is plan-evaluation only -- never triggered by SCOS.
        "scala-parser-combinators_2.12-2.3.0.jar",
        # Janino compiler (commons-compiler API jar). WholeStageCodegen only;
        # SCOS has no executors and never JIT-compiles physical plans.
        "commons-compiler-3.1.9.jar",
        # Apache Commons Crypto. RPC / IO cipher only loaded when
        # spark.network.crypto.enabled or spark.io.encryption.enabled is set.
        # SCOS does not enable either; no SparkContext is ever created.
        "commons-crypto-1.1.0.jar",
        # Apache Commons Compress. bzip2/XZ/Zstd codec implementations.
        # CompressionCodec companion defers instantiation until data is
        # actually read/written; SCOS never reads/writes compressed data.
        "commons-compress-1.26.0.jar",
        # Apache Commons IO. Only referenced by Driver/executor operational
        # classes (DiskStore, DriverLogger, etc.) not reachable from SCOS.
        "commons-io-2.16.1.jar",
        # Apache Commons Collections 4. Only BroadcastManager and
        # StageDataWrapperSerializer; SCOS has no SparkContext/broadcast.
        "commons-collections4-4.4.jar",
        # Apache Commons Logging / JCL. Only JettyLogHandler (Jetty web UI
        # is never started in SCOS). SLF4J's JCL bridge already covers it.
        "commons-logging-1.1.3.jar",
        # Jackson Java-8 date/time module. ObjectMapperFactory registers
        # JavaTimeModule only inside a factory method body (lazy); not a
        # field type -- not loaded on the normal SCOS gRPC hot path.
        "jackson-datatype-jsr310-2.15.2.jar",
    }
)


# Exact jar filenames required ONLY by the ``snowpark-connect-execute-jar``
# CLI (``server.execute_jar()``). See module docstring for full rationale
# and the CI evidence captured in PR #3685.
#
# Today these jars are still added to the default server classpath so they
# do *not* appear in ``_CLASSPATH_DROP_JARS``. The set is exposed as a
# named constant so a future PR can wire ``execute_jar()`` to add them
# lazily and remove them from the default server classpath.
_EXECUTE_JAR_ONLY_JARS: frozenset[str] = frozenset(
    {
        "spark-connect-client-jvm_2.12-3.5.6.jar",
        "spark-tags_2.12-3.5.6.jar",
    }
)


def is_classpath_filtering_disabled() -> bool:
    """Return True when the user has opted out of classpath filtering."""
    return os.environ.get(_FULL_CLASSPATH_ENV, "") == "1"


def should_include_on_classpath(jar_path: Path) -> bool:
    """Return True if ``jar_path`` should be added to the JVM classpath."""
    if is_classpath_filtering_disabled():
        return True
    return jar_path.name not in _CLASSPATH_DROP_JARS


def filter_classpath_jars(
    jar_paths: list[Path],
) -> tuple[list[Path], list[Path]]:
    """Partition ``jar_paths`` into ``(kept, dropped)`` by the drop list.

    When ``SCOS_JVM_CLASSPATH_FULL=1`` is set, every jar is kept and the
    dropped list is empty.

    Emits a WARNING for any entry in ``_CLASSPATH_DROP_JARS`` /
    ``_EXECUTE_JAR_ONLY_JARS`` that no longer matches a shipped jar -- the
    pinned filenames have drifted from the deps packages and need an
    update.
    """
    if is_classpath_filtering_disabled():
        return list(jar_paths), []
    kept: list[Path] = []
    dropped: list[Path] = []
    for jar_path in jar_paths:
        if should_include_on_classpath(jar_path):
            kept.append(jar_path)
        else:
            dropped.append(jar_path)

    shipped_names = {p.name for p in jar_paths}
    stale_drops = sorted(_CLASSPATH_DROP_JARS - shipped_names)
    stale_execjar = sorted(_EXECUTE_JAR_ONLY_JARS - shipped_names)
    if stale_drops:
        logger.warning(
            "JVM classpath filter has stale drop entries (no longer shipped, "
            "likely a deps package version bump): %s",
            ", ".join(stale_drops),
        )
    if stale_execjar:
        logger.warning(
            "JVM classpath filter has stale execute_jar-only entries "
            "(no longer shipped): %s",
            ", ".join(stale_execjar),
        )
    return kept, dropped


def log_classpath_filter_summary(kept: list[Path], dropped: list[Path]) -> None:
    """Emit an INFO summary and a DEBUG list of dropped jars."""
    if is_classpath_filtering_disabled():
        logger.info(
            "JVM classpath filter disabled via %s; loading all %d jars.",
            _FULL_CLASSPATH_ENV,
            len(kept),
        )
        return
    logger.info(
        "JVM classpath: %d jars included, %d dropped "
        "(set %s=1 to restore the full classpath).",
        len(kept),
        len(dropped),
        _FULL_CLASSPATH_ENV,
    )
    if dropped:
        logger.debug(
            "Dropped from JVM classpath: %s",
            ", ".join(sorted(p.name for p in dropped)),
        )
