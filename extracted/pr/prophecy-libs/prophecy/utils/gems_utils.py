from prophecy.config import is_scala_disabled, get_scala_disabled_error

def concatenateFiles(spark, file_format, mode, inputDir, outputFileName, deleteTempPath=True, fileFormatHasHeaders=True):
    if is_scala_disabled():
        raise RuntimeError(get_scala_disabled_error("concatenateFiles"))
    
    jvm = spark.sparkContext._jvm
    jvm.io.prophecy.libs.package.concatenateFiles(spark._jsparkSession, file_format, mode, inputDir, outputFileName, deleteTempPath, fileFormatHasHeaders)

