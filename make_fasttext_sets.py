import os
import re
import math
from random import shuffle
import matplotlib.pyplot as plt
import numpy as np


#Only used when creating the corpus for fasttext. Creates one large file with every line consisting of
# __label__"DEWEY" + text. Outputs the result in name.txt Input must be in the folder "folder".
def to_fasttext_keywords(folder,name):
    rootdir = folder
    label_file=open(name+'.txt','a')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if str(file)[:5] == "meta-":
                f = open(os.path.join(subdir, file), "r+")
                meta_tekst = f.read()
                keyword = re.search('word:::(.+?)\n', meta_tekst)
                if keyword:
                    found = keyword.group(1)
                print(found.replace(' ','-'))
                file_name=os.path.join(subdir, file)
                file_name_text=file_name.replace("meta-","")
                tekst_fil=open(os.path.join(subdir, file_name_text), "r+")
                tekst=tekst_fil.read()


                label_file.write('__label__'+found+' '+tekst+'\n')



#Only used when creating the corpus for fasttext. Creates one large file with every line consisting of
# __label__"DEWEY" + text. Outputs the result in name.txt Input must be in the folder "folder".
def to_fasttext_dewey(folder,name):
    rootdir = folder
    label_file=open(name+'.txt','w')
    total_tekst=""
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if str(file)[:5] == "meta-":
                #print(subdir)
                f = open(os.path.join(subdir, file), "r+")
                for line in f.readlines():
                    if "dewey:::" in line:
                        dewey=line.split(":::")[1]

                found=dewey.replace(".","-").replace("\n","")
                found=found[:3]

                #print(found)
                file_name=os.path.join(subdir, file)
                file_name_text=file_name.replace("meta-","")
                tekst_fil=open(file_name_text, "r+")
                tekst=tekst_fil.read()

                total_tekst+='__label__'+found+' '+tekst+'\n'
    label_file.write(total_tekst)


#This function takes text file(originalname) and creates a test set and training set
# with a split based on test_percentage and minimum number of articles needed per deweynumber.
def create_test_and_training_set(original_name, test_name,training_name,test_percentage,min_art):
    articles=open(original_name+'.txt',"r")
    articles=articles.readlines()
    dewey_dict={}
    training_set=[]
    test_set=[]
    antall_dewey_stor_nok = 0
    dewey_freq = {}

    for article in articles:
        dewey=article.partition(' ')[0].replace("__label__","")
        if dewey in dewey_dict:
            dewey_dict[dewey].append(article)
        else:
            dewey_dict[dewey]=[article]
    print("antall deweys:"+str(len(dewey_dict)))

    for key in dewey_dict.keys():
        temp = dewey_dict[key]
        shuffle(temp)
        dewey_freq[key] = len(temp)
        if len(temp)>=min_art:
            antall_dewey_stor_nok=antall_dewey_stor_nok+1
            if len(temp)>1:
                split=max(1,math.floor(len(temp)*test_percentage))
                test_set.extend(temp[:split])
                training_set.extend(temp[split:])
            else:
                training_set.extend(temp)

    shuffle(training_set)
    print("antall deweys 100: " +str(antall_dewey_stor_nok))
    print(dewey_freq)
    dewey_list = sorted(dewey_freq.items())
    deweys,freq = zip(*dewey_list)
    newlist_dewey = [int(i) for i in deweys]
    plt.plot(newlist_dewey,freq)
    #plt.bar(newlist,dewey_freq.values(), width = 1.0, color='g')
    plt.show()
    shuffle(test_set)
    training="".join(training_set)
    test= "".join(test_set)
    f=open(training_name+".txt","w")
    f.write(training)
    f = open(test_name + ".txt", "w")
    f.write(test)

create_test_and_training_set("labels_filtered", "test_meta2_filtered","training_meta2_filtered",0.20,100)
# for i in range(1):
#     to_fasttext_dewey("training_"+str(i),"training_"+str(i))
#     to_fasttext_dewey(""+str(i),"test_"+str(i))

#to_fasttext_dewey("innhenting","complete_stemmed_correctly")
#min_art=[1,2,5,10,100]
#for i in min_art:
#i=1
#create_test_and_training_set("complete_stemmed_correctly","test_final"+str(i),"training_final"+str(i),0.25,i)

#to_fasttext_dewey("data/data_dewey/test_set","dewey_test_set2")
#to_fasttext_dewey("data/data_dewey/training_set","dewey_training_set2")
