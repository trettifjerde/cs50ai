import sys

from crossword import *

from collections import deque

from time import perf_counter as pc

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
        	for word in self.domains[var].copy():
        		if len(word) != var.length:
        			self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        xn, yn = self.crossword.overlaps[x, y]

        for wordX in self.domains[x].copy():
        	satisfies = False
        	for wordY in self.domains[y]:
        		if wordX[xn] == wordY[yn]:
        			satisfies = True
        	if not satisfies:
        		self.domains[x].remove(wordX)
        		revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
        	arcs = [(v1, v2) for v1, v2 in self.crossword.overlaps if self.crossword.overlaps[v1, v2] != None]
        while arcs:
            arc = arcs.pop()
            if self.revise(*arc):
            	if self.domains[arc[0]]:
            		arcs.extend((
            			(v3, v1) for v3, v1 in self.crossword.overlaps 
            			if self.crossword.overlaps[v3, v1]
            			and (v3, v1) not in arcs 
            			and v1 == arc[0] 
            			and v3 != arc[1]))
            	else:
            		return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
        	return True
        else:
        	return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var1 in assignment:
        	for var2 in assignment:
        		if var1 == var2:
        			continue
        		if assignment[var1] == assignment[var2]:
        			return False
        		overlap = self.crossword.overlaps[var1, var2]
        		if overlap and assignment[var1][overlap[0]] != assignment[var2][overlap[1]]:
        			return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = [neighbor for v, neighbor in self.crossword.overlaps 
        			if neighbor not in assignment and v == var and self.crossword.overlaps[v, neighbor]]

       	word_rules_out = []
        for word in self.domains[var]:
        	ruled_out = 0
        	for neighbor in neighbors:
        		overlap = self.crossword.overlaps[var, neighbor]
        		for nei_word in self.domains[neighbor]:
        			if word[overlap[0]] != nei_word[overlap[1]]:
        				ruled_out += 1
        	word_rules_out.append((word, ruled_out))

        order = deque(word[0] for word in sorted(word_rules_out, key=lambda word: word[1]))
        return order

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = {}
        for var in self.crossword.variables - assignment.keys():
            unassigned.setdefault(len(self.domains[var]), set()).add(var)
        fewest = unassigned[min(unassigned.keys())]
        if len(fewest) > 1:
            return max(fewest, key=lambda var: len(self.crossword.neighbors(var)))
        return fewest.pop()

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        new_var = self.select_unassigned_variable(assignment)
        new_var_words = self.order_domain_values(new_var, assignment)
        while new_var_words:
            new_assignment = assignment.copy()
            word = new_var_words.popleft()
            new_assignment[new_var] = word
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
    print(pc())
