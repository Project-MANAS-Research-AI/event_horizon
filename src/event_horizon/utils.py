import numpy as np
from typing import Dict

def sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid function."""
    z = np.clip(z, -30, 30)
    return 1.0 / (1.0 + np.exp(-z))


def binary_cross_entropy(y: np.ndarray, p: np.ndarray) -> float:
    """Binary cross-entropy loss calculation."""
    eps = 1e-9
    return float(-(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)).mean())


def classification_accuracy(y: np.ndarray, p: np.ndarray) -> float:
    """Binary classification accuracy ratio (0.0 to 1.0)."""
    return float(((p >= 0.5).astype(int) == y).mean())


def initialize_weights(hidden: int = 24, seed: int = 1) -> Dict[str, np.ndarray]:
    """Standard Xavier/He weight initialization for a 2-hidden-1 MLP."""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, 1, (2, hidden)) * np.sqrt(2 / 2),
        "b1": np.zeros((1, hidden)),
        "W2": rng.normal(0, 1, (hidden, 1)) * np.sqrt(2 / hidden),
        "b2": np.zeros((1, 1)),
    }


def run_safely(fn, title: str):
    """Executes a diagnostic function safely, trapping exceptions for debugging."""
    try:
        return fn()
    except Exception as error:
        print(f"\n[CRASH DETECTED] {title}")
        print(f"  Error Type: {type(error).__name__}")
        print(f"  Error Message: {error}")
        return None
