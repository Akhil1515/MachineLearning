
import os
import math
import sys


class TextClassification1:
    def __init__(self, stopwordsuse):
        #initializing all variables
        self.h_count = 0  # ham count
        self.s_count = 0  # spam count
        self.h_map = {}   
        self.s_map = {}
        self.stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        self.stopwordsuse = stopwordsuse # contains True or False
        self.words_set = None
        
    def function(self):
        k = []
        l = []
        files_in_folder = os.listdir('train/spam')  #path where the spam files are stored
        for i in files_in_folder:
            with open('train/spam/' + i, 'r', encoding='utf-8', errors='ignore') as f:  #opening each spam file present in folder
                temp = f.read().lower().replace('\n', ' ').split(' ')
                k = k + temp
        s_list = k
        self.s_count = len(files_in_folder)  #number of files in spam folder
        files_in_folder1 = os.listdir('train/ham')   #path where the ham files are stored
        for j in files_in_folder1:
            with open('train/ham/' + j, 'r', encoding='utf-8', errors='ignore') as f:   #opening each ham file present in folder
                temp = f.read().lower().replace('\n', ' ').split(' ')
                l = l + temp
        h_list = l
        self.h_count = len(files_in_folder1)  #number of files in ham folder

        # delete empty string from spam list
        if '' in s_list:
            s_list.remove('')
            
        # delete empty string from ham list
        if '' in h_list:
            h_list.remove('')
        
        # remove stop words from spam list
        if self.stopwordsuse:
            for word in self.stop_words:
                if word in s_list:
                    s_list.remove(word)
        
        # remove stop words from ham list            
        if self.stopwordsuse:
            for word in self.stop_words:
                if word in h_list:
                    h_list.remove(word)
        
        self.words_set = set(s_list + h_list)
        #finding length of ham, spam and total 
        (s_len,h_len,words_set_len) = (len(s_list),len(h_list),len(self.words_set))

        temp = {}
        for w in h_list:
            if w not in temp:
                temp[w] = 0
            else:
                temp[w] = temp[w] + 1
        self.h_map = temp
        
        temp1 = {}
        for w in s_list:
            if w not in temp1:
                temp1[w] = 0
            else:
                temp1[w] = temp1[w] + 1
        self.s_map = temp1
        
        # total number of ham and spam counts
        (s_total,h_total) = (s_len + words_set_len,h_len + words_set_len)

        for a in self.h_map.keys():
            self.h_map[a] = math.log2((self.h_map[a] + 1) * 1.0 / h_total)

        for b in self.s_map.keys():
            self.s_map[b] = math.log2((self.s_map[b] + 1) * 1.0 / s_total)

        return s_total, h_total

    def spamham(self, s_total, h_total):
        #dealing with spam content:
        #taking all files under spam folder
        files_in_spam = os.listdir('test/spam')  # path where spam files are stored
        spam_count_in_test = len(files_in_spam)  # total number of spam files
        count1 = 0
        count2 = 0

        for i in files_in_spam:
            with open('test/spam/' + i, 'r', encoding='utf-8', errors='ignore') as f: # opening spam file
                temp = f.read().lower().replace('\n', ' ').split(' ')
            a = self.h_count
            b = self.s_count
            tot = self.h_count + self.s_count
            h_prop = math.log2(a * 1.0 / tot)
            s_prop = math.log2(b * 1.0 / tot)

            # delete empty string
            if '' in temp:
                temp.remove('')
            # delete stop_words from spam list
            if self.stopwordsuse:
                for word in self.stop_words:
                    if word in temp:
                        temp.remove(word)

            for word in temp:
                if word not in self.s_map:
                    rec = 1/s_total
                    s_prop = s_prop + math.log2(rec)
                else:
                    s_prop = s_prop + self.s_map[word]

            for word in temp:
                if word not in self.h_map:
                    rec = 1/h_total
                    h_prop = h_prop + math.log2(rec)
                else:
                    h_prop = h_prop + self.h_map[word]

            if s_prop < h_prop:
                pass
            else:
                count1 += 1

        spam_accuracy = count1 * 1.0 / spam_count_in_test

        #dealing with ham content:
        #taking all files under ham folder
        files_in_ham = os.listdir('test/ham') # path where ham files are stored
        ham_count_in_test = len(files_in_ham) # number of ham files

        for j in files_in_ham:
            with open('test/ham' + '/' + j, 'r', encoding='utf-8', errors='ignore') as f: #opening ham file
                temp = f.read().lower().replace('\n', ' ').split(' ')

            # delete empty string
            if '' in temp:
                temp.remove('')

            a = self.h_count
            b = self.s_count
            tot = self.h_count + self.s_count
            h_prop = math.log2(a * 1.0 / tot)
            s_prop = math.log2(b * 1.0 / tot)

            # delete stop_words from ham list
            if self.stopwordsuse:
                for word in self.stop_words:
                    if word in temp:
                        temp.remove(word)

            for word in temp:
                if word not in self.s_map:
                    rec = 1/s_total
                    s_prop = s_prop + math.log2(rec)
                else:
                    s_prop = s_prop + self.s_map[word]

            for word in temp:
                if word not in self.h_map:
                    rec = 1/h_total
                    h_prop = h_prop + math.log2(rec)
                else:
                    h_prop = h_prop + self.h_map[word]

            if s_prop > h_prop:
                pass
            else:
                count2 += 1

        ham_accuracy = count2 * 1.0 / ham_count_in_test

        total_success_ratio = (count1 + count2) * 1.0 / (spam_count_in_test + ham_count_in_test)

        print('Accuracy for spam mails using Naive Bayes: %.4f%%' %(spam_accuracy*100))
        print('Accuracy for ham mails using Naive Bayes: %.4f%%' %(ham_accuracy*100))
        print('Accuracy for all mails using Naive Bayes: %.4f%%' %(total_success_ratio*100))

def execute(stopwordsuse):
    naivebayes = TextClassification1(stopwordsuse)
    spam_total_count, ham_total_count = naivebayes.function()

    naivebayes.spamham(spam_total_count, ham_total_count)

if __name__ == "__main__":
    if sys.argv[1] == 'True' or sys.argv[1] == 'true' or sys.argv[1] == 'TRUE':
        stopwordsuse = True
    else:
        stopwordsuse = False
    execute(stopwordsuse)
