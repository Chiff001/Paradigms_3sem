class unique(object):
    def __init__(self, items, **kwargs):
        if "ignore_case" not in kwargs.keys():
            self._ignore_case = False
        else:
            self._ignore_case = kwargs["ignore_case"]
        self.a = []
        for i in items:
            if self._ignore_case:
                x = i.lower()
            else:
                x = i
            if x not in self.a:
                self.a.append(x)
        self.ind = 0

    def __next__(self):
        if self.ind != len(self.a):
            print(self.a[self.ind])
            self.ind += 1

    def __iter__(self):
        return self
