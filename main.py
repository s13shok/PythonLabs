class Calculator():
    def plus(self, a:int, b:int):
        if not isinstance(a, int) or not isinstance(b, int):
            raise Exception("No int")
        return a+b