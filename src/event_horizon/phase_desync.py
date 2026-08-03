import numpy as np

try:
    from .utils import sigmoid, binary_cross_entropy
    from .dataset import get_shared_telemetry_data, summarize_run
except ImportError:
    from event_horizon.utils import sigmoid, binary_cross_entropy
    from event_horizon.dataset import get_shared_telemetry_data, summarize_run


def train_diagnostic_03(X: np.ndarray, y: np.ndarray, hidden: int = 24, seed: int = 5, epochs: int = 1800, learning_rate: float = 0.25):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1, (2, hidden)) * np.sqrt(2 / 2)
    b1 = np.zeros((1, hidden))
    W2 = rng.normal(0, 1, (hidden, 1)) * np.sqrt(2 / hidden)
    b2 = np.zeros((1, 1))

    losses = []
    for _ in range(epochs):
        z1 = X @ W1 + b1

        a1 = z1

        z2 = a1 @ W2 + b2
        p = sigmoid(z2)
        losses.append(binary_cross_entropy(y, p))

        dz2 = (p - y) / len(X)
        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)
        dz1 = (dz2 @ W2.T) * (z1 > 0)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)

        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2

    return {"W1": W1, "b1": b1, "W2": W2, "b2": b2}, np.array(losses)


def predict(model: dict, X: np.ndarray) -> np.ndarray:
    z1 = X @ model["W1"] + model["b1"]
    a1 = z1
    return sigmoid(a1 @ model["W2"] + model["b2"])


def run_diagnostic():
    X_train, y_train, X_test, y_test = get_shared_telemetry_data()
    print("\n--- Diagnostic 03: Testing Forward/Backward Activation Alignment ---")

    model, losses = train_diagnostic_03(X_train, y_train)
    summarize_run(losses, lambda X: predict(model, X), "Diagnostic 03 Output")


if __name__ == "__main__":
    run_diagnostic()
