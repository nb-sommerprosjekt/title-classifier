from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#with open("titler.txt",'r') as title_file:
#    tittel_file = title_file.readlines()
#important_words = open("important_words.txt",'w')
titler  = []

def important_words (title):

    tittel=title.replace('\n','')
    tokenized_tittel=word_tokenize(tittel)
    filtered_title =[word for word in tokenized_tittel if word not in stopwords.words('norwegian')]
    filtered_title2 = [word for word in filtered_title if not word.isdigit() and len(word)>2]

    tittel_string_filtered =' '.join(filtered_title2)
        #titler.append(filtered_title)
        #important_words.write(tittel_string_filtered+'\n')
    return(tittel_string_filtered)

#important_words.close()
#print(filtered_title)
#print(len(filtered_title))



