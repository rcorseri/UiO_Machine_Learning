
###Author: R Corseri

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.utils import resample

from functions import LinReg, RidgeReg, LassoReg
from DesignMatrix import DesignMatrix
import FrankeFunction as FF


#Model complexity - polynomial degree up to 10
maxdegree= 5

#Number of bootstraps
n_bootstraps = 75

#For Ridge regression, set up the hyper-parameters to investigate
nlambdas = 9
lambdas = np.logspace(-4, 4, nlambdas)


# Make data set.
n = 100
x1 = np.random.uniform(0,1,n)
x2 = np.random.uniform(0,1,n)
y = FF.FrankeFunction(x1,x2)

#Add normally distributed noise
#y = y + np.random.normal(0,0.1,y.shape)

x1 = np.array(x1).reshape(n,1)
x2 = np.array(x2).reshape(n,1)
x = np.hstack((x1,x2)).reshape(n,2)

#Split train (80%) and test(20%) data before looping on polynomial degree
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    
#Scaling
#y_train_mean = np.mean(y_train)
#x_train_mean = np.mean(x_train)
#x_train = x_train - x_train_mean
#y_train = y_train - y_train_mean
#x_test = x_test - x_train_mean
#y_test = y_test - y_train_mean



#Initialize before looping:
TestError = np.zeros(maxdegree)
TrainError = np.zeros(maxdegree)
TestR2 = np.zeros(maxdegree)
TrainR2 = np.zeros(maxdegree)
polydegree = np.zeros(maxdegree)
predictor =[]

error = np.zeros(maxdegree)
bias = np.zeros(maxdegree)
variance = np.zeros(maxdegree)
polydegree = np.zeros(maxdegree)


#Initialize bootstrap matrice
y_pred = np.empty((y_test.shape[0],n_bootstraps))


for l in range(nlambdas):
    for degree in range(maxdegree):   
        for i in range(n_bootstraps):
            x_, y_ = resample(x_train,y_train)
      
            X_train = DesignMatrix(x_[:,0],x_[:,1],degree+1)
            X_test = DesignMatrix(x_test[:,0],x_test[:,1],degree+1)
            y_fit, y_pred[:,i] = LassoReg(X_train, X_test, y_, y_test,lambdas[l])
                    
        y_test = np.reshape(y_test, (len(y_test),1))
        polydegree[degree] = degree+1
           
        error[degree] = np.mean( np.mean((y_test - y_pred)**2, axis=1, keepdims=True) )
        bias[degree] = np.mean( (y_test - np.mean(y_pred, axis=1, keepdims=True))**2 )
        variance[degree] = np.mean( np.var(y_pred, axis=1, keepdims=True) )
    
    #####Plots for each lambda####
    
    plt.plot(polydegree, error, label='Error')
    plt.plot(polydegree, bias, label='bias')
    plt.plot(polydegree, variance, label='Variance')
    plt.xticks(np.arange(1, len(polydegree)+1, step=1))  # Set label locations.
    plt.ylabel('Mean squared error')
    plt.xlabel('Model complexity')
    plt.title('Bias-Variance trade off (Lasso Reg) for lambda = %.0e' %lambdas[l])
    plt.legend()
    plt.savefig("Results/Lasso/Lasso_Bias_Variance_trade_off_lambda=%.0e.png" %lambdas[l],dpi=150)
    plt.show()
    

    

















