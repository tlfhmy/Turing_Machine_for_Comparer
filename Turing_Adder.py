from graphviz import Digraph

"""
...Lambda Lambda Lambda..Lambda Lambda S  b  b  b  b  b ... b M b b b b ... b Lambda Lambda Lambda...  ->   the tape
                        |              |       |              |           |
                   result bits       init   first number     sep    second number
"""


class ptr:

    def __init__(self, status, position, final_status, trans_dict):
        self.status = status
        self.position = position
        self.final_status = final_status
        self.trans_dict = trans_dict

    def trans(self, cont) -> str:
        if not (cont, self.status) in self.trans_dict:
            self.status = self.final_status
            return cont
        # print((self.status, self.position))
        tmp = self.trans_dict[(cont, self.status)]
        self.position += tmp[2]
        self.status = tmp[1]
        return tmp[0]


class Machine:

    def __init__(self, n):
        self.n = n
        self.tape = ['Lambda'] * (3 * n + 11)
        self.status = ['q0', 'gr', 'r', 'rg', 'rg1', 'rg0',
                       'rg11', 'rg00', 'gl', 'l', 'lg',
                       'lg1', 'lg0', 'lg11', 'lg00', 'lg0p', 'lg1p', 'lp', 'lpp',
                       'rf', 'ff', 'ff0', 'ff1', 'f1', 'f',
                       '0_check_R', '1_check_R', 'R_set_1', 'R_set_0', '0_CR', '1_CR']
        self.init_status = 'q0'
        self.init_cell = 6 + self.n
        self.final_status = 'f'
        self.alphabets = ['0', '1', 'X', 'Lambda', 'R', 'M', 'S']
        self.program = None
        self.init_program()

    def set_numbers(self, n1, n2):
        n1_s = format(n1, "b").zfill(self.n)
        n2_s = format(n2, "b").zfill(self.n)
        self.tape[6 + self.n] = 'S'
        self.tape[6 + 2 * self.n + 1] = "M"
        self.tape[2] = '0'
        self.tape[3] = 'R'
        for i in range(self.n):
            self.tape[i + 7 + self.n] = n1_s[i]
            self.tape[i + 7 + 2 * self.n + 1] = n2_s[i]

    def init_program(self):
        prog = []

        # Initial step, to get the first bit of the second number
        prog.extend([(('S', 'q0'), ('S', 'gr', 1)), (('1', 'gr'), ('1', 'gr', 1)),
                     (('0', 'gr'), ('0', 'gr', 1)), (('M', 'gr'), ('M', 'r', 1))])
        prog.extend([(('1', 'r'), ('1', 'r', 1)), (('0', 'r'), ('0', 'r', 1)),
                     (('Lambda', 'r'), ('Lambda', 'rg', -1)), (('X', 'r'), ('X', 'rg', -1))])

        # Get the first bit of the rest bits of the second number, and set it to 'X'
        prog.extend([(('1', 'rg'), ('X', 'rg1', -1)), (('0', 'rg'), ('X', 'rg0', -1))])

        # Skip the others bits
        for p in ['1', '0', 'X', 'M', 'S']:
            for q in ['rg1', 'rg0']:
                prog.append(((p, q), (p, q, -1)))

        # Put the bit which we got to the result bits
        prog.extend([(('Lambda', 'rg0'), ('Lambda', 'rg00', -1)),
                     (('Lambda', 'rg1'), ('Lambda', 'rg11', -1)),
                     (('Lambda', 'rg00'), ('0', '0_check_R', -1)),
                     (('Lambda', 'rg11'), ('1', '1_check_R', -1))])

        # Skip set bit till Lambda while present status with rg00 or rg11
        for p in ['0', '1']:
            for q in ['rg00', 'rg11']:
                prog.append(((p, q), (p, q, -1)))

        # Skip all alphabet till 'R' while present status is 0_check_R or 1_check_R
        for p in ['0', '1', 'Lambda']:
            for q in ['0_check_R', '1_check_R']:
                prog.append(((p, q), (p, q, -1)))

        # Check overflow and handle these cases
        prog.extend([(('R', '0_check_R'), ('R', '0_CR', -1)), (('R', '1_check_R'), ('R', '1_CR', -1)),
                     (('0', '0_CR'), ('0', 'gl', 1)), (('0', '1_CR'), ('0', 'gl', 1)),
                     (('1', '0_CR'), ('0', 'R_set_1', 1)), (('1', '1_CR'), ('1', 'R_set_0', 1))])
        prog.extend([(('Lambda', 'R_set_0'), ('Lambda', 'R_set_0', 1)),
                     (('Lambda', 'R_set_1'), ('Lambda', 'R_set_1', 1)),
                     (('R', 'R_set_0'), ('R', 'R_set_0', 1)),
                     (('R', 'R_set_1'), ('R', 'R_set_1', 1))])
        prog.extend([(('0', 'R_set_0'), ('0', 'gl', 1)), (('0', 'R_set_1'), ('1', 'gl', 1)),
                     (('1', 'R_set_0'), ('0', 'gl', 1)), (('1', 'R_set_1'), ('1', 'gl', 1))])

        prog.extend([(('0', 'rg00'), ('0', 'rg00', -1)), (('1', 'rg00'), ('1', 'rg00', -1)),
                     (('P', 'rg00'), ('1', 'gl', 1))])

        # Go back to the initial position and prepare to get the corresponding bit in the first number
        for p in ['0', '1', 'Lambda', 'R']:
            prog.append(((p, 'gl'), (p, 'gl', 1)))

        # To get the corresponding bit of the first number
        prog.extend([(('S', 'gl'), ('S', 'l', 1)),
                     (('1', 'l'), ('1', 'l', 1)), (('0', 'l'), ('0', 'l', 1)),
                     (('M', 'l'), ('M', 'lg', -1)), (('X', 'l'), ('X', 'lg', -1))])
        prog.extend([(('1', 'lg'), ('X', 'lg1', -1)), (('0', 'lg'), ('X', 'lg0', -1))])
        for p in ['1', '0', 'S']:
            for q in ['lg1', 'lg0']:
                prog.append(((p, q), (p, q, -1)))

        # Put the bit we got to the result bits and handle some cases
        prog.extend([(('Lambda', 'lg1'), ('Lambda', 'lg11', -1)),
                     (('Lambda', 'lg0'), ('Lambda', 'lg00', -1))])
        # Skip the last bits
        for p in ['0', '1']:
            for q in ['lg00', 'lg11']:
                prog.append(((p, q), (p, q, -1)))

        # Handling these cases
        prog.extend([(('Lambda', 'lg00'), ('Lambda', 'lg0p', 1)), (('Lambda', 'lg11'), ('Lambda', 'lg1p', 1)),
                     (('0', 'lg0p'), ('0', 'q0', 1)), (('0', 'lg1p'), ('1', 'q0', 1)),
                     (('1', 'lg0p'), ('1', 'q0', 1)), (('1', 'lg1p'), ('0', 'lp', -1)),
                     (('Lambda', 'lp'), ('Lambda', 'lp', -1)), (('R', 'lp'), ('R', 'lpp', -1)),
                     (('0', 'lpp'), ('1', 'q0', 1))])

        # Go back to the initial position and execute the next bit
        for p in ['0', '1', 'Lambda', 'R']:
            prog.append(((p, 'q0'), (p, 'q0', 1)))

        # When we handle all the bits, then halt.

        prog.extend([(('X', 'gr'), ('X', 'gr', 1)),
                     (('M', 'rg'), ('M', 'rf', -1))])

        for p in ['0', '1', 'X', 'S', 'Lambda']:
            prog.append(((p, 'rf'), (p, 'rf', -1)))

        prog.extend([(('R', 'rf'), ('R', 'ff', -1)), (('0', 'ff'), ('0', 'ff0', 1)),
                     (('1', 'ff'), ('0', 'ff1', 1))])

        for p in ['Lambda', 'R']:
            for q in ['ff0', 'ff1']:
                prog.append(((p, q), (p, q, 1)))

        prog.extend([(('0', 'ff0'), ('0', 'f', 0)), (('1', 'ff0'), ('1', 'f', 0)),
                     (('0', 'ff1'), ('0', 'f1', -1)), (('Lambda', 'f1'), ('1', 'f', 0)),
                     (('1', 'ff1'), ('1', 'f1', -1))])

        res_dict = {}
        for ele in prog:
            if ele in res_dict:
                print("Duplicated transposition exists!")
                break
            res_dict[ele[0]] = ele[1]

        self.program = res_dict

    def execute(self):
        Pointor = ptr(self.init_status, self.init_cell, self.final_status, self.program)
        while True:
            last_position = Pointor.position
            # print(self.tape)
            self.tape[last_position] = Pointor.trans(self.tape[Pointor.position])
            if Pointor.status == self.final_status:
                res = []
                i = Pointor.position
                while self.tape[i] != "Lambda":
                    res.append(self.tape[i])
                    i += 1
                return res

    def generGraph(self):
        g = Digraph("Adder")
        for ele in self.status:
            if ele == self.init_status:
                g.node(name=ele, color="green", shape="doublecircle")
            elif ele == self.final_status:
                g.node(name=ele, color="red", shape="parallelogram")
            else:
                g.node(name=ele)

        for k, v in self.program.items():
            if k[1] == v[1]:
                if k[1] in ['rf', 'rg1', 'rg0', 'gr', 'q0', 'ff1', 'ff0',
                            'rg00', 'rg11', 'lg00', 'lg11',
                            '0_check_R', '1_check_R',
                            'R_set_0', 'R_set_1',
                            'gl', 'l',
                            'lg0', 'lg1']:
                    continue
            g.edge(k[1], v[1], f'({k[0]},{v[0]},{v[2]})')
        g.edge('rf', 'rf', '(t,t,-1) t in {0,1,X,S,Lambda}')
        g.edge('rg1', 'rg1', '(t,t,-1) t in {0,1,X,S,M}')
        g.edge('rg0', 'rg0', '(t,t,-1) t in {0,1,X,S,M}')
        g.edge('gr', 'gr', '(t,t,1) t in {0,1,X}')
        g.edge('q0', 'q0', '(t,t,1) t in {0,1,R,Lambda}')
        g.edge('ff1', 'ff1', '(t,t,1) t in {R,Lambda}')
        g.edge('ff0', 'ff0', '(t,t,1) t in {R,Lambda}')
        g.edge('rg00', 'rg00', '(t,t,-1) t in {0,1}')
        g.edge('rg11', 'rg11', '(t,t,-1) t in {0,1}')
        g.edge('0_check_R', '0_check_R', '(t,t,-1) t in {0,1,Lambda}')
        g.edge('1_check_R', '1_check_R', '(t,t,-1) t in {0,1,Lambda}')
        g.edge('R_set_0', 'R_set_0', '(t,t,1) t in {R,Lambda}')
        g.edge('R_set_1', 'R_set_1', '(t,t,1) t in {R,Lambda}')
        g.edge('gl', 'gl', '(t,t,1) t in {0,1,R,Lambda}')
        g.edge('l', 'l', '(t,t,1) t in {0,1}')
        g.edge('lg0', 'lg0', '(t,t,-1) t in {0,1,S}')
        g.edge('lg1', 'lg1', '(t,t,-1) t in {0,1,S}')
        g.edge('lg00', 'lg00', '(t,t,-1) t in {0,1}')
        g.edge('lg11', 'lg11', '(t,t,-1) t in {0,1}')
        g.render("Adder.gv", view=True)


tst = Machine(32)
m, n = 123223, 43234
tst.set_numbers(m, n)
print(tst.tape)
# print(len(tst.tape))
res = tst.execute()
print(tst.tape)
print(res)
tst.generGraph()
print(int(''.join(res), 2))
print(m + n)
