import random


BOUNDS = (-1, 1)
H = 30
W = 30

IMG_W = (W - 1) * 5
IMG_H = (H - 1) * 5


def random_value(lb, hb):
    return random.random() * (hb - lb) + lb


def random_vector(lb, hb):
    return (random_value(lb, hb), random_value(lb, hb))


def grid_str(grid):
    return '\n'.join([' '.join(['(%+2.3f %+2.3f)' % vector
         for vector in row]) for row in grid])
    

def grid_definition(w, h, lb, hb):
    """Define a grid with random vectors"""
    grid = [
        [random_vector(lb, hb) for _ in range(w)]
        for _ in range(h)]
    return grid
    

def computation(w, h, grid):
    """Interpolate values in all the points of image"""
    GH = len(grid)
    GW = len(grid[0])
    PW = w // (GW - 1)
    PH = h // (GH - 1)
    result = []

    def dot_product(gx, gy, x, y):
        dx, dy = (x - gx * PW) / PW, (y - gy * PH) / PH
        return (dx * grid[gy][gx][0] + dy * grid[gy][gx][1])

    for y in range(h):
        y0 = y // PH
        y1 = y0 + 1
        dy = (y - y0 * PH) / PH
        row = []

        for x in range(w):
            x0 = x // PW
            x1 = x0 + 1
            dx = (x - x0 * PW) / PW
            # print('%d%d ' % (x0, y0), end='')
            # print(dx, dy)
            hi1 = ((1.0 - dx) * dot_product(x0, y0, x, y) +
                          dx  * dot_product(x1, y0, x, y))
            # print('hi1: ', hi1)
            hi2 = ((1.0 - dx) * dot_product(x0, y1, x, y) +
                          dx  * dot_product(x1, y1, x, y))
            # print('hi2: ', hi2)
            v = (1.0 - dy) * hi1 + dy * hi2
            # print('v: ', v)
            row.append(v)
            
        result.append(row)
        # print()

    return result


V = [
    (-0.9, '\033[38;5;232m#\033[0m'),
    (-0.7, '\033[38;5;235m#\033[0m'),
    (-0.5, '\033[38;5;238m#\033[0m'),
    (-0.2, '\033[38;5;241m#\033[0m'),
    ( 0.0, '\033[38;5;244m#\033[0m'),
    ( 0.2, '\033[38;5;247m#\033[0m'),
    ( 0.5, '\033[38;5;250m#\033[0m'),
    ( 0.7, '\033[38;5;253m#\033[0m'),
    ( 1.0, '\033[38;5;255m#\033[0m')]


def v_to_str(v):
    for thr, str_v in V:
        if v <= thr:
            return str_v


def perlin_str(grid):
    return '\n'.join(
        [''.join(v_to_str(v) for v in row)
            for row in grid])


# result = interpolation(computation(grid_definition(W, H)))
if __name__ == '__main__':
    grid = grid_definition(W, H, *BOUNDS)
    with open('output.txt', 'w') as f:
        f.write(perlin_str(computation(IMG_W, IMG_H, grid)))
        f.write('\n')
