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


def mem_eff_DP(x, y):
  m = len(x)
  n = len(y)
  x = '#' + x
  y = '#' + y
  
  T_cur_col = [delta*i for i in range(0, n+1)]
  for i in range(1, m+1):
    T_prev_col = T_cur_col.copy()
    T_cur_col[0] = T_prev_col[0] + delta # Match x[i] with a gap (this is 0th row, and y[:0] has no chars)
    for j in range(1, n+1):
      T_cur_col[j] = min(T_prev_col[j-1] + alpha[(x[i], y[j])], T_cur_col[j-1] + delta, T_prev_col[j] + delta)

  return T_cur_col

# memory efficient divide and conquer algorithm
# which contains dp algorithm in the divide step
# x, y are the two strings to compare
def div_and_conquer(x, y):
    m = len(x)
    n = len(y)
    # Combine Step (Step 0)
    if m == 0:
        return (delta*n, "_"*n, y)
    if n == 0:
        return (delta*m, x, "_"*m)
    if m == 1:
      # x may have 1 char that matches a char in y, fill rest of y with gaps
      # or x may not match anything in y
      # check cheapest option (match x with something in y, or do not and use gaps)
      min_cost_alignment = (999999999999, None, None) # cost, x alignment, y alignment
      for i in range(n):
        # cost of matching single character x with all possibilities in y
        cost = delta * (n-1) + alpha[(x, y[i])]
        x_alignment = "_"*i + x + "_"*(n-1-i) # first string alignment
        y_alignment = y                       # second string alignment
        if cost <= min_cost_alignment[0]:
          min_cost_alignment = (cost, x_alignment, y_alignment)
      # Check special case of not matching x with any character of y 
      # cost = all of y is a gap, and the one character of x is a gap (+1 gap)
      cost = delta * n + delta 
      # check that cost of not matching x with any character in y is cheaper
      if (cost < min_cost_alignment[0]): 
        min_cost_alignment = (cost, x + "_"*n, "_"+y)
      return min_cost_alignment

    if n == 1: 
      # y may have 1 char that matches a char in x, fill in rest of x with gaps
      # or y may not match anything in x
      # check cheapest option (match y with something in x or do not, and use gaps)
      min_cost_alignment = (999999999999, None, None)
      for i in range(m):
        # cost of matching single character y with all possibilities in x
        cost = delta * (m-1) + alpha[(x[i], y)]
        y_alignment = "_"*i + y + "_"*(m-1-i) # single character in y matched with x
        x_alignment = x                          
        if cost <= min_cost_alignment[0]:
          min_cost_alignment = (cost, x_alignment, y_alignment)
      # Check special case of not matching y with any character of x
      # cost = all of x is a gap, and the one character of y is a gap (+1 gap)
      cost = delta * m + delta 
      # check that cost of not matching y with any character in x is cheaper
      if (cost < min_cost_alignment[0]): 
        min_cost_alignment = (cost, "_"+x, y + "_"*m) 
      return min_cost_alignment
            
    # Conquer Step
    # Here we find the partition into halves y_left, y_right
    # that match with the left and right halves of x in an optimal alignment

    #1. Do the DP for table1
    T1 = mem_eff_DP(x[:m//2], y)
    #2. Do the DP for table2
    T2 = mem_eff_DP(x[m//2:][::-1], y[::-1])

    # Find a min cost matching of first and second halves of x with portions
    # of y
    min_cost = 9999999999999999 # don't think we can use math.inf since
                                # no libraries allowed to help with solution, min cost of the split
    min_cost_i = 0 # index of the min cost split point
    for i in range(0, n+1):
      # cost = 
      #        ith row in final col of table 1
      #        + (n-i)th row in final col of table2
      # optimal split point is at i
      cost = T1[i] + T2[n-i]
      if cost < min_cost:
        min_cost = cost
        min_cost_i = i

    # Split Y into portions matched with first and second halves of x
    # in an optimal (i.e. min cost) matching
    y_l = y[:min_cost_i]
    y_r = y[min_cost_i:]

    # Divide Step (Steps 2-4)
    x_align_info = div_and_conquer(x[:m//2], y_l) # left alignment info
    y_align_info = div_and_conquer(x[m//2:], y_r) # right alignment info
    assert(min_cost == x_align_info[0] + y_align_info[0])
    return (min_cost, x_align_info[1] + y_align_info[1], x_align_info[2] + y_align_info[2])


  
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
  soln = div_and_conquer(s1, s2)
  end_time = time.time()
  running_time = (end_time - start_time)*1000 # milliseconds

  process = psutil.Process()
  memory_info = process.memory_info()
  memory_usage = int(memory_info.rss/1024) # in KB
  
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