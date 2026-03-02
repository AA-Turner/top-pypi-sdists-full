import numpy as np
from multiprocessing import Pool
from functools import partial
from joblib import Parallel, delayed
import time


# Function to simulate distance calculation (Euclidean distance in this case)
def compute_distance(patch, mfcc_ref):
    return np.linalg.norm(mfcc_ref - patch)


# Function for multiprocessing.Pool.map (using patch index)
def compute_distance_from_index(index, mfcc_deg_patches, mfcc_ref):
    patch = mfcc_deg_patches[:, index, :]  # Extract the patch using the index
    return np.linalg.norm(mfcc_ref - patch)


# Function for multiprocessing.Pool.starmap
def parallel_pool_starmap(mfcc_deg_patches, mfcc_ref, n_jobs=4):
    num_patches = mfcc_deg_patches.shape[1]  # Number of patches (second dimension of mfcc_deg_patches)

    # Prepare a list of tuples for starmap: (index, mfcc_deg_patches, mfcc_ref)
    args = [(i, mfcc_deg_patches, mfcc_ref) for i in range(num_patches)]

    with Pool(processes=n_jobs) as pool:
        results = pool.starmap(compute_distance_from_index, args)

    return results


# Parallel method using multiprocessing.Pool.map
def parallel_pool_map(mfcc_deg_patches, mfcc_ref, n_jobs=4):
    num_patches = mfcc_deg_patches.shape[1]  # Number of patches (second dimension of mfcc_deg_patches)
    partial_func = partial(compute_distance_from_index, mfcc_deg_patches=mfcc_deg_patches, mfcc_ref=mfcc_ref)
    with Pool(processes=n_jobs) as pool:
        results = pool.map(partial_func, range(num_patches))
    return results


# Parallel method using joblib.Parallel
def parallel_joblib(mfcc_deg_patches, mfcc_ref, n_jobs=4):
    num_patches = mfcc_deg_patches.shape[1]  # Number of patches
    results = Parallel(n_jobs=n_jobs)(delayed(compute_distance_from_index)(i, mfcc_deg_patches, mfcc_ref) for i in range(num_patches))
    return results


# Function to generate large fake MFCC data for testing
def generate_fake_data(num_patches, n_mfcc, cols_per_patch):
    mfcc_ref = np.random.randn(n_mfcc, cols_per_patch)  # Fake reference MFCC (n_mfcc, cols_per_patch)
    mfcc_deg_patches = np.random.randn(n_mfcc, num_patches, cols_per_patch)  # Fake degraded patches (n_mfcc, num_patches, cols_per_patch)
    return mfcc_ref, mfcc_deg_patches


# Main testing function to compare performance
def test_parallel_methods():
    # Parameters
    n_jobs = 8  # Number of parallel processes
    num_patches = 5000  # Number of patches to simulate (large dataset)
    n_mfcc = 13  # Number of MFCC coefficients
    cols_per_patch = 40  # Number of columns per patch (window size)

    # Generate large fake data
    mfcc_ref, mfcc_deg_patches = generate_fake_data(num_patches, n_mfcc, cols_per_patch)

    # Test with Pool.map
    print("Testing with multiprocessing.Pool.map...")
    start_time = time.time()
    pool_map_results = parallel_pool_map(mfcc_deg_patches, mfcc_ref, n_jobs=n_jobs)
    pool_map_time = time.time() - start_time
    print(f"Pool.map took: {pool_map_time:.3f} seconds")

    # Test with Pool.starmap
    print("Testing with multiprocessing.Pool.starmap...")
    start_time = time.time()
    pool_starmap_results = parallel_pool_starmap(mfcc_deg_patches, mfcc_ref, n_jobs=n_jobs)
    pool_starmap_time = time.time() - start_time
    print(f"Pool.starmap took: {pool_starmap_time:.3f} seconds")

    # Test with joblib.Parallel
    print("Testing with joblib.Parallel...")
    start_time = time.time()
    joblib_results = parallel_joblib(mfcc_deg_patches, mfcc_ref, n_jobs=n_jobs)
    joblib_time = time.time() - start_time
    print(f"joblib.Parallel took: {joblib_time:.3f} seconds")

    # Verify all methods give the same results
    assert np.allclose(pool_map_results, pool_starmap_results), "Results do not match between Pool.map and Pool.starmap!"
    assert np.allclose(pool_map_results, joblib_results), "Results do not match between Pool.map and joblib.Parallel!"
    print("All methods produced the same results!")


if __name__ == "__main__":
    test_parallel_methods()
