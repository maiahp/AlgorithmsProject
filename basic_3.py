#import processfile
import sys
from resource import *
import time
# Run `pip install psutil` on machine
import psutil

# Global variables:
# Create table of mismatched-alignment penalties for A, C, G, T
alpha = {
    ('A', 'A'): 0,
    ('A', 'C'): 110,
    ('A', 'G'): 48,
    ('A', 'T'): 94,
    ('C', 'A'): 110,
    ('C', 'C'): 0,
    ('C', 'G'): 118,
    ('C', 'T'): 48,
    ('G', 'A'): 48,
    ('G', 'C'): 118,
    ('G', 'G'): 0,
    ('G', 'T'): 110,
    ('T', 'A'): 94,
    ('T', 'C'): 48,
    ('T', 'G'): 110,
    ('T', 'T'): 0
}
# Create gap penalty delta
delta = 30


# bottom-up pass to reconstruct the two sequence aligned strings (with gaps)
def reconstruct_solution(T, s1, s2):
    i = len(s1)  # m
    j = len(s2)  # n

    s1_alignment = []
    s2_alignment = []
    s1 = '#' + s1
    s2 = '#' + s2
    while (i, j) != (0, 0):
      if i == 0:  # no more characters of s1 case
        s1_alignment.append("_")
        s2_alignment.append(s2[j])
        j = j - 1
        continue
      elif j == 0:  # no more characters of s2 case
        s1_alignment.append(s1[i]) 
        s2_alignment.append("_")
        i = i - 1
        continue

      # Which of three options was used to determing T[cur]?
      option1 = T[i - 1][j - 1] + alpha[(s1[i], s2[j])]
      option2 = T[i - 1][j] + delta
      option3 = T[i][j - 1] + delta

      if T[i][j] == option1:
        # Aligning s1[i] and s2[j] is optimal (s1[i] and s2[j] are a pair)
        # the very last characters we look at are the end of the string
        s1_alignment.append(s1[i])
        s2_alignment.append(s2[j])
        # move to the cell in the table that was the opt solution to build i,j
        i = i - 1
        j = j - 1
      elif T[i][j] == option3:
        # s2[j-1] is matched with s1[i], so s2[j] is matched with a gap
        s1_alignment.append("_")
        s2_alignment.append(s2[j]) 
        # move to the cell in the table that was the opt solution to build i,j, i doesn't change
        j = j - 1
      elif T[i][j] == option2:
        # 2. Aligning s1[i-1] and s2[j] and putting a gap after s1[i-1]
        # s1[i-1] is matched with s2[j], so s1[i] is matched with gap
        s1_alignment.append(s1[i]) 
        s2_alignment.append("_")
        # move to the cell in the table that was the opt solution to build i,j, j doesn't change
        i = i - 1
      else:
        assert(False)

    #assert(len(s1_alignment) == len(s2_alignment))
    s1_alignment.reverse()
    s2_alignment.reverse()
    return ("".join(s1_alignment), "".join(s2_alignment))


# given s1 of length m, s2 of length n
# find the minimum cost of aligning the two strings
def basic_dp_alg(s1, s2):
    # Fill in table of size (m+1)x(n+1)
    m, n = len(s1), len(s2)
    T = [[0 for _ in range(n + 1)]
         for _ in range(m + 1)]  # m+1 = number of rows, n+1 = number of cols

    # Fill in base cases
    # T[i][0] refers to the first i characters of s1
    for i in range(m + 1):
        T[i][0] = i * delta

# T[0][j] refers to the first j characters of s2
    for j in range(n + 1):
        T[0][j] = j * delta

    # Fill in recursive cases
    s1 = '#' + s1  # if we add a char at the beginning, s[i] refers to ith character
    s2 = '#' + s2
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Take minimum of three (-indexed) things:
            # 1. Align s1[i] and s2[j]
            # 2. Aligning s1[i-1] and s2[j] and putting a gap after s1[i-1]
            # 3. Aligning s1[i] and s2[j-1] and putting a gap after s2[j-1]
            T[i][j] = min(
                T[i - 1][j - 1] + alpha[(s1[i], s2[j])], T[i - 1][j] + delta,
                T[i][j - 1] +
                delta)  # double check if alpha[s1[i-1], [j-1]] is correct

    # Return solution
    return (T)

def basic_dp_soln(s1, s2):
    T = basic_dp_alg(s1, s2)
    alignments = reconstruct_solution(T, s1, s2)
    return (T[-1][-1], alignments[0], alignments[1])

def main2():
    # Read in input files and get the pair of strings to match
    #data = processfile.main()
    data = []
    strings = data[0]
    outfile_data = data[1]

    # test string
    #basic_dp_alg('ACTG', 'ACGT')

    # process first string in the test file 'input1.txt'
    #basic_dp_alg(strings[0][0], strings[0][1])

    # process all strings in the test files and check the value of opt solution is correct
    for i, s in enumerate(strings):
        #print(s)
        soln = basic_dp_soln(s[0], s[1])
        # check that the value is correct by comparing it with the data in the outfile
        print(soln[0], outfile_data[i][0])
        assert (soln[0] == outfile_data[i][0])

        print(soln[1], soln[2])
        assert (soln[1] == outfile_data[i][1])
        assert (soln[2] == outfile_data[i][2])

      
# given the original string: s and the list: L
# construct and return s': a copy of s placed into s[L[0]]
# construct and return s'': a copy of s' placed into s'[L[1]]
# and so on, until we've iterated through all numbers in L array
def construct_string(s, L):
    for index in L:
        s = s[:index+1] + s + s[index+1:]
    return s


# take in the file given in the argument
# piece it into s1, L1, s2, L2
# L1, L2 are the digit lists used to construct the string
def process_inputfile(f):
    s, L = [], [[], []]  # s = [s1, s2], L = [L1, L2]
    count = -1
    for row in f:
        row = row if row[-1] != '\n' else row[:len(row) - 1]
        if row.isdigit():                    # if we have a digit (ignore \n)
            L[count].append(int(row))
        else:                                # otherwise we must have a string of len greater than 0
            count += 1
            s.append(row)     # append the string without \n
    return (s, L)

def main():
  # Get command-line arguments
  assert(len(sys.argv) == 2 + 1)
  input_filename = sys.argv[1]
  output_filename = sys.argv[2]
  
  # Read in input from input file
  input_file = open(input_filename, 'r')
  s, L = process_inputfile(input_file)
  s1 = construct_string(s[0], L[0])
  s2 = construct_string(s[1], L[1])
  input_file.close()  

  # Run algorithm and measure it
  start_time = time.time()
  soln = basic_dp_soln(s1, s2)
  end_time = time.time()
  running_time = (end_time - start_time)*1000 # in ms

  process = psutil.Process()
  memory_info = process.memory_info()
  # https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info
  memory_usage = int(memory_info.rss/1024) # in kb 
  
  # Write output to output file:
  # 1. Cost of alignment (integer)
  # 2. First string alignment
  # 3. Second string alignment
  # 4. Time (in ms, float)
  # 5. Memory (in kb, float)
  output_file = open(output_filename, 'w')
  output_file.write(str(soln[0]) + '\n')
  output_file.write(str(soln[1]) + '\n')
  output_file.write(str(soln[2]) + '\n')
  output_file.write(str(running_time) + '\n')
  output_file.write(str(memory_usage))
  output_file.close() 

if __name__ == '__main__':
  main()
