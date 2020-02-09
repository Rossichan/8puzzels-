#!/usr/bin/env python

#Author: Slash at 
#Course: AI 2016
#Lab 3
from sys import argv
from time import time
from node import *
import random
import math

class Searcher(object):
    """Searcher that manuplate searching process."""

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def print_path(self, state):
        path = []
        while state:
            path.append(state)
            state = state.prev
        path.reverse()  #队列翻转
        print("\n-->\n".join([str(state) for state in path]))

    #通过维护一个栈实现
    #这样想，首先用append()从尾部添加一个，又用pop()从尾部拿出一个，这样不就是后进先出吗
    #或者用deque()实现。首先用popleft()从头部拿出一个，又用appendleft()从头部添加一个，这样不就是先进先出吗
    def dfs(self, depth = 100):
        stack = [self.start]
        visited = set()
        found = False

        while stack:
            state = stack.pop()

            if state == self.goal:
                found = state
                break

            if state in visited or state.step > depth:
                continue

            visited.add(state)

            for s in state.next():
                stack.append(s)

        if found:
            self.print_path(found)
            print ("Find solution")
        else:
            print("No solution found")

    #通过维护一个队列实现
    #这样想，首先用insert()从头部插入一个，再用pop()从尾部拿出一个，这样不就是先进后出吗
    #或者用deque()实现。首先用popleft()从头部拿出一个，又用append()从尾部添加一个，这样不就是先进后出吗
    def bfs(self, depth = 50):
        """Run Breadth-first search."""
        #TODO: Implement breadth first search
        queue = [self.start]
        visited = set()
        found = False

        while queue:
            state = queue.pop()

            if state == self.goal:
                found = state
                break

            if state in visited or state.step > depth:
                continue

            visited.add(state)

            for s in state.next():
                queue.insert(0, s)

        if found:
            self.print_path(found)
            print ("Find solution")
        else:
            print("No solution found")

    # 最陡爬山算法是在首选爬山算法上的一种改良,它规定每次选取邻近点价值最大的那个点作为爬上的点
    def steepest_ascent_hill_climbing(self):
        """Run steepest ascent hill climbing search."""
        #TODO Implement hill climbing.
        stack = [self.start]

        while stack:
            state = stack.pop()
            if state == self.goal:
                self.print_path(state)
                print ("Find solution")
                break

            h_val = state.manhattan_distance() + state.hamming_distance()
            next_state = False
            for s in state.next():
                h_val_next = s.manhattan_distance() + s.hamming_distance()
                if h_val_next < h_val:
                    next_state = s
                    h_val = h_val_next

            if next_state: 
                stack.append(next_state)
            else:
                self.print_path(state)
                print ("Cannot find solution")

    # 依次寻找该点X的邻近点中首次出现的比点X价值高的点,并将该点作为爬山的点. 依次循环,直至该点的邻近点中不再有比其大的点. 我们成为该点就是山的顶点,又称为最优点.
    def hill_climbing(self):
        """Run hill climbing search."""
        #TODO Implement hill climbing.
        stack = [self.start]

        while stack:
            state = stack.pop()
            if state == self.goal:
                self.print_path(state)
                print ("Find solution")
                break
            #计算当前状态的启发f函数
            h_val = state.manhattan_distance() + state.hamming_distance()
            next_state = False
            for s in state.next():
                h_val_next = s.manhattan_distance() + s.hamming_distance()
                if h_val_next < h_val:
                    next_state = s
                    h_val = h_val_next
                    #与最抖爬山法的区别在于它将每一个邻居都放入stack。而最抖爬山法只将代价最小的放入stack。
                    stack.append(next_state)
                    break

            if not next_state:
                self.print_path(state)
                print ("Cannot find solution")

    #模拟退火方法与爬山法类似，爬山法是一直向上爬，只吸收代价最低的节点，擅长找到局部最优解。而模拟退火法以一定概率吸收代价不是最低的点，
    #这样避免了只能找到局部最优解的情况，有可能找到全局最优解。
    # 算法接受较差解的概率 P = exp[-(highcost-lowcost)/temperature]
    def simulated_annealing(self):
        """Run Simulated Annealing Search"""
        #TODO Implement Simulated Annealing.
        #先初始化
        stack = [self.start]
        T=10000.0
        cool=0.98
        while stack:
            state = stack.pop()
            if state == self.goal:
                self.print_path(state)
                print ("Find solution")
                break
            #计算当前状态的启发f函数
            h_val = state.manhattan_distance() + state.hamming_distance()
            next_state = False
            for s in state.next():
                h_val_next = s.manhattan_distance() + s.hamming_distance()
                #%温度越低，越不太可能接受新解；新老距离差值越大，越不太可能接受新解
                if h_val_next < h_val or random.random() < math.exp(-(h_val_next - h_val) / T):
                    next_state = s
                    h_val = h_val_next
                    stack.append(next_state)
                    break
            T = T*cool
            if not next_state:
                self.print_path(state)
                print ("Cannot find solution")
            

    #通过维护一个优先级队列实现，每次拿出F最小的元素
    def astar(self, depth = 75):
        """Run A* search."""
        #TODO: Implement a star search.
        priotity_queue = PriorityQueue()
        #初始的启发函数。
        h_val = self.start.manhattan_distance() + self.start.hamming_distance()
        # g_val always is start.step
        #与局部搜索的区别在于A*是启发搜索，所以把初始F放在这。
        f_val = h_val + self.start.step
        priotity_queue.push(self.start, f_val)
        visited = set()
        found = False

        while not priotity_queue.isEmpty():
            state = priotity_queue.pop()

            if state == self.goal:
                found = state
                break

            if state in visited or state.step > depth:
                continue

            visited.add(state)

            for s in state.next():
                #寻路中的启发函数
                h_val_s = s.manhattan_distance() + s.hamming_distance()
                f_val_s = h_val_s + s.step
                priotity_queue.push(s, f_val_s)

        if found:
            self.print_path(found)
            print ("Find solution")
        else:
            print("No solution found")


if __name__ == "__main__":
    script, strategy = argv

    #Unit test
    print("Search for solution\n")
    start = Node([2,0,1,4,5,3,8,7,6])
    goal = Node([1,2,3,4,5,6,7,8,0])

    #print start.hamming_distance()
    #print start.manhattan_distance()

    search = Searcher(start, goal)

    start_time = time()
    if strategy == "dfs":
        search.dfs()
    elif strategy == "bfs":
        search.bfs()
    elif strategy == "hc":
        search.hill_climbing()
    elif strategy == "sahc":
        search.steepest_ascent_hill_climbing()
    elif strategy == "astar":
        search.astar()
    elif strategy == "sa":
        search.simulated_annealing()   
    else:
        print ("Wrong strategy")
    end_time = time()
    elapsed = end_time - start_time
    print ("Search time: %s" % elapsed)
    print ("Number of initialized node: %d" % Node.n)
