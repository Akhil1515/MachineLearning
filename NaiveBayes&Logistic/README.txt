NAIVE BAYES:

naive bayes is stored as naivebayes.py

train and test folders should be in the same folder as that of naivebayes.py
For instance, a folder named machinelearning should contain naivebayes.py and train and test folders

Go to command prompt and go to machinelearning folder where naivebayes.py and train and test folders are present and type:
 python naivebayes.py <true/false>

 If entered false type following command:
 python naivebayes.py false
 Accuracy for spam mails using naive bayes: 98.4615%
 Accuracy for ham mails using naive bayes: 94.8276%
 Accuracy for all mails using naive bayes: 95.8159%

 If entered true type following command:
 python naivebayes.py true
 Accuracy for spam mails using naive bayes: 98.4615%
 Accuracy for ham mails using naive bayes: 94.2529%
 Accuracy for all mails using naive bayes: 95.3975%

 --> We observe that accuracy is 95.8159 when stopwords are not considered and 95.3975 when stopwords are considered


LOGISTIC REGRESSION:

logistic regression is stored as logistic.py

train and test folders should be in the same folder as that of logistic.py
For instance, a folder named machinelearning should contain logistic.pyand train and test folders

Go to command prompt and go to machinelearning folder where logistic.py and train and test folders are present and type:
 python logistic.py <lambda_value> <number_of_iterations> <true/false>

 <lambda_value> indicates value of lambda ex: 0.1 or 0.2
 <number_of_iterations> indicates total number of iterations like 100 or 200
 
 If entered false type following command:
 python logistic.py 0.1 100 true
 Accuracy for spam mails : 82.9268%
 Accuracy for ham mails : 99.1176%
 Accuracy for all mails : 94.8164%

 If entered true type following command:
 python logistic.py 0.1 100 false
 Accuracy for spam mails : 87.8049%
 Accuracy for ham mails : 97.3529%
 Accuracy for all mails : 94.8164%

 --> We observe that accuracy is 94.8164 when stopwords are not considered and 94.8164 when stopwords are considered

