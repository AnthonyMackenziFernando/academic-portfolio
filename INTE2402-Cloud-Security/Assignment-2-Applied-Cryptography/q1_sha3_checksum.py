def sha3_round_1_matrices():
    #Initialize the exact 25-character string
    s = "Anthony Fernando S4129857"
    
    #Create the 5x5 Initial State Matrix
    A = [[0]*5 for _ in range(5)]
    for i, char in enumerate(s):
        x = i % 5
        y = i // 5
        A[x][y] = ord(char)
        
    def print_matrix(mat, name):
        print(f"---{name} Output---")
        for y in range(5):
            row = [f"{mat[x][y]:02X}" for x in range(5)]
            print(" ".join(row))
        print()

    print_matrix(A, "Initial State")

    #Step01- Theta(Parity diffusion)
    C = [0]*5
    for x in range(5):
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]
        
    D = [0]*5
    for x in range(5):
        #Calculate C[x+1] rotated left by 1 bit (8-bit circular shift)
        C_next = C[(x+1) % 5]
        rot = ((C_next << 1) | (C_next >> 7)) & 0xFF
        D[x] = C[(x-1) % 5] ^ rot
        
    A_theta = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
    print_matrix(A_theta, "Theta")

    #Step02- Rho(Bitwise dispersion/rotation)
    r_mod_8 = [
        [0, 1, 6, 4, 3],
        [4, 4, 6, 7, 4],
        [3, 2, 3, 1, 7],
        [1, 5, 7, 5, 0],
        [2, 2, 5, 0, 0]
    ]
    
    A_rho = [[0]*5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            val = A_theta[x][y]
            rot = r_mod_8[y][x]
            #Circular left shift by 'rot' bits
            A_rho[x][y] = ((val << rot) | (val >> (8 - rot))) & 0xFF
    print_matrix(A_rho, "Rho")

    #Step03- Pi(Coordinate permutation)
    A_pi = [[0]*5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            A_pi[x][y] = A_rho[(x + 3*y) % 5][x]
    print_matrix(A_pi, "Pi")

    #Step04- Chi(Non-linear bitwise logic)
    A_chi = [[0]*5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            not_x1 = (~A_pi[(x+1) % 5][y]) & 0xFF
            A_chi[x][y] = A_pi[x][y] ^ (not_x1 & A_pi[(x+2) % 5][y])
    print_matrix(A_chi, "Chi")

    #Step05- Iota(Round Constant addition)
    A_iota = [[A_chi[x][y] for y in range(5)] for x in range(5)]
    RC = 0x01 #Round Constant for the 1st round
    A_iota[0][0] ^= RC
    print_matrix(A_iota, "Iota")

if __name__ == "__main__":
    sha3_round_1_matrices()
