"""Module providing metrics_calculator_oop functionality."""

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


class ObjectDetectionMetrics:

    def __init__(
        self,
        split,
        outputs,
        targets,
        index_to_labels,
    ):
        self.split = split
        self.outputs = outputs
        self.targets = targets
        self.index_to_labels = index_to_labels
        self.num_classes = len(index_to_labels)
        self.precision, self.recall, self.f1 = self._calculate_detection_metrics()
        self.mAP, self.mAP_50, self.mAP_75 = self._calculate_mAP_metrics()

    def get_results(self):
        """Get formatted evaluation results"""
        results = []
        overall_metrics = {
            "precision": self.precision.mean(),
            "recall": self.recall.mean(),
            "f1_score": self.f1.mean(),
            "mAP": self.mAP.mean(),
            "mAP_50": self.mAP_50.mean(),
            "mAP_75": self.mAP_75.mean(),
        }
        for (
            name,
            value,
        ) in overall_metrics.items():
            results.append(
                {
                    "category": "all",
                    "splitType": self.split,
                    "metricName": name,
                    "metricValue": float(value.item()),
                }
            )
        for i in range(len(self.precision)):
            class_metrics = {
                "precision": self.precision[i],
                "recall": self.recall[i],
                "f1_score": self.f1[i],
                "mAP": self.mAP[i],
                "mAP_50": self.mAP_50[i],
                "mAP_75": self.mAP_75[i],
            }
            for (
                name,
                value,
            ) in class_metrics.items():
                results.append(
                    {
                        "category": self.index_to_labels[str(i)],
                        "splitType": self.split,
                        "metricName": name,
                        "metricValue": float(value.item()),
                    }
                )
        return results

    def _calculate_detection_metrics(self):
        """Calculate precision, recall and F1 scores"""
        true_pos = torch.zeros(self.num_classes)
        false_pos = torch.zeros(self.num_classes)
        false_neg = torch.zeros(self.num_classes)
        for output, target in zip(self.outputs, self.targets):
            for label in range(1, self.num_classes):
                pred_boxes = output["boxes"][output["labels"] == label]
                target_boxes = target["boxes"][target["labels"] == label]
                if len(target_boxes) > 0:
                    if len(pred_boxes) == 0:
                        false_neg[label] += len(target_boxes)
                    else:
                        iou = torchvision.ops.box_iou(
                            pred_boxes,
                            target_boxes,
                        )
                        matched = (iou.max(dim=0)[0] >= 0.5).sum().item()
                        false_neg[label] += len(target_boxes) - matched
        precision = true_pos / (true_pos + false_pos + 1e-06)
        recall = true_pos / (true_pos + false_neg + 1e-06)
        f1 = 2 * precision * recall / (precision + recall + 1e-06)
        return precision, recall, f1

    def _calculate_mAP_metrics(self):
        """Calculate mAP metrics at different IoU thresholds"""
        mAP = torch.zeros(self.num_classes)
        mAP_50 = torch.zeros(self.num_classes)
        mAP_75 = torch.zeros(self.num_classes)
        iou_thresholds = torch.linspace(0.5, 0.95, 10)
        for label in range(1, self.num_classes):
            predictions = []
            targets = []
            for output, target in zip(self.outputs, self.targets):
                pred_boxes = output["boxes"][output["labels"] == label]
                pred_scores = output["scores"][output["labels"] == label]
                target_boxes = target["boxes"][target["labels"] == label]
                predictions.append((pred_boxes, pred_scores))
                targets.append(target_boxes)
            ap_sum = sum(
                self._calculate_ap(predictions, targets, iou_t) for iou_t in iou_thresholds
            )
            mAP[label] = ap_sum / len(iou_thresholds)
            mAP_50[label] = self._calculate_ap(predictions, targets, 0.5)
            mAP_75[label] = self._calculate_ap(predictions, targets, 0.75)
        return mAP, mAP_50, mAP_75

    def _calculate_ap(self, predictions, targets, iou_threshold):
        """Calculate Average Precision for single class at specific IoU threshold"""
        total_tp = total_fp = 0
        total_gt = sum(len(t) for t in targets)
        if total_gt == 0:
            return 0.0
        all_preds = [
            (box, score)
            for pred_boxes, pred_scores in predictions
            for box, score in zip(pred_boxes, pred_scores)
        ]
        all_preds.sort(key=lambda x: x[1], reverse=True)
        matched = {i: [] for i in range(len(targets))}
        precisions = []
        recalls = []
        for pred_box, _ in all_preds:
            max_iou = iou_threshold
            best_match = None
            best_target_idx = None
            for (
                target_idx,
                target_boxes,
            ) in enumerate(targets):
                if len(target_boxes) == 0:
                    continue
                unmatched = [i for i in range(len(target_boxes)) if i not in matched[target_idx]]
                if not unmatched:
                    continue
                target_boxes_unmatched = target_boxes[unmatched]
                ious = torchvision.ops.box_iou(
                    pred_box.unsqueeze(0),
                    target_boxes_unmatched,
                )
                max_iou_target, max_idx = ious.max(dim=1)
                if max_iou_target > max_iou:
                    max_iou = max_iou_target
                    best_match = unmatched[max_idx]
                    best_target_idx = target_idx
            if best_match is not None:
                matched[best_target_idx].append(best_match)
                total_tp += 1
            else:
                total_fp += 1
            precisions.append(total_tp / (total_tp + total_fp))
            recalls.append(total_tp / total_gt)
        if not precisions:
            return 0.0
        precisions = torch.tensor(precisions)
        recalls = torch.tensor(recalls)
        for i in range(len(precisions) - 1, 0, -1):
            precisions[i - 1] = max(precisions[i - 1], precisions[i])
        ap = 0
        for i in range(len(precisions)):
            if i == 0:
                ap += precisions[i] * recalls[i]
            else:
                ap += precisions[i] * (recalls[i] - recalls[i - 1])
        return ap


class ClassificationMetrics:

    def __init__(
        self,
        split_type,
        outputs,
        targets,
        index_to_labels,
    ):
        self.split_type = split_type
        self.outputs = outputs
        self.targets = targets
        self.index_to_labels = index_to_labels
        self.num_classes = len(index_to_labels)
        self.predictions = torch.argmax(outputs, dim=1)

    def get_results(self):
        """Get formatted evaluation results"""
        results = []
        acc1, acc5 = self._calculate_accuracy()
        macro_metrics = self._calculate_macro_metrics()
        micro_metrics = self._calculate_micro_metrics()
        weighted_metrics = self._calculate_weighted_metrics()
        overall_metrics = {
            "acc@1": acc1,
            "acc@5": acc5,
            "MCC": self._calculate_mcc(),
            "AUC-ROC": self._calculate_auc_roc(),
            "AUC-PR": self._calculate_auc_pr(),
            "Cohen's Kappa": self._calculate_cohen_kappa(),
            "log_loss": self._calculate_log_loss(),
            "specificity": self._calculate_specificity(),
            **macro_metrics,
            **micro_metrics,
            **weighted_metrics,
        }
        for (
            name,
            value,
        ) in overall_metrics.items():
            results.append(
                {
                    "category": "all",
                    "splitType": self.split_type,
                    "metricName": name,
                    "metricValue": float(value),
                }
            )
        per_class_metrics = {
            "precision": self._calculate_precision_per_class,
            "recall": self._calculate_recall_per_class,
            "f1_score": self._calculate_f1_per_class,
            "specificity": self._calculate_specificity_per_class,
            "accuracy": self._calculate_accuracy_per_class,
        }
        for (
            metric_name,
            metric_func,
        ) in per_class_metrics.items():
            for (
                class_idx,
                value,
            ) in metric_func().items():
                results.append(
                    {
                        "category": self.index_to_labels[str(class_idx)],
                        "splitType": self.split_type,
                        "metricName": metric_name,
                        "metricValue": float(value),
                    }
                )
        return results

    def _calculate_accuracy(self):
        """Calculate top-1 and top-5 accuracy"""
        acc1 = accuracy(self.outputs, self.targets, topk=(1,))[0]
        acc5 = (
            accuracy(
                self.outputs,
                self.targets,
                topk=(5,),
            )[0]
            if self.num_classes >= 5
            else torch.tensor([1])
        )
        return acc1.item(), acc5.item()

    def _calculate_macro_metrics(self):
        """Calculate macro-averaged metrics"""
        return {
            "macro_precision": precision_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="macro",
            ),
            "macro_recall": recall_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="macro",
            ),
            "macro_f1": f1_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="macro",
            ),
        }

    def _calculate_micro_metrics(self):
        """Calculate micro-averaged metrics"""
        return {
            "micro_precision": precision_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="micro",
            ),
            "micro_recall": recall_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="micro",
            ),
            "micro_f1": f1_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="micro",
            ),
        }

    def _calculate_weighted_metrics(self):
        """Calculate weighted-averaged metrics"""
        return {
            "weighted_precision": precision_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="weighted",
            ),
            "weighted_recall": recall_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="weighted",
            ),
            "weighted_f1": f1_score(
                self.predictions.cpu(),
                self.targets.cpu(),
                average="weighted",
            ),
        }

    def _calculate_mcc(self):
        return matthews_corrcoef(
            self.targets.cpu(),
            self.predictions.cpu(),
        )

    def _calculate_auc_roc(self):
        targets_bin = label_binarize(
            self.targets.cpu(),
            classes=range(self.num_classes),
        )
        probs = torch.nn.functional.softmax(self.outputs, dim=1).cpu().numpy()
        return roc_auc_score(
            targets_bin,
            probs,
            average="macro",
            multi_class="ovr",
        )

    def _calculate_auc_pr(self):
        targets_bin = label_binarize(
            self.targets.cpu(),
            classes=range(self.num_classes),
        )
        probs = torch.nn.functional.softmax(self.outputs, dim=1).cpu().numpy()
        return average_precision_score(targets_bin, probs, average="macro")

    def _calculate_cohen_kappa(self):
        return cohen_kappa_score(
            self.targets.cpu(),
            self.predictions.cpu(),
        )

    def _calculate_log_loss(self):
        probs = torch.nn.functional.softmax(self.outputs, dim=1).cpu().numpy()
        return log_loss(self.targets.cpu(), probs)

    def _calculate_specificity(self):
        tp, tn, fp, fn = calculate_metrics(self.outputs, self.targets)
        return float(tn.sum() / (tn.sum() + fp.sum() + 1e-10))

    def _calculate_precision_per_class(self):
        tp, _, fp, _ = calculate_metrics(self.outputs, self.targets)
        return {i: (tp[i] / (tp[i] + fp[i] + 1e-10)) for i in range(self.num_classes)}

    def _calculate_recall_per_class(self):
        tp, _, _, fn = calculate_metrics(self.outputs, self.targets)
        return {i: (tp[i] / (tp[i] + fn[i] + 1e-10)) for i in range(self.num_classes)}

    def _calculate_f1_per_class(self):
        prec = self._calculate_precision_per_class()
        rec = self._calculate_recall_per_class()
        return {
            i: (2 * prec[i] * rec[i] / (prec[i] + rec[i] + 1e-10)) for i in range(self.num_classes)
        }

    def _calculate_specificity_per_class(self):
        _, tn, fp, _ = calculate_metrics(self.outputs, self.targets)
        return {i: (tn[i] / (tn[i] + fp[i] + 1e-10)) for i in range(self.num_classes)}

    def _calculate_accuracy_per_class(self):
        tp, tn, fp, fn = calculate_metrics(self.outputs, self.targets)
        return {
            i: ((tp[i] + tn[i]) / (tp[i] + tn[i] + fp[i] + fn[i] + 1e-10))
            for i in range(self.num_classes)
        }


def get_object_detection_evaluation_results(split, outputs, targets, index_to_labels):
    metrics = ObjectDetectionMetrics(split, outputs, targets, index_to_labels)
    return metrics.get_results()


def get_classification_evaluation_results(split_type, outputs, targets, index_to_labels):
    metrics = ClassificationMetrics(
        split_type,
        outputs,
        targets,
        index_to_labels,
    )
    return metrics.get_results()


def calculate_metrics(output, target):
    """Calculate TP, TN, FP, FN for multi-class classification"""
    _, pred = output.max(1)
    pred = pred.cpu()
    tp = torch.zeros(output.size(1))
    tn = torch.zeros(output.size(1))
    fp = torch.zeros(output.size(1))
    fn = torch.zeros(output.size(1))
    for i in range(len(target)):
        pred_class = pred[i]
        true_class = target[i]
        for class_label in range(output.size(1)):
            if pred_class == class_label and true_class == class_label:
                tp[class_label] += 1
            elif pred_class == class_label and true_class != class_label:
                fp[class_label] += 1
            elif pred_class != class_label and true_class == class_label:
                fn[class_label] += 1
            else:
                tn[class_label] += 1
    return tp, tn, fp, fn


def accuracy(output, target, topk=(1,)):
    """Compute accuracy for top k predictions"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)
        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))
        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(1.0 / batch_size))
        return res
