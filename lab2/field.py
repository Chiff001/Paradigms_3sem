def field(a, *arg):
    res = []
    for i in a:
        if len(arg) == 1:
            if i[arg[0]] != '':
                res.append(i[arg[0]])
        else:
            b = dict()
            for j in arg:
                if i[j] != '':
                    b[j] = i[j]
            res.append(b)
    print(res)
