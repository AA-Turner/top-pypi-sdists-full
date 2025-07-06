"""Module providing metrics_calculator functionality."""

import torch
import torchvision
from sklearn.preprocessing import label_binarize
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
    roc_auc_score,
    average_precision_score,
    cohen_kappa_score,
    log_loss,
)


def get_object_detection_evaluation_results(
    split,
    all_outputs,
    all_targets,
    index_to_labels,
):
    """
    Calculate and format object detection evaluation metrics.

    Args:
        split: Dataset split type (e.g., 'train', 'val', 'test')
        all_outputs: Model predictions
        all_targets: Ground truth annotations
        index_to_labels: Mapping from class indices to label names

    Returns:
        List of dictionaries containing formatted metrics
    """
    results = []
    (
        precision_class,
        recall_class,
        f1_score_class,
    ) = calculate_detection_metrics(
        all_outputs,
        all_targets,
        len(index_to_labels),
    )
    (
        mAP_50_class,
        mAP_75_class,
        mAP_90_class,
        mAP_50_95_class,
    ) = calculate_mAP_metrics(
        all_outputs,
        all_targets,
        len(index_to_labels),
    )
    (
        mAR_50_class,
        mAR_75_class,
        mAR_90_class,
        mAR_50_95_class,
    ) = calculate_mAR_metrics(
        all_outputs,
        all_targets,
        len(index_to_labels),
    )
    results.extend(
        [
            {
                "category": "all",
                "splitType": split,
                "metricName": "precision",
                "metricValue": float(precision_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "recall",
                "metricValue": float(recall_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "f1_score",
                "metricValue": float(f1_score_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAP@50",
                "metricValue": float(mAP_50_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAP@75",
                "metricValue": float(mAP_75_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAP@50-95",
                "metricValue": float(mAP_50_95_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAP@90",
                "metricValue": float(mAP_90_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAR@50",
                "metricValue": float(mAR_50_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAR@75",
                "metricValue": float(mAR_75_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAR@50-95",
                "metricValue": float(mAR_50_95_class.mean().item()),
            },
            {
                "category": "all",
                "splitType": split,
                "metricName": "mAR@90",
                "metricValue": float(mAR_90_class.mean().item()),
            },
        ]
    )
    metrics_per_class = {
        "precision": precision_class,
        "recall": recall_class,
        "f1_score": f1_score_class,
        "AP@50": mAP_50_class,
        "AP@75": mAP_75_class,
        "AP@90": mAP_90_class,
        "AP@50-95": mAP_50_95_class,
        "AR@50": mAR_50_class,
        "AR@75": mAR_75_class,
        "AR@90": mAR_90_class,
        "AR@50-95": mAR_50_95_class,
    }
    for i in range(len(index_to_labels)):
        for (
            metric_name,
            metric_value,
        ) in metrics_per_class.items():
            if metric_value[i].isnan().item():
                metric_value[i] = torch.tensor(0.0)
            results.append(
                {
                    "category": index_to_labels[str(i)],
                    "splitType": split,
                    "metricName": metric_name,
                    "metricValue": float(metric_value[i].item()),
                }
            )
    return results


def calculate_mAP_metrics(outputs, targets, num_classes):
    mAP = torch.zeros(num_classes)
    mAP_50 = torch.zeros(num_classes)
    mAP_75 = torch.zeros(num_classes)
    mAP_50_95 = torch.zeros(num_classes)
    mAP_90 = torch.zeros(num_classes)
    iou_thresholds_50_95 = torch.linspace(0.5, 0.95, 10)
    iou_threshold_standard = 0.5
    for label in range(num_classes):
        all_predictions, all_targets = collect_predictions_and_targets(outputs, targets, label)
        mAP[label] = calculate_ap(
            all_predictions,
            all_targets,
            iou_threshold_standard,
        )
        mAP_50[label] = calculate_ap(all_predictions, all_targets, 0.5)
        mAP_75[label] = calculate_ap(all_predictions, all_targets, 0.75)
        mAP_90[label] = calculate_ap(all_predictions, all_targets, 0.9)
        ap_sum_50_95 = sum(
            calculate_ap(
                all_predictions,
                all_targets,
                iou_threshold,
            )
            for iou_threshold in iou_thresholds_50_95
        )
        mAP_50_95[label] = ap_sum_50_95 / len(iou_thresholds_50_95)
    return mAP_50, mAP_75, mAP_90, mAP_50_95


def collect_predictions_and_targets(outputs, targets, label):
    all_predictions = []
    all_targets = []
    for output, target in zip(outputs, targets):
        pred_boxes = output["boxes"][output["labels"] == label]
        pred_scores = output["scores"][output["labels"] == label]
        target_boxes = target["boxes"][target["labels"] == label]
        all_predictions.append((pred_boxes, pred_scores))
        all_targets.append(target_boxes)
    return all_predictions, all_targets


def calculate_ap(predictions, targets, iou_threshold):
    """
    Calculate Average Precision for a single class at a specific IoU threshold
    """
    total_gt = sum(len(t) for t in targets)
    if total_gt == 0:
        return torch.tensor(0.0)
    all_predictions = [
        (box, score)
        for pred_boxes, pred_scores in predictions
        for box, score in zip(pred_boxes, pred_scores)
    ]
    if not all_predictions:
        return torch.tensor(0.0)
    all_predictions.sort(key=lambda x: x[1], reverse=True)
    matched_targets = {i: [] for i in range(len(targets))}
    precisions, recalls = calculate_precision_recall(
        all_predictions,
        targets,
        matched_targets,
        iou_threshold,
        0,
        0,
        total_gt,
    )
    if not precisions:
        return torch.tensor(0.0)
    precisions = torch.tensor(precisions)
    recalls = torch.tensor(recalls)
    for i in range(len(precisions) - 1, 0, -1):
        precisions[i - 1] = max(precisions[i - 1], precisions[i])
    ap = 0.0
    for i in range(len(precisions)):
        if i == 0:
            ap += precisions[i] * recalls[i]
        else:
            ap += precisions[i] * (recalls[i] - recalls[i - 1])
    return torch.tensor(ap)


def calculate_precision_recall(
    all_predictions,
    targets,
    matched_targets,
    iou_threshold,
    total_tp,
    total_fp,
    total_gt,
):
    precisions = []
    recalls = []
    for pred_box, _ in all_predictions:
        max_iou, best_match, best_target_idx = find_best_match(
            pred_box,
            targets,
            matched_targets,
            iou_threshold,
        )
        if best_match is not None:
            matched_targets[best_target_idx].append(best_match)
            total_tp += 1
        else:
            total_fp += 1
        precision = total_tp / (total_tp + total_fp)
        recall = total_tp / total_gt if total_gt > 0 else 0
        precisions.append(precision)
        recalls.append(recall)
    return precisions, recalls


def calculate_mAR_metrics(outputs, targets, num_classes):
    """
    Calculate average recall metrics for object detection.
    """
    torch.zeros(num_classes)
    mAR_50 = torch.zeros(num_classes)
    mAR_75 = torch.zeros(num_classes)
    mAR_50_95 = torch.zeros(num_classes)
    mAR_90 = torch.zeros(num_classes)
    iou_thresholds_50_95 = torch.linspace(0.5, 0.95, 10)
    for label in range(num_classes):
        all_predictions, all_targets = collect_predictions_and_targets(outputs, targets, label)
        mAR_50[label] = calculate_recall_at_iou(all_predictions, all_targets, 0.5)
        mAR_75[label] = calculate_recall_at_iou(all_predictions, all_targets, 0.75)
        mAR_90[label] = calculate_recall_at_iou(all_predictions, all_targets, 0.9)
        mAR_50_95[label] = sum(
            calculate_recall_at_iou(
                all_predictions,
                all_targets,
                iou_threshold,
            )
            for iou_threshold in iou_thresholds_50_95
        ) / len(iou_thresholds_50_95)
    return mAR_50, mAR_75, mAR_90, mAR_50_95


def calculate_recall_at_iou(predictions, targets, iou_threshold):
    """Calculate recall at a specific IoU threshold for a single class."""
    total_gt = sum(len(t) for t in targets)
    if total_gt == 0:
        return torch.tensor(0.0)
    total_tp = 0
    matched_targets = {i: [] for i in range(len(targets))}
    for pred_boxes, pred_scores in predictions:
        for pred_box, _ in zip(pred_boxes, pred_scores):
            (
                max_iou,
                best_match,
                best_target_idx,
            ) = find_best_match(
                pred_box,
                targets,
                matched_targets,
                iou_threshold,
            )
            if best_match is not None:
                matched_targets[best_target_idx].append(best_match)
                total_tp += 1
    recall = total_tp / total_gt
    return torch.tensor(recall)


def find_best_match(
    pred_box,
    targets,
    matched_targets,
    iou_threshold,
):
    max_iou = iou_threshold
    best_match = None
    best_target_idx = None
    for target_idx, target_boxes in enumerate(targets):
        if len(target_boxes) == 0:
            continue
        unmatched_indices = [
            i for i in range(len(target_boxes)) if i not in matched_targets[target_idx]
        ]
        if not unmatched_indices:
            continue
        target_boxes_unmatched = target_boxes[unmatched_indices]
        ious = torchvision.ops.box_iou(
            pred_box.unsqueeze(0),
            target_boxes_unmatched,
        )
        max_iou_for_target, max_idx = ious.max(dim=1)
        if max_iou_for_target > max_iou:
            max_iou = max_iou_for_target
            best_match = unmatched_indices[max_idx]
            best_target_idx = target_idx
    return max_iou, best_match, best_target_idx


def calculate_detection_metrics(outputs, targets, num_classes):
    all_true_positives = torch.zeros(num_classes)
    all_false_positives = torch.zeros(num_classes)
    all_false_negatives = torch.zeros(num_classes)
    iou_threshold = 0.5
    for output, target in zip(outputs, targets):
        for label in range(num_classes):
            pred_boxes = output["boxes"][output["labels"] == label]
            output["scores"][output["labels"] == label]
            target_boxes = target["boxes"][target["labels"] == label]
            if len(target_boxes) == 0:
                if len(pred_boxes) > 0:
                    all_false_positives[label] += len(pred_boxes)
                continue
            if len(pred_boxes) == 0:
                all_false_negatives[label] += len(target_boxes)
                continue
            ious = torchvision.ops.box_iou(pred_boxes, target_boxes)
            matched_pred_indices = set()
            for target_idx in range(len(target_boxes)):
                max_iou, pred_idx = ious[:, target_idx].max(dim=0)
                if max_iou >= iou_threshold and pred_idx.item() not in matched_pred_indices:
                    all_true_positives[label] += 1
                    matched_pred_indices.add(pred_idx.item())
                else:
                    all_false_negatives[label] += 1
            all_false_positives[label] += len(pred_boxes) - len(matched_pred_indices)
    precision_class = all_true_positives / (all_true_positives + all_false_positives + 1e-10)
    recall_class = all_true_positives / (all_true_positives + all_false_negatives + 1e-10)
    f1_score_class = (
        2 * (precision_class * recall_class) / (precision_class + recall_class + 1e-10)
    )
    return (
        precision_class,
        recall_class,
        f1_score_class,
    )


def get_classification_evaluation_results(split_type, outputs, targets, index_to_labels):
    predictions = torch.argmax(outputs, dim=1)
    results = []
    acc1 = accuracy(outputs, targets, topk=(1,))[0]
    acc5 = (
        accuracy(outputs, targets, topk=(5,))[0]
        if len(index_to_labels) >= 5
        else torch.tensor([1])
    )
    predictions_cpu = predictions.cpu()
    targets_cpu = targets.cpu()
    macro_metrics = {
        "precision": precision_score(
            targets_cpu,
            predictions_cpu,
            average="macro",
            zero_division=0,
        ),
        "recall": recall_score(
            targets_cpu,
            predictions_cpu,
            average="macro",
            zero_division=0,
        ),
        "f1_score": f1_score(
            targets_cpu,
            predictions_cpu,
            average="macro",
            zero_division=0,
        ),
    }
    micro_metrics = {
        "precision": precision_score(
            targets_cpu,
            predictions_cpu,
            average="micro",
            zero_division=0,
        ),
        "recall": recall_score(
            targets_cpu,
            predictions_cpu,
            average="micro",
            zero_division=0,
        ),
        "f1_score": f1_score(
            targets_cpu,
            predictions_cpu,
            average="micro",
            zero_division=0,
        ),
    }
    weighted_metrics = {
        "precision": precision_score(
            targets_cpu,
            predictions_cpu,
            average="weighted",
            zero_division=0,
        ),
        "recall": recall_score(
            targets_cpu,
            predictions_cpu,
            average="weighted",
            zero_division=0,
        ),
        "f1_score": f1_score(
            targets_cpu,
            predictions_cpu,
            average="weighted",
            zero_division=0,
        ),
    }
    additional_metrics = {
        "acc@1": acc1.item(),
        "acc@5": acc5.item(),
        "MCC": calculate_mcc(predictions, targets),
        "AUC-ROC": calculate_auc_roc(outputs, targets, len(index_to_labels)),
        "AUC-PR": calculate_auc_pr(outputs, targets, len(index_to_labels)),
        "Cohen's Kappa": calculate_cohen_kappa(predictions, targets),
        "log_loss": calculate_log_loss(outputs, targets),
        "specificity": specificity_all(outputs, targets),
        "micro_precision": micro_metrics["precision"],
        "micro_recall": micro_metrics["recall"],
        "micro_f1_score": micro_metrics["f1_score"],
        "macro_precision": macro_metrics["precision"],
        "macro_recall": macro_metrics["recall"],
        "macro_f1_score": macro_metrics["f1_score"],
        "weighted_precision": weighted_metrics["precision"],
        "weighted_recall": weighted_metrics["recall"],
        "weighted_f1_score": weighted_metrics["f1_score"],
    }
    for (
        metric_name,
        value,
    ) in additional_metrics.items():
        results.append(
            {
                "category": "all",
                "splitType": split_type,
                "metricName": metric_name,
                "metricValue": float(value),
            }
        )
    metrics_per_class = {
        "precision": precision,
        "f1_score": f1_score_per_class,
        "recall": recall,
        "specificity": specificity,
        "acc@1": accuracy_per_class,
    }
    for (
        metric_name,
        metric_func,
    ) in metrics_per_class.items():
        class_metrics = metric_func(outputs, targets)
        for (
            class_idx,
            value,
        ) in class_metrics.items():
            results.append(
                {
                    "category": index_to_labels[str(class_idx)],
                    "splitType": split_type,
                    "metricName": metric_name,
                    "metricValue": float(value),
                }
            )
    return results


def calculate_metrics(output, target):
    """
    Calculate true positives, true negatives, false positives, and false negatives for a
        multi-class classification.
    """
    _, pred = output.max(1)
    pred = pred.cpu()
    target = target.cpu()
    num_classes = output.size(1)
    true_positives = torch.zeros(num_classes)
    true_negatives = torch.zeros(num_classes)
    false_positives = torch.zeros(num_classes)
    false_negatives = torch.zeros(num_classes)
    for class_idx in range(num_classes):
        true_positives[class_idx] = ((pred == class_idx) & (target == class_idx)).sum().item()
        true_negatives[class_idx] = ((pred != class_idx) & (target != class_idx)).sum().item()
        false_positives[class_idx] = ((pred == class_idx) & (target != class_idx)).sum().item()
        false_negatives[class_idx] = ((pred != class_idx) & (target == class_idx)).sum().item()
    return (
        true_positives,
        true_negatives,
        false_positives,
        false_negatives,
    )


def accuracy_per_class(output, target):
    tp, tn, fp, fn = calculate_metrics(output, target)
    accuracy_per_class = {}
    for class_idx in range(output.size(1)):
        total = tp[class_idx] + tn[class_idx] + fp[class_idx] + fn[class_idx]
        accuracy = (tp[class_idx] + tn[class_idx]) / total if total > 0 else 0.0
        accuracy_per_class[class_idx] = accuracy
    return accuracy_per_class


def specificity_all(output, target):
    _, tn, fp, _ = calculate_metrics(output, target)
    total_tn = tn.sum().item()
    total_fp = fp.sum().item()
    return total_tn / (total_tn + total_fp + 1e-10)


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = min(max(topk), output.size(1))
        batch_size = target.size(0)
        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))
        res = []
        for k in topk:
            k = min(k, maxk)
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def precision(output, target):
    tp, _, fp, _ = calculate_metrics(output, target)
    precision_per_class = {}
    for class_idx in range(output.size(1)):
        denominator = tp[class_idx] + fp[class_idx]
        precision_per_class[class_idx] = tp[class_idx] / denominator if denominator > 0 else 0.0
    return precision_per_class


def recall(output, target):
    tp, _, _, fn = calculate_metrics(output, target)
    recall_per_class = {}
    for class_idx in range(output.size(1)):
        denominator = tp[class_idx] + fn[class_idx]
        recall_per_class[class_idx] = tp[class_idx] / denominator if denominator > 0 else 0.0
    return recall_per_class


def f1_score_per_class(output, target):
    precision_scores = precision(output, target)
    recall_scores = recall(output, target)
    f1_scores = {}
    for class_idx in range(output.size(1)):
        p = precision_scores[class_idx]
        r = recall_scores[class_idx]
        denominator = p + r
        f1_scores[class_idx] = 2 * (p * r) / denominator if denominator > 0 else 0.0
    return f1_scores


def specificity(output, target):
    _, tn, fp, _ = calculate_metrics(output, target)
    specificity_per_class = {}
    for class_idx in range(output.size(1)):
        denominator = tn[class_idx] + fp[class_idx]
        specificity_per_class[class_idx] = tn[class_idx] / denominator if denominator > 0 else 0.0
    return specificity_per_class


def confusion_matrix_per_class(output, target):
    tp, tn, fp, fn = calculate_metrics(output, target)
    confusion_matrix = {}
    for class_idx in range(output.size(1)):
        confusion_matrix[class_idx] = [
            [
                int(tp[class_idx]),
                int(fp[class_idx]),
            ],
            [
                int(fn[class_idx]),
                int(tn[class_idx]),
            ],
        ]
    return confusion_matrix


def confusion_matrix(output, target):
    num_classes = output.size(1)
    confusion_matrix_overall = torch.zeros(
        (num_classes, num_classes),
        dtype=torch.int64,
    )
    _, predicted_classes = output.max(1)
    for i in range(target.size(0)):
        predicted_class = predicted_classes[i]
        true_class = target[i]
        confusion_matrix_overall[true_class][predicted_class] += 1
    return confusion_matrix_overall


def calculate_mcc(predictions, targets):
    try:
        return matthews_corrcoef(
            targets.cpu().numpy(),
            predictions.cpu().numpy(),
        )
    except Exception as e:
        print(e)
        return 0.0


def calculate_auc_roc(outputs, targets, num_classes):
    try:
        targets_one_hot = label_binarize(
            targets.cpu().numpy(),
            classes=range(num_classes),
        )
        probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()
        if num_classes == 2:
            return roc_auc_score(
                targets_one_hot,
                probabilities[:, 1],
            )
        else:
            return roc_auc_score(
                targets_one_hot,
                probabilities,
                average="macro",
                multi_class="ovr",
            )
    except Exception as e:
        print(e)
        return 0.0


def calculate_auc_pr(outputs, targets, num_classes):
    try:
        targets_one_hot = label_binarize(
            targets.cpu().numpy(),
            classes=range(num_classes),
        )
        probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()
        return average_precision_score(
            targets_one_hot,
            probabilities,
            average="macro",
        )
    except Exception as e:
        print(e)
        return 0.0


def calculate_cohen_kappa(predictions, targets):
    try:
        return cohen_kappa_score(
            targets.cpu().numpy(),
            predictions.cpu().numpy(),
        )
    except Exception as e:
        print(e)
        return 0.0


def calculate_log_loss(outputs, targets):
    try:
        probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()
        return log_loss(
            targets.cpu().numpy(),
            probabilities,
            labels=range(outputs.size(1)),
        )
    except Exception as e:
        print(e)
        return 0.0
