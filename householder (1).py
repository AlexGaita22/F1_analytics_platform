import numpy as np

def tort_householder(A):
    """
    Triangularizare cu reflectori Householder (TORT).
    Suprascrie A cu R și returnează R, U, beta.
    """
    A = A.astype(float).copy()
    m, n = A.shape
    p = min(m - 1, n)

    U = np.zeros((m, p))
    beta = np.zeros(p)

    for k in range(p):
        # normă coloană k (de la k la m)
        col = A[k:, k]
        norm_col = np.linalg.norm(col)

        if norm_col == 0:# Dacă norma este 0, coloana este deja zero.
            beta[k] = 0.0
            continue

        sigma = np.sign(A[k, k]) * norm_col
        if sigma == 0:
            beta[k] = 0.0
            continue

        # construim vectorul u_k
        U[k, k] = A[k, k] + sigma
        U[k+1:, k] = A[k+1:, k]

        beta[k] = sigma * U[k, k]

        # actualizăm A
        A[k, k] = -sigma
        A[k+1:, k] = 0.0

        # aplicăm reflectorul pe coloanele următoare
        for j in range(k + 1, n):
            tau = (U[k:, k] @ A[k:, j]) / beta[k]
            A[k:, j] -= tau * U[k:, k]

    R = A
    return R, U, beta


def apply_householders_to_b(b, U, beta, n):
    """
    Aplică reflectorii Householder asupra vectorului b.
    Calculează d = Q^T b (fără a forma Q).
    """
    b = b.astype(float).copy()
    m = len(b)

    for k in range(n):
        if beta[k] == 0:
            continue
        tau = (U[k:m, k] @ b[k:m]) / beta[k]
        b[k:m] -= tau * U[k:m, k]

    return b


def back_substitution(R, d):
    """
    Rezolvă sistem triunghiular superior R x = d.
    """
    n = R.shape[0]
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        if R[i, i] == 0:
            raise ValueError("Matrice R singulară.")
        x[i] = (d[i] - R[i, i+1:] @ x[i+1:]) / R[i, i]

    return x

def ls_householder(A, b):
    """
    Rezolvă problema celor mai mici pătrate:
        min ||Ax - b||
    folosind Householder (TORT + CMMP).
    """
    m, n = A.shape
    if m <= n:
        raise ValueError("Sistemul trebuie să fie supradeterminat (m > n).")

    # Pas 1: TORT
    R, U, beta = tort_householder(A)

    # Pas 2: aplicăm reflectorii pe b
    d = apply_householders_to_b(b, U, beta, n)

    # Pas 3: extragem sistemul triunghiular
    R0 = R[:n, :n]
    d0 = d[:n]

    # Pas 4: rezolvare
    x = back_substitution(R0, d0)

    return x, R, d

