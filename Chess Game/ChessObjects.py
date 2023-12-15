# Use an object-oriented approach to creating a playable chess board, with no chess packages.

# A piece class with subclasses for each piece, storing color and movement data.
class Piece:
    def __init__(self, color):
        while True:
            if color == 'white' or 'black':
                self.color = color
                break
            else:
                color = input('Invalid color. Please enter "white" or "black": ')
        self.hasMoved = False

    def __str__(self):
        if self.color == 'white':
            return self.singleLetterRep.upper()
        elif self.color == 'black':
            return self.singleLetterRep.lower()

    def getColor(self):
        return self.color
    def getHasMoved(self):
        return self.hasMoved
    def markAsMoved(self):
        self.hasMoved = True
    
class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'k'
class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'q'
class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'r'
class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'b'
class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'n'
class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.singleLetterRep = 'p'

# A square class that has file, rank, color, and occupation data.
class Square:
    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

        fileMap = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        if (fileMap[file] % 2 == 0 and rank % 2 == 0) or (fileMap[file] % 2 != 0 and rank % 2 != 0):
            self.color = 'dark'
        else:
            self.color = 'light'
        
        self.occupyingPiece = None
        
    def getFile(self):
        return self.file
    def getRank(self):
        return self.rank
    def getColor(self):
        return self.color
    def getOccupyingPiece(self):
        return self.occupyingPiece

    def addPiece(self, piece):
        self.occupyingPiece = piece
    def removePiece(self):
        self.occupyingPiece = None

    def __str__(self):
        if self.occupyingPiece is None:
            return'[ ]'
        else:
            return f'[{self.occupyingPiece}]'

# Board class that can have variable size and starting data.
class Board:
    def __init__(self, fen = 'standard'):
        #Initialize all of the squares.
        self.squares = []
        for rank in range(1,9):
            for file in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                self.squares.append(Square(file, rank))

        #Initialize all pieces based on fen and add them to squares.
        if fen == 'standard':
            self.startingPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        elif fen == 'empty':
            self.startingPosition = '8/8/8/8/8/8/8/8'
        else:
            self.startingPosition = fen

        fenFormat1 = list(reversed(self.startingPosition.split('/')))
        fenFormat1 = ''.join(fenFormat1)

        fenFormat2 = []
        for character in fenFormat1:
            try:
                numBlanks = int(character)
                for i in range(numBlanks):
                    fenFormat2.append(' ')
            except:
                fenFormat2.append(character)

        #Finally, time to assign pieces to each square.

        pieceMap = {'k': King, 'q': Queen, 'r': Rook, 'n': Knight, 'b': Bishop,
                    'p': Pawn}

        for square, pieceLetter in zip(self.squares, fenFormat2):
            if pieceLetter == ' ':
                continue
            elif pieceLetter.isupper():
                square.addPiece( pieceMap[pieceLetter.lower()](color = 'white') )
            elif pieceLetter.islower():
                square.addPiece( pieceMap[pieceLetter.lower()](color = 'black') )

    # Method that maps a square location input (ie. e1 or f7) to its correct square object.
    # This could be used to edit a board using Board.accessSquare('piece_coordinate').addPiece()
    def accessSquare(self, position):
        fileMap = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        coordinate = [character for character in position]
        rankMultiplier = int(coordinate[1]) - 1
        fileAdder = fileMap[coordinate[0]]
        squaresIdx = (8 * rankMultiplier) + fileAdder
        return self.squares[squaresIdx]

    def __str__(self):
        boardList = []
        for rank in range(8, 0, -1):
            thisRankList = []

            for square in self.squares:
                if square.getRank() == rank:
                    thisRankList.append(str(square))

            thisRankList.append('\n')
            for square in thisRankList:
                boardList.append(square)

        boardStr = ''.join(boardList)

        return boardStr

class chessGame:
    def __init__(self, board, toMove = 'white'):
        self.board = board
        self.toMove = toMove
        self.firstMove = toMove
        self.movesList = []

    def getTurn(self):
        return self.toMove
    def getMoves(self):
        movesStrList = []
        if self.firstMove == 'white':
            startingIdx = 0
        else:
            movesStrList.append(f'1. ?, {self.movesList[0]}')
            startingIdx = 1

        for index, move in enumerate(self.movesList[startingIdx:]):
            thisAppend = []
            if index % 2 == 0:
                thisAppend.append(f'1. {move}, ')
            else:
                thisAppend.append(f'{move}\n')
            movesStrList.append(''.join(thisAppend))
        return ''.join(movesStrList)


    def move(self, UCImove):
        fromSquare = UCImove[:2]
        toSquare = UCImove[2:4] # Important note: fromSquare and toSquare are the strings (ie. 'e4'), not objects...
        promotionChoice = UCImove[4] if len(UCImove) == 5 else None
        fromPiece = self.board.accessSquare(fromSquare).getOccupyingPiece()
        toPiece = self.board.accessSquare(toSquare).getOccupyingPiece()     # ...while fromPiece & toPiece are piece objects.

        #To check legality, we need to process distance moved data.
        xMovement = ord(toSquare[0]) - ord(fromSquare[0])
        yMovement = int(toSquare[1]) - int(fromSquare[1])

        # To check legality, we also need to check if there are pieces in between the from and to squares.
        # True means that there is a piece between the to and from squares.
        def checkBetweenSquares():
            deltax = xMovement // abs(xMovement) if xMovement != 0 else 0
            deltay = yMovement // abs(yMovement) if yMovement != 0 else 0
            numSquares = max((xMovement), abs(yMovement))
            for i in range(1, numSquares):
                newFile = chr(ord(fromSquare[0]) + (i*deltax))
                newRank = int(fromSquare[1]) + (i*deltay)
                if self.board.accessSquare(f'{newFile}{newRank}').getOccupyingPiece() is not None:
                    return True
            return False

        def checkLegality():
            fromPieceString = f'{fromPiece}'.lower()

            if all(Rulebook[fromPieceString]) and all(Rulebook['general']):
                return True
            else:
                return False

        Rulebook = {
            'general':[
                fromPiece.getColor() == self.getTurn(),
                (toPiece is None) or (fromPiece.getColor() != toPiece.getColor()),   # Cannot capture your own piece.
                isinstance(fromPiece, Knight) or not checkBetweenSquares(),     # Cannot jump over pieces unless you move a knight.
            ],
            'k': [
                (abs(xMovement) < 2 and abs(yMovement) < 2) or (    # King can't move more than 1 square unless castling...
                    not fromPiece.getHasMoved() and  # ...which means the King hasn't moved,
                    yMovement == 0 and abs(xMovement) == 2 and (    # ... the King is moving 2 spaces left or right,
                        (
                            xMovement > 0 and  # King is moving right,
                            isinstance(self.board.accessSquare(f'{chr(ord(fromSquare[0]) + 3)}{fromSquare[1]}').getOccupyingPiece(), Rook) and  # Rook is on h file,
                            not self.board.accessSquare(f'{chr(ord(fromSquare[0]) + 3)}{fromSquare[1]}').getOccupyingPiece().getHasMoved()  # Rook on h file hasn't moved.
                        ) or
                        (
                            xMovement < 0 and # King is moving left,
                            isinstance(self.board.accessSquare(f'{chr(ord(fromSquare[0]) - 4)}{fromSquare[1]}').getOccupyingPiece(), Rook) and  # Rook is on a file,
                            not self.board.accessSquare(f'{chr(ord(fromSquare[0]) - 4)}{fromSquare[1]}').getOccupyingPiece().getHasMoved()  # Rook on a file hasn't moved.

                        )
                    )
                )
                ],
            'q': [
                (abs(xMovement) == abs(yMovement)) or (xMovement == 0 or yMovement == 0),    # Diagonal or horizontal/vertical moves
            ],
            'r': [
                xMovement == 0 or yMovement == 0,    # Horizontal/vertical moves only
            ],
            'n': [
                abs(xMovement*yMovement) == 2 and max(abs(xMovement), abs(yMovement)) == 2,  # 'L' moves only
            ],
            'b': [
                abs(xMovement) == abs(yMovement),    # Diagonal moves only
            ],
            'p': [
                (fromPiece.getColor() == 'white' and yMovement > 0) or (fromPiece.getColor() == 'black' and yMovement < 0), # White pawns go forward, black pawns go backwards.
                abs(yMovement) == 1 or (abs(yMovement) == 2 and not fromPiece.getHasMoved()),    # Pawn moves 1 square unless it has not moved yet.
                abs(xMovement) * abs(yMovement) == 0 or (abs(xMovement) * abs(yMovement) == 1 and self.board.accessSquare(toSquare).getOccupyingPiece() is not None)    # Pawn only moves diagonally when capturing.
            ],
            'none':[
                False   # Cannot move from an empty square
            ]
        }

        if checkLegality() is True:
            movingPiece = self.board.accessSquare(fromSquare).getOccupyingPiece()


            if isinstance(movingPiece, King) and abs(xMovement) == 2:   # Must move rook if castling is played.
                oldRookSquare = f'{chr(ord(fromSquare[0]) + 3)}{fromSquare[1]}' if xMovement > 0 else f'{chr(ord(fromSquare[0]) - 4)}{fromSquare[1]}'
                movingRook = self.board.accessSquare(oldRookSquare).getOccupyingPiece() if xMovement > 0 else self.board.accessSquare(oldRookSquare).getOccupyingPiece()
                # obnoxious code to find the moving rook if we castle.
                newRookSquare = f'{chr(ord(toSquare[0]) - 1)}{fromSquare[1]}' if xMovement > 0 else f'{chr(ord(toSquare[0]) + 1)}{fromSquare[1]}'
                movingRook.markAsMoved()
                self.board.accessSquare(newRookSquare).addPiece(movingRook)
                self.board.accessSquare(oldRookSquare).removePiece()

            movingPiece.markAsMoved()  # Move a piece, add move to move list, and mark piece as moved.
            self.board.accessSquare(toSquare).addPiece(movingPiece)
            self.board.accessSquare(fromSquare).removePiece()
            self.movesList.append(UCImove)

            if isinstance(movingPiece, Pawn) and toSquare[1] == '8':    # Must turn pawn into different piece if it reaches the 8th rank
                promotionPieceMap = {'q': Queen, 'r': Rook, 'n': Knight, 'b': Bishop}
                if promotionChoice is not None:
                    self.board.accessSquare(toSquare).addPiece(promotionPieceMap[promotionChoice](color = fromPiece.getColor()))

            if self.toMove == 'white':  # Change the turn.
                self.toMove = 'black'
            elif self.toMove == 'black':
                self.toMove = 'white'
        else:
            raise RuntimeError('This is not a legal move.')

# Testing it out
board1 = Board('standard')
print(board1)

game1 = chessGame(board1)

game1.move('e2e4')
game1.move('e7e5')
game1.move('g1f3')
game1.move('b8c6')
game1.move('f1e2')
game1.move('d7d6')
game1.move('e1g1')
game1.move('c8d7')
game1.move('a2a3')
game1.move('d8e7')
game1.move('b1c3')
game1.move('e8c8')
game1.move('e2a6')
game1.move('b7a6')
board1.accessSquare('b7').addPiece(Pawn('white'))
game1.move('b7b8b')
print(board1)

print(game1.getMoves())