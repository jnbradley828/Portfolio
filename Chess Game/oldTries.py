## A really complicated and ugly try to define legal moves. I think it needs more thought, might try a different solution.


# Work in progress Define a function to determine whether a move is legal by inputting a board, player turn, and proposed move.
def isLegal(board: Board, playerTurn, UCImove, lastMove = None):
    print(UCImove)
    moveFrom = UCImove[:2]
    moveTo = UCImove[2:]
    try:
        colorFromPiece = board.accessSquare(moveFrom).getOccupyingPiece().getColor()
    except:
        colorFromPiece = None
    try:
        colorToPiece = board.accessSquare(moveTo).getOccupyingPiece().getColor()
    except:
        colorToPiece = None

    # Case 1: The moving piece belongs to the wrong player or there is no piece on that square.
    if colorFromPiece != playerTurn:
        return (False, 'Moving piece belongs to wrong player, or there is no piece to move.')
    # Case 2: The moving piece is being moved to a square occupied by its own color piece.
    if colorFromPiece == colorToPiece:
        return (False, 'Moving piece is being moved to a square occupied by its own piece.')
    # Case 3: The proposed move is from or to 'out of bounds'.
    for character in UCImove:
        if character not in [str(i) for i in range(9)] and character not in ['a','b','c','d','e','f','g','h']:
            return (False, 'One of these squares is out of bounds.')

    # Case 4: The proposed piece does not move that way.
    # Some useful data for this part \/

    horizontalMovement = ord(moveTo[0]) - ord(moveFrom[0])
    verticalMovement = int(moveTo[1]) - int(moveFrom[1])
    fromPieceMovement = board.accessSquare(moveFrom).getOccupyingPiece().getDirectionMoves()
    fromPieceAttributes = board.accessSquare(moveFrom).getOccupyingPiece().getMoveAttributes()
    try:
        fromPieceHasMoved = board.accessSquare(moveFrom).getOccupyingPiece().getHasMoved()
    except:
        fromPieceHasMoved = None

    def betweenSquares(moveFrom, moveTo, verticalMovement, horizontalMovement):
        intermediateSquare = moveFrom
        try:
            horiDirection = abs(horizontalMovement) // horizontalMovement
        except:
            horiDirection = 0
        try:
            vertDirection = abs(verticalMovement) // verticalMovement
        except:
            vertDirection = 0
        while intermediateSquare != moveTo:
            intermediateFile = chr(ord(intermediateSquare[0]) + vertDirection)
            intermediateRank = str(int(intermediateSquare[1]) + horiDirection)
            intermediateSquare = ''.join(intermediateFile + intermediateRank)
            if board.accessSquare(intermediateSquare).getOccupyingPiece() is not None and intermediateSquare != moveTo:
                return True
    # Work in Progress 4a. Piece moved in wrong direction.

    # 4a1. Queen moved off path.
    if 'all' in fromPieceMovement and 'multiple' in fromPieceAttributes:
        if horizontalMovement != 0 and verticalMovement != 0:
            if horizontalMovement != verticalMovement:
                return (False, 'This queen moved off path.')
    # 4a2. Rook moved off path.
    if 'cardinal' in fromPieceMovement and 'multiple' in fromPieceAttributes:
        if horizontalMovement != 0 and verticalMovement != 0:
            return (False, 'This rook moved off path.')
    # 4a3. Bishop moved off path.
    if 'diagonal' in fromPieceMovement and 'multiple' in fromPieceAttributes:
        if abs(horizontalMovement) != abs(verticalMovement):
            return (False, 'This bishop moved off path.')
    # 4a4. Knight moved off path.
    if '2x1' in fromPieceMovement:
        if not abs(horizontalMovement*verticalMovement) == 2:
            return (False, 'This knight moved off path.')

    # 4a5. Pawn moved off path pt 1. - backwards moves
    if 'forward' in fromPieceMovement:
        if verticalMovement < 1:
            return (False, 'This pawn moved off path.')
    if 'backward' in fromPieceMovement:
        if verticalMovement > -1:
            return (False, 'This pawn moved off path.')

    # 4a6. Pawn moved off path pt 2. - illegal diagonal moves
    # We need to make an exception for en passant.

    try:
        lastMoveFrom = lastMove[:2]
        lastMoveTo = lastMove[2:]
        lastMovePiece = board.accessSquare(lastMoveTo).getOccupyingPiece()
    except:
        lastMoveFrom = lastMoveTo = lastMovePiece = None
    def enPassantSquare(lastMoveFrom, lastMoveTo, lastMovePiece):
        if lastMoveFrom == None or lastMovePiece not in ['p', 'P']:
            return None
        else:
            horizontalMovement = ord(lastMoveTo[0]) - ord(lastMoveFrom[0])
            verticalMovement = int(lastMoveTo[1]) - int(lastMoveFrom[1])
            if horizontalMovement == 0 and abs(verticalMovement) == 2:
                print(f'{lastMoveTo[0]}{int(lastMoveTo[1])-(verticalMovement//2)}')
                return board.accessSquare(f'{lastMoveTo[0]}{int(lastMoveTo[1])-(verticalMovement//2)}')

    #back to the path-finding.
    if 'forward' in fromPieceMovement or 'backward' in fromPieceMovement:
        if abs(verticalMovement*horizontalMovement) == 1 and colorToPiece is None and enPassantSquare(lastMoveFrom, lastMoveTo, lastMovePiece) == moveTo:
            return (False, 'This pawn moved off path.')
        if abs(verticalMovement*horizontalMovement) == 0 and colorToPiece is not None:
            return (False, 'This pawn moved off path.')

    # 4b. Single-square moving piece moved too far, includes case for pawn's first move and castling.
    if 'single' in fromPieceAttributes and ( ('two squares first' not in fromPieceAttributes) or (fromPieceHasMoved is True) ):
        if abs(horizontalMovement) > 1 or abs(verticalMovement) > 1:
            if 'castle' not in fromPieceAttributes:
                return (False, 'This piece can only move 1 square at a time.')
            elif 'castle' in fromPieceAttributes:
                if betweenSquares(moveFrom, moveTo) is True or fromPieceHasMoved is True:
                    return (False, 'Castling is not allowed now.')
    if 'single' in fromPieceAttributes and 'two squares first' in fromPieceAttributes and fromPieceHasMoved is False:
            if abs(horizontalMovement) > 1 or abs(verticalMovement) > 2:
                return (False, 'This piece can only move 1 or 2 squares at a time.')

    # Work in Progress 4c. Non-jumping piece ran into something.
    # Need a function that finds squares in between the from and to squares.

    if 'jump' not in fromPieceAttributes and 'single' not in fromPieceMovement:
        if betweenSquares(moveFrom, moveTo, verticalMovement, horizontalMovement) is True:
            return (False, 'There is a piece in the way')

    return True


rankMap = {idx: range(8, 0, -1)[idx] for idx in (range(8))}
fileMap = {idx: chr(ord('a') + idx) for idx in range(8)}