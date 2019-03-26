import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from textblob import TextBlob
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
from scipy import interp
import numpy as np

file1 = open("combinedData2.txt",'r')
data=file1.read().split('\n')
#print(data)

x = []
for i in data:
    decision=TextBlob(i)
    if decision.polarity==0:
        x.append(0)
    elif decision.polarity>0:
        x.append(1)
    else:
        x.append(-1)

x=pd.Series(x)

labelencoder_y = LabelEncoder()
x = labelencoder_y.fit_transform(x)

cv=CountVectorizer(max_features=1500)
X=cv.fit_transform(data).toarray()
#print(X)

X_train, X_test, y_train, y_test = train_test_split(X, x, test_size = 0.25, random_state = 0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test,y_pred)
print("Confusion matrix:")
print(cm)

y_score = classifier.predict(X_test)
print(100* (classifier.score(X_test, y_test)))

y_score=label_binarize(y_score, classes=[0, 1, 2])
y_test = label_binarize(y_test, classes=[0, 1, 2])
n_classes = y_test.shape[1]

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
lw = 2
plt.plot(fpr["macro"], tpr["macro"],
         label='RF ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='darkorange', linestyle=':', linewidth=4)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
