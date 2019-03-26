import os
import math
import sys


class TextClassification2:
    # taking 0.001 as the learning rate
    learning_rate = 0.001
    w = {}

    def __init__(self, stopwordsuse,lambdaval,numiterations):
        self.stopwordsuse = stopwordsuse
        self.stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        self.lambdaval = lambdaval
        self.numiterations = numiterations
        self.m_list = []
        self.class_list = []
        self.words_set = None
        

    def function2(self):
        
        files_in_ham = os.listdir('train/ham') #path where ham files are stored
        files_in_spam = os.listdir('train/spam') #path where spam files are stored

        k = []
        for file_name in files_in_spam:
            with open('train/spam' + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as f:
                temp = f.read().lower().replace('\n', ' ').split(' ')
                k = k + temp

        
        s_list =  k
        l = []
        for file_name in files_in_ham:
            with open('train/ham' + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as f:
                temp = f.read().lower().replace('\n', ' ').split(' ')
                l = l + temp

        
        h_list =  l

         #combining ham and spam
        tot = s_list + h_list
        self.words_set = set(tot)

        # delete empty string
        if '' in self.words_set:
            self.words_set.remove('')

        # use stop_words
        if self.stopwordsuse:
            for word in self.stop_words:
                if word in self.words_set:
                    self.words_set.remove(word)

        for i in self.words_set:
            self.w[i] = 0.0
        self.w['zero'] = 0.0
        
        file_content = os.listdir('train/spam')
        for i in file_content:
            k1 = {}
            with open('train/spam/' + i, 'r', encoding='utf-8', errors='ignore') as f:
                t = f.read().lower().replace('\n', ' ').split(' ')
                for j in t:
                    if j in self.words_set:
                        if j not in k1:
                            k1[j] = 0
                        k1[j] += 1

            self.m_list.append(k1)
            self.class_list.append('spam')
        
        self.mapping('train/ham', 'ham')
        
        class_list_len = len(self.class_list)
        number = self.numiterations
        l_r = self.learning_rate
        for i in range(0,number):
            print('iteration %d' % (i))
            for j in self.w:
                sum1 = 0.0
                for alpha in range(0,class_list_len):
                    inst = self.m_list[alpha]

                    if j in inst:
                        name = self.class_list[alpha]
                        if name == 'spam':
                            val = 1
                        else:
                            val = 0
                        prob = self.calculate(inst, 'spam')
                        sum1 += float(inst[j] * (val - prob))
                        
                self.w[j] = self.w[j] + (l_r * sum1 - float(self.lambdaval) * l_r * self.w[j])
                
    def calculate(self, inst, name):
        w = self.w['zero']

        for word in inst:
            if word not in self.w:
                self.w[word] = 0.0
            w = w + self.w[word] * float(inst[word])
        float_w = float(w)
        exp_weight = math.exp(float_w)

        sigmoid_func = exp_weight / (1 + exp_weight)
        
        if name == 'spam':
            return sigmoid_func
        else:
            return 1 - sigmoid_func

    def hamspam(self):

        files_in_ham = os.listdir('train/ham') #path where ham files are stored
        files_in_spam = os.listdir('train/spam') #path where spam files are stored

        k = []
        for file_name in files_in_spam:
            with open('train/spam' + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as f:
                temp = f.read().lower().replace('\n', ' ').split(' ')
                k = k + temp
        s_list =  k
        s_count = len(files_in_spam)
        l = []
        for file_name in files_in_ham:
            with open('train/ham' + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as f:
                temp = f.read().lower().replace('\n', ' ').split(' ')
                l = l + temp
        h_list =  l
        h_count = len(files_in_ham)
        # clear train data
        self.class_list = []
        self.m_list = []
        self.words_set = None

        #adding ham and spam list        
        tot = h_list + s_list
        self.words_set = set(tot)

        # delete empty string
        if '' in self.words_set:
            self.words_set.remove('')

        # use stop_words
        if self.stopwordsuse:
            for word in self.stop_words:
                if word in self.words_set:
                    self.words_set.remove(word)

        file_content = os.listdir('test/spam')
        for i in file_content:
            k1 = {}
            with open('test/spam/' + i, 'r', encoding='utf-8', errors='ignore') as f:
                t = f.read().lower().replace('\n', ' ').split(' ')
                for j in t:
                    if j in self.words_set:
                        if j not in k1:
                            k1[j] = 0
                        k1[j] += 1

            self.m_list.append(k1)
            self.class_list.append('spam')
        
        file_content2 = os.listdir('test/ham')
        for i in file_content2:
            k2 = {}
            with open('test/ham/' + i, 'r', encoding='utf-8', errors='ignore') as f:
                t = f.read().lower().replace('\n', ' ').split(' ')
                for j in t:
                    if j in self.words_set:
                        if j not in k2:
                            k2[j] = 0
                        k2[j] += 1

            self.m_list.append(k2)
            self.class_list.append('ham')
            
        #self.mapping('test/ham', 'ham')

        # initialize spam, ham and total success to be zero
        spam_success, ham_success, tot_success = 0,0,0
            
        length1 = len(self.class_list)
        for i in range(0,length1):
            inst = self.m_list[i]
            name = self.class_list[i]
            result = self.findType(inst)
            if name!= result:
                pass
            else:
                tot_success += 1
                if name == 'ham':
                    ham_success = ham_success + 1
                else:
                    spam_success = spam_success + 1

        print('Accuracy For Spam Emails: %.4f%%' % ((spam_success * 1.0 / s_count) * 100))
        print('Accuracy For Ham Emails: %.4f%%' % ((ham_success * 1.0 / h_count) * 100))
        print('Accuracy For All Emails: %.4f%%' % ((tot_success * 1.0 / (s_count + h_count))* 100))

    def findType(self, instance):
        s_p = self.calculate(instance, 'spam')
        h_p = 1 - s_p
        if s_p <= h_p:
            return 'ham'
        else:
            return 'spam'

    def mapping(self, folder, class_type):
        file_content = os.listdir(folder)

        for file_name in file_content:
            tempMap = {}
            with open(folder + '/' + file_name, 'r', encoding='utf-8', errors='ignore') as f:
                temp = f.read().lower().replace('\n', ' ').split(' ')
                for word in temp:
                    if word in self.words_set:
                        if word not in tempMap:
                            tempMap[word] = 0
                        tempMap[word] += 1

            self.m_list.append(tempMap)
            self.class_list.append(class_type)
    
def execute(stopwordsuse,lambdaval, numiterations):
    logreg = TextClassification2(stopwordsuse,lambdaval, numiterations)
    logreg.function2()
    logreg.hamspam()

if __name__ == "__main__":
    lambdaval = sys.argv[1]
    numiterations = sys.argv[2]
    if sys.argv[3] == 'True' or sys.argv[3] == 'TRUE' or sys.argv[3] == 'true':
        stopwordsuse = True
    else:
        stopwordsuse = False
    execute(stopwordsuse,float(lambdaval), int(numiterations))
