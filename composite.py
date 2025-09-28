
import matplotlib.pyplot as plt
from shared import *

n = 10
symmetry_order = 3
coset_size = 3
fixed_points = 1
assert n == symmetry_order*coset_size+fixed_points


def find_max_eigenvalue():
    count = 0
    max_third_eigenvalue = float('-inf')
    max_adj = None

    list_coset_self = get_symmetrical_matrices(coset_size)
    list_coset_plus1 = get_matrices(coset_size, coset_size)
    list_coset_to_fixed = get_matrices(coset_size, fixed_points)
    list_fixed_self = get_symmetrical_matrices(fixed_points)

    expected_count = len(list_coset_self) * len(list_coset_plus1) * len(list_coset_to_fixed) * len(list_fixed_self)
    print("expected count:", expected_count)

    for coset_self in list_coset_self:
        for coset_plus1 in list_coset_plus1:
            coset_plus1_t = coset_plus1.T
            for coset_to_fixed in list_coset_to_fixed:
                coset_to_fixed_t = coset_to_fixed.T
                for fixed_self in list_fixed_self:
                    adj = np.block([
                        [coset_self, coset_plus1, coset_plus1_t, coset_to_fixed],
                        [coset_plus1_t, coset_self, coset_plus1, coset_to_fixed],
                        [coset_plus1, coset_plus1_t, coset_self, coset_to_fixed],
                        [coset_to_fixed_t, coset_to_fixed_t, coset_to_fixed_t, fixed_self]
                    ])

                    # Compute eigenvalues
                    eigenvalues = np.linalg.eigvals(adj).real
                    eigenvalues = np.sort(eigenvalues)[::-1]  # Sort in descending order

                    # Get third largest eigenvalue (if it exists)
                    if len(eigenvalues) >= 3:
                        third_eigenvalue = eigenvalues[2]

                        # Check if this is a new maximum
                        if third_eigenvalue > max_third_eigenvalue:
                            max_third_eigenvalue = third_eigenvalue
                            max_adj = adj

                            print(f"\nNew maximum 3rd eigenvalue found: {max_third_eigenvalue:.6f}")
                            print("Adjacency matrix:")
                            print(adj.astype(int))

                            # Draw the graph
                            g = nx.from_numpy_array(adj)
                            plt.title(f"3rd largest eigenvalue: {max_third_eigenvalue:.6f}")
                            nx.draw(g)
                            plt.show()

                    count += 1
                    if count % 100000 == 0:
                        print(f"Processed {count}/{expected_count} matrices, current max 3rd eigenvalue: {max_third_eigenvalue:.6f}")

    print(f"\nTotal matrices processed: {count}/{expected_count}")
    print(f"Final maximal 3rd largest eigenvalue: {max_third_eigenvalue:.6f}")
    print("Adjacency matrix:")
    print(max_adj.astype(int))