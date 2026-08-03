import numpy as np

from event_horizon.dataset import make_boundary_focused_data, make_plasma_vortex
from event_horizon.field_stress import prune_dead_neurons, train_healthy
from event_horizon.utils import (
    binary_cross_entropy,
    classification_accuracy,
    initialize_weights,
    sigmoid,
)


def test_sigmoid_is_numerically_stable() -> None:
    values = sigmoid(np.array([-100.0, 0.0, 100.0]))

    assert np.isclose(values[1], 0.5)
    assert values[0] > 0.0
    assert values[2] < 1.0


def test_binary_metrics_match_known_values() -> None:
    labels = np.array([[0.0], [1.0], [1.0], [0.0]])
    probabilities = np.array([[0.1], [0.9], [0.8], [0.2]])

    assert binary_cross_entropy(labels, probabilities) < 0.2
    assert classification_accuracy(labels, probabilities) == 1.0


def test_plasma_vortex_is_deterministic_and_balanced() -> None:
    X_first, y_first = make_plasma_vortex(n=200, seed=42)
    X_second, y_second = make_plasma_vortex(n=200, seed=42)

    assert X_first.shape == (200, 2)
    assert y_first.shape == (200, 1)
    assert set(np.unique(y_first)) == {0.0, 1.0}
    assert y_first.sum() == 100
    np.testing.assert_array_equal(X_first, X_second)
    np.testing.assert_array_equal(y_first, y_second)


def test_boundary_focused_data_has_expected_contract() -> None:
    X, y = make_boundary_focused_data(n=125, seed=11)

    assert X.shape == (125, 2)
    assert y.shape == (125, 1)
    assert set(np.unique(y)).issubset({0.0, 1.0})
    assert np.isfinite(X).all()


def test_weight_initialization_uses_expected_shapes() -> None:
    model = initialize_weights(hidden=16, seed=3)

    assert model["W1"].shape == (2, 16)
    assert model["b1"].shape == (1, 16)
    assert model["W2"].shape == (16, 1)
    assert model["b2"].shape == (1, 1)


def test_healthy_training_reduces_loss() -> None:
    X, y = make_plasma_vortex(n=200, seed=7)
    model, losses = train_healthy(X, y, hidden=16, epochs=100)

    assert set(model) == {"W1", "b1", "W2", "b2"}
    assert len(losses) == 100
    assert np.isfinite(losses).all()
    assert losses[-1] < losses[0]


def test_pruning_api_returns_a_predictable_model_contract() -> None:
    X, y = make_plasma_vortex(n=120, seed=7)
    model, _ = train_healthy(X, y, hidden=16, epochs=40)
    pruned = prune_dead_neurons(model, X)

    assert set(pruned) == {"W1", "b1", "W2", "b2"}
    assert pruned["W1"].shape[0] == 2
    assert pruned["b1"].shape[0] == 1
    assert pruned["W2"].shape[1] == 1
    assert pruned["b2"].shape == (1, 1)
