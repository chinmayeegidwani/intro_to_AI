# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import re
from collections import Counter

def train_frequency(train_words, train_tags):
    # Returns dictionary key:value --> word: tag
    # tag = most frequently ocurring tag for word in the train set

    final = dict()
    # loop through train words
    # for every tag, add it to final[word][tag] count
    # return dict containing most frequent counts

    #print(train_words)
    #print(train_tags)

    zipped = zip(train_words, train_tags)
    #print(tuple(zipped))
    d = Counter(zipped)
    #print("\n")
    #print(d)
    #print("\n")
    for word, tag in d:
        #d = Counter(zip(train_words[i], train_tags[i]))
        #print(d[word, tag])
        tag_count = d[word, tag]
        if word not in final.keys():
            # if word has not been added to final dict yet
            final[word] = {tag:tag_count}
        elif final.get(word).get(tag):
            final[word][tag] += 1 # if already in final dict, count++

    #print(final)

    return final

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    #print("Tagging the file.")
    train_words = []
    train_tags = []

    # separate words and tags into lists
    for file in training_list:
        train = open(file)
        #print(train)
        for line in train.readlines():
            train_words.append(re.split(' : ', line)[0])
            train_tags.append(re.split(' : ', line)[1])
            #train_tags.append()
            #print(line)
            #break

    train_frequency(train_words, train_tags)










    #
    # YOUR IMPLEMENTATION GOES HERE
    #

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    print(training_list)
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)