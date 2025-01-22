
# t - мусор
# b - урна
# d - сборщик
#? по мусору можно пройти, а по урне нет (столкновение, как с собой). Хотя может и не надо это...
# можно еще учитывать размер мусора, сколько места он будет занимать в мешке, влезет ли он в урну, емкость урны тоже надо учитывать, ее состояние...
# p - пакет (будущее дополнение). Временное расширение емкости
# можно также ввести тип мусора и не в каждую урну его можно будет положить...
# 
#


import random


class Map:
    def __init__(self, w=10, h=10):
        self.width = w
        self.height = h
        self.map = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.dustman = None


    def show(self):
        border = " " + "-=-" * len(self.map[0])
        print(border)
        for y in range(self.height):
            print("|", end="")
            num_line = " "
            for x in range(self.width):
                num_line += f" {x} "
                if self.map[y][x].dustman_here:
                    print(" d ", end="")
                    continue
                content = self.map[y][x].content
                if content is None:
                    print("   ", end="")
                elif isinstance(content, Trash):
                    print(" t ", end="")
                elif isinstance(content, Bin):
                    print(" b ", end="")
            print("|", y)
        print(border)
        print(num_line)
        
        
    def add_dustman(self, d):
        if self.dustman is not None:
            return
        
        self.dustman = d
        self.map[d.y][d.x].dustman_here = True
        d.map_link = self
        
        
    def remove_dustman(self, d):
        if d == self.dustman:
            d.map_link = None
            self.dustman = None
            self.map[d.y][d.x].dustman_here = False


    def add_trash(self, nums=5):
        count = 0
        while count < nums:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if self.map[y][x].content is None:
                self.map[y][x].content = Trash()
                count += 1


    def add_bin(self, nums=3, diff=2):
        def check_coords(new_bin, bins, diff):
            for added_bin in bins:
                a = ((added_bin[0] - diff) <= new_bin[0] <= (added_bin[0] + diff)) 
                b = ((added_bin[1] - diff) <= new_bin[1] <= (added_bin[1] + diff)) 
                if a and b:
                    return False
            return True
        
        count = 0
        bins = []
        iteration = 0
        ITERATIONS_LIMIT = 100
        while count < nums:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if self.map[y][x].content is None:
                # проверка по списку уже добавленных корзин, чтобы координаты не были рядом
                if check_coords((y, x), bins, diff):
                    self.map[y][x].content = Bin()
                    bins.append((y, x))
                    count += 1
                    iteration = 0
                    continue
                    
            iteration += 1
            if iteration == ITERATIONS_LIMIT:
                print("very long time, stop process")
                return


class Dustman:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.level = 1
        self.trash_capacity = 1
        self.trash_bag = []
        self.map_link = None
        self.throwed_trash = 0
        
        
    def show(self):
        print(f"""Dustman:
        Name: {self.name}
        Position: {self.x, self.y}
        Level: {self.level}
        Trash capacity: {self.trash_capacity}
        Trash bag: {self.trash_bag}
        """)
    
    
    def move(self, new_dir):
        dirs = {
            "right": (0, 1),
            "down": (1, 0),
            "left": (0, -1),
            "up": (-1, 0),
        }
        
        print(new_dir)
        new_y = self.y + dirs[new_dir][0]
        # если дошли до границы карты, то выходим с другой стороны
        # можно и убрать эту штуку, но пока пускай так будет..
        map = self.map_link.map
        if new_y < 0:
            new_y = len(map) - 1
        elif new_y == len(map):
            new_y = 0
        new_x = self.x + dirs[new_dir][1]
        if new_x < 0:
            new_x = len(map[0]) - 1
        elif new_x == len(map[0]):
            new_x = 0

        self.map_link.map[self.y][self.x].dustman_here = False
        self.y = new_y
        self.x = new_x
        self.map_link.map[new_y][new_x].dustman_here = True
        
        # self.map_link.show()
    
    
    def pick_up_trash(self):
        content = self.map_link.map[self.y][self.x].content
        if not isinstance(content, Trash):
            print("There is no trash here!")
            return
        
        if len(self.trash_bag) == self.trash_capacity:
            print("Trash bag is full!")
            return
        
        self.trash_bag.append(content)
        self.map_link.map[self.y][self.x].content = None
        print("Trash is picked!", self.trash_bag)
    
    
    def throw_away_trash(self):
        if len(self.trash_bag) == 0:
            print("No trash in the bag!")
            return
        
        content = self.map_link.map[self.y][self.x].content
        if isinstance(content, Bin):
            # сброс в корзину
            if content.is_full():
                print("This bin is full!")
                return
            content.add_trash(self.trash_bag.pop())
            print("The trash has been added to bin!", self.trash_bag, content.trash)
            self.throwed_trash += 1
            self.check_level()
        elif isinstance(content, Trash):
            print("This cell already contains the trash!")
            return
        elif content is None:
            # просто выбросить
            self.map_link.map[self.y][self.x].content = self.trash_bag.pop()
            print("The trash has been thrown out!", self.trash_bag)


    def check_level(self):
        levels = {
            1: {
                "max_throwed_trash": 2,
                "trash_capacity": 1
            },
            2: {
                "max_throwed_trash": 5,
                "trash_capacity": 2
            },
            3: {
                "max_throwed_trash": 10,
                "trash_capacity": 4
            },
        }
        
        if self.throwed_trash == levels[self.level]["max_throwed_trash"]:
            if self.level + 1 not in levels:
                print("You have max level!")
                return
            self.level += 1
            self.trash_capacity = levels[self.level]["trash_capacity"]
            print("Level up to:", self.level)
            print("New trash_capacity:", self.trash_capacity)


class Cell:
    def __init__(self):
        self.dustman_here = False
        self.content = None


class Trash:
    pass


class Bin:
    def __init__(self, capacity=5):
        self.trash = []
        self.capacity = capacity
        
    def add_trash(self, t):
        if self.is_full():
            print("This bin is full!")
            return
        self.trash.append(t)
        
    def is_full(self) -> bool:
        return (len(self.trash) == self.capacity)


class Packet:
    pass


def main():
    map = Map()
    # map.show()
    dustman = Dustman("Nick")
    # dustman.show()
    map.add_dustman(dustman)
    # map.show()
    map.add_trash(10)
    # map.map[0][3].content = Trash()
    # map.map[0][4].content = Trash()
    map.add_bin(5, 3)
    # map.map[0][6].content = Bin()
    map.show()

    # dustman.pick_up_trash()
    # dustman.throw_away_trash()
    # dustman.move("right")
    # dustman.move("right")
    # dustman.move("right")
    # dustman.pick_up_trash()
    # dustman.move("right")
    # dustman.pick_up_trash()
    # dustman.move("right")
    # dustman.move("right")
    # dustman.throw_away_trash()
    # dustman.move("left")
    # dustman.move("left")
    # dustman.pick_up_trash()
    # dustman.move("right")
    # dustman.move("right")
    # dustman.throw_away_trash()
    # dustman.move("right")
    # dustman.move("right")

    while True:
        com = input()
        if com == "q":
            break
        elif com == "s":
            dustman.move("left")
        elif com == "f":
            dustman.move("right")
        elif com == "e":
            dustman.move("up")
        elif com == "d":
            dustman.move("down")
        elif com == "a":
            dustman.pick_up_trash()
        elif com == "r":
            dustman.throw_away_trash()
        map.show()


if __name__ == "__main__":
    main()
