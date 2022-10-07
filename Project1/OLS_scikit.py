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
from Functions import DesignMatrix, LinReg, RidgeReg, LassoReg, MSE, R2, Beta_std
from FrankeFunction import FrankeFunction


#Define maximal model complexity
maxdegree= 5

# Generate dataset with n observations
n = 100
x1 = np.random.uniform(0,1,n)
x2 = np.random.uniform(0,1,n)

##Define noise
var = 0.01
noise = np.random.normal(0,var,n)

#y = FrankeFunction(x1,x2) + noise 

##Simple benchmark test the function a bi-variate polynomial of degree 2
y=np.ones(n)+x1+x2+x1*x2+(x1**2)+(x2**2)

x1 = np.array(x1).reshape(n,1)
x2 = np.array(x2).reshape(n,1)
x = np.hstack((x1,x2)).reshape(n,2)
y = np.array(y).reshape(n,1)

#Split train (80%) and test(20%) data before looping on polynomial degree
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Scaling data Scikit
#scaler = StandardScaler()
#x_train = scaler.fit_transform(x_train)
#x_test = scaler.fit_transform(x_test)

#Scaling manual
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
predictor = []

for degree in range(maxdegree):
    
    #OLS with scikit-learn
    model = Pipeline([('poly', PolynomialFeatures(degree=degree+1)),('linear',\
                  LinearRegression(fit_intercept=False))])
    model = model.fit(x_train,y_train) 
    Beta = model.named_steps['linear'].coef_
    predictor=np.append(predictor,Beta)

    y_fit = model.predict(x_train)
    y_pred = model.predict(x_test) 
    
#    y_fit = y_fit + np.mean(y_train)
#    y_pred = y_pred + np.mean(y_train)
#    y_test = y_test + np.mean(y_train)
#    y_train = y_train + np.mean(y_train)

    polydegree[degree] = degree+1
    TestError[degree] = MSE(y_test,y_pred)
    TrainError[degree] = MSE(y_train,y_fit)
    TestR2[degree] = R2(y_test,y_pred)
    TrainR2[degree] = R2(y_train,y_fit)
    
    #Display regression results for each polynomial degree
    print("\n\n\nModel complexity:")
    print(degree+1)
    print("\nOptimal estimator Beta")
    print(Beta.shape)
    print("\nTraining error")
    print("MSE =",MSE(y_train,y_fit))
    print("R2 =",R2(y_train,y_fit))
    print("\nTesting error")
    print("MSE =",MSE(y_test,y_pred))
    print("R2  =",R2(y_test,y_pred))


#####Plots####
    
#MSE
plt.plot(polydegree, TestError,'r-o' , label='Test MSError')
plt.plot(polydegree, TrainError,'b-o', label='Train MSError')

plt.xlabel("model complexity (degree)")
plt.ylabel("Mean squared error")
plt.legend()
plt.savefig("Results/OLS/OLS_scikit_MSE_vs_complexity.png",dpi=150)
plt.show()

#R2 score
plt.plot(polydegree, TestR2,'r-d', label='Test R2')
plt.plot(polydegree, TrainR2, 'b-d',label='Train R2')
plt.xticks(np.arange(1, len(polydegree)+1, step=1)) # Set label locations.
plt.xlabel("model complexity (degree)")
plt.ylabel("R2 score")
plt.legend()
plt.savefig("Results/OLS/OLS_scikit_R2_vs_complexity.png",dpi=150)
plt.show()

#Beta coefficients
print(predictor.shape)

plt.plot(predictor[0:3],'md-' , label='degree=1')
plt.plot(predictor[3:9],'r-*' , label='degree=2')
plt.plot(predictor[9:19],'b-*' , label='degree=3')
plt.plot(predictor[19:34],'g*-' , label='degree=4')
plt.plot(predictor[34:55],'y*-' , label='degree=5')

locs, labels = plt.xticks()  # Get the current locations and labels.
plt.xticks(np.arange(0, 1, step=1))  # Set label locations.
plt.xticks(np.arange(21), [r'$\beta_0$', r'$\beta_1$', r'$\beta_2$', \
           r'$\beta_3$', r'$\beta_4$', r'$\beta_5$', \
           r'$\beta_6$', r'$\beta_7$', r'$\beta_8$', \
           r'$\beta_9$', r'$\beta_{10}$', r'$\beta_{11}$', \
           r'$\beta_{12}$', r'$\beta_{13}$', r'$\beta_{14}$', \
           r'$\beta_{15}$', r'$\beta_{16}$', r'$\beta_{17}$', \
           r'$\beta_{18}$', r'$\beta_{19}$', r'$\beta_{20}$',r'$\beta_{21}$'\
           ], rotation=45)  # Set text labels.

plt.ylabel("Optimal Beta - predictor value")
plt.legend()
plt.savefig("Results/OLS/OLS_Optimal_Beta_scikit.png",dpi=150)










