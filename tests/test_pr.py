"""Held-out behavioral tests used by the pull-request challenge workflow."""

import numpy as np

from event_horizon.batch_flux import train_diagnostic_02
from event_horizon.dataset import get_shared_telemetry_data, make_plasma_vortex
from event_horizon.field_stress import (
    predict as predict_pruned,
    prune_dead_neurons,
    train_healthy,
)
from event_horizon.phase_desync import (
    predict as predict_diagnostic_03,
    train_diagnostic_03,
)
from event_horizon.tensor_alignment import (
    predict as predict_diagnostic_01,
    train_diagnostic_01,
)
from event_horizon.utils import classification_accuracy, sigmoid


def test_diagnostic_01_trains_with_aligned_output_weights() -> None:
    X_train, y_train, X_test, _ = get_shared_telemetry_data()

    model, losses = train_diagnostic_01(
        X_train,
        y_train,
        hidden=16,
        epochs=300,
        seed=1,
    )
    predictions = predict_diagnostic_01(model, X_test)

    assert model["W2"].shape == (16, 1)
    assert predictions.shape == (len(X_test), 1)
    assert np.isfinite(losses).all()
    assert np.isfinite(predictions).all()
    assert losses[-1] < losses[0] * 0.25


def test_diagnostic_02_gradient_scale_is_batch_size_invariant() -> None:
    initial_norms = []

    for size in (50, 500, 5000):
        X, y = make_plasma_vortex(n=size, noise=0.12, seed=7)
        _, losses, gradient_norms = train_diagnostic_02(
            X,
            y,
            epochs=1,
            seed=2,
        )
        assert np.isfinite(losses).all()
        assert np.isfinite(gradient_norms).all()
        initial_norms.append(gradient_norms[0])

    assert max(initial_norms) / min(initial_norms) < 2.0


def test_diagnostic_03_uses_relu_consistently_and_converges() -> None:
    X_train, y_train, X_test, y_test = get_shared_telemetry_data()

    model, losses = train_diagnostic_03(
        X_train,
        y_train,
        hidden=24,
        epochs=400,
        seed=5,
    )
    predictions = predict_diagnostic_03(model, X_test)
    hidden = np.maximum(0, X_test @ model["W1"] + model["b1"])
    expected = sigmoid(hidden @ model["W2"] + model["b2"])

    np.testing.assert_allclose(predictions, expected, rtol=0, atol=1e-12)
    assert losses[-1] < losses[0] * 0.25
    assert classification_accuracy(y_test, predictions) > 0.95


def test_diagnostic_04_prunes_all_dead_neurons_without_changing_output() -> None:
    X, y = make_plasma_vortex(n=240, noise=0.12, seed=7)
    model, _ = train_healthy(X, y, hidden=32, epochs=50, seed=42)
    original = {name: values.copy() for name, values in model.items()}
    predictions_before = predict_pruned(model, X)

    pruned = prune_dead_neurons(model, X)
    predictions_after = predict_pruned(pruned, X)

    assert pruned is not model
    assert pruned["W1"].shape == (2, 26)
    assert pruned["b1"].shape == (1, 26)
    assert pruned["W2"].shape == (26, 1)
    assert pruned["b2"].shape == (1, 1)
    np.testing.assert_allclose(predictions_after, predictions_before, rtol=0, atol=1e-12)

    for name, values in original.items():
        np.testing.assert_array_equal(model[name], values)

    activations = np.maximum(0, X @ pruned["W1"] + pruned["b1"])
    assert np.all(np.any(activations > 0, axis=0))
