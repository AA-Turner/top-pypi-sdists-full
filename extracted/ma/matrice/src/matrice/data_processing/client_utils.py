"""Module providing client_utils functionality."""

import os
import json
import logging
import requests
import zipfile
import shutil
import random
import math

MAX_PARTITION_SIZE_BYTES = 2 * 1024 * 1024 * 1024
ANNOTATION_EXTENSIONS = [
    ".json",
    ".txt",
    ".xml",
    ".ndjson",
    ".yaml",
    ".csv",
    ".ini",
]
SAMPLES_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".ti",
    ".webp",
    ".mp4",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".mkv",
    ".webm",
]
COMPRESSED_EXTENSIONS = [
    ".zip",
    ".tar",
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
]
ANNOTATION_PARTITION_TYPE = "annotation"
SAMPLES_PARTITION_TYPE = "samples"


def get_size_mb(path):
    """Calculate total size in MB for a file, folder, or list of paths."""
    total_size = 0

    def get_file_size(file_path):
        if os.path.isfile(file_path) and not os.path.islink(file_path):
            return os.path.getsize(file_path)
        return 0

    def get_folder_size(folder_path):
        size = 0
        for dirpath, _, filenames in os.walk(folder_path):
            for filename in filenames:
                size += get_file_size(os.path.join(dirpath, filename))
        return size

    if isinstance(path, (list, tuple)):
        for p in path:
            total_size += get_file_size(p) if os.path.isfile(p) else get_folder_size(p)
    else:
        total_size += get_file_size(path) if os.path.isfile(path) else get_folder_size(path)
    return -(-total_size // (1024 * 1024))


def rename_mot_file(file_path: str) -> str:
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    parts = file_path.split(os.sep)
    split_folders = {"train", "test", "val"}
    split_index = -1
    video_folder = None
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in split_folders:
            split_index = i
            break
    if split_index != -1 and split_index + 1 < len(parts):
        video_folder = parts[split_index + 1]
    else:
        raise ValueError("Could not determine video folder from path")
    expected_suffix = f"_train_{video_folder}"
    if not name.endswith(expected_suffix):
        new_name = f"{name}{expected_suffix}{ext}"
    else:
        new_name = file_name
    new_path = os.path.join(dir_path, new_name)
    if new_path != file_path:
        os.rename(file_path, new_path)
    return new_path

def restructure_davis_dataset(base_path):
    """
    Restructure the DAVIS dataset to organize frames into segments and distribute them across train/test/val splits.
    All categories will be present in all splits, with segments of frames distributed across splits.
    
    Args:
        base_path (str): Path to the root of the DAVIS dataset
    """
    logging.info(f"Restructuring DAVIS dataset at {base_path}")
    
    # Define paths
    annotations_path = os.path.join(base_path, "Annotations")
    jpeg_images_path = os.path.join(base_path, "JPEGImages")
    imagesets_path = os.path.join(base_path, "ImageSets")
    
    # Get all categories from Annotations directory
    categories = []
    if os.path.exists(annotations_path):
        categories = [d for d in os.listdir(annotations_path) if os.path.isdir(os.path.join(annotations_path, d))]
    
    # Also check for categories in ImageSets
    for split_file in ["train.txt", "test.txt", "val.txt"]:
        file_path = os.path.join(imagesets_path, split_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                categories.extend([line.strip() for line in f.readlines() if line.strip()])
    
    # Remove duplicates
    categories = list(set(categories))
    logging.info(f"Found {len(categories)} categories: {categories}")
    
    # Create new structure
    new_structure = {
        "JPEGImages": {"train": {}, "test": {}, "val": {}},
        "Annotations": {"train": {}, "test": {}, "val": {}}
    }
    
    # Initialize all categories in all splits
    for split in ["train", "test", "val"]:
        for category in categories:
            new_structure["JPEGImages"][split][category] = []
            new_structure["Annotations"][split][category] = []
    
    # Process each category
    for category in categories:
        logging.info(f"Processing category: {category}")
        
        # Get list of frames for this category
        annotations_category_path = os.path.join(annotations_path, category)
        jpeg_category_path = os.path.join(jpeg_images_path, category)
        
        if not os.path.exists(annotations_category_path) or not os.path.exists(jpeg_category_path):
            logging.warning(f"Warning: Category {category} not found in both Annotations and JPEGImages. Creating empty directories.")
            continue
        
        # Get frames (assuming annotations and jpeg have the same frame numbers)
        annotation_frames = [f for f in os.listdir(annotations_category_path) if f.endswith('.png')]
        jpeg_frames = [f for f in os.listdir(jpeg_category_path) if (f.endswith('.jpg') or f.endswith('.jpeg'))]
        
        # Check if both annotation and jpeg frames exist
        annotation_frame_nums = set([os.path.splitext(f)[0] for f in annotation_frames])
        jpeg_frame_nums = set([os.path.splitext(f)[0] for f in jpeg_frames])
        common_frames = sorted(list(annotation_frame_nums.intersection(jpeg_frame_nums)))
        
        if not common_frames:
            logging.warning(f"Warning: No matching frames found for category {category}.")
            continue
        
        # Calculate segment size
        num_frames = len(common_frames)
        segment_size = 16
        if num_frames < segment_size:
            segment_size = max(1, num_frames // 10)
            logging.info(f"Adjusting segment size to {segment_size} for category {category} with {num_frames} frames")
        
        # Create segments
        segments = []
        for i in range(0, num_frames, segment_size):
            segment_frames = common_frames[i:i+segment_size]
            # Include all segments, complete or partial
            if len(segment_frames) > 0:
                segments.append(segment_frames)
        
        if not segments:
            logging.info(f"Warning: No segments could be created for category {category}. This is unexpected.")
            # This is a fallback but should never happen since we include all segments above
            segments = [common_frames[:min(segment_size, len(common_frames))]]
        
        logging.info(f"Created {len(segments)} segments for category {category}")
        
        # Shuffle segments for random distribution
        random.shuffle(segments)
        
        # Calculate split counts
        total_segments = len(segments)
        train_count = math.ceil(total_segments * 0.8)
        test_count = math.ceil(total_segments * 0.1)
        val_count = total_segments - train_count - test_count
        
        # Distribute segments into splits
        split_segments = {
            "train": segments[:train_count],
            "test": segments[train_count:train_count+test_count],
            "val": segments[train_count+test_count:]
        }
        
        # Handle edge cases where a split might be empty
        for split in ["train", "test", "val"]:
            if not split_segments[split] and segments:
                # Borrow a segment from train if possible
                if split == "test" and split_segments["train"]:
                    split_segments["test"] = [split_segments["train"].pop()]
                elif split == "val" and split_segments["train"]:
                    split_segments["val"] = [split_segments["train"].pop()]
        
        # Store segment information in new structure
        for split, split_segments_list in split_segments.items():
            for segment in split_segments_list:
                for frame in segment:
                    # Check if the frame exists with .jpg or .jpeg extension
                    if os.path.exists(os.path.join(jpeg_category_path, f"{frame}.jpg")):
                        new_structure["JPEGImages"][split][category].append(f"{frame}.jpg")
                    elif os.path.exists(os.path.join(jpeg_category_path, f"{frame}.jpeg")):
                        new_structure["JPEGImages"][split][category].append(f"{frame}.jpeg")
                    new_structure["Annotations"][split][category].append(f"{frame}.png")
    
    # Create temporary directory for the new structure
    import tempfile
    temp_dir = tempfile.mkdtemp()
    logging.info(f"Creating temporary structure in {temp_dir}")
    
    for data_type in ["JPEGImages", "Annotations"]:
        for split in ["train", "test", "val"]:
            for category in categories:
                # Create destination directory (even if empty)
                dest_dir = os.path.join(temp_dir, data_type, split, category)
                os.makedirs(dest_dir, exist_ok=True)
                
                # Copy files if they exist
                frames = new_structure[data_type][split].get(category, [])
                for frame in frames:
                    src_path = os.path.join(base_path, data_type, category, frame)
                    dest_path = os.path.join(dest_dir, frame)
                    if os.path.exists(src_path):
                        shutil.copy2(src_path, dest_path)
                    else:
                        logging.info(f"Warning: File not found: {src_path}")
    
    # Create new ImageSets directory with all categories in each split file
    new_imagesets_path = os.path.join(temp_dir, "ImageSets")
    os.makedirs(new_imagesets_path, exist_ok=True)
    
    for split in ["train", "test", "val"]:
        with open(os.path.join(new_imagesets_path, f"{split}.txt"), 'w') as f:
            f.write('\n'.join(categories))
    
    # Replace the original directory with the new structure
    # First, back up the original directory (optional)
    backup_dir = f"{base_path}_backup"
    logging.info(f"Backing up original dataset to {backup_dir}")
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    shutil.copytree(base_path, backup_dir)
    
    # Remove the original content
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    # Copy new structure to the original path
    for item in os.listdir(temp_dir):
        src_path = os.path.join(temp_dir, item)
        dest_path = os.path.join(base_path, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
            
    # Clean up temp directory
    shutil.rmtree(temp_dir)
    
    logging.info(f"Dataset restructured successfully. Original dataset at {base_path} has been replaced.")
    
    # logging.info statistics
    logging.info("\nRestructured Dataset Statistics:")
    for split in ["train", "test", "val"]:
        category_count = len(categories)
        total_frames = sum(len(frames) for frames in new_structure["JPEGImages"][split].values())
        logging.info(f"  {split.capitalize()}: {category_count} categories, {total_frames} frames")



def rename_davis_file(file_path: str) -> str:
    dir_path, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    if ext.lower() != ".png":
        return file_path
    file_path.split(os.sep)
    parent_folder = os.path.basename(os.path.dirname(file_path))
    new_name = f"{name}_{parent_folder}{ext}"
    new_path = os.path.join(dir_path, new_name)
    logging.debug("new path constructed: %s", new_path)
    if new_path != file_path:
        os.rename(file_path, new_path)
        logging.debug(
            "Renamed %s to %s",
            file_path,
            new_path,
        )
    return new_path


def scan_folder(folder_path):
    print(f"Scanning folder at {folder_path}")
    file_paths = []
    for root, _, files in os.walk(folder_path):
        if "SegmentationClass" in root or "SegmentationObject" in root:
            continue
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths


def scan_dataset(
    base_path,
    rename_annotation_files=False,
    input_type=None,
):
    logging.debug("Scanning dataset at %s", base_path)
    annotation_files = []
    image_files = []
    file_paths = scan_folder(base_path)
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path.lower())
        if input_type == "davis":
            if ".png" not in ANNOTATION_EXTENSIONS:
                ANNOTATION_EXTENSIONS.append(".png")
            if ".png" in SAMPLES_EXTENSIONS:
                SAMPLES_EXTENSIONS.remove(".png")
        if ext in ANNOTATION_EXTENSIONS:
            annotation_files.append(file_path)
        elif ext in SAMPLES_EXTENSIONS:
            image_files.append(file_path)
    logging.debug(
        "Found %s annotation files and %s image files",
        len(annotation_files),
        len(image_files),
    )
    return annotation_files, image_files


def get_mot_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".png")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        parent_folder = os.path.basename(os.path.dirname(file_path))
        video_id = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        if not parent_folder.startswith("img"):
            continue
        if video_id not in video_groups:
            video_groups[video_id] = []
        try:
            frame_num = int(os.path.splitext(file_name)[0])
        except ValueError:
            continue
        video_groups[video_id].append((file_path, frame_num, file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if total_video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    {video_id: [file_path for file_path, _, _ in frames]},
                    total_video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for video %s with %s frames",
                partition_num,
                video_id,
                len(frames),
            )
        else:
            if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
                if current_partition:
                    partitions.append(
                        create_partition(
                            current_partition,
                            current_size,
                            partition_num,
                        )
                    )
                    partition_num += 1
                    logging.debug(
                        "Created partition %s with %s videos",
                        partition_num,
                        len(current_partition),
                    )
                current_partition = {}
                current_size = 0
            current_partition[video_id] = [file_path for file_path, _, _ in frames]
            current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions, len(video_groups)


def get_davis_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".jpeg")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        video_folder = os.path.dirname(file_path)
        partition_folder = os.path.basename(os.path.dirname(video_folder))  # train / val / test
        video_name = os.path.basename(video_folder)
        video_id = f"{partition_folder}_{video_name}"  # e.g., train_video_1
        if video_id not in video_groups:
            video_groups[video_id] = []
        try:
            frame_num = int(os.path.splitext(file_name)[0])
        except ValueError:
            continue
        video_groups[video_id].append((file_path, frame_num, file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if total_video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    {video_id: [file_path for file_path, _, _ in frames]},
                    total_video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for video %s with %s frames",
                partition_num,
                video_id,
                len(frames),
            )
        else:
            if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
                if current_partition:
                    partitions.append(
                        create_partition(
                            current_partition,
                            current_size,
                            partition_num,
                        )
                    )
                    partition_num += 1
                    logging.debug(
                        "Created partition %s with %s videos",
                        partition_num,
                        len(current_partition),
                    )
                current_partition = {}
                current_size = 0
            current_partition[video_id] = [file_path for file_path, _, _ in frames]
            current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions, len(video_groups)


def get_video_imagenet_partitions(video_files):
    logging.debug("Creating video partitions")
    video_list = []
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        ):
            continue
        file_size = os.path.getsize(file_path)
        video_list.append((file_path, file_size))
    video_list.sort(key=lambda x: x[1], reverse=True)
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(videos, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(videos),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [video[0] for video in videos],
        }

    for video_path, video_size in video_list:
        if video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    [(video_path, video_size)],
                    video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for large video %s",
                partition_num,
                video_path,
            )
        else:
            if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = []
                current_size = 0
            current_partition.append((video_path, video_size))
            current_size += video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions, len(video_list)

def create_video_blank_dataset_items(partition_number, rpc, dataset_id, dataset_version, num_dataset_items, project_id):
    
    logging.info("Number of dataset items: %d", num_dataset_items)
    
    # STEP 1: Create blank dataset items
    blank_items_payload = {
        "datasetId": dataset_id,
        "itemsCount": num_dataset_items,
        "partitionNumber": partition_number,
        "version": dataset_version,
    }

    logging.info("Creating blank dataset items with payload: %s", blank_items_payload)

    response = rpc.post(
        f"/v2/dataset/add_blank_video_dataset_items?projectId={project_id}",
        payload=blank_items_payload,
    )

    if not response or not response.get("success"):
        logging.error("Failed to create blank dataset items or missing datasetItemIds.")

    dataset_item_ids = response["data"]
    logging.info("Received dataset item IDs: %s", dataset_item_ids)
    return dataset_item_ids

def get_kinetics_partitions(video_files):
    logging.debug("Creating video partitions")
    video_list = []
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        ):
            continue
        file_size = os.path.getsize(file_path)
        video_list.append((file_path, file_size))
    video_list.sort(key=lambda x: x[1], reverse=True)
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(videos, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(videos),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [video[0] for video in videos],
        }

    for video_path, video_size in video_list:
        if video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    [(video_path, video_size)],
                    video_size,
                    partition_num,
                )
            )
            partition_num += 1
            logging.debug(
                "Created partition %s for large video %s",
                partition_num,
                video_path,
            )
        else:
            if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = []
                current_size = 0
            current_partition.append((video_path, video_size))
            current_size += video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    return partitions, len(video_list)

def get_video_mscoco_partitions(video_files):
    logging.debug("Creating video partitions")

    video_groups = {}
    valid_splits = {"train", "val", "test"}

    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith(('.jpg', '.jpeg')):
            continue

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        # Extract split and video_id dynamically by walking backward
        split = None
        video_id = None
        path_parts = file_path.split(os.sep)

        for i in range(len(path_parts) - 1, -1, -1):
            part = path_parts[i].lower()
            if part in valid_splits and i + 1 < len(path_parts):
                split = part
                video_id = path_parts[i + 1]
                break

        if not split or not video_id:
            continue  # Skip if split or video_id not found

        unique_video_key = f"{split}/{video_id}"

        # Extract frame number
        try:
            frame_num = int(os.path.splitext(file_name)[0])
        except ValueError:
            continue

        if unique_video_key not in video_groups:
            video_groups[unique_video_key] = []

        video_groups[unique_video_key].append((file_path, frame_num, file_size))

    # Sort frames by frame number
    for frames in video_groups.values():
        frames.sort(key=lambda x: x[1])

    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": sum(len(v) for v in samples.values()),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)]
        }

    for video_key, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)

        if total_video_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(create_partition({video_key: [fp for fp, _, _ in frames]}, total_video_size, partition_num))
            logging.debug(f"Created partition {partition_num} for {video_key} with {len(frames)} frames")
            partition_num += 1
        else:
            if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
                partitions.append(create_partition(current_partition, current_size, partition_num))
                logging.debug(f"Created partition {partition_num} with {len(current_partition)} videos")
                partition_num += 1
                current_partition = {}
                current_size = 0

            current_partition[video_key] = [fp for fp, _, _ in frames]
            current_size += total_video_size

    if current_partition:
        partitions.append(create_partition(current_partition, current_size, partition_num))
        logging.debug(f"Created final partition {partition_num} with {len(current_partition)} videos")

    logging.debug(f"Created {len(partitions)} video partitions in total")
    return partitions, len(video_groups)

# def get_video_mscoco_partitions(video_files):
#     logging.debug("Creating video partitions")
#     video_list = []
#     for file_path in video_files:
#         if not os.path.exists(file_path) or not file_path.endswith(
#             (".mp4", ".avi", ".mov", ".mkv")
#         ):
#             continue
#         file_size = os.path.getsize(file_path)
#         video_list.append((file_path, file_size))
#     video_list.sort(key=lambda x: x[1], reverse=True)
#     partitions = []
#     current_partition = []
#     current_size = 0
#     partition_num = 1

#     def create_partition(videos, total_size, num):
#         return {
#             "partitionNum": num,
#             "sampleCount": len(videos),
#             "diskSizeMB": -(-total_size // (1024 * 1024)),
#             "type": SAMPLES_PARTITION_TYPE,
#             "files": [video[0] for video in videos],
#         }

#     for video_path, video_size in video_list:
#         if video_size > MAX_PARTITION_SIZE_BYTES:
#             partitions.append(
#                 create_partition(
#                     [(video_path, video_size)],
#                     video_size,
#                     partition_num,
#                 )
#             )
#             partition_num += 1
#             logging.debug(
#                 "Created partition %s for large video %s",
#                 partition_num,
#                 video_path,
#             )
#         else:
#             if current_size + video_size > MAX_PARTITION_SIZE_BYTES:
#                 partitions.append(
#                     create_partition(
#                         current_partition,
#                         current_size,
#                         partition_num,
#                     )
#                 )
#                 partition_num += 1
#                 logging.debug(
#                     "Created partition %s with %s videos",
#                     partition_num,
#                     len(current_partition),
#                 )
#                 current_partition = []
#                 current_size = 0
#             current_partition.append((video_path, video_size))
#             current_size += video_size
#     if current_partition:
#         partitions.append(
#             create_partition(
#                 current_partition,
#                 current_size,
#                 partition_num,
#             )
#         )
#     logging.debug(
#         "Created %s video partitions",
#         len(partitions),
#     )
#     return partitions

def extract_frames_from_videos(file_paths):
    import cv2
    # Step 1: Categorize input paths by split and type
    split_jsons = {'train': None, 'val': None, 'test': None}
    split_videos = {'train': [], 'val': [], 'test': []}

    for path in file_paths:
        if path.endswith('.json'):
            for split in split_jsons:
                if split in os.path.basename(path).lower():
                    split_jsons[split] = path
        elif path.endswith('.mp4'):
            for split in split_videos:
                if f"/{split}/" in path.replace("\\", "/"):
                    split_videos[split].append(path)

    # Step 2: Process each split
    for split in ['train', 'val', 'test']:
        json_path = split_jsons[split]
        if not json_path or not os.path.exists(json_path):
            print(f"Skipping {split}: no JSON found.")
            continue

        with open(json_path, 'r') as f:
            data = json.load(f)

        video_meta = {v['file_name']: v for v in data.get('videos', [])}

        for video_path in split_videos[split]:
            video_filename = os.path.basename(video_path)
            if video_filename not in video_meta:
                print(f"Warning: {video_filename} not found in {split} annotation JSON.")
                continue

            meta = video_meta[video_filename]
            video_id = meta['id']
            expected_frames = meta['frames']
            fps = meta['fps']

            output_dir = os.path.splitext(video_path)[0]  # same name as video file
            os.makedirs(output_dir, exist_ok=True)

            cap = cv2.VideoCapture(video_path)
            actual_fps = cap.get(cv2.CAP_PROP_FPS)
            if abs(actual_fps - fps) > 1:
                print(f"Note: FPS mismatch for {video_filename}: Annotation FPS = {fps}, Actual FPS = {actual_fps}")

            frame_idx = 0
            saved_frame_count = 0
            success = True
            while success:
                success, frame = cap.read()
                if not success:
                    break
                frame_path = os.path.join(output_dir, f"{frame_idx:06}.jpg")
                cv2.imwrite(frame_path, frame)
                frame_idx += 1

            cap.release()

            print(f"Extracted {frame_idx} frames for {video_filename} (expected: {expected_frames})")

            # Optional: Check frame count
            if abs(frame_idx - expected_frames) > 10:
                print(f"WARNING: Extracted frame count differs significantly from expected for {video_filename}")

            # Delete original video
            os.remove(video_path)


def get_youtube_bb_partitions(video_files):
    logging.debug("Creating video partitions")
    video_groups = {}
    for file_path in video_files:
        if not os.path.exists(file_path) or not file_path.endswith((".jpg", ".png")):
            continue
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        if "_" not in file_name:
            continue
        file_name = os.path.splitext(file_name)[0]
        video_id, frame_num = file_name.rsplit("_", 1)
        if not frame_num.isdigit():
            continue
        if video_id not in video_groups:
            video_groups[video_id] = []
        video_groups[video_id].append((file_path, int(frame_num), file_size))
    for video_id in video_groups:
        video_groups[video_id].sort(key=lambda x: x[1])
    partitions = []
    current_partition = {}
    current_size = 0
    partition_num = 1

    def create_partition(samples, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(samples),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": [samples[vid] for vid in sorted(samples)],
        }

    for video_id, frames in video_groups.items():
        total_video_size = sum(size for _, _, size in frames)
        if current_size + total_video_size > MAX_PARTITION_SIZE_BYTES:
            if current_partition:
                partitions.append(
                    create_partition(
                        current_partition,
                        current_size,
                        partition_num,
                    )
                )
                partition_num += 1
                logging.debug(
                    "Created partition %s with %s videos",
                    partition_num,
                    len(current_partition),
                )
                current_partition = {}
                current_size = 0
        current_partition[video_id] = [file_path for file_path, _, _ in frames]
        current_size += total_video_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s video partitions",
        len(partitions),
    )
    logging.debug(
        "Final Partitions from get_youtube_bb_partitions: %s",
        partitions,
    )
    return partitions, len(video_groups)


def get_youtube_bb_relative_path(abs_path):
    """
    Extract the relative path starting from the folder containing train/test/val directories.

    Args:
        abs_path (str): Absolute path to the file

    Returns:
        str: Relative path starting from the folder containing the parent directory of
            train/test/val
    """
    abs_path = os.path.normpath(abs_path)
    path_parts = abs_path.split(os.sep)
    try:
        split_index = next(
            i for i, part in enumerate(path_parts) if part in ["train", "test", "val"]
        )
        if split_index > 0:
            split_index -= 1
    except StopIteration:
        return None
    return os.path.join(*path_parts[split_index:])


def get_davis_relative_path(abs_path: str) -> str:
    """
    Extract the relative path starting from the grand-grandparent directory.

    Args:
        abs_path (str): Absolute path to the file

    Returns:
        str: Relative path starting from the grand-grandparent directory
    """
    abs_path = os.path.normpath(abs_path)
    path_parts = abs_path.split(os.sep)
    if len(path_parts) > 3:
        split_index = len(path_parts) - 4
    else:
        return None
    return os.path.join(*path_parts[split_index:])


def get_images_partitions(image_files):
    """Split image files into partitions and return partition stats."""
    logging.debug("Creating image partitions")
    partitions = []
    current_partition = []
    current_size = 0
    partition_num = 1

    def create_partition(files, total_size, num):
        return {
            "partitionNum": num,
            "sampleCount": len(files),
            "diskSizeMB": -(-total_size // (1024 * 1024)),
            "type": SAMPLES_PARTITION_TYPE,
            "files": files,
        }

    for image_file in image_files:
        file_size = os.path.getsize(image_file)
        if current_size + file_size > MAX_PARTITION_SIZE_BYTES:
            partitions.append(
                create_partition(
                    current_partition,
                    current_size,
                    partition_num,
                )
            )
            partition_num += 1
            current_partition = [image_file]
            current_size = file_size
        else:
            current_partition.append(image_file)
            current_size += file_size
    if current_partition:
        partitions.append(
            create_partition(
                current_partition,
                current_size,
                partition_num,
            )
        )
    logging.debug(
        "Created %s image partitions",
        len(partitions),
    )
    return partitions


def get_annotations_partition(annotation_files):
    logging.debug("Creating annotations partition")
    return {
        "partitionNum": 0,
        "sampleCount": len(annotation_files),
        "diskSizeMB": get_size_mb(annotation_files),
        "type": ANNOTATION_PARTITION_TYPE,
        "files": annotation_files,
    }

def get_video_mscoco_cloud_file_path(
    dataset_id,
    dataset_version,
    base_dataset_path,
    file_path,
    include_version_in_cloud_path=False,
):
    abs_file_path = os.path.abspath(file_path)
    abs_base_path = os.path.abspath(base_dataset_path)
    
    # Handle the case where file is within base path
    if abs_file_path.startswith(abs_base_path):
        # Split paths into components
        base_components = abs_base_path.split(os.sep)
        file_components = abs_file_path.split(os.sep)
        
        # Find the last occurrence of the last base component in the file path
        last_base_component = base_components[-1]
        
        # Find the index of the last occurrence of the last base component
        for i in range(len(file_components) - 1, -1, -1):
            if file_components[i] == last_base_component:
                # Take the path from this component onward
                rel_components = file_components[i:]
                rel_path = os.path.join(*rel_components)
                break
        else:
            # If no match found, fallback to basename
            rel_path = os.path.basename(abs_file_path)
    else:
        # If file is not within base path, just use the filename
        rel_path = os.path.basename(abs_file_path)
    
    # Construct the final path based on whether to include version
    if include_version_in_cloud_path:
        final_path = os.path.join(dataset_id, dataset_version, rel_path).replace(os.sep, "/")
    else:
        final_path = os.path.join(dataset_id, rel_path).replace(os.sep, "/")
    
    # logging.debug(
    #     "constructed cloud file path: %s",
    #     final_path,
    # )
    return final_path

def get_video_mot_cloud_file_path(
    dataset_id, 
    dataset_version,
    base_dataset_path,
    file_path,
    include_version_in_cloud_path=False,
):
    abs_file_path = os.path.abspath(file_path)
    abs_base_path = os.path.abspath(base_dataset_path)
    if abs_file_path.startswith(abs_base_path):
        rel_path = os.path.relpath(abs_file_path, abs_base_path)
    else:
        rel_path = os.path.basename(abs_file_path)
    if include_version_in_cloud_path:
        final_path = os.path.join(dataset_id, dataset_version, rel_path).replace(os.sep, "/")
        logging.debug(
            "constructed cloud file path: %s",
            final_path,
        )
        return final_path
    else:
        final_path = os.path.join(dataset_id, rel_path).replace(os.sep, "/")
        logging.debug(
            "constructed cloud file path: %s",
            final_path,
        )
        return final_path


def get_cloud_file_path(
    dataset_id,
    dataset_version,
    base_dataset_path,
    file_path,
    include_version_in_cloud_path=False,
):  
    # TODO: check if uncommenting this required for video datasets
    # abs_file_path = os.path.abspath(file_path)
    # abs_base_path = os.path.abspath(base_dataset_path)
    # if os.path.commonpath([abs_file_path]) == os.path.commonpath([abs_base_path, abs_file_path]):
    #     rel_path = os.path.relpath(abs_file_path, abs_base_path)
    # else:
    #     rel_path = os.path.basename(abs_file_path)
    
    rel_path = os.path.relpath(file_path, base_dataset_path)
    if include_version_in_cloud_path:
        return os.path.join(dataset_id, dataset_version, rel_path).replace(os.sep, "/")
    else:
        return os.path.join(dataset_id, rel_path).replace(os.sep, "/")

def get_batch_pre_signed_upload_urls(
    cloud_file_paths,
    rpc,
    type,
    bucket_alias="",
    account_number="",
    project_id="",
):
    logging.debug(
        "Getting presigned URLs for %s files",
        len(cloud_file_paths),
    )
    payload_get_presigned_url = {
        "fileNames": cloud_file_paths,
        "type": type,
        "isPrivateBucket": (True if bucket_alias else False),
        "bucketAlias": bucket_alias,
        "accountNumber": account_number,
    }
    resp = rpc.post(
        f"/v2/dataset/get_batch_pre_signed_upload_urls?projectId={project_id}",
        payload={
            "fileNames": cloud_file_paths,
            "type": type,
            "isPrivateBucket": (True if bucket_alias else False),
            "bucketAlias": bucket_alias,
            "accountNumber": account_number,
        },
    )
    logging.debug(
        "payload for getting the presigned urls: %s",
        payload_get_presigned_url,
    )
    if resp["success"]:
        return resp["data"]
    else:
        logging.error(
            "Failed to get presigned URLs: %s",
            resp["message"],
        )
        return resp["message"]


def upload_file(local_path, presigned_url, max_attempts=5):
    if not presigned_url:
        logging.error(
            "Missing presigned URL for %s",
            local_path,
        )
        return False
    for attempt in range(max_attempts):
        try:
            with open(local_path, "rb") as f:
                response = requests.put(
                    presigned_url,
                    data=f,
                    allow_redirects=True,
                    timeout=30,
                )
                if response.status_code == 200:
                    logging.debug(
                        "Successfully uploaded %s to %s",
                        local_path,
                        presigned_url,
                    )
                    return True
                else:
                    logging.warning(
                        "Failed to upload %s (status: %s), attempt %s/%s",
                        local_path,
                        response.status_code,
                        attempt + 1,
                        max_attempts,
                    )
                    response.raise_for_status()
        except Exception as e:
            if attempt == max_attempts - 1:
                logging.error(
                    "Failed to upload %s after %s attempts. Error: %s",
                    local_path,
                    max_attempts,
                    e,
                )
                return False
            else:
                logging.warning(
                    "Attempt %s/%s failed for %s. Retrying... Error: %s",
                    attempt + 1,
                    max_attempts,
                    local_path,
                    e,
                )


def update_annotation_bucket_url(
    rpc,
    dataset_id,
    partition_number,
    annotation_bucket_url,
):
    payload = {
        "partitionNumber": partition_number,
        "path": annotation_bucket_url,
    }
    logging.debug(
        "Updating annotation bucket URL for partition %s with URL: %s",
        partition_number,
        annotation_bucket_url,
    )
    url = f"/v2/dataset/update_annotation_path/{dataset_id}"
    response = rpc.post(url, payload=payload)
    return response


def upload_compressed_dataset(
    rpc,
    dataset_path,
    bucket_alias="",
    account_number="",
    project_id="",
):
    file_name = os.path.basename(dataset_path)
    presigned_urls = get_batch_pre_signed_upload_urls(
        [file_name],
        rpc,
        "compressed",
        bucket_alias,
        account_number,
        project_id=project_id,
    )
    upload_url = presigned_urls[file_name]
    upload_file(dataset_path, upload_url)
    return upload_url.split("?")[0]


def compress_annotation_files(file_paths, base_dataset_path):
    zip_file_path = os.path.join(base_dataset_path, "annotations.zip")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(
                file_path,
                arcname=os.path.relpath(file_path, base_dataset_path).replace(os.sep, "/"),
            )
    logging.info(
        "Files zipped successfully into %s",
        zip_file_path,
    )
    return zip_file_path


def is_file_compressed(file_path):
    _, ext = os.path.splitext(file_path.lower())
    return ext in COMPRESSED_EXTENSIONS


def update_partitions_numbers(
    rpc,
    dataset_id,
    items,
    partition_key="partitionNum",
):
    try:
        logging.info(
            "Updating partition numbers for dataset %s",
            dataset_id,
        )
        dataset_info = rpc.get(f"/v2/dataset/{dataset_id}").get("data")
        if dataset_info:
            dataset_partition_stats = dataset_info.get("partitionStats")
            if dataset_partition_stats:
                max_partition_num = max([p["partitionNum"] for p in dataset_partition_stats])
                for item in items:
                    item[partition_key] = max_partition_num + item[partition_key]
    except Exception as e:
        logging.error(
            "Error updating partition numbers: %s",
            e,
        )
    return items


def complete_dataset_items_upload(
    rpc,
    dataset_id,
    partition_stats,
    target_version="v1.0",
    source_version="",
    action_type="data_import",
):
    logging.debug(
        "partition_stats for complete_dataset_items_upload: %s",
        partition_stats,
    )
    logging.info(
        "Completing dataset items upload for dataset %s",
        dataset_id,
    )
    url = "/v2/dataset/complete_dataset_items_upload"
    payload = {
        "action": action_type,
        "_id": dataset_id,
        "sourceVersion": source_version,
        "targetVersion": target_version,
        "totalSample": sum(
            [p["sampleCount"] for p in partition_stats if p["type"] == SAMPLES_PARTITION_TYPE]
        ),
        "partitionInfo": [
            {
                "partitionNum": p["partitionNum"],
                "sampleCount": p["sampleCount"],
                "diskSizeMB": p["diskSizeMB"],
                "type": p["type"],
            }
            for p in (
                [partition_stats[0]] + partition_stats[1]
                if isinstance(partition_stats, tuple)
                else (partition_stats if isinstance(partition_stats, list) else [partition_stats])
            )
            if p["type"] == SAMPLES_PARTITION_TYPE
        ],
    }
    logging.info("Payload: %s", payload)
    response = rpc.post(url, payload=payload)
    logging.info("Response: %s", response)
    return response


def create_partition_stats(
    rpc,
    partition_stats,
    dataset_id,
    target_version,
    source_version="",
):
    logging.info(
        "Creating partition stats for dataset %s",
        dataset_id,
    )
    new_partition_stats = [stat for stat in partition_stats if stat is not None]
    payload = {
        "datasetId": dataset_id,
        "sourceVersion": source_version,
        "targetVersion": target_version,
        "partitionStats": new_partition_stats,
    }
    url = "/v2/dataset/create-partition"
    logging.debug(
        "Making request to %s with payload: %s",
        url,
        payload,
    )
    response = rpc.post(url, payload=payload)
    logging.debug(
        "response after calling create-partition API: %s",
        response,
    )
    return response
