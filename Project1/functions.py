from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from random import random, seed
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import make_pipeline
from sklearn.utils import resample
from imageio import imread
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


        
def LinReg(X_train, X_test, y_train, y_test):
    OLSbeta = np.linalg.pinv(X_train.T @ X_train) @ X_train.T @ y_train
    ytildeTrain = X_train @ OLSbeta
    ytildeTest = X_test @ OLSbeta
    return ytildeTrain, ytildeTest, OLSbeta


def RidgeReg(X_train, X_test, y_train, y_test,lmb):
    Ridgebeta = np.linalg.pinv(X_train.T @ X_train + lmb*np.identity(X_train.shape[1])) @ X_train.T @ y_train
    ytildeTrain = X_train @ Ridgebeta
    ytildeTest = X_test @ Ridgebeta
    return ytildeTrain, ytildeTest, Ridgebeta

def LassoReg(X_train, X_test, y_train, y_test,lmb):
    modelLasso = Lasso(lmb,fit_intercept=False)
    modelLasso.fit(X_train,y_train)
    ytildeTrain = modelLasso.predict(X_train)
    ytildeTest = modelLasso.predict(X_test)
    return ytildeTrain, ytildeTest


def R2(y_data, y_model):
    return 1 - np.sum((y_data - y_model) ** 2) / np.sum((y_data - np.mean(y_data)) ** 2)

def MSE(y_data,y_model):
    n = np.size(y_model)
    return np.sum((y_data-y_model)**2)/n

def Beta_std(var,X_train,Beta,p):
    Beta_var = var*np.linalg.pinv(X_train.T @ X_train)
    err = []
    for p_ in range(p):
        err = np.append(err,Beta_var[p_,p_] ** 0.5)
    return err
    

