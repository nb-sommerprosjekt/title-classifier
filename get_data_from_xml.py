import os
import pymarc
import find_important_words

file_name = "norart20170906.xml"
full_file = os.path.abspath(os.path.join('data',file_name))
#pickle_klassebetegnelser = open('klassebetegnelser_dict_fixed.pckl', 'wb+')
corpus_file = open('dewey_corpora_filtered.txt','w')
label_file = open("labels_filtered.txt",'w')
#nyttig error:  https://github.com/edsu/pymarc/issues/73


deweynr = []
klassedict = {}
antall_docs_uten_keywords = 0
total_docs=0
antall_docs_med_keywords=0
title_file = open("titler.txt",'w')
with open(full_file, 'rb') as fh:
    for record in pymarc.parse_xml_to_array(fh):

        total_docs = total_docs+1

        if  "245" in record and "082" in record and "650" not in record:
                 if "a" in record["245"] and "a" in record["082"]:

                    antall_docs_uten_keywords = antall_docs_uten_keywords +1

                    corpus_file.write(":::tittel:::"+record['245']['a']
                                       + ":::dewey:::"
                                       + record["082"]["a"].replace(".","")
                                       + ":::nøkkelord:::"
                                       + '\n')
                    deweynr = record['082']['a'].replace(".","")
                    deweynr = deweynr.replace("-","")
                    label_file.write("__label__"+deweynr[:3]+ " "+find_important_words.important_words(record['245']['a']) + '\n')
                    title_file.write(record['245']['a']+'\n')
        else:
            if  "245" in record and "082" in record and "650" in record:
                    if "a" in record["245"] and "a" in record["082"] and "a" in record["650"]:
                            antall_docs_med_keywords = antall_docs_med_keywords + 1
                            corpus_file.write(":::tittel:::" + record['245']['a']
                                           + ":::dewey:::"
                                           + record["082"]["a"].replace(".","")
                                           + ":::nøkkelord:::"
                                           +record["650"]["a"]
                                           +'\n')
                            deweynr = record['082']['a'].replace(".", "")
                            deweynr = deweynr.replace("-", "")
                            label_file.write("__label__" + deweynr[:3] + " " + find_important_words.important_words(record['245']['a']) + " " + find_important_words.important_words(record["650"]["a"]) + '\n')
                            title_file.write(record['245']['a'] + '\n')
print("Total antall docs:"+str(total_docs))
print("Antall docs uten keywords:"+ str(antall_docs_uten_keywords))
print("Antall docs med keywords:"+ str(antall_docs_med_keywords))
print("Antall docs med som har dewey og tittel og har og ikke har keywords:"+ str(antall_docs_med_keywords+antall_docs_uten_keywords))


corpus_file.close()
label_file.close()