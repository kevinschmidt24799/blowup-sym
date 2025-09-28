from shared import *
import time


class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.count = 0
        self.start_time = time.time()
        print(f"Total combinations to process: {total:,}")

    def update(self):
        self.count += 1
        if self.count % 100000 == 0:
            elapsed = time.time() - self.start_time
            rate = self.count / elapsed
            remaining_items = self.total - self.count
            estimated_seconds = remaining_items / rate
            hours = int(estimated_seconds // 3600)
            minutes = int((estimated_seconds % 3600) // 60)
            print(f"Progress: {self.count:,}/{self.total:,} ({100*self.count/self.total:.1f}%) - Est. {hours}h {minutes}m remaining")


def find_max_third_eigenvalue(A_list, n, total_B_count):
    max_third_eigen_value = float('-inf')
    max_M = None

    total = len(A_list) * total_B_count
    progress = ProgressTracker(total)

    for A in A_list:
        for B_t_sum in get_matrix_transposed_sum(n):
            M = A + B_t_sum
            eigenvalues = np.linalg.eigvals(M).real
            eigenvalues = np.sort(eigenvalues)[::-1]

            if eigenvalues[2] >= max_third_eigen_value:
                max_third_eigen_value = eigenvalues[2]
                max_M = M
                print(f"New max third eigenvalue: {max_third_eigen_value}")
                print("Matrix:")
                print(max_M.astype(int))

            progress.update()

    return max_third_eigen_value, max_M


def spectrum_m1(n):
    assert n >= 3

    A_list = get_symmetrical_matrices(n)
    B_count = get_matrix_transposed_sum_count(n)

    max_third_eigen_value, max_M = find_max_third_eigenvalue(
        A_list,
        n,
        B_count
    )

    print(f"Final max third eigenvalue: {max_third_eigen_value}")
    print("Final max matrix:")
    print(max_M.astype(int))
    return
