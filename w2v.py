import sys
import numpy as np

#load file into numpy arrays
def load_file(file_name):
    words = list()
    W_vecs = list()
    file = open(file_name, 'r', encoding='utf-8')
    if file:
        lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            split_line = stripped_line.split()
            words.append(split_line[0])
            W_vecs.append(np.array([float(v) for v in split_line[1:]]))
    return np.array(W_vecs), words

#print the num most similar words, wiether by context to by word
def print_similarities(vectors,words,word2idx,num,contexts = False,flag = False):
    for target in TARGET_WORDS:
        target_vec = vectors[word2idx[target]]
        #sims = vectors.dot(target_vec)
        sims = vectors.dot(target_vec) if not flag else contexts.dot(target_vec) 
        sorted_similarities = (-sims).argsort()
        print("\t" + target + ":")
        for i in range(1,num+1):
            print(" " + words[sorted_similarities[i]])
            
if __name__ == "__main__":
    words_f_name = sys.argv[1]
    context_f_name = sys.argv[2]
    #words_f_name = "deps.words"
    #context_f_name = "deps.contexts"    
    TARGET_WORDS = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar", "piano"]    
    SIMILARITIES_NUM = 20
    CONTEXT_SIMILARITIES_NUM = 10
    W_vecs, words = load_file(words_f_name)
    word2idx = {w:i for i, w in enumerate(words)}
    C_vecs, contexts = load_file(context_f_name)
    #context2idx = {w:i for i, w in enumerate(contexts)}
    
    print("WORD BASED SIMILARITIES:")
    print_similarities(W_vecs,words,word2idx,20)
    print("CONTEXT BASED SIMILARITIES:")
    #print_similarities(C_vecs,contexts,context2idx,10)
    print_similarities(W_vecs,contexts,word2idx,10,C_vecs,True)
