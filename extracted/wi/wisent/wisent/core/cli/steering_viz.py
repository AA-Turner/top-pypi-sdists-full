"""CLI command for steering effect visualization."""

import os
os.environ["NUMBA_NUM_THREADS"] = "1"

import sys
import json
import base64
from pathlib import Path


def execute_steering_viz(args):
    """Execute the steering-viz command."""
    import torch
    import random
    import numpy as np
    from wisent.core.geometry.repscan_with_concepts import (
        load_activations_from_database, load_pair_texts_from_database,
    )
    from wisent.core.geometry.steering_visualizations import create_steering_effect_figure
    from wisent.core.wisent import Wisent
    from wisent.core.classifiers.classifiers.models.logistic import LogisticClassifier
    from wisent.core.classifiers.classifiers.models.mlp import MLPClassifier
    from wisent.core.classifiers.classifiers.core.atoms import ClassifierTrainConfig
    from wisent.core.cli.steering_viz_helpers import (
        select_steering_direction, create_steering_method, extract_response,
        load_all_layer_activations, create_all_layer_steering, parse_layer_config,
        collect_behavioral_labels,
    )

    print(f"\n{'='*60}\nSTEERING EFFECT VISUALIZATION\n{'='*60}")

    # Load pairs and split 80/20
    print(f"\nLoading all pairs for train/test split...")
    all_pair_texts = load_pair_texts_from_database(task_name=args.task, limit=1000, database_url=args.database_url)
    all_pair_ids = list(all_pair_texts.keys())
    random.seed(42)
    random.shuffle(all_pair_ids)
    split_idx = int(len(all_pair_ids) * 0.8)
    train_ids, test_ids = set(all_pair_ids[:split_idx]), all_pair_ids[split_idx:]
    print(f"  Total: {len(all_pair_ids)}, Train: {len(train_ids)}, Test: {len(test_ids)}")

    # Load model first to get num_layers
    print(f"\nLoading model: {args.model}")
    wisent = Wisent.for_text(args.model)
    adapter = wisent.adapter
    num_layers = adapter.num_layers
    direction_method = getattr(args, 'direction_method', 'mean_diff')
    steering_method_name = getattr(args, 'steering_method', 'linear')
    multi_layer = getattr(args, 'multi_layer', False)

    # Parse layers argument if provided
    specified_layers = None
    if getattr(args, 'layers', None):
        specified_layers = [int(x.strip()) for x in args.layers.split(',')]

    autotune = getattr(args, 'autotune', False)
    val_split = getattr(args, 'val_split', 0.5)

    if multi_layer:
        from wisent.core.cli.steering_behavioral import collect_behavioral_labels_all_layers
        from wisent.core.evaluators.rotator import EvaluatorRotator
        EvaluatorRotator.discover_evaluators("wisent.core.evaluators.oracles")
        EvaluatorRotator.discover_evaluators("wisent.core.evaluators.benchmark_specific")

        # Load activations for all layers
        print(f"\nLoading activations for ALL {num_layers} layers...")
        pos_by_layer, neg_by_layer = load_all_layer_activations(
            model_name=args.model, task_name=args.task, num_layers=num_layers, train_ids=train_ids,
            prompt_format=args.prompt_format, extraction_strategy=args.extraction_strategy,
            limit=args.limit, database_url=args.database_url, layers=specified_layers
        )
        print(f"  Loaded {len(pos_by_layer)} layers")

        # Collect behavioral labels
        eval_tmp = EvaluatorRotator(evaluator=None, task_name=args.task).current
        pair_texts_tmp = {pid: all_pair_texts[pid] for pid in train_ids}
        available_layers = sorted(pos_by_layer.keys())
        print(f"\nPhase 1: Collecting behavioral labels ({len(train_ids)} prompts, {len(available_layers)} layers)...")
        behavioral_acts_by_layer, behavioral_labels = collect_behavioral_labels_all_layers(
            adapter, list(train_ids), pair_texts_tmp, eval_tmp, available_layers, max_new_tokens=50
        )
        print(f"  Behavioral labels: {sum(behavioral_labels)}/{len(behavioral_labels)} truthful")

        if autotune:
            from wisent.core.cli.steering_autotuner import run_autotune_multilayer
            _, steering_vectors_dict, methods_dict, scales_dict, test_ids = run_autotune_multilayer(
                adapter, train_ids, test_ids, all_pair_texts, pos_by_layer, neg_by_layer,
                behavioral_acts_by_layer, behavioral_labels, val_split, getattr(args, 'max_new_tokens', 100)
            )
        else:
            layer_strengths = parse_layer_config(getattr(args, 'layer_strengths', None))
            layer_methods = parse_layer_config(getattr(args, 'layer_methods', None))
            steering_vectors_dict, methods_dict, scales_dict = create_all_layer_steering(
                pos_by_layer, neg_by_layer, steering_method_name, args.strength, direction_method,
                layer_strengths=layer_strengths, layer_methods=layer_methods,
                behavioral_acts_by_layer=behavioral_acts_by_layer, behavioral_labels=behavioral_labels
            )
        print(f"  Created steering for {len(steering_vectors_dict)} layers")
        ref_layer = available_layers[len(available_layers)//2]
        pos_ref = torch.from_numpy(pos_by_layer[ref_layer]).float()
        neg_ref = torch.from_numpy(neg_by_layer[ref_layer]).float()
        layer_name = f"layer.{ref_layer}"
    else:
        # Single layer steering
        layer_name = f"layer.{args.layer}"
        print(f"\nLoading reference activations (layer={args.layer})...")
        pos_ref, neg_ref = load_activations_from_database(
            model_name=args.model, task_name=args.task, layer=args.layer,
            prompt_format=args.prompt_format, extraction_strategy=args.extraction_strategy,
            limit=args.limit, database_url=args.database_url, pair_ids=train_ids
        )
        print(f"  Loaded {len(pos_ref)} training reference pairs")

        # For behavioral direction, collect labels from actual model outputs first
        behavioral_acts, behavioral_labels = None, None
        if direction_method == "behavioral":
            from wisent.core.evaluators.rotator import EvaluatorRotator
            EvaluatorRotator.discover_evaluators("wisent.core.evaluators.oracles")
            EvaluatorRotator.discover_evaluators("wisent.core.evaluators.benchmark_specific")
            eval_tmp = EvaluatorRotator(evaluator=None, task_name=args.task).current
            pair_texts_tmp = {pid: all_pair_texts[pid] for pid in train_ids}
            print(f"\nPhase 1: Collecting behavioral labels from {len(train_ids)} training prompts...")
            behavioral_acts, behavioral_labels = collect_behavioral_labels(
                adapter, list(train_ids), pair_texts_tmp, eval_tmp, layer_name, max_new_tokens=50
            )
            print(f"  Behavioral labels: {sum(behavioral_labels)}/{len(behavioral_labels)} truthful")

        steering_vector, direction_desc, direction_acc = select_steering_direction(
            pos_ref, neg_ref, direction_method,
            behavioral_activations=behavioral_acts, behavioral_labels=behavioral_labels
        )
        print(f"Direction: {direction_desc} (norm={steering_vector.norm().item():.4f}, acc={direction_acc:.2f})")
        pos_ref_np, neg_ref_np = pos_ref.cpu().numpy(), neg_ref.cpu().numpy()
        steering_method = create_steering_method(steering_method_name, args.strength, pos_ref_np, neg_ref_np)
        print(f"Steering method: {steering_method.name if steering_method else 'default linear'}")
        steering_vectors_dict = {layer_name: steering_vector}
        methods_dict = {layer_name: steering_method} if steering_method else None
        scales_dict = {layer_name: args.strength}

    # Prepare test set
    pair_texts = {pid: all_pair_texts[pid] for pid in test_ids}
    test_prompts = [pair_texts[pid].get("prompt", "") for pid in test_ids]

    # Extract base activations for visualization (using reference layer)
    print(f"\nExtracting base activations for visualization (layer {layer_name})...")
    base_acts, steered_acts = [], []
    ref_vec = steering_vectors_dict.get(layer_name)
    for i, prompt in enumerate(test_prompts):
        if i % 10 == 0:
            print(f"  Processing {i+1}/{len(test_prompts)}...")
        base_layer_acts = adapter.extract_activations(prompt, layers=[layer_name])
        base_act = base_layer_acts.get(layer_name)
        if base_act is not None:
            base_acts.append(base_act[0, -1, :])
            steered_act = base_act[0, -1, :] + ref_vec.to(base_act.device) if ref_vec is not None else base_act[0, -1, :]
            steered_acts.append(steered_act.cpu())
    if not base_acts:
        print("ERROR: No activations extracted")
        sys.exit(1)
    base_activations = torch.stack(base_acts)
    steered_activations = torch.stack(steered_acts)
    print(f"  Extracted {len(base_activations)} base/steered pairs")

    # Evaluate responses
    print(f"\nEvaluating responses...")
    from wisent.core.evaluators.rotator import EvaluatorRotator
    from wisent.core.activations.core.atoms import LayerActivations
    from wisent.core.adapters.base import SteeringConfig

    EvaluatorRotator.discover_evaluators("wisent.core.evaluators.oracles")
    EvaluatorRotator.discover_evaluators("wisent.core.evaluators.benchmark_specific")
    evaluator = EvaluatorRotator(evaluator=None, task_name=args.task).current
    print(f"  Using evaluator: {evaluator.name}")

    # Create config with steering method(s) and per-layer scales
    steering_vectors = LayerActivations(steering_vectors_dict)
    config = SteeringConfig(scale=scales_dict, method=methods_dict)
    max_new_tokens = getattr(args, 'max_new_tokens', 100)
    if multi_layer:
        print(f"  Multi-layer steering active on {len(steering_vectors_dict)} layers")

    base_evaluations, steered_evaluations, all_responses = [], [], []
    for i, pair_key in enumerate(test_ids):
        pair_data = pair_texts[pair_key]
        prompt, pos_ref_text, neg_ref_text = pair_data.get("prompt", ""), pair_data.get("positive", ""), pair_data.get("negative", "")
        correct_answers = [pos_ref_text] if pos_ref_text else []
        incorrect_answers = [neg_ref_text] if neg_ref_text else []

        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = adapter.apply_chat_template(messages, add_generation_prompt=True)

        # Generate and extract responses
        base_response = extract_response(adapter._generate_unsteered(formatted_prompt, max_new_tokens=max_new_tokens, temperature=0.1, do_sample=True))
        steered_response = extract_response(adapter.forward_with_steering(formatted_prompt, steering_vectors=steering_vectors, config=config))

        # Evaluate
        base_result = evaluator.evaluate(base_response, pos_ref_text, correct_answers=correct_answers, incorrect_answers=incorrect_answers)
        steered_result = evaluator.evaluate(steered_response, pos_ref_text, correct_answers=correct_answers, incorrect_answers=incorrect_answers)

        base_evaluations.append(base_result.ground_truth)
        steered_evaluations.append(steered_result.ground_truth)
        all_responses.append({"pair_id": pair_key, "prompt": prompt, "positive_reference": pos_ref_text,
            "negative_reference": neg_ref_text, "base_response": base_response, "base_eval": base_result.ground_truth,
            "steered_response": steered_response, "steered_eval": steered_result.ground_truth})

        if i % 10 == 0:
            print(f"  Evaluated {i+1}/{len(test_ids)}...")

    base_truthful = sum(1 for e in base_evaluations if e == "TRUTHFUL")
    steered_truthful = sum(1 for e in steered_evaluations if e == "TRUTHFUL")
    print(f"\nText Evaluation: Base={base_truthful}/{len(base_evaluations)}, Steered={steered_truthful}/{len(steered_evaluations)}")

    # Train activation space classifier
    classifier_type = getattr(args, 'space_classifier', 'mlp')
    print(f"\nTraining activation space classifier ({classifier_type})...")
    X_train = torch.cat([pos_ref, neg_ref], dim=0).cpu().numpy()
    y_train = np.concatenate([np.ones(len(pos_ref)), np.zeros(len(neg_ref))])
    space_classifier = MLPClassifier(device="cpu", hidden_dim=256) if classifier_type == "mlp" else LogisticClassifier(device="cpu")
    train_report = space_classifier.fit(X_train, y_train, config=ClassifierTrainConfig(test_size=0.2, num_epochs=100, batch_size=32))
    print(f"  Accuracy: {train_report.final.accuracy:.3f}, AUC: {train_report.final.auc:.3f}")

    # Classify activations
    base_space_probs = space_classifier.predict_proba(base_activations.cpu().numpy())
    steered_space_probs = space_classifier.predict_proba(steered_activations.cpu().numpy())
    base_space_probs = base_space_probs if isinstance(base_space_probs, list) else [base_space_probs]
    steered_space_probs = steered_space_probs if isinstance(steered_space_probs, list) else [steered_space_probs]
    base_in_truthful = sum(1 for p in base_space_probs if p >= 0.5)
    steered_in_truthful = sum(1 for p in steered_space_probs if p >= 0.5)
    print(f"\nActivation Space: Base={base_in_truthful}/{len(base_space_probs)} truthful, Steered={steered_in_truthful}/{len(steered_space_probs)}")

    # Generate visualization
    print(f"\nGenerating visualization...")
    multipanel = getattr(args, 'multipanel', False)
    layer_info = f"all {len(steering_vectors_dict)} layers" if multi_layer else f"layer {args.layer}"
    viz_args = dict(pos_activations=pos_ref, neg_activations=neg_ref, base_activations=base_activations,
        steered_activations=steered_activations, title=f"Steering Effect: {args.task} ({layer_info}, strength {args.strength})",
        base_evaluations=base_evaluations, steered_evaluations=steered_evaluations,
        base_space_probs=base_space_probs, steered_space_probs=steered_space_probs)
    if multipanel:
        from wisent.core.geometry.steering_multipanel import create_steering_multipanel_figure
        viz_b64 = create_steering_multipanel_figure(**viz_args)
    else:
        viz_b64 = create_steering_effect_figure(**viz_args)

    # Save outputs
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(viz_b64))
    print(f"\nVisualization saved to: {output_path}")

    json_path = output_path.with_suffix('.json')
    steered_layers = list(steering_vectors_dict.keys()) if multi_layer else [layer_name]
    with open(json_path, 'w') as f:
        json.dump({"model": args.model, "task": args.task, "strength": args.strength,
            "multi_layer": multi_layer, "steered_layers": steered_layers, "num_layers": len(steered_layers),
            "direction_method": direction_method, "steering_method": steering_method_name,
            "text_evaluation": {"base_truthful": base_truthful, "steered_truthful": steered_truthful, "total": len(base_evaluations)},
            "activation_space_location": {"classifier_type": classifier_type, "classifier_accuracy": train_report.final.accuracy,
                "classifier_auc": train_report.final.auc, "base_in_truthful_region": base_in_truthful,
                "steered_in_truthful_region": steered_in_truthful, "total": len(base_space_probs),
                "base_mean_prob": float(np.mean(base_space_probs)), "steered_mean_prob": float(np.mean(steered_space_probs)),
                "base_probs": [float(p) for p in base_space_probs], "steered_probs": [float(p) for p in steered_space_probs]},
            "responses": all_responses}, f, indent=2)
    print(f"Responses saved to: {json_path}")
    print(f"\n{'='*60}\nSTEERING VISUALIZATION COMPLETE\n{'='*60}")
    return {"output": str(output_path), "json_output": str(json_path)}
