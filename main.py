from random import randint

class Cell :
    def __init__(self, open_status) :
        """Инициализирует атрибуты класса Cell"""
        self.open_status = open_status
        #status = -1  -  bomb
        #status = 0-8  -  bomb amount around
        self.close_status = 0
        # open_status = 0 - flag not setted
        # open_status = 1 - flag not setted
        # open_status = 2 - number of bombs
        # open_status = 3 - bomb found

    
    def make_action(self, action) :
        """Устанавливает(снимает, если уже установлен) флаг"""
        if action == "flag" :
            if self.close_status == 0 :
                self.close_status = 1
            elif self.close_status == 1 :
                self.close_status = 0


class Field :
    def __init__(self, init_width = 10, init_hight = 10, init_num_bobmbs = 5) :
        """Инициализирует атрибуты класса Field"""
        self.width = init_width
        self.hight = init_hight
        self.num_bombs = init_num_bobmbs
        self.bomb_opend_status = 0
        self.num_closed_cells = init_width * init_hight
        self.field = [[Cell(0) for i in range(self.width)] for j in range(self.hight)]
    def create_field(self) :
        """Создает игровое поле"""
        i = 0
        while i < self.num_bombs :
            tmp_x = randint(0, self.width - 1)
            tmp_y = randint(0, self.hight - 1)
            # print("N: ", i, "tmp_x =", tmp_x , "tmp_y =", tmp_y)
            if self.field[tmp_y][tmp_x].open_status != -1:
                self.field[tmp_y][tmp_x].open_status = -1
                i += 1
                # self.field[tmp_y][tmp_x].close_status = 3

        for i in range(self.hight) :
            for j in range(self.width) :
                if self.field[i][j].open_status == 0 :
                    num_bombs_around = 0
                    delta = [-1, 0, 1]
                    for di in delta :
                        for dj in delta :
                            if (0 <= i + di <= self.hight - 1) &\
                                (0 <= j + dj <= self.width - 1) & (not(di == dj == 0)) :
                                # print("i + di =", di + i, "j + dj", dj + j)
                                if self.field[i + di][j + dj].open_status == -1 :
                                    num_bombs_around += 1
                    self.field[i][j].open_status = num_bombs_around

    def open_all(self) :
        """Открывает все ячейки, чтобы увидеть, стоит вызать метод visualize_field() после open_all()"""
        for i in range(self.hight) :
            for j in range(self.width) :
                if self.field[i][j].open_status == -1 :
                    self.field[i][j].close_status = 3
                else :
                    self.field[i][j].close_status = 2

    def open_neighbors_cell(self, x, y) :
        """Вызывает action_type(x, y, "open") для каждой соседней ячейки"""
        delta = [-1, 0, 1]
        for di in delta :
            for dj in delta :
                if (0 <= x + dj <= self.width - 1) \
                    & (0 <= y + di <= self.hight - 1) & (not(di == dj == 0)) :
                    if self.field[y + di][x + dj].open_status >= 0 :
                        self.action_type(x + dj, y + di, "open")

    def action_type(self, x, y, action) :
        """Устанавливает флаг или открывет ячейку(ки) в зависимости от действия"""
        if (action == "flag") :
            self.field[y][x].make_action("flag")
        elif (action == "open") :
            if self.field[y][x].close_status == 0 :
                if self.field[y][x].open_status == 0 :
                    self.field[y][x].close_status = 2
                    self.num_closed_cells -= 1
                    self.open_neighbors_cell(x, y)
                elif self.field[y][x].open_status > 0 :
                    self.field[y][x].close_status = 2
                    self.num_closed_cells -= 1
                elif self.field[y][x].open_status == -1 :
                     self.field[y][x].close_status = 3
                     self.bomb_opend_status = 1

    def save_field(self, filename) :
        """Сохраняет состояние поля, но так, чтобы никто не увидел бомбы, открыв сохранение"""
        f = open(filename, 'w')
        s = ''
        f.write((str(self.hight) + '\n'))
        f.write((str(self.hight) + '\n'))
        for i in range(self.hight) :
            for j in range(self.width) :
                n = (i+j) % 3 + 7
                s = s + '{0:05b}'.format(self.field[i][j].close_status + n) +\
                '{0:05b}'.format(self.field[i][j].open_status + n)
                # print(int(s[0:8], base = 2))

        # print(s)
        while s != '' :
            f.write(chr(int(s[0:8], base = 2)))
            # print(chr(int(s[0:8], base = 2)))
            s = s[8:]
        f.close()
 
    def load_field(self, filename) :
        """Загружает ранее сохраненное поле (мы же знаем алгоритм сохранения)"""
        f = open(filename, 'r')
        self.hight = int(f.readline())
        self.width = int(f.readline())        
        self.num_closed_cells = self.width * self.hight
        self.field = [[Cell(0) for i in range(self.width)] for j in range(self.hight)]
        # print(self.hight)
        # print(self.width)
        num_bombs = 0
        s = f.read()
        bin_s = ''
        # print(s)
        s_len = len(s)
        for i in range(s_len) :
            if (i == s_len - 1) :
                tmp = self.hight * self.width * 10 % 8
                tmp = tmp if tmp > 0 else 8
                bin_s += '{0:0{n}b}'.format(ord(s[i]), n = tmp)
            else :
                bin_s += '{0:08b}'.format(ord(s[i]))
        # print(bin_s)
        for i in range(self.hight) :
            for j in range(self.width) :
                n = (i+j) % 3 + 7
                # print(bin_s[0:5])
                self.field[i][j].close_status = int(bin_s[0:5], base = 2) - n
                bin_s = bin_s[5:]
                
                # print(bin_s[0:5])
                self.field[i][j].open_status = int(bin_s[0:5], base = 2) - n
                bin_s = bin_s[5:]

                if  self.field[i][j].open_status == -1 :
                    num_bombs += 1
                if  self.field[i][j].close_status == 2 :
                    self.num_closed_cells -= 1
        self.num_bombs = num_bombs
        self.bomb_opend_status = 0
        f.close()


    def visualize_field(self) :
        """Визуализирует игровое поле"""
        x = self.width
        y = self.hight
        max_x_str_len = 0
        x_str = [str(i) for i in range(x)]
        max_x_str_len = len(x_str[-1])
        print()
        while max_x_str_len > 0 :
            print(' '*6, end = '')
            for i in range(len(x_str)) :
                if (len(x_str[i]) == max_x_str_len) :
                    print(x_str[i][0], end = ' ')
                    x_str[i] = x_str[i][1:]
                else :
                    print(' ', end = ' ')
            max_x_str_len -= 1
            print()
        print(' '*6 + '__'*(x - 1) + '_')
        for i in range(y) :
            print("%4d"%i, end = ' ')
            out = '|'
            for j in range(x) :
                if self.field[i][j].close_status == 0 :
                    if j != x - 1 :
                        out += '▢ '
                    else :
                        out += '▢'
                elif self.field[i][j].close_status == 1 :
                    if j != x - 1 :
                        out += '▣ '
                    else :
                        out += '▣'
                elif self.field[i][j].close_status == 2 :
                    if j != x - 1 :
                        out = out + str(self.field[i][j].open_status) + ' '
                    else :
                        out = out + str(self.field[i][j].open_status)
                elif self.field[i][j].close_status == 3 :
                    if j != x - 1 :
                        out += '✹ '
                    else :
                        out += '✹'

            print(out + '|')
        print(' '*6 + '‾‾'*(x - 1) + '‾')


def main() :
    first_input = []
    while not(len(first_input) == 3 or len(first_input) == 2) :
        first_input = input("Enter Width, Hight, Num_bombs separated by space\n        or Action(Load) and Filename.txt\n").split()
    field = Field()
    if len(first_input) == 2 :
        Action, Filename = first_input[0].lower(), first_input[1]
        if Action == "load" :
            if (Filename[-4:] == ".txt") : Filename = Filename[:-4]
            field.load_field(Filename + ".txt")
        else :
            return 
    elif len(first_input) == 3 :
        Width, Hight, Num_bombs =  map(int, first_input)
        field = Field(Width, Hight, Num_bombs)
        field.create_field()
    field.visualize_field()

    while field.bomb_opend_status == 0 :
        input_str = input("Enter X, Y, Action(Open or Flag) separated by space\n        or Action(Save) and Filename.txt\n").split()
        if len(input_str) == 2 :
            Action, Filename = input_str[0].lower(), input_str[1]
            if Action == "save" :
                if (Filename[-4:] == ".txt") : Filename = Filename[:-4]
                field.save_field(Filename + ".txt")
                continue
            else :
                print ("\n!!!!!  Incorrect input  !!!!!\n")
                continue
        elif len(input_str) == 3 :
            X, Y =  int(input_str[0]), int(input_str[1])
            Action = input_str[2].lower()
            if (0 <= X < field.width ) & (0 <= Y < field.hight) & (Action in ["open", "flag"]) :
                field.action_type(X, Y, Action)
                if field.bomb_opend_status == 0 :
                    field.save_field("auto_save.txt")
                    field.visualize_field()
                    if field.num_closed_cells == field.num_bombs :
                        print ("\n        !!!!!  YOU  WIN  !!!!!\n         (you can, try again)")
                        break
            else :
                print ("\n!!!!!  Incorrect input  !!!!!\n")
        else :
            print ("\n!!!!!  Incorrect input  !!!!!\n")
    if field.bomb_opend_status == 1 : 
        field.open_all()
        field.visualize_field()
        print ("\n        !!!!!  YUO LOSE  !!!!!\n       (don't worry, try again)")

main()
