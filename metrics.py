"""
Modul de metrici
================
Calculează metrici de evaluare pentru modele de regresie.
"""

import numpy as np


def compute_residual_norm(A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
    """
    Calculează ||Ax - b||₂ (norma L2 a rezidualilor).
    """
    residuals = A @ x - b
    return np.linalg.norm(residuals, ord=2)


def compute_rmse(A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
    """
    Calculează RMSE: sqrt(mean((Ax - b)^2)).
    """
    residuals = A @ x - b
    mse = np.mean(residuals ** 2)
    return np.sqrt(mse)


def compute_condition_number(A: np.ndarray) -> float:
    """
    Calculează numărul de condiție al matricei A.
    """
    try:
        cond = np.linalg.cond(A)
        return cond
    except:
        return np.inf

