def parse_dimacs(filename):
  clauses = []
  with open(filename, 'r') as input_file:
    for line in input_file:
      if line[0] in ['c', 'p']:
        continue
      literals = list(map(int, line.split()))
      assert literals[-1] == 0
      literals = literals[:-1]
      clauses.append(literals)
  return clauses