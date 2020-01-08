from collections import Counter
from math import log, sqrt

#parse the file and save only the relevant parts
def load_and_parse_file(file_name):
    print("START: load_and_parse_file")
    
    file_data = open(file_name, encoding="utf8")
    lines = file_data.readlines()
    parsed_lines = []
    
    for line in lines:
        tokens = line.split()
        if tokens:
            word_id = int(tokens[0])
            form = tokens[1]
            lemma = tokens[2]
            cpostag = tokens[3]
            head = tokens[6]
            parsed_lines.append({"id": word_id, "form": form, "lemma": lemma,
                                 "cpostag": cpostag, "head": head})
    return parsed_lines

#count the number of appearances of each word
def count_words_appearances(dataset):
    print("START: count_words_appearances")
    counter_obj = Counter()
    for word_context in dataset:
        counter_obj[word_context['lemma']] +=1
    return counter_obj

#get a set of words that are more frequent than the threshold        
def get_high_freq_lemmas(words_counter,thresh):
    print("START: get_high_freq_lemmas")
    high_freq_lemmas = set()
    for lemma in words_counter:
        if words_counter[lemma] >= thresh:
            high_freq_lemmas.add(lemma)
            
    return high_freq_lemmas        

def save_most_freq_to_file(words_count,file_name,threshold):
    file = open(file_name,"w")
    for lemma in words_count.most_common(threshold):
        file.write(str(lemma[0]) + " " + str(lemma[1]) + "\n")
    file.close()
    
def count_dep_contexts(vectors):
    counter_obj = Counter()
    for vec in vectors:
        for i in vectors[vec]:
            counter_obj[i] += 1
    return counter_obj
        
def save_dep_to_file(dep_context_count,file_name,threshold):
    file = open(file_name,"w")
    for a in dep_context_count.most_common(threshold):
        file.write(str(a[0]) + " " + str(a[1]) + "\n")
    
#convert the dataset into a sentences structer    
def convert_to_sentences(dataset, lemmas_only = False):
    print("START: convert_to_sentences")
    sentences = []
    i = 0
    
    while i+1 < len(dataset):
        words = [dataset[i]["lemma"]] if lemmas_only else [dataset[i]]
        for j in range(i+1,len(dataset)):
            #if current sentence ended
            if dataset[j]["id"] == 1:
                break
            if lemmas_only:
                words.append(dataset[j]["lemma"])
            else:    
                words.append(dataset[j])
        i=j
        sentences.append(words)
    return sentences
    
def calc_pmi_vectors(weight_vectors,word_counter,high_freq_lemmas):
    print("START: calc_pmi_vectors")
    pmi = {}
    total_words = sum(word_counter.values())
    words_vector_counter = {word: sum(vector.values()) for word,vector in weight_vectors.items() if word in high_freq_lemmas}
    
    for word in weight_vectors:
        if word not in high_freq_lemmas:
            continue
        if word not in pmi:
            pmi[word] = {}
        attributes_of_word = weight_vectors[word]
        for attr in attributes_of_word:
            #if float(weight_vectors[word][attr]) < 75:
            #    continue
            calc_weight_attr_by_words = (float(weight_vectors[word][attr]) / words_vector_counter[word])
            words_by_total = (float(word_counter[attr]) / total_words)
            pmi[word][attr] = log(calc_weight_attr_by_words / words_by_total, 2)
    
    return pmi
        
#calculate the similarities between target words and all the other words
def calc_similarities(target_words, pmi_vectors,similarities_num):
    print("START: calc_similarities")
    target_mults = {}
    count_features = {}
    mutual_features_threshold = 10
    for target in target_words:
        if target not in pmi_vectors:
            continue
        count_features[target] = Counter()
        for word in pmi_vectors:
            #bool_mult_is_zero = False
            if word == target:
                continue
            multiplication, mutual_feature_count = mult(pmi_vectors[word],pmi_vectors[target]) 
            
            #mult did not return values
            if multiplication == 0.0:
                continue
            count_features[target][word] = mutual_feature_count
            if target not in target_mults:
                target_mults[target] = {}
            target_mults[target][word] = multiplication
                
    print("START: calc_similarities - Top 20")
    for target in target_mults:
        sorted_attributes = sorted(
            [attr for attr in target_mults[target] if count_features[target][attr] > mutual_features_threshold],
            key=lambda attr: target_mults[target][attr], reverse=True)
        max_size = len(sorted_attributes) if similarities_num > len(sorted_attributes) else similarities_num
        print("\tWord '%s':" % target)
        print(' '.join(
            "%s(%s)" % (attribute, count_features[target][attribute]) for attribute in sorted_attributes[:max_size]))
    
#multiply two vectors            
def mult(vec_a, vec_b):
    total = 0.0
    count_features = 0
    for word in filter(lambda x: x in vec_b,vec_a.keys()):
        total += vec_a[word] * vec_b[word]
        count_features += 1
    product_of_total_by_size = total / (size(vec_a) * size(vec_b))
    return product_of_total_by_size, count_features

#calculate the size of a vector
def size(vec):
    total = 0.0
    for word in vec:
        total += sqrt(vec[word]*vec[word])
    return total    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    