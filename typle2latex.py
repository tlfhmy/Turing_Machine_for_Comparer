def t2l(lst):
    def add_(s):
        if len(s) >= 2:
            tmp = s[0] + '_{'
            tmp += s[1:] + '}'
            return tmp
        return s
    for l, r in lst:
        l = list(l)
        r = list(r)
        p0 = l[0]
        q0 = l[1]
        if len(p0) != 1:
            p0 = '\\' + l[0]
        q0 = add_(q0)

        p1 = r[0]
        q1 = r[1]
        m = r[2]
        if len(p1) != 1:
            p1 = '\\' + r[0]
        q1 = add_(q1)

        res = ""

        res += '('
        res += str(p0)
        res += ', '
        res += str(q0)
        res += ') \\mapsto '
        res += '('
        res += str(p1)
        res += ', '
        res += str(q1)
        res += ', '
        res += str(m)
        res += ')'
        print(res)


t2l([(('0', 'ff0'), ('0', 'f', 0)), (('1', 'ff0'), ('1', 'f', 0)),
                     (('0', 'ff1'), ('0', 'f1', -1)), (('Lambda', 'f1'), ('1', 'f', 0)),
                     (('1', 'ff1'), ('1', 'f1', -1))])
