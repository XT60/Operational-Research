import itertools

perms = [
    # permutes two edges: U face, bottom edge and right edge
    "F' L' B' R' U' R U' B L F R U R' U",
    "x L2 D2 L' U' L D2 L' U L'",
    "x' L2 D2 L U L' D2 L U' L",
    "x R2 F R F' R U2 r' U r U2",
    "R U R' F' R U R' U' R' F R2 U' R'",
    "R U R' U R U2 R'"
    #permutes two edges: U face, bottom edge and left edge
    "F R B L U L' U B' R' F' L' U' L U'",
    # permutes two corners: U face, bottom left and bottom right
    "U2 B U2 B' R2 F R' F' U2 F' U2 F R'",
    # # permutes three corners: U face, bottom left and top left
    # "U2 R U2 R' F2 L F' L' U2 L' U2 L F'",
    # # permutes three centers: F face, top, right, bottom
    # "U' B2 D2 L' F2 D2 B2 R' U'",
    # # permutes three centers: F face, top, right, left
    # "U B2 D2 R F2 D2 B2 L U",
    # U face: bottom edge <-> right edge, bottom right corner <-> top right corner
    # "D' R' D R2 U' R B2 L U' L' B2 U R2",
    # U face: bottom edge <-> right edge, bottom right corner <-> left right corner
    # "D L D' L2 U L' B2 R' U R B2 U' L2",
    # U face: top edge <-> bottom edge, bottom left corner <-> top right corner
    # "R' U L' U2 R U' L R' U L' U2 R U' L U'",
    # U face: top edge <-> bottom edge, bottom right corner <-> top left corner
    # "L U' R U2 L' U R' L U' R U2 L' U R' U",
    # permutes three corners: U face, bottom right, bottom left and top left
    # "F' U B U' F U B' U'",
    # permutes three corners: U face, bottom left, bottom right and top right
    "F U' B' U F' U' B U",
    # permutes three edges: F face bottom, F face top, B face top
    # "L' U2 L R' F2 R",
    # permutes three edges: F face top, B face top, B face bottom
    # "R' U2 R L' B2 L",
    # H permutation: U Face, swaps the edges horizontally and vertically
    "M2 U M2 U2 M2 U M2"
]


moves = ['F', 'R', 'U', 'B', 'L', 'D', 'x', 'y', 'z']
moves_xyz = ['x', 'y', 'z', '']
directions = ['', "'", '2']

viable_moves = [move + direction for move in moves for direction in directions]
print(viable_moves)
n = 3
pp = [' '.join(perm).strip() for perm in list(itertools.permutations(moves_xyz, n)) + list(itertools.permutations(moves_xyz, 1))]
viable_moves_xyz = [move + direction for move in pp for direction in directions][:-3]

print(viable_moves_xyz)

perms_all = [xyz + " " + p for xyz in viable_moves_xyz for p in perms]
print(perms_all)