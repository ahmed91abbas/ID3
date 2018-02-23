#!/usr/bin/python3
import random
import copy
import math
import sys

'''Reads the file and returns a dict with the attributes and thier values,
a list with the examples and the classification values'''
def arrfReader(path):
    attributes = {}
    attributesNames = []
    examples = []
    classifier = ""
    with open(path) as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        line = line.replace("\t", " ")
        if line[0] == '%' or line == "\n":
            continue
        if "@attribute".lower() in line.lower():
            line = line[:-1]
            whiteSpaceIndex = line.find(" ")
            line = line[whiteSpaceIndex+1:]
            whiteSpaceIndex = line.find(" ")
            key = line[:whiteSpaceIndex]
            line = line[whiteSpaceIndex+1:] #the values are left
            line = line.replace(",", " ")
            line = line.replace("{", "")
            line = line.replace("}", "")
            values = line.split(" ")
            filtered_values = []
            for i in range(len(values)):
                value = values[i].replace(" ", "")
                if value != "":
                    filtered_values.append(value)
            attributes[key] = filtered_values
            classifier = key
            attributesNames.append(key)
        elif line[0] == '@':
            continue
        else:
            line = line[:-1]
            values = line.split(",")
            for i in range(len(values) - 1):
                value = values[i].replace(" ", "")
                values[i] = (attributesNames[i], value)
            values[len(values) - 1] = values[len(values) - 1].replace(" ", "")
            examples.append(values)
    classifierValues = attributes[classifier]
    attributes.pop(classifier)
    return attributes, examples, classifierValues

'''Selects the most common classifier value among a the examples'''
def plurality_value(examples, classifier):
    nbr_values = len(classifier)
    scores = {}
    for value in classifier:
        scores[value] = 0

    for example in examples:
        classification_value = example[len(example) -1]
        scores[classification_value] = scores[classification_value] + 1

    dominating_value = ""
    max = -1
    for key, value in scores.items():
        if value > max:
            max = value
            dominating_value = key
    return dominating_value

'''Calculates the entropy of the givin attribute among the input examples'''
def entropy(attribute, examples, classifier):
    values = attributes[attribute]
    entropy = 0
    for value in values:
        value_total = 0
        value_frequency = {}
        for class_value in classifier:
            value_frequency[class_value] = 0
        for example in examples:
            for i in range(len(example) - 1):
                if example[i][1] == value:
                    value_total = value_total + 1
                    class_value = example[len(example) - 1]
                    value_frequency[class_value] = value_frequency[class_value] + 1
        p_value = value_total / len(examples)
        e_value = 0
        for class_value in classifier:
            freq = value_frequency[class_value]
            if freq != 0:
                x = freq/value_total
                e_value = e_value - (x * math.log2(x))
        entropy = entropy + p_value * e_value
    return entropy

'''Returns the best attribute to split the tree with, which is the attribute
with the least entropy'''
def importance(attributes, examples, classifier):
    attributes_entropy = {}
    for att in attributes:
        attributes_entropy[att] = entropy(att, examples, classifier)
    min_value = sys.maxsize
    best_choise = ""
    for key, value in attributes_entropy.items():
        if value < min_value:
            min_value = value
            best_choise = key
    return best_choise

'''´The ID3 algoritem for constructing a decition tree from the input examples and attributes'''
def decision_tree_learning(examples, attributes, parent_examples, classifier):
    classificationList = []
    for example in examples:
        classificationList.append(example[len(example)-1])

    if not examples: #examples is empty
        #print("examples empty")
        return plurality_value(parent_examples, classifier)

    elif all(x == classificationList[0] for x in classificationList):
        #print("class")
        return classificationList[0]

    elif not attributes:
        #print("attr empty")
        return plurality_value(examples, classifier)

    else:
        a = importance(attributes, examples, classifier)
        tree = []
        attribute_values = copy.deepcopy(attributes[a])
        #print(a + "     "  + str(attribute_values))
        for v in attribute_values:
            #print(a + " before " + v)
            exs = []
            for ex in examples:
                for value in ex:
                    if value[0] == a and value[1] == v:
                        exs.append(ex)
            try:
                attributes.pop(a)
            except:
                pass
            subtree = decision_tree_learning(exs, attributes, examples, classifier)
            tree.append(str(a) + " = " + str(v))
            tree.append(subtree)
        return tree

#Prints the tree with indent formatting
def print_tree(node, nbr_indent):
    indent = "    " * nbr_indent
    if type(node) != list:
        if "=" not in node:
            indent = indent + "    "
        print(indent + node)
    else:
        for n in node:
            print_tree(n, nbr_indent + 1)

if __name__ == "__main__":
    nbr_arg = len(sys.argv)
    file = "restaurang.arff"
    if nbr_arg > 1:
       file = str(sys.argv[1])
    attributes, examples, classifier = arrfReader(file)
    tree = decision_tree_learning(examples, attributes, examples, classifier)
    for node in tree:
        print_tree(node, 0)
