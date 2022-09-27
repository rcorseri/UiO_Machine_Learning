###This program performs Ordinary least square regression on a synthetic dataset generated by the Franke Function
###and returns model evalutation (MSE and R2) and optimal predictor
###The loop is on polynomial degree
###Author: R Corseri

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
from sklearn.model_selection import KFold

from functions import LinReg
from DesignMatrix import DesignMatrix
import FrankeFunction as FF
import Calculate_MSE_R2 as error


#Model complexity (polynomial degree up to 7)
maxdegree= 10

#Number of k-fold (between 5 and 10) for cross-validation
k = 5
kfold = KFold(n_splits = k)

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

#Scaling
#y_train_mean = np.mean(y_train)
#x_train_mean = np.mean(x_train)
#x_train = x_train - x_train_mean
#y_train = y_train - y_train_mean
#x_test = x_test - x_train_mean
#y_test = y_test - y_train_mean



#Initialize before looping:
polydegree = np.zeros(maxdegree)
error_Kfold = np.zeros((maxdegree,k))
estimated_mse_Kfold = np.zeros(maxdegree)
bias = np.zeros(maxdegree)
variance = np.zeros(maxdegree)



i=0

#OLS
for degree in range(maxdegree): 
    j=0
    for train_inds, test_inds in kfold.split(x):
        
        x_train = x[train_inds]
        y_train = y[train_inds]   
        x_test = x[test_inds]
        y_test = y[test_inds]
             
        X_train = DesignMatrix(x_train[:,0],x_train[:,1],degree+1)
        X_test = DesignMatrix(x_test[:,0],x_test[:,1],degree+1)
        y_fit, y_pred, Beta = LinReg(X_train, X_test, y_train, y_test)
        
        error_Kfold[i,j] = error.MSE(y_test,y_pred)
        
        j+=1
        
    estimated_mse_Kfold[degree] = np.mean(error_Kfold[i,:])
    polydegree[degree] = degree+1
    
    i+=1
     

#####Plots####
    
plt.plot(polydegree, estimated_mse_Kfold, label='Error Cross Validation')
plt.xticks(np.arange(1, len(polydegree)+1, step=1))  # Set label locations.
plt.xlabel('Model complexity')
plt.legend()
plt.savefig("Results/Error_CrossValidation.png",dpi=150)
plt.show()















