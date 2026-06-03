#!/usr/bin/env python3
"""
Test remaining benchmarks after gpqa (59 benchmarks).
Continues from where the previous test stopped.
"""

import json
import logging
import subprocess
import time
from pathlib import Path

# Remaining benchmarks after gpqa
REMAINING_BENCHMARKS = [
    "gpqa_diamond", "gpqa_extended", "gpqa_main_zeroshot", "gpqa_diamond_zeroshot",
    "gpqa_extended_zeroshot", "gpqa_main_cot_zeroshot", "gpqa_diamond_cot_zeroshot",
    "gpqa_extended_cot_zeroshot", "supergpqa", "supergpqa_physics", "supergpqa_chemistry",
    "supergpqa_biology", "gsm8k", "math", "math500", "hendrycks_math", "aime", "aime2025",
    "aime2024", "hmmt", "hmmt_feb_2025", "polymath", "polymath_en_medium", "polymath_zh_medium",
    "polymath_en_high", "polymath_zh_high", "livemathbench", "livemathbench_cnmo_en",
    "livemathbench_cnmo_zh", "arithmetic", "asdiv", "humaneval", "mbpp", "mmmlu", "wikitext",
    "humaneval_plus", "instructhumaneval", "apps", "mbpp_plus", "ds1000", "multiple_py",
    "multiple_js", "multiple_java", "multiple_cpp", "multiple_rs", "multiple_go", "recode",
    "conala", "concode", "codexglue_code_to_text_python", "codexglue_code_to_text_go",
    "codexglue_code_to_text_ruby", "codexglue_code_to_text_java",
    "codexglue_code_to_text_javascript", "codexglue_code_to_text_php", "mercury", "hle",
    "hle_exact_match", "hle_multiple_choice"
]

# Skip all gpqa variants and supergpqa variants (likely also gated)
SKIP_BENCHMARKS = {
    "gpqa_diamond", "gpqa_extended", "gpqa_main_zeroshot", "gpqa_diamond_zeroshot",
    "gpqa_extended_zeroshot", "gpqa_main_cot_zeroshot", "gpqa_diamond_cot_zeroshot",
    "gpqa_extended_cot_zeroshot", "supergpqa", "supergpqa_physics", "supergpqa_chemistry",
    "supergpqa_biology"
}

# Configuration
MODEL = "meta-llama/Llama-3.1-8B-Instruct"
LAYER = 15
LIMIT = 10
TOKEN_STRATEGY = "max_pooling"

def test_remaining_benchmarks():
    """Test remaining benchmarks after gpqa."""
    
    # Filter out gpqa variants
    benchmarks_to_test = [b for b in REMAINING_BENCHMARKS if b not in SKIP_BENCHMARKS]
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('remaining_benchmarks.log'),
            logging.StreamHandler()
        ]
    )
    
    logging.info(f"Testing {len(benchmarks_to_test)} remaining benchmarks (skipping gpqa/supergpqa variants)")
    
    results = {}
    successful = 0
    failed = 0
    
    for i, benchmark in enumerate(benchmarks_to_test, 1):
        print(f"\n[{i}/{len(benchmarks_to_test)}] Testing {benchmark}...")
        logging.info(f"Starting test for benchmark: {benchmark}")
        start_time = time.time()
        
        try:
            cmd = [
                "python", "-m", "wisent_guard.cli", "tasks", benchmark,
                "--model", MODEL,
                "--layer", str(LAYER),
                "--limit", str(LIMIT),
                "--token-targeting-strategy", TOKEN_STRATEGY,
                "--split-ratio", "0.8",
                "--allow-small-dataset"
            ]
            
            logging.info(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
                # No timeout
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                output = result.stdout
                metrics = {}
                if "accuracy" in output.lower():
                    for line in output.split('\n'):
                        if 'accuracy' in line.lower():
                            try:
                                import re
                                match = re.search(r'accuracy[:\s]+([0-9.]+)', line, re.IGNORECASE)
                                if match:
                                    metrics['accuracy'] = float(match.group(1))
                            except:
                                pass
                
                results[benchmark] = {
                    "status": "success",
                    "duration": duration,
                    "metrics": metrics,
                    "output": output[-1000:] if len(output) > 1000 else output
                }
                print(f"  [PASS] {benchmark} completed in {duration:.2f}s")
                logging.info(f"SUCCESS: {benchmark} completed in {duration:.2f}s")
                successful += 1
            else:
                raise Exception(f"Command failed with return code {result.returncode}: {result.stderr}")
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            results[benchmark] = {
                "status": "failed",
                "error": error_msg,
                "duration": duration
            }
            print(f"  [FAIL] {benchmark} failed: {error_msg[:100]}")
            logging.error(f"FAILED: {benchmark} after {duration:.2f}s - Error: {error_msg}")
            failed += 1
    
    # Save results
    with open('remaining_benchmarks_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Remaining Benchmarks Testing Complete")
    print(f"Successful: {successful}/{len(benchmarks_to_test)}")
    print(f"Failed: {failed}")
    print(f"Results saved to: remaining_benchmarks_results.json")
    print(f"Logs saved to: remaining_benchmarks.log")

if __name__ == "__main__":
    test_remaining_benchmarks()