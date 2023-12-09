# Use an object-oriented approach to creating a playable chess board, with no chess packages.

class Piece:
    def __init__(self, color, starting_position, board = None):
        self.color = color
        self.position = starting_position
        self.board = board
        self.LegalMoves = None

    def getLegalMoves(self):
        return self.LegalMoves
    def getBoard(self):
        return self.board
    def getPosition(self):
        return self.position
    def getColor(self):
        return self.color

    def addToBoard(self, boardName):
        self.board = boardName

class King(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        self.LegalMoves = ['N', 'E', 'S', 'W', 'NE', 'SE', 'NW', 'SW']

class Queen(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        self.LegalMoves = ['N', 'E', 'S', 'W', 'NE', 'SE', 'NW', 'SW']

class Rook(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        self.LegalMoves = ['N', 'E', 'S', 'W']

class Bishop(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        self.LegalMoves = ['NE', 'SE', 'NW', 'SW']

class Knight(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        self.LegalMoves = ['NNE', 'NNW', 'EEN', 'WWN', 'WWS', 'WWS', 'SSE', 'SSW']

class Pawn(Piece):
    def __init__(self, color, starting_position, board = None):
        Piece.__init__(self, color, starting_position, board)
        if self.color == 'white':
            self.LegalMoves = ['N', 'NE', 'NW']
        elif self.color == 'black':
            self.LegalMoves = ['S', 'SE', 'SW']
def fenParser(fen: str):
    fenSplit = fen.split('/')

    rankMap = {idx: range(8,0,-1)[idx] for idx in (range(8))}
    fileMap = {idx: chr(ord('a') + idx) for idx in range(8)}
    pieceMap = {'k': King, 'q': Queen, 'r': Rook, 'n': Knight, 'b': Bishop,
                'p': Pawn}
    boardPieces = []

    def fenColor(pieceLetter):
        if pieceLetter.isupper() is True:
            return 'white'
        elif pieceLetter.islower() is True:
            return 'black'

    for rankIdx, rank in enumerate(fenSplit):
        for fileIdx, piece in enumerate(rank):
            if piece.lower() in pieceMap:
                boardPieces.append(  pieceMap[piece.lower()](  color = fenColor(piece), starting_position= f'{fileMap[fileIdx]}{rankMap[rankIdx]}' )  )

    return boardPieces

class Board:
    def __init__(self, name, fen = 'standard'):
        if fen == 'standard':
            self.startingPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        else:
            self.startingPosition = fen
        self.name = name

        self.pieces = fenParser(self.startingPosition)
        for piece in self.pieces:
            piece.addToBoard(self.name)

    def getPieces(self):
        return self.pieces

##Testing
a = Board(name = 'my favorite board', fen = 'standard')
a_pieces = a.getPieces()

for piece in a_pieces:
    pieceType = type(piece).__name__
    pieceColor = piece.getColor()
    piecePosition = piece.getPosition()
    print(f'A {pieceColor} {pieceType} is on {piecePosition}')
