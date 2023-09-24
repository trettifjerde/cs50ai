from generate import CrosswordCreator
from crossword import Crossword
import sys
from time import perf_counter

def print_vars(cc):
	for x in cc.domains:
		print(f"{x}. Words in domain: {len(cc.domains[x])}")
	print()

def main():
	if len(sys.argv) not in [3, 4]:
		sys.exit("Usage: python generate.py structure words [output]")

	structure = sys.argv[1]
	words = sys.argv[2]
	output = sys.argv[3] if len(sys.argv) == 4 else None

	crossword = Crossword(structure, words)
	c = CrosswordCreator(crossword)

	print("initialization")
	print_vars(c)

	c.enforce_node_consistency()
	print("node consistency enforced")
	print_vars(c)

	c.ac31()
	print("updated with ac3")
	print_vars(c)

main()
print(perf_counter())