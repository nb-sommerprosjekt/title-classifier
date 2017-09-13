import fasttext
import time
import os
from datetime import datetime

def create_classifier(epoch,lr1,DIMENSIONS, up_rate,ws,loss1,wiki):
    print(epoch,lr,DIMENSIONS,ws,up_rate,loss,wiki)
    if wiki:
        return fasttext.supervised(TRAIN_FILE+'.txt',
                                                     'skilnad3_'+str(nr),
                                                     epoch=epoch,
                                                     lr=lr1,
                                                     pretrained_vectors='wiki.no.vec',
                                                     dim=DIMENSIONS,
                                                     ws=ws,
                                                    lr_update_rate=up_rate,
                                                     loss=loss1,
                                                    bucket=500000)
    else:

        return fasttext.supervised(TRAIN_FILE+'.txt',
                               TRAIN_FILE+str(nr),
                               epoch=epoch,
                               lr=lr1,
                               dim=DIMENSIONS,
                               ws=ws,
                               lr_update_rate=up_rate,
                               loss=loss1)

#parameters


EPOCHs=[50,75,100,125,150,200,300]
LRs=[0.3]
UP_RATEs=[100]
WS=[5]
LOSS=["hs"]
WIKI_VEC=[False]
Ks=[1,5,10]
TRAIN_FILES=["training_meta2_filtered"]#["training_failed1","training_failed2","training_failed5","training_failed10","training_failed100","training_correct1","training_correct2","training_correct5","training_correct10","training_correct100"]
TEST_FILES=["test_meta2_filtered"]#["test_failed1","test_failed2","test_failed5","test_failed10","test_failed100","test_correct1","test_correct2","test_correct5","test_correct10","test_correct100"]


DIMENSIONS=300
tid=time.time()
total_iterations=len(EPOCHs)*len(LRs)*len(UP_RATEs)*len(WS)*len(LOSS)*len(WIKI_VEC)*len(TEST_FILES)
count=0
for j in range(len(TRAIN_FILES)):
    TRAIN_FILE=TRAIN_FILES[j]
    TEST_FILE =TEST_FILES[j]
    for nr in range(1):
        for epoch in EPOCHs:
            for lr in LRs:
                for up_rate in UP_RATEs:
                    for ws in WS:
                        for loss in LOSS:
                            for wiki_vec in WIKI_VEC:
                                count+=1
                                print("It is : "+str(datetime.now()))
                                tid=time.time()
                                print("Iteration nr {} out of {}".format(count,total_iterations))
                                classifier=create_classifier(epoch,lr,DIMENSIONS,up_rate,ws,loss,wiki_vec)
                                print("Creating the classifier took {} seconds.".format(time.time()-tid))
                                tid=time.time()
                                if not os.path.exists("logs-"+TEST_FILE):
                                    os.makedirs("logs-"+TEST_FILE)
                                with open("logs-"+TEST_FILE+"/" + "log-{}-{}-{}-{}-{}-{}-{}-{}.txt".format(str(nr),str(epoch), str(lr).replace(".",""), str(up_rate),str(ws), loss, str(wiki_vec),TRAIN_FILE),"w") as logfile:

                                    logfile.write("epoch:::{}\n".format(str(epoch)))
                                    logfile.write("lr:::{}\n".format(str(lr)))
                                    logfile.write("lr_up_rate:::{}\n".format(str(up_rate)))
                                    logfile.write("Word context length:::{}\n".format(str(ws)))
                                    logfile.write("loss:::{}\n".format(loss))
                                    logfile.write("wiki_vec:::{}\n".format(str(wiki_vec)))
                                    for k in Ks:

                                        print("K-run:{}".format(k))
                                        result = classifier.test(TEST_FILE+".txt", k)
                                        print("Running took {} seconds.".format(time.time() - tid))
                                        tid = time.time()
                                        precision = result.precision
                                        recall=result.recall
                                        logfile.write("log k={}:::{}:::{}\n".format(k,precision,recall))

#create_classifier(epoch=75,lr1=0.1,DIMENSIONS=300, up_rate=100, ws=5,loss1='softmax',wiki=False)