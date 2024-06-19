import  sys
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
class Maze():
    def __init__(self, filename):
        # 读取文件并设置迷宫的高度和宽度
        with open(filename) as f:
            contents = f.read()
        # 验证起点和终点
        if contents.count("A") != 1:
            raise Exception("迷宫必须有且只有一个起点")
        if contents.count("B") != 1:
            raise Exception("迷宫必须有且只有一个终点")
        # 确定迷宫的高度和宽度
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)  # 修正宽度计算

        # 记录墙壁的位置
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def print(self):
        # 如果有解，则将其路径取出
        # 如果
        # `self.solution`
        # 有值，就把
        # `self.solution[1]`
        # 赋给
        # `solution`；如果
        # `self.solution`
        # 是
        # `None`，那就让
        # `solution`
        # 也为
        # `None`
        solution = self.solution[1] if self.solution is not None else None
        print()  # 打印一个空行用于美观

        # 遍历迷宫的每一行
        for i, row in enumerate(self.walls):
            # 遍历迷宫的每一列
            for j, col in enumerate(row):
                if col:
                    # 如果当前位置是墙壁，则打印墙壁符号
                    print("█", end="")
                elif (i, j) == self.start:
                    # 如果当前位置是起点，则打印起点符号
                    print("A", end="")
                elif (i, j) == self.goal:
                    # 如果当前位置是终点，则打印终点符号
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    # 如果当前位置在解路径中，则打印路径符号
                    print("*", end="")
                else:
                    # 否则，打印空白
                    print(" ", end="")
            # 每行结束后打印一个换行符
            print()
        print()  # 打印一个空行用于美观

    def neighbors(self, state):
        # 将当前状态解包为行和列
        row, col = state

        # 定义所有可能的移动方向及其对应的新位置
        candidates = [
            ("up", (row - 1, col)),  # 上移
            ("down", (row + 1, col)),  # 下移
            ("left", (row, col - 1)),  # 左移
            ("right", (row, col + 1))  # 右移
        ]

        # 用于存储有效的邻居节点
        result = []

        # 遍历每一个候选方向和位置
        for action, (r, c) in candidates:
            # 检查新位置是否在迷宫范围内，并且不是墙壁
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                # 如果有效，则将该方向和位置加入结果列表
                result.append((action, (r, c)))

        # 返回所有有效的邻居节点
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self,filename,show_solution=True,show_explored=False):
        from PIL import Image, ImageDraw
        cell_size=50
        cell_border=2

        # Create a blank canvas
        img=Image.new('RGBA',(self.width*cell_size,self.height*cell_size),"black")
        draw=ImageDraw.Draw(img)

        solution=self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                # Walls
                if col:
                    fill=(40,40,40)
                # Start:
                elif (i,j) == self.start:
                    fill=(255,0,0)
                # Goal
                elif (i,j) == self.goal:
                    fill = (0, 171, 28)
                # Solution
                elif solution is not None and show_solution and (i,j) in solution:
                    fill=(220,235,113)
                # Explored
                elif solution is not None and show_explored and (i,j) in self.explored:
                    fill=(212,97,85)
                # Empty cell
                else:
                    fill=(237,240,252)
                 # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
        img.save(filename)

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)