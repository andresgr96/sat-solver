# Sat-solver
Repository for the SAT solver project for the Knowledge &amp; Representation Class

## DIMACS Format
DIMACS CNF is a textual format. Any line that begins with the character c is considered a comment. Some other parsers require comments to start with c and/or support comments only at the beginning of a file. Varisat supports them anywhere in the file.

A DIMACS file begins with a header line of the form p cnf variables clauses. Where variables and clauses are replaced with decimal numbers indicating the number of variables and clauses in the formula.

Following the header line are the clauses of the formula. The clauses are encoded as a sequence of decimal numbers separated by spaces and newlines. For each clause the contained literals are listed followed by a 0. Usually each clause is listed on a separate line, using spaces between each of the literals and the final zero. Sometimes long clauses use multiple lines. Varisat will accept any combination of spaces and newlines as separators, including multiple clauses on the same line.

As an example the formula (X ∨ Y ∨ ¬Z) ∧ (¬Y ∨ Z) could be encoded as this:
```
p cnf 3 2
1 2 -3 0
-2 3 0
```

## Running the Solver

You can run the solver using the main file, specifying the two arguments  "--input_file" is the CNF in DIMACS format you wish to solve, and "--s" os the type of solver, where 1, 2 and 3 correspond to the basic solver with no heuristics, using Jersolow-Wang, and using Jersolow-Wang two sided herustics respectively. The data/examples folder contains 5 sudoku puzzles encoded in DIMACS which you can run for verification.

Example command:

```
python3 SAT.py --input_file "data/examples/sudoku1.cnf" --s 3
```
