#!/usr/bin/env python
# coding: utf-8

# In[262]:


import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sn
import category_encoders as ce

df = pd.read_csv("filtered.csv")
feature_columns = df.columns 
df.head()


# In[239]:


print(df['length'].value_counts())


# In[240]:


{k: v for k,v in zip(labels,list(range(0,len(labels))))}


# In[241]:


replace_map = {'verb_POS': {'VVG': 1, 'VV': 0}}
labels = df['verb_POS'].astype('category').cat.categories.tolist()
replace_map_ = {'verb_POS' : {k: v for k,v in zip(labels,list(range(0,len(labels))))}}
df_replace = df.copy()
df_replace.replace(replace_map_, inplace=True)

print(df_replace.head())


# In[242]:


df_replace.boxplot('length','verb_POS' ,rot = 30,figsize=(5,6))


# In[243]:


df_normalize = df.copy()
df_replace.loc[df_replace['length'] <= 5, 'length'] = 0
df_replace.loc[df_replace['length'] > 5, 'length'] = 1
#X.loc['4'] = int(X.loc['column_name'])
#df_replace.loc[:,'4'] =  df_replace.loc[:,'column_name']
df_replace.drop(columns =['target_form'])
print(df_replace.head())


# In[ ]:





# In[244]:


#split dataset in features and target variable
X = df_replace.iloc[:, 4:14]
Y = df_replace.iloc[:, 14]


# In[245]:


#10 01 şeklinde binary ayrımı yapmak için gerekli
#ce_binary = ce.BinaryEncoder(cols = ['4'])
#ce_binary.fit_transform(X.iloc[:,0])


# In[246]:


def split_data():
    size = random.uniform(0.1, 0.5)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=size)
    
    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier()

    # Train Decision Tree Classifer
    clf = clf.fit(X_train,y_train)

    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred)
    return size, score


# In[247]:


score = split_data()
score


# In[248]:


sizes = []
scores = []
size_range = list(range(1, 20))
for i in size_range:
    size, score = split_data()
    print("Test Size:",round(size, 2),'%')
    
    print("Test Score:",score)
    #score = metrics.accuracy_score(y_test, y_pred)
    scores.append(score)
    sizes.append(size)
    
opt_size = scores.index(max(scores))

plt.xlabel("size %")
plt.ylabel("accuracy")
plt.scatter(sizes,scores)


# In[249]:


ideal_size = sizes[opt_size]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=ideal_size)
# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


# In[250]:


from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import tree #For our Decision Tree
import pandas as pd # For our DataFrame
import pydotplus # To create our Decision Tree Graph
from IPython.display import Image  # To Display a image of our graph


# In[251]:


#dot_data = StringIO()
#export_graphviz(clf, out_file=dot_data,  
#                filled=True, rounded=True,
#                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
#graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
#graph.write_png('diabetes.png')
#Image(graph.create_png())



# criterion : optional (default=”gini”) or Choose attribute selection measure: This parameter allows us to use the different-different attribute selection measure. Supported criteria are “gini” for the Gini index and “entropy” for the information gain.
# 
# splitter : string, optional (default=”best”) or Split Strategy: This parameter allows us to choose the split strategy. Supported strategies are “best” to choose the best split and “random” to choose the best random split.
# 
# max_depth : int or None, optional (default=None) or Maximum Depth of a Tree: The maximum depth of the tree. If None, then nodes are expanded until all the leaves contain less than min_samples_split samples. The higher value of maximum depth causes overfitting, and a lower value causes underfitting (Source).

# In[252]:


# List of values to try for max_depth:
max_depth_range = list(range(1, 20))
# List to store the average RMSE for each value of max_depth:
accuracy = []
for depth in max_depth_range:
    
    clf = DecisionTreeClassifier(max_depth = depth, 
                             random_state = 0)
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    accuracy.append(score)


# In[270]:


plt.xlabel("max_depth")
plt.ylabel("accuracy")
plt.plot(max_depth_range,accuracy)
depth = accuracy.index(max(accuracy))+1


# In[254]:


clf = DecisionTreeClassifier(criterion="entropy", max_depth=depth)

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


# In[264]:


import numpy as np


def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()


# In[266]:


plot_confusion_matrix(cm           = np.asarray(confusion_matrix(y_test, y_pred)), 
                      normalize    = False,
                      target_names = ['0', '1'],
                      title        = "Confusion Matrix")


# In[255]:


importances = pd.DataFrame({'feature':X_train.columns,'importance':np.round(clf.feature_importances_,3)})
importances = importances.sort_values('importance',ascending=False)
importances


# In[268]:


from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
Image(graph.create_png())


# In[ ]:




