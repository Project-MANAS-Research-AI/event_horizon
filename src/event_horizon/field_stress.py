import numpy as np

try:
    from .utils import sigmoid, binary_cross_entropy, classification_accuracy, initialize_weights
    from .dataset import make_plasma_vortex, get_shared_telemetry_data, summarize_run
except ImportError:
    from event_horizon.utils import sigmoid, binary_cross_entropy, classification_accuracy, initialize_weights
    from event_horizon.dataset import make_plasma_vortex, get_shared_telemetry_data, summarize_run


def train_healthy(X: np.ndarray, y: np.ndarray, hidden: int = 32, seed: int = 42, epochs: int = 1500, learning_rate: float = 0.25):
    model = initialize_weights(hidden=hidden, seed=seed)
    losses = []

    for _ in range(epochs):
        z1 = X @ model["W1"] + model["b1"]
        a1 = np.maximum(0, z1)
        p = sigmoid(a1 @ model["W2"] + model["b2"])
        losses.append(binary_cross_entropy(y, p))

        dz2 = (p - y) / len(X)
        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)
        dz1 = (dz2 @ model["W2"].T) * (z1 > 0)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)

        model["W1"] -= learning_rate * dW1
        model["b1"] -= learning_rate * db1
        model["W2"] -= learning_rate * dW2
        model["b2"] -= learning_rate * db2

    dead_indices = [i for i in [4, 11, 18, 23, 27, 30] if i < hidden]
    model["W1"][:, dead_indices] = 0.0
    model["b1"][:, dead_indices] = -50.0
    model["W2"][dead_indices, :] = 0.0

    return model, np.array(losses)


def predict(model: dict, X: np.ndarray) -> np.ndarray:
    hidden = np.maximum(0, X @ model["W1"] + model["b1"])
    return sigmoid(hidden @ model["W2"] + model["b2"])


def prune_dead_neurons(model: dict, X: np.ndarray) -> dict:
    return model


def run_diagnostic():
    X_train, y_train, X_test, y_test = get_shared_telemetry_data()

    print("\n--- Diagnostic 04: Flight Hardware Neural Pruning Audit ---")
    raw_model, losses = train_healthy(X_train, y_train)

    acc_raw = classification_accuracy(y_test, predict(raw_model, X_test))
    h_raw = raw_model["W1"].shape[1]

    print(f"\n[BASELINE MODEL]")
    print(f"  Hidden Neurons: {h_raw}")
    print(f"  Test Accuracy:  {acc_raw:.1%}")

    pruned_model = prune_dead_neurons(raw_model, X_train)
    acc_pruned = classification_accuracy(y_test, predict(pruned_model, X_test))
    h_pruned = pruned_model["W1"].shape[1]

    print(f"\n[PRUNED MODEL AUDIT]")
    print(f"  Hidden Neurons: {h_pruned}")
    print(f"  Test Accuracy:  {acc_pruned:.1%}")

    if h_pruned < h_raw and abs(acc_pruned - acc_raw) < 1e-4:
        print(f"\n[STATUS: PASSED] Successfully pruned {h_raw - h_pruned} dead neurons without loss of accuracy!")
        summarize_run(losses, lambda X: predict(pruned_model, X), "Diagnostic 04 Pruned Model")
    elif h_pruned == h_raw:
        print(f"\n[STATUS: FAILED] No dead neurons were pruned. Implement `prune_dead_neurons` in field_stress.py!")
        summarize_run(losses, lambda X: predict(raw_model, X), "Diagnostic 04 Baseline Model")
    else:
        print(f"\n[STATUS: FAILED] Accuracy degraded after pruning! Check your pruning logic.")


if __name__ == "__main__":
    run_diagnostic()
