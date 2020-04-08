from modules import *
from functools import lru_cache


class Trapezoid:
    def __init__(self, formula: str):
        self.f = None
        try:
            eval(formula.replace('x', '1'))
        except ZeroDivisionError:
            pass
        except Exception as what:
            print(f'Formula is incorect! Check the sintax.\n{what}')
            exit()
        else:
            def ff(x):
                try:
                    return eval(formula.replace('x', str(x)))
                except ZeroDivisionError:
                    pass
            self.f = ff


    @lru_cache
    def get_integral_value(self, a, b, h):
        res = h * (self.f(a) + self.f(b)) / 2 + h * sum(self.f(x) for x in interval(a + h, b, h))
        return res


    @lru_cache
    def runge(self, a, b, h):
        by_h = self.get_integral_value(a, b, h)
        by_h_2 = self.get_integral_value(a, b, h / 2)
        res = (by_h_2 - by_h) / 3
        return res


if __name__ == '__main__':
    tmp = Trapezoid('(x)**2')
    print(tmp.get_integral_value(1, 4, 0.001))
    print(tmp.runge(1, 4, 0.001))
