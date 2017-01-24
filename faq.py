import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

CSV_FILENAME = "faqs.csv"

f = pd.read_csv(CSV_FILENAME)
df = pd.DataFrame(f)

def find_similarity(s,li):
    '''
    Returns lexical similarity score of s with all the strings
    in li.
    '''
    x = np.ones((len(li)+1,len(li)+1))
    try:
        li.append(unicode(s,errors='replace'))
        vect = TfidfVectorizer(min_df=1)
        tfidf = vect.fit_transform(li)
        x = cosine_similarity(tfidf[-1],tfidf)
    except  Exception,e:
        print str(e)
    return x[-1]

# def read_content(path):
#     s= ''
#     try:
#         with open(root_path+path,'r') as myfile:
#             s = myfile.read().replace('\n', '')
#     except:
#         pass
#     return s

# class_list = []
# code_list = []

# l = 2
# for i in range(300):
#     fname = unicode(df["files"][i],errors='replace')
#     class_list.append((fname))
#     code_list.append(read_content(fname))

# similarity_scores = []