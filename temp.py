import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg, optimize
import scipy.optimize as OP
from sympy import *
# TODO: GUI it or make it easier to edit

temp_in_C = [
    0.7,
    2.,
    5.3,
    8.06,
    9.95,
    14.82,
    20.4,
    29.6,
    41.,
    49.1,
    53.9,
    60.,
    65.,
    70.,
    74.4,
    78.3
]
res_in_ohms = [
    22976.98, 
    21263.83,
    17935,
    15690.9,
    14003.87,
    11851.83,
    9262.09,
    6926.95,
    4575.89,
    3430.07,
    2987.74,
    2436.42,
    2070.49,
    1806.5,
    1489.12,
    1349.3
]


# temp_in_C.sort()
# res_in_ohms.sort(reverse=True) 

list_of_solving_methods = ['Nelder-Mead', 'Powell', 'COBYLA']
initial_guess_13 = [0.002108508173, 0.00007979204727, 0.0000006535076315]
initial_guess_123 = [0.00644441, -0.00164640, 0.000217293, -0.00000805052]
initial_guess_135 = [0.00333904, -0.000266943, 0.00000475034, -0.0000000176248]
initial_guess_1235 = [-0.0761385, 0.0344660, -0.00538390, 0.000316953, -0.000000434551]
initial_guess_1345 = [-0.0369644, 0.0114826, -0.000312489, 0.0000367271, -0.00000129017]
initial_guess_1357 = [-0.0201583, 0.00573250, -0.0000763939, 0.000000634558, -0.00000000206047]
initial_guess_12345 = [1.03172, -0.610294, 0.144445, -0.0170607, 0.00100597, -0.0000236873]
initial_guess_13579 = [0.0990296, -0.0284433, 0.000538900, -0.00000678944, 0.0000000450002, -0.000000000120970]
initial_guess_1357911 = [1.16136, -0.363635, 0.00809594, -0.000128757, 0.00000121005, -0.00000000614569, 0.0000000000130364]

plot_tem = []
plot_res = []
for i in range(2, 5001):
    plot_res.append(i*10)
    plot_tem.append(i)

if(len(temp_in_C) != len(res_in_ohms)):
    print('Temperature list and Resistance list have different lengths')
    print('Temperature List length: ' + str(len(temp_in_C)))
    print('Resistance List length: ' + str(len(res_in_ohms)))
    print('Exiting Now...')
    exit()
else: 
    range_of_data_points = range(0, len(temp_in_C))

mean = 0
for data_index in range_of_data_points:
    mean += temp_in_C[data_index]

mean = mean/(len(range_of_data_points))    

SStot = 0
for data_index in range_of_data_points:
    SStot += (temp_in_C[data_index] - mean)**2

if (len(range_of_data_points) < 3): 
    print("Too few data points. Come back with at least 3 points")
    print("Exiting Now...")
    exit()

mean = 0
for data_index in range_of_data_points:
    mean += temp_in_C[data_index]
mean = mean/(len(range_of_data_points))    

SStot = 0
for data_index in range_of_data_points:
    SStot += (temp_in_C[data_index] - mean)**2

one_over_temp_in_k = [0] * len(range_of_data_points)

for i in range_of_data_points:
    one_over_temp_in_k[i] = float(1/(temp_in_C[i] + 273.15))

log_res = np.log(res_in_ohms)

print('at least here')

class curve:
    def __init__(self, list_of_powers, initial_guess):
        if(not(0 in list_of_powers)):
            list_of_powers.insert(0, 0)
        self.list_of_powers = list_of_powers
        self.initial_guess = initial_guess
        self.fitted_result = initial_guess
        self.range_of_power_series = range(0, len(list_of_powers))
        self.name = str(list_of_powers)

    
    def sum_errors(self, params):
        sum = 0
        for i in range_of_data_points:
            partial_pred_temp = 0
            for index_of_power in self.range_of_power_series:
                partial_pred_temp += params[index_of_power]*log_res[i]**(self.list_of_powers[index_of_power])
            sum += (partial_pred_temp - one_over_temp_in_k[i])**2
        return sum

    def regress(self, initial_guess, tries):
        self.sum = 100
        guess = initial_guess
        while True:
            tries -= 1
            temp_sum = 100
            temp_fit = None
            for m in list_of_solving_methods:
                result = optimize.minimize(self.sum_errors, guess, method=m)
                if (result.success and self.sum_errors(result.x) < self.sum):
                    temp_fit = result.x
                    temp_sum = self.sum_errors(result.x)
            if(temp_sum < self.sum and tries > 0):
                self.sum = temp_sum
                self.fitted_result = temp_fit
                guess = temp_fit
            else:
                break
        return self.fitted_result
    
    def temp(self, res):
        sum_of_power_logs = 0
        for index_of_power in self.range_of_power_series:
            sum_of_power_logs += self.fitted_result[index_of_power]*(np.log(res))**(self.list_of_powers[index_of_power])
        return (1/sum_of_power_logs) - 273.15
    
    def plot(self):
        plt.figure(num='Regression Line ' + self.name)
        plt.title('Regression Line ' + self.name)
        plt.xlabel('Resistance')
        plt.ylabel('Temperature')
        plt.ylim(-10, 125)
        plt.xlim(-50, 50000)
        for res in plot_res:
            plot_tem[plot_res.index(res)] = self.temp(res)
        SSres = 0
        obs_list = []
        for data_index in range_of_data_points:
            SSres += (temp_in_C[data_index] - self.temp(res_in_ohms[data_index]))**2
        r_sq = 1 - (SSres/SStot)
        plt.figtext(.5, .8, "R Sq = " + str(r_sq))
        plt.plot(plot_res, plot_tem)
        plt.scatter(res_in_ohms, temp_in_C)
        plt.plot(range(-250000, 250000, 50000), ([0]*10))
        plt.plot(([0]*3), range(-100, 820, 450))


curves = [curve([1, 3], initial_guess_13), curve([1, 2, 3], initial_guess_123), curve([1, 3, 5], initial_guess_135), curve([1, 2, 3, 4, 5], initial_guess_12345), curve([1, 3, 4, 5], initial_guess_1345), curve([1, 3, 5, 7], initial_guess_1357), curve([1, 3, 5, 7, 9], initial_guess_13579), curve([1, 3, 5, 7, 9, 11], initial_guess_1357911)]

for c in curves:
    c.regress(c.initial_guess, 30)
    c.plot()

plt.show()