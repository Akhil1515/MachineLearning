from textblob import TextBlob
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
from scipy import interp
import numpy as np
import warnings
import Svmlib
import DT
import naivebayes
import randforest

warnings.filterwarnings("ignore")

nfile=open("combinedData2.txt",'r')
data=nfile.read().split('\n')
#print(data)
y=[]
for j in data:
    decision=TextBlob(j)
    if decision.polarity==0:
        y.append(0)
    elif decision.polarity>0:
        y.append(1)
    else:
        y.append(-1)

#print(y)

y=pd.Series(y)
print(y)

labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)
print(y)


cv=CountVectorizer(max_features=1500)
X=cv.fit_transform(data).toarray()
print(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 0)


sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)


y_score = classifier.predict(X_test)
print( classifier.score(X_test, y_test))

cm = confusion_matrix(y_test, y_score)
print(cm)
y_score=label_binarize(y_score, classes=[0, 1, 2])
y_test = label_binarize(y_test, classes=[0, 1, 2])
n_classes = y_test.shape[1]
print(n_classes)
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))


mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])


mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])


plt.figure()
plt.plot(fpr["macro"], tpr["macro"],
         label='LG ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='darkorange', linestyle=':', linewidth=4)
plt.plot(Svmlib.fpr["macro"], Svmlib.tpr["macro"],
         label='SVM ROC curve (area = {0:0.2f})'
               ''.format(Svmlib.roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)
plt.plot(DT.fpr["macro"], DT.tpr["macro"],
         label=' DT ROC curve (area = {0:0.2f})'
               ''.format(DT.roc_auc["macro"]),
         color='darkred', linestyle=':', linewidth=4)
plt.plot(naivebayes.fpr["macro"], naivebayes.tpr["macro"],
         label=' NB ROC curve (area = {0:0.2f})'
               ''.format(naivebayes.roc_auc["macro"]),
         color='lightgreen', linestyle=':', linewidth=4)
plt.plot(randforest.fpr["macro"], randforest.tpr["macro"],
         label='RF ROC curve (area = {0:0.2f})'
               ''.format(randforest.roc_auc["macro"]),
         color='green', linestyle=':', linewidth=4)
lw=2

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
