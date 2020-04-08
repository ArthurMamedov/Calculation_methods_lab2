if __name__ != '__main__':
    exit()

from Rectangle import Rectangle
from Trapezoid import Trapezoid
from Simpson import Simpson
from prettytable import PrettyTable
from modules import dispenser, interval, find_best, wrapper, draw_function, stop_therads
from threading import Thread
from time import time

acc = '{:.7f}'.format
threads = list()
try:
    while True:
        formula = input('Enter the formula: ')  #my variant: (3 * (x) + 4) / (2 * (x) + 7) 
        if formula == 'exit':
            exit()
        a = float(input('Enter "a": '))
        b = float(input('Enter "b": '))
        n = int(input('Enter "n": '))
        rct = Rectangle(formula)
        trp = Trapezoid(formula)
        sim = Simpson(formula)
        h = (b - a) / n; print(f'h is {h}')

        Names = ['Left rectangle', 'Right rectangle', 'Middle rectangle', 'Trapezoid', 'Simpson']

        Integrals = [
            rct.integral_left,
            rct.integral_right,
            rct.integral_middle,
            trp.get_integral_value,
            sim.get_integral_value
        ]

        Runge = [
            rct.runge_left,
            rct.runge_right,
            rct.runge_middle,
            trp.runge,
            sim.runge
        ]

        Methods = {
            'Left rectangles' : rct.integral_left,
            'Right rectangles' : rct.integral_right,
            'Middle rectangles' : rct.integral_middle,
            'Trapezoids' : trp.get_integral_value,
            'Simpson' : sim.get_integral_value
        }

        Errors = {
            'Left rectangles' : rct.runge_left,
            'Right rectangles' : rct.runge_right,
            'Middle rectangles' : rct.runge_middle,
            'Trapezoids' : trp.runge,
            'Simpson' : sim.runge
        }

        results = dict()
        threads = [
            Thread(daemon=True, target=wrapper, args=(results, 'Left rectangles', rct, a, b, 'l')),
            Thread(daemon=True, target=wrapper, args=(results, 'Right rectangles', rct, a, b, 'r')),
            Thread(daemon=True, target=wrapper, args=(results, 'Middle rectangles', rct, a, b, 'm')),
            Thread(daemon=True, target=wrapper, args=(results, 'Trapezoids', trp, a, b)),
            Thread(daemon=True, target=wrapper, args=(results, 'Simpson', sim, a, b)),
        ]


        for therad in threads:
            therad.start()

        tbl = PrettyTable()
        tbl.add_column('', ['Integral value with h', 'Integral value with h/2', 'Runge error'])
        for name, val, err in zip(Names, Integrals, Runge):
            tbl.add_column(name, (acc(val(a, b, h)), acc(val(a, b, h / 2)), acc(err(a, b, h))))
        print(tbl)
        print('Calculating the best "n" for all methods. This may take a long time. Please, wait.')

        drawer = Thread(target = draw_function, args = (rct.f, a, b))
        drawer.run()

        for therad in threads:
            therad.join()

        for name, n in zip(results.keys(), results.values()):
            print(f'{name}s best n: {n}')
            print(f'\tValue: {acc(Methods[name](a, b, (b - a) / n))}, error: {acc(Errors[name](a, b, (b - a) / n))}')


except KeyboardInterrupt:
    try:
        stop_therads = True
        print('Program finished.')
        exit()
    except:
        pass
except:
    print('Unexpected error happend!')