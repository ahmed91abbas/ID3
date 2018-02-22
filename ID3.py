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
    for key in attributes:
        if key == "Pat":
            return key
    for key in attributes:
        if key == "Hun":
            return key
    for key in attributes:
        if key == "Type":
            return key
    for key in attributes:
        if key == "Fri":
            return key
    return key

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

def decision_tree_learning(examples, attributes, parent_examples, classifier, indent):
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
        a = importance(attributes, examples)
        indent = indent + 1
        tree = ""
        test = []
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
            subtree = decision_tree_learning(exs, attributes, examples, classifier, indent)
            test.append(str(a) + " = " + str(v))
            test.append(subtree)
        return test

def print_tree(node, nbr_indent):
    indent = "    " * nbr_indent
    if type(node) != list:
        if "=" not in node:
            indent = indent + "    "
        print(indent + node)
    else:
        for n in node:
            print_tree(n, nbr_indent + 1)

attributes, examples, classifier = arrfReader("data//restaurang.arff")
tree = decision_tree_learning(examples, attributes, examples, classifier, 0)
for node in tree:
    print_tree(node, 0)
