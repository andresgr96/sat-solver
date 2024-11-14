# Sat-solver
Repository for the SAT solver project for the Knowledge &amp; Representation Class

## DIMACS Format
DIMACS CNF is a textual format. Any line that begins with the character c is considered a comment. Some other parsers require comments to start with c and/or support comments only at the beginning of a file. Varisat supports them anywhere in the file.

A DIMACS file begins with a header line of the form p cnf variables clauses. Where variables and clauses are replaced with decimal numbers indicating the number of variables and clauses in the formula.

Varisat does not require a header line. If it is missing, it will infer the number of clauses and variables. If a header line is present, though, the formula must have the exact number of clauses and may not use variables represented by a number larger than indicated.

Following the header line are the clauses of the formula. The clauses are encoded as a sequence of decimal numbers separated by spaces and newlines. For each clause the contained literals are listed followed by a 0. Usually each clause is listed on a separate line, using spaces between each of the literals and the final zero. Sometimes long clauses use multiple lines. Varisat will accept any combination of spaces and newlines as separators, including multiple clauses on the same line.

As an example the formula (x ∨ y ∨ ¬z) ∧ (¬y ∨ z) could be encoded as this:
```
p cnf 3 2
1 2 -3 0
-2 3 0
```
