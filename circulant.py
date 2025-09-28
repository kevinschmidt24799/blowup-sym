from shared import *



def spectrum_m1(n):
    assert n >= 3

    A_list = get_symmetrical_matrices(n)
    B_transposed_sum_list = get_matrix_transposed_sum(n)

    max_third_eigen_value = float('-inf')
    max_M = None

    total = len(A_list) * len(B_transposed_sum_list)
    count = 0
    print(f"Total combinations to process: {total:,}")

    for A in A_list:
        for B_t_sum in B_transposed_sum_list:
            M = A+B_t_sum
            eigenvalues = np.linalg.eigvals(M).real
            eigenvalues = np.sort(eigenvalues)[::-1]
            if eigenvalues[2] >= max_third_eigen_value:
                max_third_eigen_value = eigenvalues[2]
                max_M = M
                print(f"New max third eigenvalue: {max_third_eigen_value}")
                print("Matrix:")
                print(max_M.astype(int))

            count += 1
            if count % 100000 == 0:
                print(f"Progress: {count:,}/{total:,} ({100*count/total:.1f}%)")

    print(f"Final max third eigenvalue: {max_third_eigen_value}")
    print("Final max matrix:")
    print(max_M.astype(int))
    return
