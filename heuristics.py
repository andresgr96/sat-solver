from collections import defaultdict

# Jersolow-Wang method
def jersolow_wang_method(cnf):
  literal_weight = defaultdict(int)
  for clause in cnf:
    for literal in clause:
      literal_weight[literal] += 2 ** -len(clause)
  return max(literal_weight, key=literal_weight.get)

# Jersolow-Wang 2-sided method (consider only positive literals)
# this is faster by 50% relative improvement in speed
# ref: http://www.cril.univ-artois.fr/~coste/Articles/coste-etal-sat05.pdf
def jersolow_wang_2_sided_method(cnf):
  literal_weight = defaultdict(int)
  for clause in cnf:
    for literal in clause:
      literal_weight[abs(literal)] += 2 ** -len(clause)
  return max(literal_weight, key=literal_weight.get)

