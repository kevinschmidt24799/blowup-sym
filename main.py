import os
from composite import find_max_eigenvalue
from circulant import spectrum_m1

def main():
    # Disable NumPy's internal threading to avoid conflicts with our threading
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'

    # find_max_eigenvalue()
    spectrum_m1(6)

if __name__ == "__main__":
    main()