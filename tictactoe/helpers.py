def empty_cells(board, EMPTY=None):
	return sum((row.count(EMPTY) for row in board))

