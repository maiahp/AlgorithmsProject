import os, glob

# given the output file, returns the value of the match and the aligned strings s1' and s2'
def process_outputfile(f):
    data = []
    for row in f:
        row = row if row[-1] != '\n' else row[:len(row) - 1] # ignore newlines
        if row.isdigit():
            data.append(int(row))
        else:
            data.append(row)
    return data

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


# views all 'input*.txt' files in same directory and calls processing functions
def main():
    retval = None
    in_strings = [] # the constructed input strings to be given to the algorithms
    count = 0
    path = './SampleTestCases'

    # grab input files
    for filename in sorted(glob.glob(os.path.join(path, 'input*.txt'))):  # for each file 'input*.txt'
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            retval = process_inputfile(f)
            in_strings.append([]) # empty list to hold the pair of constructed strings
            for i in range(2):
                in_strings[count].append(construct_string(retval[0][i], retval[1][i]))
            count += 1

    # grab output files
    out_data = []
    for filename in sorted(glob.glob(os.path.join(path, 'output*.txt'))):  # for each file 'output*.txt'
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            retval = process_outputfile(f)
            out_data.append(retval)

    return (in_strings, out_data)

