from graphviz import Digraph

"""
...Lambda    Lambda    Lambda S  b  b  b  b  b ... b M b b b b ... b Lambda Lambda Lambda...  ->   the tape
               |              |       |              |           |
          result bit        init   first number     sep    second number
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
        tmp = self.trans_dict[(cont, self.status)]
        self.position += tmp[2]
        self.status = tmp[1]
        return tmp[0]


class Machine:

    def __init__(self, n):
        self.n = n
        self.tape = ['Lambda'] * (2*n + 8)
        self.status = ['q0', 'q1', 'rs', 'r0', 'r1', 'r00', 'r11', 'fe', 'fee', 'f']
        self.init_status = 'q0'
        self.init_cell = 3
        self.final_status = 'f'
        self.alphabets = ['0', '1', 'S', 'M', 'Lambda', 'X', 'Less', 'Greater', 'Equal']
        self.program = None
        self.init_program()

    def set_numbers(self, n1, n2):
        n1_s = format(n1, "b").zfill(self.n)
        n2_s = format(n2, "b").zfill(self.n)
        self.tape[3] = 'S'
        self.tape[3+self.n+1] = "M"
        for i in range(self.n):
            self.tape[i+4] = n1_s[i]
            self.tape[i+4+self.n+1] = n2_s[i]

    def init_program(self):
        prog = []

        # Initial status, go to the last bit of the first number
        prog.extend([(('S', 'q0'), ('S', 'rs', 1))])

        # Get the last unreached bit of the first number and set it to 'X' and put it in the result bit
        prog.extend([(('0', 'rs'), ('X', 'r0', -1)), (('1', 'rs'), ('X', 'r1', -1)), (('X', 'rs'), ('X', 'rs', 1))])
        prog.extend([(('S', 'r0'), ('S', 'r0', -1)), (('X', 'r0'), ('X', 'r0', -1)),
                     (('S', 'r1'), ('S', 'r1', -1)), (('X', 'r1'), ('X', 'r1', -1))])
        prog.extend([(('Lambda', 'r0'), ('Lambda', 'r00', -1)), (("Lambda", 'r1'), ('Lambda', 'r11', -1)),
                     (('Lambda', 'r00'), ('0', 'q1', 1)), (("Lambda", 'r11'), ('1', 'q1', 1))])

        # Get the last unreached bit of the second number and move to the result bit
        prog.extend([(("Lambda", 'q1'), ("Lambda", 'q1', 1)), (("S", "q1"), ("S", 'q1', 1)),
                     (("0", 'q1'), ('0', 'q1', 1)), (('1', 'q1'), ('1', 'q1', 1)), (("X", 'q1'), ("X", 'q1', 1))])
        prog.extend([(('M', 'q1'), ('M', 'rs', 1))])
        prog.extend([(("M", 'r0'), ("M", 'r0', -1)), (("M", 'r1'), ("M", 'r1', -1)),
                     (("0", 'r0'), ("0", "r0", -1)), (("0", 'r1'), ("0", 'r1', -1)),
                     (("1", 'r0'), ("1", 'r0', -1)), (("1", 'r1'), ("1", 'r1', -1))])

        # Compare the two bits
        prog.extend([(("0", "r00"), ("Lambda", "q0", 1)), (("1", "r11"), ("Lambda", "q0", 1)),
                     (("Lambda", "q0"), ("Lambda", "q0", 1))])
        prog.extend([(("0", "r11"), ("Less", "f", 0)), (("1", "r00"), ("Greater", "f", 0))])
        prog.extend([(("M", "rs"), ("M", "fe", -1)), (("X", "fe"), ("X", "fe", -1)),
                     (("S", "fe"), ("S", "fe", -1)), (("Lambda", "fe"), ("Lambda", "fee", -1)),
                     (("Lambda", "fee"), ("Equal", "f", 0))])

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
            self.tape[last_position] = Pointor.trans(self.tape[Pointor.position])
            if Pointor.status == self.final_status:
                res = []
                i = Pointor.position
                while self.tape[i] != "Lambda":
                    res.append(self.tape[i])
                    i += 1
                return res
            # print(self.tape)

    def generGraph(self):
        g = Digraph("Comparator")
        for ele in self.status:
            if ele == self.init_status:
                g.node(name=ele, color="green", shape="doublecircle")
            elif ele == self.final_status:
                g.node(name=ele, color="red", shape="parallelogram")
            else:
                g.node(name=ele)

        for k, v in self.program.items():
            if k[1] == v[1]:
                if k[1] in ['r0', 'r1', 'fe', 'q1']:
                    continue
            g.edge(k[1], v[1], f'({k[0]},{v[0]},{v[2]})')
        g.edge('r0', 'r0', '(t,t,-1) t in {0,1,S,X,M}')
        g.edge('r1', 'r1', '(t,t,-1) t in {0,1,S,X,M}')
        g.edge('q1', 'q1', '(t,t,1) t in {0,1,S,X,Lambda}')
        g.edge('fe', 'fe', '(t,t,-1) t in {S,X}')
        g.render("Comparator.gv", view=True)



tst = Machine(32)
tst.set_numbers(176253, 176253)
print(tst.tape)
# print(len(tst.tape))
print(tst.execute())
tst.generGraph()