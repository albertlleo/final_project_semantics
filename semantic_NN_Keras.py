#!/usr/bin/env python
# coding: utf-8

# In[31]:



import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import ParameterGrid
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import random
from joblib import Parallel, delayed
from sklearn.base import BaseEstimator
import warnings
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras. models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import LearningRateScheduler
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.regularizers import l2


# In[ ]:





# In[32]:


# loading the dataset
df = pd.read_csv("5-features-full-corpus.csv.csv")
feature_columns = df.columns 

df = df.drop('verb_POS', axis=1)
df.head()


# In[ ]:





# In[33]:


# Fix random seed for reproducibility
seed = 7
np.random.seed(seed)
from keras.utils import to_categorical

#df_replace = df.copy()
# df.loc[df['lastmention'] >= 5, 'lastmention'] = 5
# df.loc[(df['lastmention'] < 5) & (df['lastmention'] != -1) , 'lastmention'] = 1

#print(df.head())


# Model has been trained

# In[373]:
# encoded = pd.get_dummies(df['lastmention'], prefix=['lastmention'])
# np.array(encoded)
# df = df.join(encoded)

df.head()


# In[34]:


# pd.get_dummies(df['last_ment'])


# In[35]:


# df_replace = df.copy()
# df_replace.loc[df_replace['length'] <= 5, 'length'] = 0
# df_replace.loc[df_replace['length'] > 5, 'length'] = 1
# #X.loc['4'] = int(X.loc['column_name'])
# #df_replace.loc[:,'4'] =  df_replace.loc[:,'column_name']
# df_replace = df_replace.drop(columns =['lastmention'])
# print(df_replace.head())


# In[38]:


# Splitting dataset into features (X) and target variables (Y)
X = df.iloc[:, 5:19]
Y = df.loc[:, 'target_form']
del X['target_form']

X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.2)


#from keras.utils.np_utils import to_categorical
# y_train = to_categorical(y_train)
#y_val = to_categorical(y_val) 


# In[39]:


X_train


# In[40]:


y_val = np.array(y_val)
y_train = np.array(y_train)


# In[52]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler(with_mean=False)

scaler.fit(X_train)

# Transforming the data:
X_train = np.array(scaler.transform(X_train))
X_val = np.array(scaler.transform(X_val))


# In[374]:


#Setting hyper-parameter in logarithmic range
no_func_parameter = 10
#hyper_parameter = np.logspace(-5, 0, num=no_hyper_parameter, base=10)
hyper_parameter = 10. ** np.arange(-5, 4)
#Defining other parameters
layer_dim1 = 13
layer_dim2 =  80
node_no1 = 256
node_no2 = 512
batch_size = 128

Epoch = 1000
repeat = 10

func = 'hyper_parameter'


# In[375]:


for a in hyper_parameter:
    print(a)


# In[53]:


def main():
        sc__train_list = []
        sc__val_list = []
        score_train_list = []
        score_val_list = []

        ls__train_list = []
        ls__val_list = []
        lost_train_list = []
        lost_val_list = []

        sc_max = []
        max_list = []

        # Loading the data set (PIMA Diabetes Dataset)
        #dataset = np.loadtxt('pima-indians-diabetes.csv', delimiter=",")

        # Initializing the Sequential model from KERAS.
        model = Sequential()

        # Creating a 16 neuron hidden layer with Linear Rectified activation function.
        model.add(Dense(node_no1, input_dim=layer_dim1, use_bias=True, bias_initializer='zeros'))

        model.add(Dense(node_no2, input_dim=layer_dim2,
                        kernel_regularizer=l2(0.00001), activation='relu'))

        # Adding a output layer
        model.add(Dense(1, activation='sigmoid'))

        # Compiling the model
        model.compile(loss='mean_squared_error',
                      optimizer='Adam', metrics=['accuracy'])
        
        lr_model_history = model.fit(X_train, y_train, epochs=Epoch, batch_size=256, validation_data=(X_val, y_val))
        score = model.evaluate(X_val, y_val, batch_size=batch_size)
        lr_model_history.history['accuracy']


# In[54]:


main()


# In[49]:





# In[19]:


def experiment(a):
    
#Loop through all Hyper-parameters and then repeat

    for r in np.arange(repeat):
             
        lr_model_history = model.fit(X_train, y_train, epochs=Epoch,
        batch_size=128, validation_data=(X_val, y_val))
        score = model.evaluate(X_val, y_val, batch_size=batch_size)
        
        sc__train_list.append(lr_model_history.history['accuracy'])
        ls__train_list.append(lr_model_history.history['loss'])                 
                              
        sc__val_list.append(lr_model_history.history['val_accuracy'])                    
        ls__val_list.append(lr_model_history.history['val_loss'])
                            
    score_train_list.append(np.mean(sc__train_list))
    score_val_list.append(np.mean(sc__val_list))                     
                              
    lost_train_list.append(np.mean(ls__train_list))
    lost_val_list.append(np.mean(ls__val_list))
    
    
    return r


# In[ ]:





# In[20]:


def plot_function_epoch(r):
    #Create required sequence
    N = []
    for i in range(0, no_func_parameter):
        N.append(i)
    
    # Plot the loss function
    fig, ax = plt.subplots(1, 1, figsize=(10,6))
    #ax.plot(np.sqrt(lr_model_history.history['val_loss']), 'b' ,label='val')
    #ax.plot(np.sqrt(lr_model_history.history['loss']), 'r', label='train')
    ax.plot(np.sqrt(lost_val_list), 'b' ,label='Validation')
    ax.plot(np.sqrt(lost_train_list), 'r', label='Train')
    
    plt.suptitle("Experiment with " + str(r) + " repeats", fontsize=18)
    plt.title("Loss as function of " + func + " Epoch= " + str(Epoch) )
    ax.set_xlabel(r'Epoch', fontsize=20)
    ax.set_ylabel(r'Loss', fontsize=20)
    ax.legend()
    ax.tick_params(labelsize=20)
    plt.xlim(0, len(lost_val_list))
    plt.savefig('LossE' + str(Epoch) + 'rpt' + str(repeat) + '.png')
    plt.show()

    # Plot the accuracy
    fig, ax = plt.subplots(1, 1, figsize=(10,6))
    #ax.plot(np.sqrt(lr_model_history.history['accuracy']), 'r' ,label='train')
    #ax.plot(np.sqrt(lr_model_history.history['val_accuracy']), 'b' ,label='val')
    ax.plot(np.sqrt(score_val_list), 'b' ,label='Validation')
    ax.plot(np.sqrt(score_train_list), 'r', label='Train')

    plt.title("Accuracy as function of " + func)
    ax.set_xlabel(r'Epoch', fontsize=20)
    ax.set_ylabel(r'Accuracy', fontsize=20)
    ax.legend()
    ax.tick_params(labelsize=20)
    plt.savefig('AccuracyE' + str(Epoch) + 'rpt' + str(repeat) +'.png')
    plt.show()


# In[382]:


def plot_function_alpha(r):
    #a ya gerek yok çünkü a'nın fonksiyonu olacak
    #Create required sequence
    N = []
    for i in range(0, no_func_parameter):
        N.append(i)
    
    # Plot the loss function
    fig, ax = plt.subplots(1, 1, figsize=(10,6))
    #ax.plot(np.sqrt(lr_model_history.history['val_loss']), 'b' ,label='val')
    #ax.plot(np.sqrt(lr_model_history.history['loss']), 'r', label='train')
    ax.plot(np.sqrt(lost_val_list), 'b' ,label='Validation')
    ax.plot(np.sqrt(lost_train_list), 'r', label='Train')
    
    plt.suptitle("Experiment with " + str(r) + " repeats", fontsize=18)
    plt.title("Loss as function of " + func + " Epoch= " + str(Epoch) )
    ax.set_xlabel(r'Hyper_parameter', fontsize=20)
    ax.set_ylabel(r'Loss', fontsize=20)
    ax.legend()
    ax.tick_params(labelsize=20)
    plt.savefig('LossE' + str(Epoch) + 'rpt' + str(repeat) + '.png')
    plt.show()

    # Plot the accuracy
    fig, ax = plt.subplots(1, 2, figsize=(10,6))
    #ax.plot(np.sqrt(lr_model_history.history['accuracy']), 'r' ,label='train')
    #ax.plot(np.sqrt(lr_model_history.history['val_accuracy']), 'b' ,label='val')
    ax.plot(np.sqrt(score_val_list), 'b' ,label='Validation')
    ax.plot(np.sqrt(score_train_list), 'r', label='Train')

    plt.title("Accuracy as function of " + func)
    ax.set_xlabel(r'Hyper_parameter', fontsize=20)
    ax.set_ylabel(r'Accuracy', fontsize=20)
    ax.legend()
    ax.tick_params(labelsize=20)
    plt.savefig('AccuracyE' + str(Epoch) + 'rpt' + str(repeat) +'.png')
    plt.show()


# In[ ]:





# In[22]:


r = experiment(0.0001)


# In[21]:


#len(lost_val_list)
# plot_function_epoch(2)
# len(lost_val_list)
#for a in hyper_parameter:
#main()
    
r = experiment(a)
#plot_function_alpha(r)

#Mean of means, which shows the change trend of  means, such as second derivative of the function
sum = 0
num = 1
list = []
for j in lr_model_history.history['accuracy']:
    sum += j
    list.append(sum/num)
    num += 1
plt.plot(list)


# In[ ]:


sum = 0
num = 1
list = []
for j in lr_model_history.history['loss']:
    sum += j
    list.append(sum/num)
    num += 1
plt.plot(list)


# In[ ]:




