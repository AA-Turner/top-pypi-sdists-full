import subprocess
import unittest
import os
import sqlite3
import numpy as np
from PIL import Image, ImageChops

def call_pikobs_from_python():
    """
    Calls the pikobs.timeserie.arg_call() function with pre-defined parameters using subprocess.

    Returns:
        tuple: stdout and stderr from the command execution.
    
    Raises:
        RuntimeError: If the command execution fails.
    """
    command = [
        "python", "-c", "import pikobs; pikobs.timeserie.arg_call()",
        "--path_experience_files", "maestro_archives/rel90devg2/monitoring/banco/postalt/",
        "--experience_name", "ops+NOAA21+GOES19",
        "--path_control_files", "maestro_archives/rel90devg2ops/operation.observations.banco.postalt.sqlite.g2/",
        "--control_name", "ops",
        "--pathwork", "onthefly",
        "--datestart", "2025041200",
        "--dateend", "2025041300",
        "--region", "Monde",
        "--family", "sw",
        "--flags_criteria", "assimilee",
        "--fonction", "omp",
        "--id_stn", "all",
        "--channel", "join",
        "--n_cpu", "40"]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"The command failed with error code {result.returncode}:\n{result.stderr}")

    return result.stdout, result.stderr

def files_identical(ref_file, gen_file):
    """
    Compare two files of any type based on content.

    Args:
        ref_file (str): Path to the reference file.
        gen_file (str): Path to the generated file.

    Returns:
        bool: True if files are identical, False otherwise.
    """
    if ref_file.endswith('.db'):
        return sqlite_files_are_identical(ref_file, gen_file)

    if ref_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        return images_are_identical(ref_file, gen_file)

    return True

def sqlite_files_are_identical(file1, file2):
    """
    Compares two SQLite database files.

    Args:
        file1 (str): Path to the first SQLite file.
        file2 (str): Path to the second SQLite file.

    Returns:
        bool: True if the files are structurally and content-wise identical, False otherwise.
    """
    with sqlite3.connect(file1) as conn1, sqlite3.connect(file2) as conn2:
        cursor1, cursor2 = conn1.cursor(), conn2.cursor()

        # Table and data comparison
        cursor1.execute("SELECT * FROM sqlite_master WHERE type='table';")
        cursor2.execute("SELECT * FROM sqlite_master WHERE type='table';")
        tables1 = set(cursor1.fetchall())
        tables2 = set(cursor2.fetchall())
        if tables1 != tables2:
            print(f"Tables differ between {file1} and {file2}:\n  - {tables1}\n  - {tables2}")
            return False

        for table in tables1:
            print(f"Comparing table {table[1]}")
            cursor1.execute(f"SELECT * FROM {table[1]} ORDER BY 1;")
            rows1 = sorted(cursor1.fetchall())

            cursor2.execute(f"SELECT * FROM {table[1]} ORDER BY 1;")
            rows2 = sorted(cursor2.fetchall())
            if rows1 != rows2 or not np.array_equal(rows1, rows2):
                print(f"Row data differs in table {table[0]}")
                return False

    return True

def images_are_identical(img1_path, img2_path):
    """
    Check if two images are identical.

    Args:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.

    Returns:
        bool: True if images are identical, False otherwise.
    """
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    if img1.size != img2.size or img1.mode != img2.mode:
        return False

    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is None

def files_exist_and_are_identical(reference_dir, generated_dir):
    """
    Check if all reference files exist in the generated directory and match in content.

    Args:
        reference_dir (str): Path to the directory containing reference files.
        generated_dir (str): Path to the directory containing generated files.

    Returns:
        bool: True if all files exist and are identical, False otherwise.
    """
    for root, _, files in os.walk(reference_dir):
        for name in files:
            ref_file_path = os.path.join(root, name)
            rel_path = os.path.relpath(ref_file_path, reference_dir)
            gen_file_path = os.path.join(generated_dir, rel_path)
            if not os.path.exists(gen_file_path) or not files_identical(ref_file_path, gen_file_path):
                return False

    return True

class TestCallPikObs_timeserie(unittest.TestCase):
    """
    Unit test suite for verifying file generation and comparison.

    Attributes:
        path_reference (str): Path to the reference directory

    Methods:
        setUp(): Prepares the test environment.
        test_call_and_compare(): Tests the call to pikobs and file comparisons.
    """
    path_reference = None

    def setUp(self):
        self.path_reference = self.__class__.path_reference

    def test_call_and_compare(self):
        if not self.path_reference:
            self.fail("Path to the reference directory must be provided.")

        try:
            call_pikobs_from_python()

            path_to_validate = os.path.abspath('onthefly')
            if not os.path.exists(self.path_reference):
                self.fail(f"Reference directory does not exist: {self.path_reference}")

            self.assertTrue(
                files_exist_and_are_identical(self.path_reference, path_to_validate),
                "Not all reference files exist in the generated directory with identical content."
            )
        except RuntimeError as e:
            self.fail(f"call_pikobs_from_python raised an exception: {e}")
