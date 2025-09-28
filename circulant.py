from shared import *
import time
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed


class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.global_max = float('-inf')
        print(f"Total combinations to process: {total:,}")

    def update(self, increment=1):
        with self.lock:
            old_milestone = self.count // 100000
            self.count += increment
            new_milestone = self.count // 100000

            if new_milestone > old_milestone:
                elapsed = time.time() - self.start_time
                rate = self.count / elapsed
                remaining_items = self.total - self.count
                estimated_seconds = remaining_items / rate
                hours = int(estimated_seconds // 3600)
                minutes = int((estimated_seconds % 3600) // 60)
                print(f"Progress: {self.count:,}/{self.total:,} ({100*self.count/self.total:.1f}%) - Est. {hours}h {minutes}m remaining")

    def check_and_update_max(self, eigenvalue, matrix):
        with self.lock:
            if eigenvalue > self.global_max:
                self.global_max = eigenvalue
                print(f"New max third eigenvalue: {eigenvalue}")
                print("Matrix:")
                print(matrix.astype(int))
                return True
            return False


def process_single_A_matrix(A, n, total_B_count):
    local_max_third_eigen_value = float('-inf')
    local_max_M = None
    local_count = 0

    for B_t_sum in get_matrix_transposed_sum(n):
        M = A + B_t_sum
        eigenvalues = np.linalg.eigvals(M).real
        eigenvalues = np.sort(eigenvalues)[::-1]

        if eigenvalues[2] >= local_max_third_eigen_value:
            local_max_third_eigen_value = eigenvalues[2]
            local_max_M = M

        local_count += 1

    return local_max_third_eigen_value, local_max_M, local_count


def find_max_third_eigenvalue(A_list, n, total_B_count):
    max_third_eigen_value = float('-inf')
    max_M = None

    total = len(A_list) * total_B_count
    progress = ProgressTracker(total)

    # Use ProcessPoolExecutor to process A matrices in parallel
    with ProcessPoolExecutor() as executor:
        import os
        print(f"Using {os.cpu_count()} processes for {len(A_list)} A matrices")
        # Submit all A matrices for processing
        future_to_A = {
            executor.submit(process_single_A_matrix, A, n, total_B_count): A
            for A in A_list
        }

        completed_count = 0
        total_processed = 0

        # Collect results as they complete
        for future in as_completed(future_to_A):
            local_max_value, local_max_M, local_count = future.result()
            completed_count += 1
            total_processed += local_count

            if local_max_value > max_third_eigen_value:
                max_third_eigen_value = local_max_value
                max_M = local_max_M
                print(f"New max third eigenvalue: {max_third_eigen_value}")
                print("Matrix:")
                print(max_M.astype(int))

            # Simple progress update
            if completed_count % 10 == 0:
                progress_pct = (total_processed / (len(A_list) * total_B_count)) * 100
                print(f"Completed {completed_count}/{len(A_list)} A matrices ({progress_pct:.1f}%)")

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
