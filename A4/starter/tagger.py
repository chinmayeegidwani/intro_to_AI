# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import re
from collections import Counter

def train_frequency(train_tags, train_words):
    # Returns dictionary key:value --> word: tag
    # tag = most frequently ocurring tag for word in the train set

    final = dict()
    # loop through train words
    # for every tag, add it to final[word][tag] count
    # return dict containing most frequent counts

    #print(train_words)
    #print(train_tags)

    zipped = zip(train_tags, train_words)
    #print(tuple(zipped))
    d = Counter(zipped)
    #print("\n")
    #print(d)
    #print("\n")
    #print(d.most_common(10))

    for word, tag in d:
        #d = Counter(zip(train_words[i], train_tags[i]))
        #print(d[word, tag])
        word_count = d[word, tag]
        if word not in final.keys():
            # if word has not been added to final dict yet
            final[word] = {tag:word_count}
        elif final.get(word).get(tag):
            final[word][tag] += 1 # if already in final dict, count++
        else:
            final[word][tag] = word_count
    #print(final)
    #print(final.items())
    table = dict()
    for word, tag in final.items():
        max_count = max(tag.keys(), key = (lambda key: tag[key]))
        table[word] = max_count
    #print(table)
    return table

def make_test_dic(freq_dict, test_words):
    # Use trained freq dict to predict test words
    # return dict of word:prediction
    pred = []
    for word in test_words:
        if word in freq_dict.keys():
            pred.append((word, freq_dict[word]))
            #pred[word] = freq_dict[word]
        else:
            pred.append((word, 'VVD'))
    return pred

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    #print("Tagging the file.")
    train_words = []
    train_tags = []f
    test_words = []
    # separate words and tags into lists
    for file in training_list:
        train = open(file)
        #print(train)
        for line in train.readlines():
            train_words.append(re.split(' : ', line)[0].strip('\n'))
            train_tags.append(re.split(' : ', line)[1].strip('\n'))
            #train_tags.append()
            #print(line)
            #break

    freq_dict = train_frequency(train_words, train_tags)
    test = open(test_file)
    for line in test.readlines():
        test_words.append(line.strip('\n'))

    pred_dict = make_test_dic(freq_dict, test_words)
    #print(pred_dict)
    f = open(output_file, "w")
    for pred in pred_dict:
        line = str(pred[0]) + ' : ' + str(pred[1]) + '\n'
        f.write(line)
    f.close()


    #
    # YOUR IMPLEMENTATION GOES HERE
    #

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    #print(training_list)
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)