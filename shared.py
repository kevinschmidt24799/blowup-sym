
import networkx as nx
import numpy as np


def get_symmetrical_matrices(size):
    atlas = nx.graph_atlas_g()
    matrices = [nx.to_numpy_array(G) for G in atlas if G.number_of_nodes() == size]
    return matrices

def get_matrices(rows, columns):
    total_cells = rows * columns

    if total_cells == 0:
        return [np.matrix([]).reshape(rows,columns)]

    matrices = []
    for i in range(2 ** total_cells):
        binary_str = format(i, f'0{total_cells}b')
        matrix = np.array([int(bit) for bit in binary_str]).reshape(rows, columns)
        matrices.append(matrix)

    return matrices


def get_matrix_transposed_sum(size):
    matrices = []

    # Number of diagonal elements
    diagonal_elements = size
    # Number of upper triangle elements (excluding diagonal)
    upper_triangle_elements = size * (size - 1) // 2

    # Generate all combinations for diagonal (0 or 2)
    for diag_combo in range(2 ** diagonal_elements):
        # Generate all combinations for upper triangle (0, 1, or 2)
        for upper_combo in range(3 ** upper_triangle_elements):
            matrix = np.zeros((size, size), dtype=int)

            # Set diagonal elements (0 or 2)
            diag_bits = format(diag_combo, f'0{diagonal_elements}b')
            for i in range(size):
                matrix[i, i] = 2 * int(diag_bits[i])

            # Set upper triangle elements (0, 1, or 2)
            upper_combo_temp = upper_combo
            for i in range(size):
                for j in range(i + 1, size):
                    value = upper_combo_temp % 3
                    matrix[i, j] = value
                    matrix[j, i] = value  # Make symmetric
                    upper_combo_temp //= 3

            matrices.append(matrix)

    return matrices
