import processfile

# Global variables:
# Create table of mismatched-alignment penalties for A, C, G, T
alpha = {('A','A'): 0, ('A','C'): 110, ('A','G'): 48, ('A','T'): 94,
         ('C','A'): 110, ('C','C'): 0, ('C','G'): 118, ('C','T'): 48,
         ('G','A'): 48, ('G','C'): 118, ('G','G'): 0, ('G','T'): 110,
         ('T','A'): 94, ('T','C'): 48, ('T','G'): 110, ('T','T'): 0 }
# Create gap penalty delta
delta = 30

# bottom-up pass to reconstruct the two sequence aligned strings (with gaps)
def reconstruct_solution():
    print('test')

# given s1 of length m, s2 of length n
# find the minimum cost of aligning the two strings
def basic_dp_alg(s1, s2):
    # Fill in table of size (m+1)x(n+1)
    m, n = len(s1), len(s2)
    T = [[0 for _ in range(n+1)] for _ in range(m+1)] # m+1 = number of rows, n+1 = number of cols

    # Fill in base cases
    for i in range(m+1):
        T[i][0] = i * delta
    for j in range(n+1):
        T[0][j] = j * delta

    # Fill in recursive cases
    for i in range(1, m+1):
        for j in range(1, n+1):
            T[i][j] = min(T[i-1][j-1] + alpha[(s1[i-1], s2[j-1])], T[i-1][j] + delta, T[i][j-1] + delta) # double check if alpha[s1[i-1], [j-1]] is correct

    # Return solution
    return(T[m][n])

def main():
    # Read in input files and get the pair of strings to match
    data = processfile.main()
    strings = data[0]
    outfile_data = data[1]

    # test string
    #basic_dp_alg('ACTG', 'ACGT')

    # process first string in the test file 'input1.txt'
    #basic_dp_alg(strings[0][0], strings[0][1])

    # process all strings in the test files and check the value of opt solution is correct
    for i,s in enumerate(strings):
        #print(s)
        value_of_soln = basic_dp_alg(s[0], s[1])
        # check that the value is correct by comparing it with the data in the outfile
        print(value_of_soln, outfile_data[i][0])
        assert(value_of_soln == outfile_data[i][0])

main()