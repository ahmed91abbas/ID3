#!/usr/bin/python3
import random
import copy

def arrfReader(path):
    attributes = {}
    attributesNames = []
    examples = []
    classifier = ""
    with open(path) as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        if line[0] == '%' or line == "\n":
            continue
        if "@attribute" in line:
            line = line[:-1]
            whiteSpaceIndex = line.find(" ")
            line = line[whiteSpaceIndex+1:]
            whiteSpaceIndex = line.find(" ")
            key = line[:whiteSpaceIndex]
            line = line[whiteSpaceIndex+1:] #the values are left
            line = line.replace(",", "")
            line = line.replace("{", "")
            line = line.replace("}", "")
            values = line.split(" ")
            attributes[key] = values
            classifier = key
            attributesNames.append(key)
        elif line[0] == '@':
            continue
        else:
            line = line[:-1]
            values = line.split(",")
            for i in range(len(values) - 1):
                value = values[i]
                values[i] = (attributesNames[i], value)
            examples.append(values)
    classifierValues = attributes[classifier]
    attributes.pop(classifier)
    return attributes, examples, classifierValues

def importance(attributes, examples):
    key = None
    for key in attributes:
        key = key
    return key

def plurality_value(examples, classifier):
    counter0 = 0
    counter1 = 0
    firstValue = classifier[0]
    secondValue = classifier[1]
    for example in examples:
        classification = example[len(example) -1]
        if(classification == firstValue):
            counter0 = counter0 + 1
        else:
            counter1 = counter1 + 1
    if counter0 >= counter1:
        return firstValue
    else:
        return secondValue

def decision_tree_learning(examples, attributes, parent_examples, classifier):
    classificationList = []
    for example in examples:
        classificationList.append(example[len(example)-1])

    if not examples: #examples is empty
        return plurality_value(parent_examples, classifier)


    elif all(x == classificationList[0] for x in classificationList):
        return classification[0]

    elif not attributes:
        return plurality_value(examples, classifier)

    else:
        a = importance(attributes, examples)
        tree = ""
        attribute_values = copy.deepcopy(attributes[a])
        for v in attribute_values:
            exs = []
            for ex in examples:
                for value in ex:
                    if value[0] == a and value[1] == v:
                        exs.append(ex)
            try:
                attributes.pop(a)
            except:
                continue
            subtree = decision_tree_learning(exs, attributes, parent_examples, classifier)
            tree = tree + str(a) + " = " + str(v) + "\n"
            tree = tree + str(subtree)
        print(tree)




attributes, examples, classifier = arrfReader("data//restaurang.arff")
decision_tree_learning(examples, attributes, examples, classifier)
