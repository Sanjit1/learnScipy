import scipy.optimize as optimize
import numpy as np

zee = [0.003652, 0.003532, 0.003103, 0.002877]
ex = [10.04225, 9.54709, 8.14034, 7.30594]
why = [1012.728, 870.188, 539.420, 389,968]



def f(params):
    # print(params)  # <-- you'll see that params is a NumPy array
    a, b, c = params # <-- for readability you may wish to assign names to the component variables
    sum = 0
    for i in range(1, 4):
        sum += ((a+b*ex[i]+c*why[i])-zee[i])**2
    return sum

initial_guess = [0.002108508173, 0.00007979204727, 0.0000006535076315]
result = optimize.minimize(f, initial_guess, method='Powell')
if result.success:
    fitted_params = result.x
    print(fitted_params)
    print(f(fitted_params))
else:
    raise ValueError(result.message) 