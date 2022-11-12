import glob, os

time_data_basic = {}
time_data_efficient = {}
memory_data_basic = {}
memory_data_efficient = {}

def read_data_from_file(filename) -> (str, str, float, float):
  f = open(filename, 'r')
  f.readline() # cost of alignment, throw it away
  x = f.readline()
  x = x.replace('_', '')
  y = f.readline()
  y = y.replace('_', '')
  running_time = float(f.readline())
  memory_usage = float(f.readline())
  return (x, y, running_time, memory_usage)

def main():
  print("Plot data")
  
  # Open each output file
  path = './out_basic'
  for filename in sorted(glob.glob(os.path.join(path, 'out_in*.txt'))):  # for each file 'input*.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
      # Read time data and add to time data dictionary
      results = read_data_from_file(filename)
      x = results[0]
      y = results[1]
      time_data_basic[(x, y)] = results[2]
      memory_data_basic[(x, y)] = results[3]
  
  path = './out_efficient'
  for filename in sorted(glob.glob(os.path.join(path, 'out_in*.txt'))):  # for each file 'input*.txt'
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
      # Read memory data and add to memory data dictionary
      results = read_data_from_file(filename)
      x = results[0]
      y = results[1]
      time_data_efficient[(x, y)] = results[2]
      memory_data_efficient[(x, y)] = results[3]
  
  keys = list(time_data_efficient.keys())
  keys.sort(key=lambda t: len(t[0]) + len(t[1]))
  
  # Time plot data points
  print("Time data:")
  for k in keys:
    m = len(k[0])
    n = len(k[1])
    print(m + n, ",", time_data_basic[k], ",", time_data_efficient[k]) 

  print("Memory data:")
  # Memory plot data points
  for k in keys:
    m = len(k[0])
    n = len(k[1])
    print(m + n, ",", memory_data_basic[k], ",", memory_data_efficient[k]) 

main()

