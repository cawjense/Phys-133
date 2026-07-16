import numpy as np
import matplotlib.pyplot as plt
from scipy import stats 
from scipy.optimize import curve_fit

g = 9.81 #m/s^2

L = np.linspace(20,110,10)/100 #"/100" converts cm to m 

periods = np.array([
    [0.897, 0.901, 0.895, 0.898, 0.900],
    [1.099, 1.103, 1.097, 1.101, 1.100],
    [1.270, 1.265, 1.273, 1.268, 1.271],
    [1.420, 1.425, 1.418, 1.422, 1.421],
    [1.556, 1.560, 1.553, 1.558, 1.557],
    [1.680, 1.677, 1.684, 1.681, 1.679],
    [1.794, 1.798, 1.791, 1.796, 1.793],
    [1.902, 1.905, 1.899, 1.903, 1.901],
    [2.007, 2.003, 2.010, 2.005, 2.008],
    [2.102, 2.106, 2.099, 2.104, 2.101]
])
#PART 1
means = np.mean(periods, axis=1)
standard_devs = np.std(periods,axis = 1,ddof = 1)
standard_errorofmean = stats.sem(periods,axis=1)

print(f"Mean:{means}")
print(f"Standard Deviation:{standard_devs}")
print(f"Standard Error of Mean:{standard_errorofmean}")

def func(L,a,b):
    return a*(L**b)


popt, pcov = curve_fit(func,L,means,sigma = standard_errorofmean, absolute_sigma = True)

perr = np.sqrt(np.diag(pcov))

#print(perr)

a = popt[0]
b = popt[1]

print(f"a = {popt[0]} ± {perr[0]:e}")
print(f"b = {popt[1]} ± {perr[1]:e}")

# a = 2pi/sqrt(g)
##(2pi/a)**2 = g

g_e = (2*np.pi/a)**2
g_ee = (8 * np.pi**2 / (a**3)) * perr[0]
#(sigma_g = abs(dg/da)*sigma_a)
print(f"g = {g_e} ± {g_ee}")

est = (g_e - 9.81)/g_ee
print(f"Z-Score = {est}") #Less than 1 but greater than zero, therefore, g_exp is
                          #greater than g_known 

#plt.scatter(L,means)
plt.errorbar(L,means,yerr = standard_errorofmean,fmt = 'o',label = "Average Period (measured)")
plt.plot(L,func(L,a,b), label  = f"Best Fit Curve ($aL^b$)")
plt.grid()
plt.legend()
plt.xlabel("Length (m)")
plt.ylabel("Average Period (s)")
plt.title("Average Time As a Function of Length")
plt.show()



#RESIDUALS 

T_resid = means - func(L,a,b)

plt.errorbar(L,T_resid,yerr = standard_errorofmean, fmt = 'o',label = "Residuals")
plt.axhline(y = 0, color = 'black', linestyle = '--')
plt.grid()
plt.legend()
plt.xlabel("Length (m)")
plt.ylabel('Residual Period (s)')
plt.title("Residuals of Mean Period as a Function of Length")
plt.show()
            

L_test = 100/100
L_test_sigma = 0.5/100
T_test = 2.005
T_test_sigma = 0.004

g_sigma_1 = np.sqrt(np.square(L_test_sigma)+np.square(T_test_sigma))

g = (L_test*4*np.pi**2)/(T_test**2)

g_sigma_2 = g*np.sqrt(np.square(L_test_sigma/L_test)+np.square(T_test_sigma/T_test))

print(f"g_test = {g} ± {g_sigma_2} (fractional)")


print(0.05/100)
print(2*(0.004/2.005))