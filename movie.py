import csv
from math import log
import operator
import random

def calcEntropy(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:  # the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    Ent = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        Ent -= prob * log(prob, 2)  # log base 2
    return Ent


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]  # chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # the last column is used for the labels
    baseEntropy = calcEntropy(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1
    for i in range(numFeatures):  # iterate over all the features
        featList = [example[i] for example in dataSet]  # create a list of all the examples of this feature
        uniqueVals = set(featList)  # get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcEntropy(subDataSet)


        infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy

        if (infoGain > bestInfoGain):  # compare this to the best gain so far
            bestInfoGain = infoGain  # if better than current best, set to best
            bestFeature = i
    return bestFeature  # returns an integer


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    # extracting data
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]  # stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
        return majorityCnt(classList)

    # use Information Gain
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]

    #build a tree recursively
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    for value in uniqueVals:
        subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)

    return myTree

def print_tree(mytree, level=0):
    if not hasattr(mytree, 'keys'):
        print "%s%s" % ('-' * level, mytree)
        return

    keys = mytree.keys()
    for k in keys:
        print "%s%s" % ('-' * level,k)
        print_tree(mytree[k], level + 1)


def csv_dict_reader(file_obj):
    dataset = []
    reader = csv.DictReader(file_obj, delimiter=',')

    labels = ["movie_title"]

    for col in reader:
        geners = col["genres"].split("|")
        for g in geners:
            if g not in labels:
                labels.append(g)

    file_obj.seek(0)
    reader.next()

    for col in reader:
        vec = []
        vec.insert(0, col["movie_title"])
        for i in range(1,len(labels)-1):
            vec.insert(i, 0)
        geners = col["genres"].split("|")
        for g in geners:
            for i in range(1, len(labels) - 1):
                if labels[i] == g:
                    vec[i] = 1
        dataset.append(vec)
    return dataset, labels

def print_table(dataset, lables):
    print labels
    for i in dataset:
        print i

def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)

    try:
        key = testVec[featIndex]
    except:
        return "unknown"

    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel


# Arrange data
f_obj = open("movies.csv")
dataset, labels = csv_dict_reader(f_obj)

# Split into training/test
# Give user decide which movie he likes

dataTraining = []
print "For each movie please enter L if you like, N if you don't like\n and D if you don't know this movie\n"
for i in range(0,20):
    answer = 'D'
    removedVec = []
    while answer == 'D':
        t = random.randint(0, len(dataset) - 1)
        removedVec = dataset[t]
        print "\"%s\" | L/N/D" % removedVec[0]
        answer = raw_input().upper()
    removedVec.append(answer)
    removedVec.remove(removedVec[0])
    dataTraining.append(removedVec)


labelsForModel = list(labels)
labelsForModel.remove(labelsForModel[0])

# Build model
movietree =createTree(dataTraining, labelsForModel)

# Run model on test data
print "movies you will like: "
for vec in dataset:
    cl = classify(movietree, labels, vec)
    if cl == 'L':
        print vec[0]
