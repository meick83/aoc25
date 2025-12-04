
import re
from enum import Enum
import collections
import bisect
import functools
import pathlib

wsMatcher = re.compile(r"\s+")

class Parser:

    @classmethod
    def load(cls, base_name):
        p = cls(base_name+".txt")
        return p.parse()

    @classmethod
    def ex(cls, n):
        return cls.load(f"ex{n}")

    @classmethod
    def input(cls):
        cwd = pathlib.Path().absolute()
        day_name = cwd.name
        input_path = cwd.parent / "data" / (day_name + "_input")
        return cls.load(str(input_path))

    def __init__(self, fileName):
        self.fileName = fileName
        self.data = None
    
    def parse(self):
        with open(self.fileName) as input:
            for y,line in enumerate(input):
                lineStripped = line.strip()
                self.parseLine(y,lineStripped)
        self._finish()
        return self.data

    def _finish(self):
        pass

    def parseLine(self, lineNo, line):
        for x, ch in enumerate(line):
            self._parse_cell(x, lineNo, ch)

    def _parse_cell(self, x, y, ch):
        pass

class Solver(Parser):

    def __init__(self, fileName):
        super().__init__(fileName)
        self.part1Result = None
        self.part2Result = None

    def run(self):
        self.parse()
        self.compute()
        s1 = self.getPart1Result()
        s2 = self.getPart2Result()
        print("{0:s} -> {1:d}, {2:d}".format(self.fileName, s1, s2))



    def compute(self):
        self.part1Result = self.computePart1()
        self.part2Result = self.computePart2()

    def computePart1(self):
        return 0

    def computePart2(self):
        return 0

    def run1(self):
        self.parse()
        return self.computePart1()

    def run2(self):
        self.parse()
        return self.computePart2()

    def getPart1Result(self):
        if self.part1Result != None:
            return self.part1Result
        e = self.getPart1Scores()
        return sum(e)
    
    def getPart1Scores(self):
        return ()
    
    def getPart2Result(self):
        if self.part2Result != None:
            return self.part2Result        
        e = self.getPart2Scores()
        return sum(e)
    
    def getPart2Scores(self):
        return ()
    
class Record:

    def __init__(self):
        self.id = None
        self.idStr = None

    def parse(self, line):
        idStr, content = line.split(":",1)
        self.parseIdStr(idStr)
        self.parseContent(content)

    def parseIdStr(self, idStr):
        self.idStr = idStr
        self.id = int(idStr.split(" ",1)[1])

    def parseContent(self, content):
        raise "not implemented"

class Direction(Enum):
    NORTH = (0, 0, -1,"^")
    EAST = (1, +1, 0,">")
    SOUTH = (2, 0, +1,"v")
    WEST = (3, -1, 0,"<")

    def __init__(self, val, dx, dy, sym):
        super().__init__()
        self.val = val
        self.dx = dx
        self.dy = dy
        self.sym = sym

    def left(self):
        r = (self.val + 3) % 4
        return Direction.from_id(r)
    
    def right(self):
        r = (self.val + 1) % 4
        return Direction.from_id(r)
    
    def opposite(self):
        r = (self.val + 2) % 4
        return Direction.from_id(r)

    def is_horizontal(self):
        return (self.dy == 0)

    @classmethod
    def from_sym(cls, sym):
        for v in cls.__members__.values():
            if v.sym == sym:
                return v
        raise Exception(f"symbol '{sym}' not found")

    @classmethod
    def from_id(cls, id):
        for v in cls.__members__.values():
            if v.val == id:
                return v
        raise Exception(f"id '{id}' not found")

    def __hash__(self):
        return self.val

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, Vector):
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return self.__class__(self.x - other.x, self.y - other.y)        
        else:
            return Vector(self.x - other.x, self.y - other.y)        

    def with_x(self, x):
        return self.__class__(x, self.y)

    def with_y(self, y):
        return self.__class__(self.x, y)        

    def __repr__(self):
        return "({0:d},{1:d})".format(self.x, self.y)
    
    def __eq__(self, other):
        if other is None:
            return False
        return (self.x == other.x) and (self.y == other.y)        

    def __rmul__(self, other):
        return Vector(other* self.x, other*self.y)

    def manhatten_norm(self):
        return abs(self.x) + abs(self.y)

class Point(Vector):
    
    def translate(self, d, offset=1):
        x = self.x + d.dx*offset
        y = self.y + d.dy*offset
        return Point(x,y)

    def translate_x(self, offset):
        return Point(self.x + offset,self.y)

    def translate_y(self, offset):
        return Point(self.x,  self.y + offset)

class Pose:

    def __init__(self, p, d):
        self.position = p
        self.direction = d

    def with_position(self, p):
        return Pose(p, self.direction)

    def with_direction(self, d):
        return Pose(self.position, d)

    def turn_right(self):
        return Pose(self.position, self.direction.right())

    def turn_left(self):
        return Pose(self.position, self.direction.left())        

    def turn_back(self):
        return Pose(self.position, self.direction.opposite())              

    def move_forward(self, steps = 1):
        return self.with_position(self.position.translate(self.direction, steps))

    def move_backward(self, steps = 1):
        return self.with_position(self.position.translate(self.direction, -steps))

    def __repr__(self):
        return f"({self.position}>{self.direction})"

    def __hash__(self) -> int:
        hash_pos = hash(self.position)
        hash_dir = hash(self.direction)
        return hash_pos*10 + hash_dir

    def __eq__(self, other):
        return (self.position == other.position) and (self.direction == other.direction)        

class AbstractGrid:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height

    def __setitem__(self, p, v):
        x,y = to_cords(p)
        self._setitem(x,y,v)
        self.width = max(self.width, x+1)
        self.height = max(self.height, y+1)

    def __getitem__(self, p: Point):
        x,y = to_cords(p)
        return self._getitem(x,y)
        return None     

    def is_inside(self, *p):
        x,y = to_cords(p)
        return (0 <= x) and (x < self.width) and (0 <= y) and (y < self.height)    

    def points(self):
        return GridIterator(self)

class GridIterator:

    def __init__(self, grid):
        self.next = Point(0,0)
        self.grid = grid

    def __iter__(self):
        return GridIterator(self.grid)

    def __next__(self):
        res = self.next
        if res.y >= self.grid.height:
            raise StopIteration
        self.next = res.translate_x(1)
        if self.next.x >= self.grid.width:
            self.next.x = 0
            self.next.y += 1
        return res

class Grid(AbstractGrid):

    def __init__(self, init_width=None, init_height=None):
        super().__init__()
        self.cells = []
        if init_height is not None:
            init_row = lambda: [None] * init_width
            self._ensure_size(self.cells, init_height, init_row)


    def add_row(self, row):
        if self.width > 0:
            assert len(row) == self.width
        else:
            self.width = len(row)
        self.cells.append(row)
        self.height += 1

    def _getitem(self, x,y):
        return self.cells[y][x]

    def _setitem(self, x, y, v):
        Grid._ensure_size(self.cells, y+1, lambda:[])
        Grid._ensure_size(self.cells[y], x+1, lambda:None)
        self.cells[y][x] = v

    @staticmethod
    def _ensure_size(lst, sz, ref):
        while len(lst) < sz:
            lst.append(ref())

    def copy(self):
        res = self.__class__()
        for row in self.cells:
            new_row = []
            for cell in row:
                if cell is None or isinstance(cell, int) or isinstance(cell, str):
                    new_row.append(cell)
                else:
                    new_row.append(cell.copy())
                    
            res.add_row(new_row)
        return res

class FixedWidthGrid(AbstractGrid):

    def __init__(self, init_width = None, init_height=None):
        super().__init__()
        if init_width:
            self.width = init_width
        self.cells = []
        if init_width and init_height:
            init_len = self._to_index(init_width, init_height)
            self.cells = [None] * init_len

    def _to_index(self, x, y):
        return y*self.width + x

    def _try_resize(self, x, y):
        ix = self._to_index(x,y)
        if ix < len(self.cells):
            return ix
        if (self.width <= x):
            if (self.height <= 1):
                self.cells += [None] * (x - self.width + 1)
            else:
                raise KeyError
        self.cells += [None] * (len(self.cells) - ix + 1)
        return ix

    def _setitem(self, x, y, v):
        ix = self._try_resize(x,y)
        self.cells[ix] = v

    def _getitem(self, x, y):
        ix = self._to_index(x,y)
        return self.cells[ix]

    def print(self):
        cell_strs = list(map(self._cell_str, self.cells))
        for r in range(0, self.height):
            row_data = cell_strs[r*self.width:(r+1)*self.width]
            print("".join(row_data))

    def _cell_str(self, data):
        if data is None:
            return "."
        else:
            return str(data)

class BisectList:

    @classmethod
    def with_key(cls, key_func):
        return lambda: cls(key=key_func)

    def __init__(self, key=None, lo_val = None, hi_val = None):
        self._list = list()
        self._key = key
        self._lo_val_func = to_callable(lo_val)
        self._hi_val_func = to_callable(hi_val)

    def _bisect_left(self, k):
        return bisect.bisect_left(self._list, k, key=self._key)

    def _bisect_right(self, k):
        return bisect.bisect_right(self._list, k, key=self._key)

    def _get(self, i):
        if (i < 0):
            return self._lo_val_func()
        elif (i >= len(self._list)):
            return self._hi_val_func()
        else:
            return self._list[i]
        
    def add(self, v):
        bisect.insort(self._list, v, key=self._key)

    def find_eq(self, k):
        i = self._bisect_left(k)
        v = self._get(i)
        if v is None:
            return None
        if self._key(v) == k:
            return v
        else:
            return None        

    def find_lt(self, k):
        'Find rightmost value less than k'
        i = self._bisect_left(k)
        return self._get(i-1)

    def find_le(self, k):
        'Find rightmost value less than or equal to x'
        i = self._bisect_right(k)
        return self._get(i-1)

    def slice_le(self, k):
        'Slice of values less than or equal to x'
        i = self._bisect_right(k)
        return self._list[:i]

    def find_gt(self, k):
        'Find leftmost value greater than x'
        i = self._bisect_right(k)
        return self._get(i)

    def find_ge(self, x):
        'Find leftmost item greater than or equal to x'
        i = self._bisect_left(k)
        return self._get(i)     

    def __len__(self):
        return len(self._list)

    
class SparseOrthogoalGrid(AbstractGrid):

    def __init__(self):
        super().__init__()
        self._item_type = collections.namedtuple("SparseGridItem", ("c","item"))
        new_x_list = functools.partial(
            BisectList, lambda item: item.c,
            self._mk_item(-1, None,),
            lambda: self._mk_item(self.width, None)
        )
        new_y_list = functools.partial(
            BisectList, lambda item: item.c, 
            self._mk_item(-1, None,),
            lambda: self._mk_item(self.height, None)
        )
        self._x = collections.defaultdict(new_x_list)
        self._y = collections.defaultdict(new_y_list)
        self.width = 0
        self.height = 0

    def _mk_item(self, c, item):
        return self._item_type._make((c, item))

    def _setitem(self, x, y, v):
        if v is not None:
            self._x[x].add(self._mk_item(y,v))
            self._y[y].add(self._mk_item(x,v))

    def _getitem(self, x, y):
        x_items = self._x[x]
        xy_item = x_items.find_eq(y)
        if xy_item is not None:
            return xy_item.item
        if self.is_inside(x,y):
            return None
        else:
            raise KeyError

    def find_next(self, pose: Pose):
        d = pose.direction
        p = pose.position
        if d == Direction.NORTH:
            r = self._x[p.x].find_lt(p.y)
        elif d == Direction.EAST:
            r = self._y[p.y].find_gt(p.x)
        elif d == Direction.SOUTH:
            r = self._x[p.x].find_gt(p.y)
        elif d == Direction.WEST:
            r = self._y[p.y].find_lt(p.x)
        else:
            raise ValueError(pose.direction)

        if r is None:
            return None, None
        if d.dx == 0:
            return Point(p.x, r.c), r.item
        else:
            return Point(r.c, p.y), r.item

class SparseGrid(AbstractGrid):

    def __init__(self, *p):
        super().__init__(*p)
        self._cells = {}

    def _setitem(self, x, y, v):
        if v is not None:
            self._cells[(x,y)] = v
        elif (x,y) in self._cells:
            del self._cells[(x,y)]
            
    def _getitem(self, x, y):
        v = self._cells.get((x,y))
        if v is not None:
            return v
        if self.is_inside(x,y):
            return None
        raise KeyError

    def items(self):
        return map(lambda i:(Point(*i[0]),i[1]), self._cells.items())

    def keys(self):
        return map(lambda i:Point(*i), self._cells.keys())        

    def values(self):
        return self._cells.values()

  

    
def to_cords(p):
    if isinstance(p, Point):
        return p.x, p.y
    if (len(p) == 1) and isinstance(p[0], Point):
        return p[0].x, p[0].y
    elif len(p) == 2:
        return p[0], p[1]
    else:
        raise ValueError(p, "not a point")

def to_point(p):
    if isinstance(p, aocu.Point):
        return p
    elif len(p) == 2:
        return aocu.Point(*p)
    else:
        raise ValueError(p, "not a point")

def to_callable(v):
    if callable(v):
        return v
    else:
        return lambda: v

def depth_first_search(root, func= None):
    if isinstance(root, collections.abc.Iterable):
        stack = list(root)
    else:
        stack = [root]
    while len(stack) > 0:
        current = stack.pop()
        if func != None:
            res = func(current)
        else:
            res = current.next()
        if isinstance(res, collections.abc.Iterable):
            stack.extend(res)
        else:
            return res
    return None

def breath_first_search(root, func= None):
    if isinstance(root, collections.abc.Iterable):
        queue = collections.deque(root)
    else:
        queue = collections.deque([root])
    while len(queue) > 0:
        current = queue.popleft()
        if func != None:
            res = func(current)
        else:
            res = current.next()
        if isinstance(res, collections.abc.Iterable):
            queue.extend(res)
        else:
            return res
    return None

class NamedObject:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.name == other.name)

class KeyDefaultDict(collections.defaultdict):

    def __missing__(self, key):
        x = self.default_factory(key)
        self[key] = x
        return x