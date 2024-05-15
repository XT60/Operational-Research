corner_perms = ["F R U' R' U' R U R' F' R U R' U' R' F R F'",
                "R U R' U' R' F R2 U' R' U' R U R' F'",
                "x L2 D2 L' U' L D2 L' U L'",
                "x' L2 D2 L U L' D2 L U' L",
                "R U R' F' R U R' U' R' F R2 U' R'",
                "x' L' U L D' L' U' L D L' U' L D' L' U L D",
                "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
                "R' U R' U' y R' F' R2 U' R' U R' F R F",
                "R' U' R U R' U' R U L R' U' R U R' U' R U L R' U' R U R' U' R U L2",
                "R U' R' U R U' R' U L R U' R' U R U' R' U L R U' R' U R U' R' U L2",
                "R' U' R U R' U' R U L2 R' U' R U R' U' R U R' U' R U R' U' R U L2",
                "R U' R' U R U' R' U L2 R U' R' U R U' R' U R U' R' U R U' R' U L2",
                "R U' R' U R U' R' U L R U' R' U R U' R' U R U' R' U R U' R' U L'",
                "R U' R' U R U' R' U R U' R' U R U' R' U L R U' R' U R U' R' U L'"]
edge_perms = ["M2 U M2 U2 M2 U M2",
              "M2 U' M U2 M' U' M2",
              "R U' R U R U R U' R' U' R2",
              "R2 U R U R' U' R' U' R' U R'",
              "M' U M2 U M2 U M' U2 M2"]

moves = ['F', 'R', 'U', 'B', 'L', 'D', 'M', 'E', 'S', 'x', 'y', 'z']
directions = ['', "'", '2']
viable_moves = [move + direction for move in moves for direction in directions]


def translate_moves(move_history):
    """
    Translates a sequence of indexed or shorthand moves into standard Rubik's Cube notation.

    This method processes a list of move entries where each move can be either a direct cube move notation or an index
    pointing to predefined complex permutations for corners and edges. The complex permutations are indexed to simplify
    notation and stored in predefined lists (`corner_perms` and `edge_perms`).

    Args:
        move_history (list of str): A list containing move notations and indices. Indices are expected to be prefixed with
                                    'Corners' or 'Edges' to indicate which set of predefined permutations to use.

    Returns:
        string: String where each substring seperated by a space is a move in standard Rubik's Cube notation. This expanded list translates
              complex indexed moves into a sequence of basic moves as defined in the `corner_perms` and `edge_perms` arrays.

    """
    translated_moves = []
    for move in move_history:
        if 'Corners' in move:
            index = int(move.split('_')[0])
            translated_moves.append(corner_perms[index])
        elif 'Edges' in move:
            index = int(move.split('_')[0])
            translated_moves.append(edge_perms[index])
        else:
            translated_moves.append(move)
    return " ".join(translated_moves).split(" ")


def reverse_moves(moves):
    """
        Reverses a sequence of cube moves, effectively inverting the sequence to undo the moves.

        This method takes a string of moves, splits them into individual move components, reverses the order,
        and then inverts each move. The inversion is based on the following:
        - A move with an apostrophe (') indicates a counter-clockwise move, which is inverted to a clockwise move.
        - A move with a '2' remains unchanged since a double move (180 degrees) is its own inverse.
        - Any other move is assumed to be clockwise and is inverted to a counter-clockwise move by appending an apostrophe.

        Args:
            moves (str): A string containing a sequence of moves, separated by spaces (e.g., "R U R' U'").

        Returns:
            str: A string containing the reversed and inverted move sequence, ready to be applied to a cube to undo the original sequence.
        """
    move_list = moves.strip().split()
    reversed_moves = move_list[::-1]
    inverted_moves = []
    for move in reversed_moves:
        if "'" in move:
            inverted_moves.append(move.replace("'", ""))
        elif "2" in move:
            inverted_moves.append(move)
        else:
            inverted_moves.append(move + "'")
    return ' '.join(inverted_moves)
