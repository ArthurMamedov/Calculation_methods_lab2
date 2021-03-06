from modules import *
from functools import lru_cache


class Rectangle:
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
    def get_integral_value(self, a, b, h, param = 'l'):
        if param == 'l':
            return h * sum([self.f(x) for x in interval(a, b, h)])
        elif param == 'm':
            return h * sum([self.f((x + x + h) / 2) for x in interval(a, b, h)])
        elif param == 'r':
            return h * sum([self.f(x) for x in interval(a + h, b + h, h)])
        else:
            raise RuntimeError('Parameter error: param shall be either "l", or "m", or "r".')

        
    def integral_left(self, a, b, h):
        return self.get_integral_value(a, b, h, 'l')


    def integral_middle(self, a, b, h):
        return self.get_integral_value(a, b, h, 'm')


    def integral_right(self, a, b, h):
        return self.get_integral_value(a, b, h, 'r')


    @lru_cache
    def runge(self, a, b, h, param = 'l'):
        by_h = self.get_integral_value(a, b, h, param)
        by_h_2 = self.get_integral_value(a, b, h / 2, param)
        res = (by_h_2 - by_h) / (3 if param == 'm' else 1)
        return res


    def runge_left(self, a, b, h):
        return self.runge(a, b, h, 'l')

    
    def runge_middle(self, a, b, h):
        return self.runge(a, b, h, 'm')


    def runge_right(self, a, b, h):
        return self.runge(a, b, h, 'r')


if __name__ == '__main__':
    tmp = Rectangle('(x)**2')
    print(tmp.get_integral_value(1, 4, 0.0001, 'l'))
    print(tmp.get_integral_value(1, 4, 0.0001, 'm'))
    print(tmp.get_integral_value(1, 4, 0.0001, 'r'))
    print(tmp.runge(1, 4, 0.0001, 'l'))
    print(tmp.runge(1, 4, 0.0001, 'm'))
    print(tmp.runge(1, 4, 0.0001, 'r'))
