class Class():
    def __init__(self):
        self.dict = {'key': self.f}
    def f(self, s):
        return s + ' procesed.'

c = Class()
for v in c.dict:
    print(c.dict[v](v))
