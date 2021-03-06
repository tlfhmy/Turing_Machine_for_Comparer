from graphviz import Digraph

"""
...Lambda Lambda b R......Lambda Lambda Lambda S  b  b  b  b  b ... b M b b b b ... b Lambda Lambda Lambda...  ->   the tape
                  |             |              |       |              |           |
              overflow      result bits       init   first number     sep    second number
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

    def __init__(self, formula: str):
        self.tape = []
        self.set_formula(formula)
        self.status = []
        self.init_status = 'q0'
        self.init_cell = 3
        self.final_status = 'f'
        self.alphabets = ['0', '1', 'X', 'Lambda', 'R', 'M', 'S']
        self.program = None
        self.init_program()

    def set_formula(self,formula: str):

        self.tape.extend(["Lambda", "Lambda", "Lambda", "S"])

        for ele in formula:
            self.tape.append(ele)

        self.tape.extend(["E", "Lambda", "Lambda", "Lambda"])

    def init_program(self):
        prog = []




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
                res_temp = []
                i = Pointor.position
                while self.tape[i] != "Lambda":
                    res_temp.append(self.tape[i])
                    i += 1
                return res_temp

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
                pass
            g.edge(k[1], v[1], f'({k[0]},{v[0]},{v[2]})')


tst = Machine("((((0&1)&0)|1)|((1&1)|-0)")
print(tst.tape)