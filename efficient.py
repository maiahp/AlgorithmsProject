

# memory efficient divide and conquer algorithm
# which contains dp algorithm in the divide step
# x, y are the two strings to compare
def div_and_conquer(x, y):
    # Combine Step
    if len(x) == 0:
        return ("_"*len(y), y)
    if len(y) == 0:
        return ("_"*len(x), x)
    if len(x) == 1:
        for i in range(y):
            if x[0] == y[i]:
                fsa = "_"*i + x[0] + "_"*(len(y)-1-i) # first string alignment
                ssa = y                               # second string alignment
                return (fsa, ssa)
    if len(y) == 1:
        for i in range(x):
            if y[0] == x[i]:
                fsa = x # first string alignment
                ssa = "_"*i + y[0] + "_"*(len(x)-1-i)
                return (fsa, ssa)

    # Conquer Step
    # Here we find the partition into halves y_left, y_right
    # that match with the left and right halves of x in an optimal alignment

    #1. Do the DP for table1
    #2. Do the DP for table2
    min_cost = 9999999999999999
    min_cost_i = 0
    for i in range(0, m+1):
        #cost = ith row in final col of table 1 + (m-i)th row in final col of table2 # optimal split point is at i
        #if cost < min_cost:
            #min_cost = cost
            #min_cost_i = i
    y_l = y[:i]
    y_r = y[i:]


    # Divide Step
    lai = div_and_conquer(x[:len(x)/2], y_l) # left alignment info
    rai = div_and_conquer(x[len(x)/2:], y_r) # right alignment info
    return (lai[0] + rai[0], lai[1] + rai[1])

