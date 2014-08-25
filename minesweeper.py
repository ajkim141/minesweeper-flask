# Alex Kim - Minesweeper
import atexit as _atexit
import random as _random
import sys as _sys


def render_board(game_board):
    # let's try to aim for something more like this:
    # 0 1 2 3 4 5 6
    # +-------------+
    # 0|O O O O O O O|
    # 1|O O O O O O O|
    # 2|O O O O O O O|
    # 3|O O O O O O O|
    # 4|O O O O O O O|
    # 5|O O O O O O O|
    # 6|O O O O O O O|
    # +-------------+

    # get the dimensions
    width = len(game_board[0])
    # add some white space
    print ""

    header_row = [str(i) for i in range(width)]
    print "  " + " ".join(header_row)
    boarder_row = [" +"] + (["-"] * (width * 2 - 1)) + ["+"]
    print "".join(boarder_row)

    for rn, row in enumerate(game_board):
        # let's make a list of the row's elements, along with it's boarders, to then join & print
        row_value = str(rn) + "|" + " ".join([render_tile(tile) for tile in row]) + "|"
        print row_value

    print "".join(boarder_row)
    print ""


def create_game_board(height, width, mines=None):
    """
    Create a gameboard of a specified size, with a specified number of mines
    :param height: number of rows -- 1 indexed
    :param width: number of columns -- 1 indexed
    :param mines: Optional number of mines to lay on the board. Default is 10%
    """
    # how many tiles the board needs
    num_tiles = height * width
    if not mines:
        mines = num_tiles / 10
    else:
        assert mines < num_tiles

    # each tile list has the meaning: [Visible (bool), Mine (bool), Adjacent Mines (int)]
    # THERE WAS A CRAZY BUG HERE! when multiplying lists, python doesn't create a copy, but instead passes by reference
    # this means if you change any of these lists, it affects the rest.
    # tiles = ([[False, True, 0]] * mines) + ([[False, False, 0]] * (num_tiles - mines))
    # Instead use this... these should not be references to the same list but instead independent lists.
    tiles = [[False, True, 0] for _ in range(mines)] + [[False, False, 0] for _ in range(num_tiles - mines)]

    # now randomize the list's order inplace, so we can just use pop() to take from the list. Right now, the list is all
    # mines first, then all non mines, which would be a bit too easy
    _random.shuffle(tiles)

    # initialize the board as an empty list
    game_board = list()

    for i in range(height):
        # pop() removes the end of the list and returns the value it removed to you
        # for _ in range(N) is the idiom for when you want to iterate N times but don't care about the iterators value
        # here, _ means "I don't give a shit what the value is"
        game_board.append([tiles.pop() for _ in range(width)])

    # update the board with the right number of neighboring mines
    for row_num in range(height):
        for col_num in range(width):
            neighboring_mines = len(get_neighbors(game_board, row_num, col_num, is_mine=True))
            game_board[row_num][col_num][2] = neighboring_mines

    return game_board


def get_neighbors(game_board, row_idx, col_idx, is_mine=None, is_visible=None):
    """
    for a given game board and tile location, get the neighbors without going out of bounds of the board
    :param game_board: the game board
    :param row_idx: row index number of the tile in question
    :param col_idx: column index number of the tile in question
    :param is_mine: mine state of returned neighbors
    :param is_visible: visible state of returned neighbors
    :returns list of lists [(row_idx, col_idx), tile value] for the neighbors
    """

    # bounds for where neighbors could be (min_row_num, max_row_num). You need to protect against this edge case:
    # [1,2,3,4][-1:1] --> []
    # the index method [list of things][start:finish:step] works here, but if fails when you start with a negative
    # and finish with a positive when you don't have a step that's negative.
    # the same issue doesn't exist for the finish > length case
    height = len(game_board) - 1
    width = len(game_board[0]) - 1
    row_min = row_idx - 1 if row_idx > 0 else 0
    row_max = row_idx + 1 if row_idx < height else height
    col_min = col_idx - 1 if col_idx > 0 else 0
    col_max = col_idx + 1 if col_idx < width else width

    neighbors = list()
    # now make the coordinates and get the values
    for row_num in range(row_min, row_max + 1):
        for col_num in range(col_min, col_max + 1):
            # get the tile in question
            tile = game_board[row_num][col_num]

            if not (row_num == row_idx and col_num == col_idx) \
                    and (tile[0] == is_visible or is_visible is None) \
                    and (tile[1] == is_mine or is_mine is None):
                # basically, just check the state of the tile. Don't append if:
                #   If we're on the central tile
                #   If it doesn't match what we wanted from the optionals
                # Otherwise append
                neighbors.append([(row_num, col_num), tile])

    return neighbors


def render_tile(tile):
    """
    For a given tile, render its character
    :param tile:
    :returns str value of tile
    """

    # each tile list has the meaning: [Visible (bool), Mine (bool), Adjacent Mines (int)]
    # visible, mine, adjacent_mines = tile

    if tile[0]:
        # if the tile is visible
        if tile[1]:
            # if the tile is a mine
            return "X"
        elif tile[2]:
            # if the tile has neighboring mines
            return str(tile[2])
        else:
            return " "
    else:
        return "+"


# Handle player input
def select_space(game_board):
    """
    Get user input for space selection
    :param game_board: Used for determining bounds of board
    :return: (row, col) location of selection
    """

    max_x = len(game_board[0]) - 1
    max_y = len(game_board) - 1

    row = verify_user_input("Enter Row:", lambda x: int(x), lambda x: 0 <= int(x) <= max_x)
    col = verify_user_input("Enter Column:", lambda x: int(x), lambda x: 0 <= int(x) <= max_y)

    game_on, game_board = update_board(game_board, row, col)
    return game_on, game_board


def verify_user_input(initial_prompt, cast_function, verify_function):
    """
    As this comes up a lot, script the asking the user for a valid input
    :param cast_function: cast input to required type
    :param initial_prompt: string phrase to initially ask
    :param verify_function: function used to verify input (returns bool)
    :return: valid input
    """
    thing = raw_input(initial_prompt)
    while True:
        try:
            valid_thing = cast_function(thing)
        except:
            # I know you're not supposed to do this, but I really don't care about the error type or message
            thing = raw_input("Invalid! Try Again:")
            continue

        if verify_function(valid_thing):
            return valid_thing


def update_board(game_board, row, col):
    """
    For a give tile selection, update the game board
    :param game_board: the game board
    :param row: user selected row
    :param col: user selected column
    :return: game_on, game_board
    """
    tile = game_board[row][col]
    if tile[1]:
        # Hit a mine -- unmask all mines and end the game
        for r in game_board:
            for c in r:
                if c[1]:
                    c[0] = True

        # set the game to over
        game_on = False
    else:
        # not a mine

        # unmask the selected one element
        tile[0] = True
        game_on = True

        if tile[2] == 0:
            #hit a blank space, unmask all the adjacent parts recursively
            game_board = pathfind(game_board, row, col)

    return game_on, game_board


def pathfind(game_board, row, col):
    """
    for a given starting point, traverse the board and unmask the appropriate elements
    :param game_board: the board
    :param start_x: starting row
    :param start_y: starting column
    :return: the updated board
    """
    # this is a list of all the elements that need to be checked -- only non-visible, non mines need to be checked...
    todo = [c for c in get_neighbors(game_board, row, col, is_mine=False, is_visible=False)]

    # set of all previously visited or queued tiles
    hist_coords = set([coords for coords, _ in todo])

    # loop while there are still some elements to check
    while todo:
        # grab the tile to be checked
        (row, col), tile = todo.pop(0)

        # this is made visible regardless of what it is (we know it's not a mine).
        # Leveraging pass by reference hard here
        tile[0] = True

        if tile[2] == 0:
            #this is a blank tile, so we need to check it's neighbors as well
            #the generated list is only new elements from searching at this location
            new_todo = [n for n in get_neighbors(game_board, row, col, is_mine=False, is_visible=False)
                        if n[0] not in hist_coords]

            #update the trackers with the new locations
            hist_coords.update([coords for coords, _ in new_todo])
            todo += new_todo

    return game_board


def generate_board():
    """
    Create a new game board by getting the user's inputs
    :return: game_on, game_board
    """
    rows = verify_user_input("Enter number of rows:", lambda x: int(x), lambda x: x > 1)
    cols = verify_user_input("Enter number of columns:", lambda x: int(x), lambda x: x > 1)
    mines = verify_user_input("Enter number of mines:", lambda x: int(x), lambda x: x > 0)

    game_on = True
    game_board = create_game_board(rows, cols, mines=mines)
    return game_on, game_board


def check_victory(game_board):
    """
    Check if the player has won -- loop through looking for masked non-mines
    :param game_board: the game board
    :returns: bool
    """

    for row in game_board:
        for is_visible, is_mine, _ in row:
            if not is_mine and not is_visible:
                # Still a masked tile that's not a mine left on the board
                return False

    # If we do the full loop, then they are a winner!
    return True


def run_game():
    """
    Run the game
    """
    while True:

        # Game test
        print "".join(["-"] * 11)
        print "Minesweeper"

        game_on, game_board = generate_board()
        if game_on:
            render_board(game_board)

        while game_on:
            game_on, game_board = select_space(game_board)
            render_board(game_board)

            if not game_on:
                print "Sorry, you lose!"
            elif check_victory(game_board):
                print "Congratulations, you win!"
                # end the game
                game_on = False

        # check if they would like to play again
        play_again = raw_input("Would you like to play again? [y]es/[n]o:").lower()

        while True:
            if play_again in {"y", "yes"}:
                break
            elif play_again in {"n", "no"}:
                _sys.exit(0)
            else:
                play_again = raw_input("Invalid selection! [y]es/[n]o:").lower()


@_atexit.register
def say_goodbye():
    print ""
    print "Thanks for playing"


if __name__ == "__main__":
    try:
        run_game()
    except KeyboardInterrupt:
        _sys.exit(0)

