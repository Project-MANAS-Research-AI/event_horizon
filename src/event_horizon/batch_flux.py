"""
Diagnostic 02 — Batch Flux Instability
=========================================
Symptom: Gradient updates scale uncontrollably when dataset size changes (N=50 vs N=500 vs N=5000).

Goal for Recruit:
1. Run `uv run event-horizon -d 2` to observe the gradient norms across batch sizes.
2. Fix the unnormalized gradient computation in `train_diagnostic_02` below.
"""

import numpy as np

try:
    from .utils import sigmoid, binary_cross_entropy, classification_accuracy
    from .dataset import make_plasma_vortex, summarize_run
except ImportError:
    from event_horizon.utils import sigmoid, binary_cross_entropy, classification_accuracy
    from event_horizon.dataset import make_plasma_vortex, summarize_run


def train_diagnostic_02(X: np.ndarray, y: np.ndarray, hidden: int = 24, seed: int = 2, epochs: int = 1800, learning_rate: float = 0.02):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1, (2, hidden)) * np.sqrt(2 / 2)
    b1 = np.zeros((1, hidden))
    W2 = rng.normal(0, 1, (hidden, 1)) * np.sqrt(2 / hidden)
    b2 = np.zeros((1, 1))

    losses = []
    gradient_norms = []

    for _ in range(epochs):
        z1 = X @ W1 + b1
        a1 = np.maximum(0, z1)
        p = sigmoid(a1 @ W2 + b2)
        losses.append(binary_cross_entropy(y, p))

        # 🛠️ RECRUIT TASK: Locate and repair the conceptual defect in this function.
        dz2 = p - y

        dW2 = a1.T @ dz2
        db2 = dz2.sum(axis=0, keepdims=True)
        dz1 = (dz2 @ W2.T) * (z1 > 0)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0, keepdims=True)

        gradient_norms.append(float(np.sqrt(np.sum(dW1**2) + np.sum(dW2**2))))

        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2

    return {"W1": W1, "b1": b1, "W2": W2, "b2": b2}, np.array(losses), np.array(gradient_norms)


def predict(model: dict, X: np.ndarray) -> np.ndarray:
    hidden = np.maximum(0, X @ model["W1"] + model["b1"])
    return sigmoid(hidden @ model["W2"] + model["b2"])


def run_diagnostic():
    print("\n--- Diagnostic 02: Evaluating Gradient Norms Across Batch Sizes ---")
    sizes = (50, 500, 5000)
    for n in sizes:
        Xn, yn = make_plasma_vortex(n=n, noise=0.12, seed=7)
        model, losses, norms = train_diagnostic_02(Xn, yn)
        preds = predict(model, Xn)
        acc = classification_accuracy(yn, preds)
        print(f" Size N={n:4d} | Initial Grad Norm: {norms[0]:10.4f} | Final Loss: {losses[-1]:.5f} | Train Acc: {acc:.1%}")

    print("\nDisplaying telemetry graph for N=500...")
    X_train, y_train = make_plasma_vortex(n=500, noise=0.12, seed=7)
    X_test, y_test = make_plasma_vortex(n=1200, noise=0.12, seed=107)
    model, losses, _ = train_diagnostic_02(X_train, y_train)
    summarize_run(losses, lambda X: predict(model, X), "Diagnostic 02 Output")


if __name__ == "__main__":
    run_diagnostic()
