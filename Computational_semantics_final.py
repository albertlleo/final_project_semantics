#!/usr/bin/env python
# coding: utf-8

# In[262]:


import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import numpy as np
import random
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras. models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import SGD

df = pd.read_csv("5-features-full-corpus.csv.csv")
feature_columns = df.columns 
df = df.drop('verb_POS', axis=1)


# In[263]:


df.loc[df['length'] <= 5, 'length'] = 0
df.loc[df['length'] > 5, 'length'] = 1
# Mean of all number of values
df.loc[df['lastmention'] != -1, 'lastmention'] = 0
df.loc[(df['lastmention'] >= 5) | (df['lastmention']== -1), 'lastmention'] = 1


# In[264]:


# Splitting dataset into features (X) and target variables (Y)
X = df.iloc[:, 5:19]
Y = df.loc[:, 'target_form']
del X['target_form']

X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.2)

y_val = np.array(y_val)
y_train = np.array(y_train)


# In[265]:


X_train['lastmention'].value_counts()


# In[266]:


X_train['length'].value_counts()


# In[267]:


#Defining  parameters
layer_dim1 = 13
node_no1 = 256
node_no2 = 512
batch_size = 128
Epoch = 10

def main():

        # Initializing the Sequential model from KERAS.
        model = Sequential()

        # Creating a 16 neuron hidden layer with Linear Rectified activation function.
        model.add(Dense(node_no1, input_dim=layer_dim1, 
                        use_bias=True, bias_initializer='zeros',
                        activation='relu'))
        model.add(Dropout(0.5))
        
        model.add(Dense(node_no2,
                        kernel_regularizer=l2(0.0001), activation= 'relu'))
        #model.add(Dropout(0.5))
        
        # Adding a output layer
        model.add(Dense(1, activation='sigmoid'))
        
        # Compiling the model
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        
        model.fit(X_train, y_train, epochs=Epoch, batch_size=batch_size,shuffle = True, validation_data=(X_val, y_val))
        score = model.evaluate(X_val, y_val, batch_size=batch_size)
        #lr_model_history.history['accuracy']
        return model


# In[268]:


model = main()


# In[269]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV

rfc = RandomForestClassifier(random_state=101)
rfecv = RFECV(estimator=rfc, step=1, cv=StratifiedKFold(10), scoring='accuracy')
rfecv.fit(X_train, y_train)


# In[270]:


print('Optimal number of features: {}'.format(rfecv.n_features_))


# In[271]:


import matplotlib.pyplot as plt

plt.figure(figsize=(16, 9))
plt.title('Recursive Feature Elimination with Cross-Validation', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Number of features selected', fontsize=14, labelpad=20)
plt.ylabel('% Correct Classification', fontsize=14, labelpad=20)
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#303F9F', linewidth=3)
plt.savefig('feature_elimination.jpg')
plt.show()


# In[272]:


print(np.where(rfecv.support_ == False)[0])
X.drop(X.columns[np.where(rfecv.support_ == False)[0]], axis=1, inplace=True)


# In[274]:


dset = pd.DataFrame()
dset['attr'] = X.columns
dset['importance'] = rfecv.estimator_.feature_importances_
dset = dset.sort_values(by='importance', ascending=False)

plt.figure(figsize=(16, 14))
plt.barh(y=dset['attr'], width=dset['importance'], color='#1976D2')
plt.title('Feature Importances', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Importance', fontsize=14, labelpad=20)
plt.savefig('feature_importances.jpg')
plt.show()

