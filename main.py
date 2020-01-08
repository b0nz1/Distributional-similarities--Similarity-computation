import sys
import helper
from collections import Counter

#calc weights based on sentences
def calc_weight_sentence(sentences,high_freq_lemmas):
    print("START: calc_weight_sentence")
    
    weight_vec = {}
    for sentence in sentences:
        for i in range(len(sentence)):
            if sentence[i] in high_freq_lemmas:
                if sentence[i] not in weight_vec:
                    weight_vec[sentence[i]] = {}
                #add all words as attributes except the word itself
                for j in range(len(sentence)):
                    if i!= j:
                        if sentence[j] not in weight_vec[sentence[i]]:
                            weight_vec[sentence[i]][sentence[j]] = 0
                        weight_vec[sentence[i]][sentence[j]] += 1
    return weight_vec
                        
#calc weights based on window
def calc_weight_window(dataset,functional_words):
    print("START: calc_weight_window")
    i = 0
    weight_vec = {}
    #first word
    while dataset[i]["cpostag"] in functional_words:
        i += 1
    pre_last_word = dataset[i]["lemma"]
    bool_first_word = True
    i += 1
    
    #second word
    while dataset[i]["cpostag"] in functional_words:
        i += 1
    last_word = dataset[i]["lemma"]
    bool_second_word = True
    weight_vec[last_word] = Counter()
    weight_vec[last_word][pre_last_word] += 1
    if pre_last_word not in weight_vec:
        weight_vec[pre_last_word] = Counter()
    weight_vec[pre_last_word][last_word] += 1
    
    #all the rest of the words
    if bool_first_word and bool_second_word:
        while i < len(dataset) - 1:
            i +=1
            if dataset[i]["cpostag"] in functional_words:
                continue
            next_word = dataset[i]["lemma"]
            if next_word not in weight_vec:
                weight_vec[next_word] = Counter()
            
            weight_vec[next_word][last_word] += 1
            weight_vec[next_word][pre_last_word] += 1
            weight_vec[last_word][next_word] += 1
            weight_vec[pre_last_word][next_word] += 1
            pre_last_word = last_word
            last_word = next_word
    return weight_vec       
    
#calc weights based on dependencies
def calc_weight_dependency(sentences,high_freq_lemmas):
    print("START: calc_weight_dependency")
    child = 0
    parent = 1
    weight_vec = {}
    
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        for word in sentence:
            if len(word) == 0:
                continue
            #preposition case
            if sentence[int(word["head"]) - 1]["cpostag"] == "IN":
                in_parent_position = int(sentence[int(word["head"]) - 1]["head"])
                attr = sentence[in_parent_position - 1]
                
                if attr["lemma"] not in weight_vec:
                    weight_vec[attr["lemma"]] = Counter()
                var_vec = (word["lemma"], parent, word["cpostag"])
                weight_vec[attr["lemma"]][var_vec] += 1
                
                if word["lemma"] not in weight_vec:
                    weight_vec[word["lemma"]] = Counter()
                var_vec2 = (attr["lemma"], child, attr["cpostag"])
                weight_vec[word["lemma"]][var_vec2] += 1
            #regular case    
            else:    
                attr = sentence[int(word["head"]) - 1]
                if word["lemma"] in high_freq_lemmas:
                    if word["lemma"] not in weight_vec:
                        weight_vec[word["lemma"]] = Counter()
                    var_vec = (word["lemma"], child, attr["cpostag"])
                    weight_vec[word["lemma"]][var_vec] += 1
                if attr["lemma"] in high_freq_lemmas:
                    if attr["lemma"] not in weight_vec:
                        weight_vec[attr["lemma"]] = Counter()
                    var_vec = (word["lemma"], parent, word["cpostag"])
                    weight_vec[attr["lemma"]][var_vec] += 1
    return weight_vec

#this was only used for the report...
def print_pmi_similarities(pmi):
    print("PMI SIMILARITIES: \n")
    for target in TARGET_WORDS:
        target_pmi = pmi[target]
        sorted_pmi = sorted(target_pmi, key=target_pmi.__getitem__,reverse = True)
        print("\n" + target + " ")
        i = 0
        count = 0
        #for i in sorted_pmi[-20:]:
        while count < 20:
            if sorted_pmi[i][0] != target:
                print(str(target_pmi[sorted_pmi[i]]) + " " + sorted_pmi[i][0] + " ")
                count += 1
            i += 1
    
def execute(co_type,file_name):
    dataset = helper.load_and_parse_file(file_name)
    word_counter = helper.count_words_appearances(dataset)
    high_freq_lemmas = helper.get_high_freq_lemmas(word_counter, LEMMA_THRESH)
    helper.save_most_freq_to_file(word_counter,LEMMA_FREQUENT_FILE,LEMMA_FREQUENT_SAVE)
    
    if co_type == "1":
        print("case 1")
        lemma_sentences = helper.convert_to_sentences(dataset,True)
        weight_vectors1 = calc_weight_sentence(lemma_sentences,high_freq_lemmas)
        pmi_vectors1 = helper.calc_pmi_vectors(weight_vectors1,word_counter,high_freq_lemmas)
        #print_pmi_similarities(pmi_vectors1)
        helper.calc_similarities(TARGET_WORDS,pmi_vectors1,SIMILARITIES_NUM)
    elif co_type == "2":
        print("case 2")
        weight_vectors2 = calc_weight_window(dataset,FUNCTIONAL_WORDS)
        pmi_vectors2 = helper.calc_pmi_vectors(weight_vectors2,word_counter,high_freq_lemmas)
        #print_pmi_similarities(pmi_vectors2)
        helper.calc_similarities(TARGET_WORDS,pmi_vectors2,SIMILARITIES_NUM)
    elif co_type == "3":
        print("case 3")
        sentences = helper.convert_to_sentences(dataset)
        weight_vectors3 = calc_weight_dependency(sentences,high_freq_lemmas)
        print("size features: " + str(len(weight_vectors3)))
        dep_context_counter = helper.count_dep_contexts(weight_vectors3)
        helper.save_dep_to_file(dep_context_counter,DEPENDENCY_FILE,DEPENDENCY_SAVE)
        pmi_vectors3 = helper.calc_pmi_vectors(weight_vectors3,dep_context_counter,high_freq_lemmas)
        #print_pmi_similarities(pmi_vectors3)
        helper.calc_similarities(TARGET_WORDS,pmi_vectors3,SIMILARITIES_NUM)
    print("Done!")

if __name__ == "__main__":
    co_type = sys.argv[1]
    file_name = sys.argv[2]
    #co_type = "3"
    #file_name = "wikipedia.tinysample.trees.lemmatized.txt"
    #file_name = "wikipedia.sample.trees.lemmatized"
    LEMMA_THRESH = 100
    LEMMA_FREQUENT_SAVE = 50
    LEMMA_FREQUENT_FILE = "counts_words.txt"
    DEPENDENCY_SAVE = 50
    DEPENDENCY_FILE = "counts_contexts_dep.txt"
    SIMILARITIES_NUM = 20
    #TARGET_WORDS = ["a","that"]
    TARGET_WORDS = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar", "piano"]        
    FUNCTIONAL_WORDS = set(['IN', 'PRP', 'PRP$', 'WDT', 'PDT', 'DT', 'CC', 'RP', 'TO', ',', '.', '(', ')', ';', 'MD', 'POS'])
    execute(co_type,file_name)