import numpy as np


def qr_gram_schmidt(A):
    """
    Descompunere QR folosind Gram–Schmidt modificat.
    A ∈ R^{m x n}, m >= n
    Returnează Q ∈ R^{m x n}, R ∈ R^{n x n}
    """
    A = A.astype(float).copy()
    m, n = A.shape

    Q = np.zeros((m, n))
    R = np.zeros((n, n))

    for j in range(n):
        v = A[:, j].copy()

        for i in range(j):
            R[i, j] = np.dot(Q[:, i], v)
            v = v - R[i, j] * Q[:, i]

        R[j, j] = np.linalg.norm(v)

        if R[j, j] == 0:
            raise ValueError("Coloane dependente liniar – matrice fără rang complet.")

        Q[:, j] = v / R[j, j]

    return Q, R

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

def ls_gram_schmidt(A, b):
    """
    Rezolvă problema celor mai mici pătrate:
        min ||Ax - b||
    folosind QR obținut prin Gram–Schmidt modificat.
    """
    m, n = A.shape
    if m <= n:
        raise ValueError("Sistemul trebuie să fie supradeterminat (m > n).")

    # Pas 1: QR
    Q, R = qr_gram_schmidt(A)

    # Pas 2: d = Q^T b
    d = Q.T @ b

    # Pas 3: R x = d
    x = back_substitution(R, d)

    return x, R, d
