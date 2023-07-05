from cmath import exp
from math import pi
import numpy as np

# Helper functions
def xy_to_complex(points):
    return np.array([x + 1j*y for x, y in points], dtype=np.complex64)

# Main functions
def normalize_points(line_points):
    '''
    Returns a normalized version of the line points with equal distances between points.
    '''
    line_points = np.append(line_points, line_points[0:1], axis=0)
    num_normalized = max(100, min(len(line_points) - 1, 1500))
    cum_distances = np.cumsum(np.linalg.norm(np.diff(line_points, axis=0), axis=1))
    total_distance = cum_distances[-1]

    normalized_distances = np.linspace(0, total_distance, num_normalized, endpoint=False)
    normalized_points = np.zeros((num_normalized, 2))

    for i, d in enumerate(normalized_distances):
        k = np.searchsorted(cum_distances, d)
        if k == 0:
            t = d / cum_distances[0]
        else:
            t = (d - cum_distances[k-1]) / (cum_distances[k] - cum_distances[k-1])
        normalized_points[i] = (1 - t) * line_points[k] + t * line_points[k+1]
    return normalized_points


def calculate_intermediate_points(dft_coeffs, n, K, N):
    '''
    Calculates the intermediate points of the fourier series up to the Kth coefficient
    K+1 points are returned
    '''
    intermediate_points = np.zeros(K+1, dtype=np.complex64)
    intermediate_points[0] = dft_coeffs[0]
    for k in range(1, (K+4)//2):
        i = 2 * k - 1
        if i > K:
            break
        intermediate_points[i] = intermediate_points[i-1] + dft_coeffs[k] * exp(1j*2*pi*k/N*n)    
        i = 2 * k
        if i > K:
            break
        intermediate_points[i] = intermediate_points[i-1] + dft_coeffs[-k] * exp(1j*2*pi*-k/N*n)
    return intermediate_points

# Fourier transforms
def dft(x):
    N = len(x)
    X = np.zeros(N, dtype=np.complex64)
    for k in range(N):
        for n in range(N):
            X[k] += 1/N * x[n]*exp(-1j*2*pi*k/N*n)
    return X

def idft(X, K=None):
    N = len(X)
    K_range = range(N) if K is None else range(-K//2, K//2)
    x = np.zeros(N, dtype=np.complex64)
    for n in range(N):
        for k in K_range:
            x[n] += X[k] * exp(1j*2*pi*k/N*n)
    return x


# File I/O
def save_line(points, filename):
    with open(filename, 'w') as file:
        for point in points:
            file.write(f"{point[0]},{point[1]}\n")

def read_line(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append([x, y])
    return points
