#Author: nhny at hcmut.edu.vn
#Course: AI 2016
#Lab 3
# DFS, BFS, Hill Climbing, A-Star with heuristics manhattan distance and hamming distance. 

import heapq

class Node(object):
    """
    Represent state of board in 8 puzzle problem.
    """
    n = 0

    def __init__(self, board, prev_state = None):
        #assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常
        assert len(board) == 9

        self.board = board[:]
        self.prev = prev_state
        self.step = 0
        Node.n += 1

        if self.prev:
            self.step = self.prev.step + 1 

    def __eq__(self, other):
        """Check wether two state is equal."""
        return self.board == other.board

    #生成hash值。比如2 >> 1 = 1 。2 << 1 = 4
    def __hash__(self):
        """Return hash code of object.

        Used for comparing elements in set
        """
        h = [0, 0, 0]
        h[0] = self.board[0] << 6 | self.board[1] << 3 | self.board[2]
        h[1] = self.board[3] << 6 | self.board[4] << 3 | self.board[5]
        h[2] = self.board[6] << 6 | self.board[7] << 3 | self.board[8]

        h_val = 0
        for h_i in h:
            h_val = h_val * 31 + h_i

        return h_val
    
    '''
        #输出方式
        0 1 2
        3 4 5
        6 7 8
    '''
    def __str__(self):
        string_list = [str(i) for i in self.board]
        sub_list = (string_list[:3], string_list[3:6], string_list[6:])
        return "\n".join([" ".join(l) for l in sub_list])

    def manhattan_distance(self):
        """Return Manhattan distance of state."""
        #TODO: return Manhattan distance
        distance = 0
        goal = [1,2,3,4,5,6,7,8,0]
        for i in range(1,9):
            xs, ys = self.__i2pos(self.board.index(i))
            xg, yg = self.__i2pos(goal.index(i))
            distance += abs(xs-xg) + abs(ys-yg)
        return distance

    def manhattan_score(self):
        """Return Manhattan score of state."""
        #TODO: return Manhattan score of state
        return 0

    def hamming_distance(self):
        """Return Hamming distance of state."""
        #TODO: return Hamming distance
        distance = 0
        goal = [1,2,3,4,5,6,7,8,0]
        for i in range(9):
            if goal[i] != self.board[i]: distance += 1
        return distance

    def hamming_score(self):
        """Return Hamming distance score of state."""
        #TODO return Hamming score of state
        return 0
    
    # 原理是通过控制“0”的上下左右元素互换，使得全局元素发生变化
    def next(self):
        """Return next states from this state."""
        next_moves = []
        i = self.board.index(0)  #输出0在列表中的下标

        next_moves = (self.move_up(i), self.move_down(i), self.move_left(i), self.move_right(i))

        return [s for s in next_moves if s]
    
    #这里要注意：x决定了元素在第几行，y决定了元素在第几列。所以x控制上下移动，y控制左右移动
    def move_right(self, i):
        x, y = self.__i2pos(i)
        if y < 2:
            right_state = Node(self.board, self)  #当前状态
            right = self.__pos2i(x, y+1)  #“0”元素向右移动后的下标
            right_state.__swap(i, right)  #得到“0”元素向右移动后的状态
            return right_state

    def move_left(self, i):
        x, y = self.__i2pos(i)
        if y > 0:
            left_state = Node(self.board, self)
            left = self.__pos2i(x, y - 1)
            left_state.__swap(i, left)
            return left_state

    def move_up(self, i):
        x, y = self.__i2pos(i)
        if x > 0:
            up_state = Node(self.board, self)
            up = self.__pos2i(x - 1, y)
            up_state.__swap(i, up)
            return up_state

    def move_down(self, i):
        x, y = self.__i2pos(i)
        if x < 2:
            down_state = Node(self.board, self)
            down = self.__pos2i(x + 1, y)
            down_state.__swap(i, down)
            return down_state

    #将board中下标为i和下标为j的元素互换
    def __swap(self, i, j):
        self.board[j], self.board[i] = self.board[i], self.board[j]
    
    #得到元素行号和列号
    def __i2pos(self, index):
        return (int(index / 3), index % 3)
    
    #得到元素在列表中的下标
    def __pos2i(self, x, y):
        return x * 3 + y


class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0
