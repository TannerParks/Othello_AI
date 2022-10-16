# This file exists to display some board functionality
# Erich Kramer 4/26/18
#
#
#


from Board import Board

x = Board(4, 4)

x.set_cell(1, 2, 'x')

x.set_cell(1, 3, 'B')

x.display()

y = x.cloneBoard()
y.display()
