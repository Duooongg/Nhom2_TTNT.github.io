
import copy
class State:
    def __init__(self, data = None, par = None,
                 g = 0, h = 0, op = None):
        self.data = data
        self.par = par
        self.g = g
        self.h = h
        self.op = op
    def clone(self):
        sn = copy.deepcopy(self)
        return sn
    def Print(self):
        sz = 3
        for i in range(sz):
          for j in range(sz):
              print(self.data[i*sz + j], end = ' ')
          print()
        print()
    def Key(self):
        if self.data == None:
            return None
        res = ''
        for x in self.data:
            res += (str)(x)
        return res
    def __lt__(self, other):
        if other == None:
            return False
        return self.g + self.h < other.g + other.h
    def __eq__(self, other):
        if other == None:
            return False
        return self.Key() == other.Key()

class Operator:
    def __init__(self, i):
        self.i = i

    def checkStateNull(self, s):
        return s.data is None

    def findPos(self, s):
        sz = 3
        for i in range(sz):
            for j in range(sz):
                if s.data[i * sz + j] == 0:
                    return i, j
        return None

    def swap(self, s, x, y, i):
        sz = 3
        sn = s.clone()
        x_new, y_new = x, y
        if i == 0: x_new += 1
        if i == 1: x_new -= 1
        if i == 2: y_new += 1
        if i == 3: y_new -= 1
        sn.data[x * sz + y], sn.data[x_new * sz + y_new] = sn.data[x_new * sz + y_new], 0
        return sn

    def Down(self, s):
        if self.checkStateNull(s): return None
        x, y = self.findPos(s)
        if x == 2: return None  # Không xuống được nếu đang ở hàng dưới cùng
        return self.swap(s, x, y, self.i)

    def Up(self, s):
        if self.checkStateNull(s): return None
        x, y = self.findPos(s)
        if x == 0: return None  # Không lên được nếu đang ở hàng trên cùng
        return self.swap(s, x, y, self.i)

    def Right(self, s):
        if self.checkStateNull(s): return None
        x, y = self.findPos(s)
        if y == 2: return None  # Không sang phải nếu đang ở cột cuối
        return self.swap(s, x, y, self.i)

    def Left(self, s):
        if self.checkStateNull(s): return None
        x, y = self.findPos(s)
        if y == 0: return None  # Không sang trái nếu đang ở cột đầu
        return self.swap(s, x, y, self.i)

    def Move(self, s):
        if self.i == 0: return self.Down(s)
        if self.i == 1: return self.Up(s)
        if self.i == 2: return self.Right(s)
        if self.i == 3: return self.Left(s)
        return None

def checkPriority(Open, tmp):
  if tmp == None:
    return False
  return (tmp in Open.queue)
def equal(O, G):
  if O == None:
    return False
  return O.Key() == G.Key()
def Path(O):
    if O.par:
        Path(O.par)
        print(O.op.i)  # In từng bước di chuyển
    O.Print()  # In trạng thái cuối cùng
def Hx(S, G):
  sz = 3
  res = 0
  for i in range(sz):
    for j in range(sz):
      if S.data[i*sz + j] != G.data[i*sz + j]:
        res += 1
  return res

from queue import PriorityQueue
def RUN(S, G):
    Open = PriorityQueue()
    Closed = PriorityQueue()
    S.g = 0
    S.h = Hx(S, G)
    Open.put(S)

    while True:
        if Open.empty():
            print('Tìm kiếm thất bại')
            return

        O = Open.get()
        Closed.put(O)

        if equal(O, G):
            print('Tìm kiếm thành công')
            Path(O)
            return

        for i in range(4):
            op = Operator(i)
            child = op.Move(O)
            if child == None:
              continue
            ok1 = checkPriority(Open, child)
            ok2 = checkPriority(Closed, child)
            if ok1 == False and ok2 == False:
              child.par = O
              child.op = op
              child.g = O.g + 1
              child.h = Hx(child, G)
              Open.put(child)

def init(custom_data):
    if not custom_data or len(custom_data) != 9:
        raise ValueError("Dữ liệu phải có đúng 9 phần tử.")

    G = State(data=[1, 2, 3, 4, 5, 6, 7 , 8, 0])
    S = State(data=custom_data)

    return S, G

custom_start = [1, 2, 3, 7, 4, 6, 5, 0, 8]
S, G = init(custom_start)
RUN(S, G)
