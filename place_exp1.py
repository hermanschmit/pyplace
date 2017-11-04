from scipy.optimize import minimize, rosen

x0 = [1.3, 0.7, 0.8, 1.9, 1.2]

if __name__ == '__main__':
    xopt = minimize(rosen, x0, method='Nelder-Mead')
    print xopt
