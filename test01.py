class Test():
    def __init__(self, value):
        self.value = value

    def add1(self):
        self.value += 1

test1 = Test(1)
print(test1.value)
test1.add1()
print(test1.value)
