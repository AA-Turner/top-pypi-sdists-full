"""Optional ART (Adversarial Robustness Toolbox) engine for the traditional-ML
privacy attacks.

When ``adversarial-robustness-toolbox`` is installed (the ``airt-ml`` extra), the
extraction and membership attacks route their core step through ART's reference
implementations - CopycatCNN / KnockoffNets for extraction, the black-box
membership inference attacks for membership - instead of the native
numpy/sklearn engine. Everything here is import-guarded: if ART (or torch) is
missing, :func:`art_available` returns ``False`` and callers fall back to the
native engine, so the base SDK never hard-depends on ART.

The victim is always wrapped as a black-box: ART only ever sees a
``predict_fn`` backed by predictions we already collected from the target's API,
so no extra queries are issued and the attack stays honestly black-box.
"""

import typing as t

import numpy as np
from loguru import logger


def art_available() -> bool:
    """True when the Adversarial Robustness Toolbox and torch import cleanly.

    We check for ``art.attacks.extraction`` specifically, not just ``import art``:
    the top-level ``art`` name is also owned by the ASCII-art package the SDK
    depends on, so a bare ``import art`` would false-positive on that library.
    ART is not a hard dependency (it collides with the ASCII-art ``art``); this
    returns True only in an environment where the adversarial toolbox is actually
    installed, otherwise the native engine runs.
    """
    try:
        import torch  # noqa: F401
        from art.attacks.extraction import CopycatCNN  # noqa: F401
        from art.estimators.classification import BlackBoxClassifier  # noqa: F401
    except Exception:
        return False
    return True


def _cached_victim(
    x: np.ndarray,
    proba: np.ndarray,
    nb_classes: int,
) -> t.Any:
    """A BlackBoxClassifier whose predict_fn replays already-collected target
    probabilities, keyed by feature-row bytes - ART "queries" it without issuing
    a single extra network call."""
    from art.estimators.classification import BlackBoxClassifier

    lookup = {row.tobytes(): proba[i] for i, row in enumerate(np.ascontiguousarray(x))}
    uniform = np.full(nb_classes, 1.0 / nb_classes)

    def predict_fn(batch: np.ndarray) -> np.ndarray:
        rows = np.ascontiguousarray(batch, dtype=x.dtype)
        return np.asarray([lookup.get(r.tobytes(), uniform) for r in rows])

    return BlackBoxClassifier(
        predict_fn=predict_fn,
        input_shape=(x.shape[1],),
        nb_classes=nb_classes,
    )


def _torch_thieved(n_features: int, nb_classes: int) -> t.Any:
    """A small torch MLP wrapped as an ART PyTorchClassifier - the surrogate that
    ART trains to replicate the victim."""
    import torch
    from art.estimators.classification import PyTorchClassifier
    from torch import nn

    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Linear(n_features, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, nb_classes),
    )
    return PyTorchClassifier(
        model=model,
        loss=nn.CrossEntropyLoss(),
        optimizer=torch.optim.Adam(model.parameters(), lr=1e-3),
        input_shape=(n_features,),
        nb_classes=nb_classes,
        clip_values=(-1e9, 1e9),
        device_type="cpu",
    )


def art_extract_surrogate(
    strategy: str,
    x: np.ndarray,
    proba: np.ndarray,
    nb_classes: int,
    *,
    nb_epochs: int = 30,
) -> t.Any | None:
    """Train a thieved classifier with ART's CopycatCNN (copycat) or KnockoffNets
    (knockoff) against a cached black-box victim.

    Returns the trained ART classifier (its ``.predict`` yields probabilities), or
    ``None`` if ART is unavailable or the run fails - the caller then falls back to
    the native surrogate. Only ``copycat`` and ``knockoff`` map onto ART; the other
    strategies stay native.
    """
    if strategy not in ("copycat", "knockoff") or not art_available():
        return None
    try:
        from art.attacks.extraction import CopycatCNN, KnockoffNets

        x = np.ascontiguousarray(x, dtype=np.float32)
        victim = _cached_victim(x, proba, nb_classes)
        thieved = _torch_thieved(x.shape[1], nb_classes)
        n = len(x)
        if strategy == "copycat":
            attack: t.Any = CopycatCNN(
                classifier=victim,
                batch_size_fit=32,
                batch_size_query=32,
                nb_epochs=nb_epochs,
                nb_stolen=n,
                use_probability=False,
            )
        else:  # knockoff - soft-label transfer set
            attack = KnockoffNets(
                classifier=victim,
                batch_size_fit=32,
                batch_size_query=32,
                nb_epochs=nb_epochs,
                nb_stolen=n,
                sampling_strategy="random",
                reward="all",
                verbose=False,
                use_probability=True,
            )
        stolen = attack.extract(x=x, thieved_classifier=thieved)
    except Exception as e:  # pragma: no cover - defensive fallback
        logger.warning("ART extraction ({}) failed, falling back to native: {}", strategy, e)
        return None
    else:
        logger.debug("ART {} extraction trained thieved classifier on {} samples", strategy, n)
        return stolen


def art_membership_scores(
    method: str,
    members_x: np.ndarray,
    nonmembers_x: np.ndarray,
    member_proba: np.ndarray,
    nonmember_proba: np.ndarray,
    member_labels: np.ndarray,
    nonmember_labels: np.ndarray,
    nb_classes: int,
) -> np.ndarray | None:
    """Per-record membership scores via ART's black-box rule-based membership
    inference (Yeom et al.). Returns an array aligned to
    ``[members..., nonmembers...]`` in ``[0, 1]``, or ``None`` to fall back to
    native. Only the ``threshold`` method maps onto ART's black-box rule-based
    attack; ``label_only`` stays native.
    """
    if method != "threshold" or not art_available():
        return None
    try:
        from art.attacks.inference.membership_inference import (
            MembershipInferenceBlackBoxRuleBased,
        )

        x = np.ascontiguousarray(np.vstack([members_x, nonmembers_x]), dtype=np.float32)
        proba = np.vstack([member_proba, nonmember_proba])
        labels = np.concatenate([member_labels, nonmember_labels]).astype(int)
        victim = _cached_victim(x, proba, nb_classes)
        attack = MembershipInferenceBlackBoxRuleBased(classifier=victim)
        scores = np.asarray(attack.infer(x, labels, probabilities=True), dtype=np.float64)
        # infer(probabilities=True) returns (N, 2) = [P(non-member), P(member)];
        # the member column is the per-record membership score.
        if scores.ndim == 2 and scores.shape[1] == 2:
            scores = scores[:, 1]
        return scores.ravel()
    except Exception as e:  # pragma: no cover - defensive fallback
        logger.warning("ART membership (threshold) failed, falling back to native: {}", e)
        return None
