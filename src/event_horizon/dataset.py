import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Callable
from .utils import classification_accuracy

def make_plasma_vortex(
    n: int = 500,
    noise: float = 0.12,
    lobes: int = 5,
    amplitude: float = 0.18,
    seed: int = 7
) -> Tuple[np.ndarray, np.ndarray]:
    """Generates Pulsating Plasma Vortex dataset (Option A)."""
    rng = np.random.default_rng(seed)
    n0 = n // 2
    n1 = n - n0

    angle0 = rng.uniform(0, 2 * np.pi, n0)
    radius0 = rng.uniform(0, 0.8, n0) + amplitude * np.sin(lobes * angle0)

    angle1 = rng.uniform(0, 2 * np.pi, n1)
    radius1 = rng.uniform(1.3, 2.0, n1) + amplitude * np.cos(lobes * angle1)

    inner = np.c_[radius0 * np.cos(angle0), radius0 * np.sin(angle0)]
    outer = np.c_[radius1 * np.cos(angle1), radius1 * np.sin(angle1)]

    X = np.vstack([inner, outer]) + rng.normal(0, noise, (n, 2))
    y = np.r_[np.zeros(n0), np.ones(n1)].reshape(-1, 1)

    order = rng.permutation(n)
    return X[order], y[order]


def make_boundary_focused_data(
    n: int = 1000,
    radial_center: float = 1.05,
    radial_width: float = 0.35,
    noise: float = 0.05,
    seed: int = 200
) -> Tuple[np.ndarray, np.ndarray]:
    """Generates telemetry points concentrated near the critical plasma boundary gap."""
    rng = np.random.default_rng(seed)
    angles = rng.uniform(0, 2 * np.pi, n)
    radii = rng.uniform(radial_center - radial_width, radial_center + radial_width, n)
    X = np.c_[radii * np.cos(angles), radii * np.sin(angles)]
    X += rng.normal(0, noise, X.shape)
    observed_radius = np.sqrt((X ** 2).sum(axis=1))
    y = (observed_radius >= radial_center).astype(float).reshape(-1, 1)
    return X, y


def get_shared_telemetry_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Returns standard shared train (N=500) and test (N=1200) plasma vortex datasets."""
    X_train, y_train = make_plasma_vortex(n=500, noise=0.12, seed=7)
    X_test, y_test = make_plasma_vortex(n=1200, noise=0.12, seed=107)
    return X_train, y_train, X_test, y_test


def summarize_run(
    losses: np.ndarray,
    predict_fn: Callable[[np.ndarray], np.ndarray],
    title: str,
    X_train: np.ndarray = None,
    y_train: np.ndarray = None,
    X_test: np.ndarray = None,
    y_test: np.ndarray = None
):
    """Prints metrics and pops up interactive loss & decision boundary plots on screen."""
    if X_train is None or X_test is None:
        X_train, y_train, X_test, y_test = get_shared_telemetry_data()

    losses = np.asarray(losses, dtype=float)
    train_p = predict_fn(X_train)
    test_p = predict_fn(X_test)

    train_acc = classification_accuracy(y_train, train_p)
    test_acc = classification_accuracy(y_test, test_p)

    print("\n" + "=" * 60)
    print(f" TELEMETRY SUMMARY: {title}")
    print("=" * 60)
    print(f"  Train Accuracy: {train_acc:.1%}")
    print(f"  Test Accuracy:  {test_acc:.1%}")
    print(f"  Final Loss:     {losses[-1]:.5f}")
    print(f"  Pred Range:     [{test_p.min():.3f}, {test_p.max():.3f}]")
    print("=" * 60 + "\n")

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle(f"Project Event Horizon — {title}", fontsize=14, fontweight='bold', color='#00E5FF')

    # Loss plot
    ax1.plot(losses, color='#FF5252', linewidth=2)
    ax1.set_title("Training Loss Convergence", color='#E0E0E0')
    ax1.set_xlabel("Epoch", color='#B0BEC5')
    ax1.set_ylabel("Binary Cross-Entropy Loss", color='#B0BEC5')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # Contour heatmap plot
    xx, yy = np.meshgrid(np.linspace(-2.8, 2.8, 220), np.linspace(-2.8, 2.8, 220))
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = predict_fn(grid).reshape(xx.shape)

    ax2.contourf(xx, yy, zz, levels=25, cmap='plasma', alpha=0.85)
    ax2.scatter(X_test[:, 0], X_test[:, 1], c=y_test.ravel(), cmap='cool', s=12, edgecolors='black', linewidths=0.2)
    ax2.set_title(f"Plasma Decision Boundary (Test Acc: {test_acc:.1%})", color='#E0E0E0')
    ax2.set_xlabel("X1", color='#B0BEC5')
    ax2.set_ylabel("X2", color='#B0BEC5')

    plt.tight_layout()
    print(" Displaying telemetry graph popup on screen...")
    plt.show()
