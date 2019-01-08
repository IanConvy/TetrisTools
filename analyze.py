def test_piece(surface, piece, orient):
    seq = pieces[piece]['bottom'][orient]
    length = len(seq)
    positions = []
    if seq:
        for x in range(9 - length):
            test_seq = surface[x:(x + length)]
            if seq == test_seq:
                positions.append(x)
    else:
        positions = [0,1,2,3,4,5,6,7,8]
    return positions

def test_piece_bool(surface, piece, orient):
    seq = pieces[piece]['bottom'][orient]
    length = len(seq)
    check = False
    if seq:
        for x in range(9 - length):
            test_seq = surface[x:(x + length)]
            if seq == test_seq:
                check = True
                break
    else:
        check = True
    return check

def test_surface(surface):
    result = {}
    for piece in pieces.keys():
        result[piece] = {}
        for orient in pieces[piece]['top'].keys():
            result[piece][orient] = test_piece(surface, piece, orient)
    return result

def test_surface_bool(surface):
    result = {}
    for piece in pieces.keys():
        check = False
        for orient in pieces[piece]['top'].keys():
            if test_piece_bool(surface, piece, orient):
                check = True
                break
        result[piece] = check
    return result

def add_piece(surface, position, piece, orient):
    top = pieces[piece]['top'][orient]
    height = pieces[piece]['height'][orient]
    index = 0
    for y in range(len(top)):
        surface[position + index] = top[index]
        index += 1
    if position > 0:
        surface[position - 1] += height[0]
    if position < 8 - len(top):
        surface[position + len(top)] -= height[1]
    return surface

def connect_surface(surface):
    result = {}
    for piece in pieces.keys():
        result[piece] = []
        for orient in pieces[piece]['top'].keys():
            for position in test_piece(surface, piece, orient):
                result[piece].append(add_piece(surface.copy(), position, piece, orient))
    return result

def check_perfect(connections):
    perfect = True
    for piece in connections:
        if connections[piece] == []:
            perfect = False
    return perfect

pieces = {
    'lr': {
        'name': 'L-piece right',
        'top': {
            3 : [-2],
            0 : [0, 0],
            1 : [0],
            2 : [0, 1]
        },
        'bottom': {
            3 : [0],
            0 : [1, 0],
            1 : [-2],
            2 : [0, 0]
        },
        'height': {
            3 : [3, 1],
            0 : [2, 1],
            1 : [1, 3],
            2 : [1, 2]
        }
    },

    'll': {
        'name': 'L-piece left',
        'top': {
            1 : [2],
            2 : [-1, 0],
            3 : [0],
            0 : [0, 0]
        },
        'bottom': {
            1 : [0],
            2 : [0, 0],
            3 : [2],
            0 : [0, -1]
        },
        'height': {
            1 : [1, 3],
            2 : [2, 1],
            3 : [3, 1],
            0 : [1, 2]
        }
    },

    'sr': {
        'name': 'S-piece right',
        'top': {
            0 : [1, 0],
            1 : [-1]
        },
        'bottom': {
            0 : [0, 1],
            1 : [-1]
        },
        'height': {
            0 : [1, 1],
            1 : [2, 2],
        }
    },

    'sl': {
        'name': 'S-piece left',
        'top': {
            0 : [0, -1],
            1 : [1]
        },
        'bottom': {
            0 : [-1, 0],
            1 : [1]
        },
        'height': {
            0 : [1, 1],
            1 : [2, 2]
        }
    },

    'i': {
        'name': 'I-piece',
        'top': {
            1 : [],
            0 : [0, 0 ,0]
        },
        'bottom': {
            1 : [],
            0 : [0, 0, 0]
        },
        'height': {
            1 : [4, 4],
            0 : [1, 1]
        }
    },

    't': {
        'name': 'T-piece',
        'top': {
            2 : [1, -1],
            3 : [-1],
            0 : [0, 0],
            1 : [1]
        },
        'bottom': {
            2 : [0, 0],
            3 : [1],
            0 : [-1, 1],
            1 : [-1]
        },
        'height': {
            2 : [1, 1],
            3 : [3, 1],
            0 : [1, 1],
            1 : [1, 3]
        }
    },

    's': {
        'name': 'Sq-piece',
        'top': {
            0 : [0]
        },
        'bottom': {
            0 : [0]
        },
        'height': {
            0 : [2, 2]
        }
    }
}
