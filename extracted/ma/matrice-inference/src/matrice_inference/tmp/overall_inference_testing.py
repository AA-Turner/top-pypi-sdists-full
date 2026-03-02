import asyncio
import os
import numpy as np
import logging
import time
from datetime import datetime
import subprocess
import psutil
from triton_model_manager import TritonModelManager
import GPUtil
import pytz

logger = logging.getLogger(__name__)

COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
    "toothbrush"
]

async def triton_async_benchmark(image_dir, num_requests=100, output_report="master_benchmark_report_v1.md"):
    logger.info("Starting Triton Async Inference Master Benchmark at %s IST", datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
    MODEL_NAME = "yolov8n"
    MODEL_DIR = r"./models"
    # NOTE: Place your model files (yolov8n.onnx, yolov8n.plan) in the MODEL_DIR 
    # wget https://github.com/Vedant-MatriceAI/Temporary_Model_Repository/raw/main/yolov8n.onnx
    # wget https://github.com/Vedant-MatriceAI/Temporary_Model_Repository/raw/main/yolov8n.plan

    INTERNAL_HOST = "localhost"
    INPUT_SIZE = 640
    NUM_CLASSES = 80
    NUM_MODEL_INSTANCES = 1
    MAX_BATCH_SIZE = 2  
    IS_YOLO = True

    configurations = [
        {
            "model_path": os.path.join(MODEL_DIR, "yolov8n.plan"),
            "runtime_framework": "tensorrt",
            "server_type": server_type,
            "port": 8000 if server_type == "rest" else 8001,
            "dynamic_batching": dynamic_batching,
            "use_trt_accelerator": use_trt
        }
        for server_type in ["rest", "grpc"]
        for dynamic_batching in [True, False]
        for use_trt in [True, False]
    ] + [
        {
            "model_path": os.path.join(MODEL_DIR, "yolov8n.onnx"),
            "runtime_framework": "onnx",
            "server_type": server_type,
            "port": 8000 if server_type == "rest" else 8001,
            "dynamic_batching": dynamic_batching,
            "use_trt_accelerator": False
        }
        for server_type in ["rest", "grpc"]
        for dynamic_batching in [True, False]
    ]

    logger.info(f"Total configurations to test: {len(configurations)}")

    all_metrics = []

    system_info = {
        "triton_version": "2.37.0",
        "docker_image": "nvcr.io/nvidia/tritonserver:23.08-py3",
        "cuda_version": "12.1",
        "nvidia_driver_version": "535.216.03",
        "gpu_info": "NVIDIA L4 (ID: 0, Memory: 23034.0 MB)",
        "cpu_info": f"{psutil.cpu_count(logical=True)} logical cores, {psutil.cpu_count(logical=False)} physical cores",
        "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "os": f"{subprocess.getoutput('cat /etc/os-release').split('PRETTY_NAME=')[1].splitlines()[0].strip()}"
    }
    try:
        system_info["cuda_version"] = subprocess.getoutput("nvcc --version | grep release").split("release ")[1].split(",")[0]
    except:
        logger.warning("Could not retrieve CUDA version, using fallback")
    try:
        system_info["nvidia_driver_version"] = subprocess.getoutput("nvidia-smi | grep Driver").split("Driver Version: ")[1].split()[0]
    except:
        logger.warning("Could not retrieve NVIDIA driver version, using fallback")
    try:
        gpus = GPUtil.getGPUs()
        system_info["gpu_info"] = ", ".join([f"{gpu.name} (ID: {gpu.id}, Memory: {gpu.memoryTotal} MB)" for gpu in gpus])
    except:
        logger.warning("Could not retrieve GPU info, using fallback")

    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            temp = gpus[0].temperature
            mem_used = gpus[0].memoryUsed
            mem_total = gpus[0].memoryTotal
            logger.info(f"Initial GPU status: Temperature={temp}°C, Memory={mem_used}/{mem_total} MB")
            if temp > 55 or mem_used > 0.1 * mem_total:
                logger.info("Initial GPU temperature or memory usage high, waiting for stabilization...")
                for _ in range(60):  
                    await asyncio.sleep(1)
                    gpus = GPUtil.getGPUs()
                    temp = gpus[0].temperature if gpus else 0
                    mem_used = gpus[0].memoryUsed if gpus else 0
                    if temp <= 55 and mem_used <= 0.1 * mem_total:
                        logger.info(f"GPU stabilized at {temp}°C, memory {mem_used}/{mem_total} MB")
                        break
                else:
                    logger.error(f"GPU still at {temp}°C, memory {mem_used}/{mem_total} MB after waiting. Aborting benchmark to prevent shutdown.")
                    raise RuntimeError("Initial GPU conditions unsafe for benchmarking")
    except Exception as e:
        logger.warning(f"Could not check initial GPU status: {str(e)}. Proceeding with caution.")

    image_files = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if len(image_files) < num_requests:
        logger.warning(f"Requested {num_requests} images, but only {len(image_files)} found. Using available images.")
        num_requests = len(image_files)
    image_files = image_files[:num_requests]

    if not image_files:
        raise FileNotFoundError(f"No images found in {image_dir}")

    image_bytes_list = []
    for img_path in image_files:
        with open(img_path, "rb") as f:
            image_bytes_list.append(f.read())

    for idx, config in enumerate(configurations):
        logger.info(f"Running benchmark for configuration {idx + 1}/{len(configurations)}: {config}")
        metrics = {
            "latencies": [],
            "total_time": 0,
            "num_requests": num_requests,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_objects_detected": 0,
            "failure_reason": ""
        }

        # GPU cool-down before each run
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                temp = gpus[0].temperature
                mem_used = gpus[0].memoryUsed
                mem_total = gpus[0].memoryTotal
                logger.info(f"GPU status before run: Temperature={temp}°C, Memory={mem_used}/{mem_total} MB")
                if temp > 55 or mem_used > 0.1 * mem_total:
                    logger.info("GPU temperature or memory usage high, waiting for cool-down...")
                    for _ in range(30):  
                        await asyncio.sleep(1)
                        gpus = GPUtil.getGPUs()
                        temp = gpus[0].temperature if gpus else 0
                        mem_used = gpus[0].memoryUsed if gpus else 0
                        if temp <= 55 and mem_used <= 0.1 * mem_total:
                            logger.info(f"GPU cooled to {temp}°C, memory freed to {mem_used}/{mem_total} MB")
                            break
                    else:
                        logger.warning(f"GPU still at {temp}°C, memory {mem_used}/{mem_total} MB after waiting, proceeding with run")

        except Exception as e:
            logger.warning(f"Could not check GPU status: {str(e)}")

        try:
            if not os.path.exists(config["model_path"]):
                error_msg = f"Model file not found: {config['model_path']}"
                logger.error(error_msg)
                metrics["failed_requests"] = num_requests
                metrics["failure_reason"] = error_msg
                all_metrics.append((config, metrics))
                continue

            manager = TritonModelManager(
                model_name=MODEL_NAME,
                model_path=config["model_path"],
                runtime_framework=config["runtime_framework"],
                internal_server_type=config["server_type"],
                internal_port=config["port"],
                internal_host=INTERNAL_HOST,
                input_size=INPUT_SIZE,
                num_classes=NUM_CLASSES,
                num_model_instances=NUM_MODEL_INSTANCES,
                use_dynamic_batching=config["dynamic_batching"],
                max_batch_size=MAX_BATCH_SIZE,
                is_yolo=IS_YOLO,
                use_trt_accelerator=config["use_trt_accelerator"]
            )

            async def run_inference(image_bytes, img_idx):
                start_time = time.time()
                try:
                    result, success = await manager.async_inference(image_bytes)
                    if not success or result is None or result.get("predictions") is None:
                        raise RuntimeError(f"Inference failed for image {img_idx}")

                    # Extract predictions
                    predictions = result["predictions"]
                    boxes = np.array(predictions["boxes"])
                    scores = np.array(predictions["scores"])
                    class_ids = np.array(predictions["class_ids"])

                    # Log results for first few images
                    if img_idx < 3:
                        logger.info(f"======= Results for image {img_idx}: {os.path.basename(image_files[img_idx])} =======")
                        logger.info(f"Detected {boxes.shape[0]} objects")
                        for i in range(min(boxes.shape[0], 3)):
                            try:
                                box = boxes[i]
                                score = scores[i]
                                class_id = int(class_ids[i])
                                class_name = COCO_CLASSES[class_id] if 0 <= class_id < len(COCO_CLASSES) else "unknown"
                                logger.info(f"Object {i+1}: {class_name} (Score: {score:.4f}, Box: {box})")
                            except Exception as e:
                                logger.warning(f"Failed to log object {i+1} for image {img_idx}: {e}")
                        logger.info("=============================================")

                    metrics["successful_requests"] += 1
                    metrics["total_objects_detected"] += boxes.shape[0]
                    metrics["latencies"].append(time.time() - start_time)
                except Exception as e:
                    logger.error(f"Inference failed for image {img_idx}: {str(e)}")
                    metrics["failed_requests"] += 1

            start_total_time = time.time()
            tasks = [run_inference(image_bytes, idx) for idx, image_bytes in enumerate(image_bytes_list)]
            await asyncio.gather(*tasks, return_exceptions=True)
            metrics["total_time"] = time.time() - start_total_time

            # Calculate metrics
            metrics["throughput"] = metrics["successful_requests"] / metrics["total_time"] if metrics["total_time"] > 0 else 0
            metrics["avg_fps"] = metrics["successful_requests"] / metrics["total_time"] if metrics["total_time"] > 0 else 0
            metrics["avg_latency_ms"] = (sum(metrics["latencies"]) / len(metrics["latencies"]) * 1000) if metrics["latencies"] else 0
            metrics["min_latency_ms"] = min(metrics["latencies"]) * 1000 if metrics["latencies"] else 0
            metrics["max_latency_ms"] = max(metrics["latencies"]) * 1000 if metrics["latencies"] else 0
            metrics["p95_latency_ms"] = np.percentile(metrics["latencies"], 95) * 1000 if metrics["latencies"] else 0

        except Exception as e:
            error_msg = f"Benchmark error: {str(e)}"
            logger.error(error_msg)
            metrics["failed_requests"] = num_requests
            metrics["failure_reason"] = error_msg
        finally:
            try:
                manager.triton_server_process.terminate()
                manager.triton_server_process.wait(timeout=300)
                logger.info("Triton server terminated")
            except Exception as e:
                logger.warning(f"Cleanup failed: {str(e)}")
            all_metrics.append((config, metrics))

    report_content = f"""# Triton Inference Server Master Benchmark Report
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Generated on {datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')} IST*

## System Configuration
- **Operating System**: {system_info["os"]}
- **Triton Server Version**: {system_info["triton_version"]}
- **Docker Image**: {system_info["docker_image"]}
- **CUDA Version**: {system_info["cuda_version"]}
- **NVIDIA Driver Version**: {system_info["nvidia_driver_version"]}
- **GPU Configuration**: {system_info["gpu_info"]}
- **CPU Configuration**: {system_info["cpu_info"]}
- **System Memory**: {system_info["memory_total"]}

## Benchmark Summary
| Config ID | Model Format | Server Protocol | Dynamic Batching | TensorRT Accelerator | Total Images | Failed Requests | Objects Detected | Total Time (s) | Throughput (img/s) | Avg FPS | Avg Latency (ms) | Min Latency (ms) | Max Latency (ms) | P95 Latency (ms) |
|-----------|--------------|-----------------|------------------|---------------------|--------------|-----------------|------------------|----------------|--------------------|---------|------------------|------------------|------------------|------------------|
"""
    for idx, (config, metrics) in enumerate(all_metrics):
        report_content += f"| {idx + 1} | {config['runtime_framework']} | {config['server_type']} | {config['dynamic_batching']} | {config['use_trt_accelerator']} | {metrics['successful_requests']} | {metrics['failed_requests']} | {metrics['total_objects_detected']} | {metrics['total_time']:.2f} | {metrics['throughput']:.2f} | {metrics['avg_fps']:.2f} | {metrics['avg_latency_ms']:.2f} | {metrics['min_latency_ms']:.2f} | {metrics['max_latency_ms']:.2f} | {metrics['p95_latency_ms']:.2f} |\n"

    report_content += """
## Detailed Results
"""
    for idx, (config, metrics) in enumerate(all_metrics):
        report_content += f"""
### Configuration {idx + 1}: {config['runtime_framework'].upper()} ({config['server_type'].upper()}, Dynamic Batching: {config['dynamic_batching']}, TensorRT: {config['use_trt_accelerator']})
- **Model Name**: {MODEL_NAME}
- **Model Path**: {config['model_path']}
- **Runtime Framework**: {config['runtime_framework']}
- **Server Protocol**: {config['server_type']}
- **Port**: {config['port']}
- **Input Size**: {INPUT_SIZE}x{INPUT_SIZE}
- **Number of Classes**: {NUM_CLASSES}
- **Number of Model Instances**: {NUM_MODEL_INSTANCES}
- **Dynamic Batching**: {config['dynamic_batching']}
- **Max Batch Size**: {MAX_BATCH_SIZE}
- **YOLO Model**: {IS_YOLO}
- **TensorRT Accelerator**: {config['use_trt_accelerator']}

#### Benchmark Results
"""
        if metrics["failure_reason"]:
            report_content += f"- **Status**: Failed\n- **Failure Reason**: {metrics['failure_reason']}\n"
        else:
            report_content += f"""- **Total Images Processed**: {metrics['successful_requests']}
- **Failed Requests**: {metrics['failed_requests']}
- **Total Objects Detected**: {metrics['total_objects_detected']}
- **Total Time**: {metrics['total_time']:.2f} seconds
- **Throughput**: {metrics['throughput']:.2f} images/second
- **Average FPS**: {metrics['avg_fps']:.2f} frames/second
- **Average Latency**: {metrics['avg_latency_ms']:.2f} ms
- **Min Latency**: {metrics['min_latency_ms']:.2f} ms
- **Max Latency**: {metrics['max_latency_ms']:.2f} ms
- **P95 Latency**: {metrics['p95_latency_ms']:.2f} ms
"""

    with open(output_report, "w") as f:
        f.write(report_content)
    logger.info(f"Master benchmark report saved to {output_report}")

if __name__ == "__main__":
    image_dir = r"./coco/val2017"
    # NOTE: Exec the below commands beforehand to prepare dataset

    # mkdir -p coco && cd coco
    # wget http://images.cocodataset.org/zips/val2017.zip
    # unzip val2017.zip
    
    num_requests = 100
    output_report = "master_benchmark_report_v1.md"
    asyncio.run(triton_async_benchmark(image_dir, num_requests, output_report))
    logger.info("Benchmarking completed for %d requests.", num_requests)