import pandas as pd
import random


problems = ['Sphere', 'step2', 'rastrigin', 'ackley', 'ellipsoid', 'onemax', 'order5']
gens = [5, 10, 15, 20, 50]
methods = ['RS', 'RS-1', 'RS-5', 'RS-auto', 'RS-auto1'] #, 'RS-auto2', 'RS-auto3', 'RS-auto4', 'RS-auto5', 'RS-auto6']

test = pd.DataFrame(columns=['problem', 'method', 'gens', 'value'])

for p in problems:
    for g in gens:
        for m in methods:
            test = test.append({
                'problem': p,
                'method': m,
                'gens': g,
                'value': random.random(),
                'FFE': random.random(),
            }, ignore_index=True)


test.to_csv('test.csv', index=False)