from math import log
import json


def read_file():
    with open('test.txt', 'r') as file:
        element = [line.strip() for line in file]

    return [el.split(',') for el in element]

#counts unique values in given column
def unique_values(dataSet, col):
    counts = {}
    for row in dataSet:
        label = row[col]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def propability(dictoniary_values):
    prob = []
    suma = sum(dictoniary_values.values())
    for i in dictoniary_values.keys():
        p = dictoniary_values[i]/ suma
        prob.append(p)
    return prob


def entropy(dictoniary_values):
    entr = 0
    for i in dictoniary_values.keys():
        p = dictoniary_values[i]/rowNumber
        entr += -p * log(p, 2)
    return entr


def decision_column(dataSet):
    return [example[-1] for example in dataSet]


#for decision column
decyzja = [row[len(read_file()[0])-1] for row in read_file()] #decision table
rowNumber = len([row[0] for row in decyzja])
atrrNumber = len(read_file()[0])-1 #without decision table

print("=====")
print(unique_values(read_file(), atrrNumber))
print(propability(unique_values(read_file(), atrrNumber)))
print("Entropia (dec): ", entropy(unique_values(read_file(), atrrNumber)))
print("=====")


def gain(dataSet):
    atrrNumber = len(dataSet[0])-1
    all_gains= []
    print(atrrNumber)
    for el in range(atrrNumber): # for each column
        actualCol = [row[el] for row in dataSet]
        atrr = unique_values(dataSet, el)
        sumAtrr = sum(atrr.values())
        p={}
        entr = entropy(atrr) #entropia

        print("A", el+ 1)
        print(atrr)
        print(sumAtrr)

        for row_number, row in enumerate(actualCol):#po wartosciach w danej kolumnie
            temp = [decision_column(dataSet)[rowNb] for rowNb, row2 in enumerate(actualCol) if row2 == row]
            p[row] = {a:  temp.count(a) for wart in temp for a in decision_column(dataSet)}

        info=0
        split = 0

        for k in sorted(p.keys()):
            #print("Decyzje")
            d = p[k]
            suma2 = sum(d.values())
            prop = propability(d)
            #print("\t", d)
            #print("\t", prop)
            #print("\t", (-1)*sum([p * log(p,2) for p in prop if p!=0]),'*', suma2/sumAtrr)

            info += (suma2/sumAtrr * (-1)*sum([p * log(p,2) for p in prop if p!=0]))
            split += ((-1)*sum([suma2/sumAtrr * log(suma2/sumAtrr,2)]))

        gain = entropy(unique_values(dataSet, atrrNumber)) - info
        all_gains.append(gain)

        print("Info A{0}: {1}".format(el + 1, info))
        print("Gain: ", gain)
        print("Split: ", split)
        if split > 0:
            print("Gain Ratio: ", gain/split)
        print("\n")

    return all_gains


def best_gain(gains):
    bestGain = -1
    for gain in gains:
        if gain > bestGain:
            bestGain = gain
            att = gains.index(gain)

    return att, bestGain


def class_counts(rows):
    counts = {}
    for row in rows:
        if row not in counts.keys():
            counts[row] = 0
        counts[row] += 1
    return max(counts) #max appearing el

#create new dataSet
#The filtered sample set whose value is the value of the axis feature and does not contain the data axis
def new_data(dataSet, axis, value):
    newSet = []
    for sample in dataSet:
        if sample[axis] == value:
            newSetSample = sample[:axis]        #making copy
            newSetSample.extend(sample[axis+1:])#extends the list by adding all items of a list
            newSet.append(newSetSample)     #add to new Set
    return newSet

#feature -> decision table
def build_tree(dataSet):
    bestFeature, bestGain = best_gain(gain(dataSet))
    classList = decision_column(dataSet)

    #Conditions to stop dividing
    #The last item in the data set: the label is the same value (same category)
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    #If S is empty, return a single node with value Failure;
    if not dataSet:
        return "Empty data"

    if bestGain < 0 or bestGain == 0:
        return class_counts(classList)

    #Remaining labels
    if len(dataSet[0]) == 1:
        return class_counts(classList)

    # Creating tree
    best_feature_name = "A" + str(bestFeature+1)
    tree = { best_feature_name: {}}

    #delete bestFeature from feature table
    featuresample = [example[bestFeature] for example in dataSet]

    uniqueVals = set(featuresample)

    for value in uniqueVals:
        tree[best_feature_name][value] = build_tree(new_data(dataSet, bestFeature, value))

    return tree


def print_tree(d, indent=0):
    for key, value in d.items():
        print('\t*' * indent + str(key))
        print("|")

        if isinstance(value, dict):
            print_tree(value, indent+1)
        else:
            print('\t-' * (indent+1) + str(value))


data = read_file()
myTree = build_tree(data)
print(json.dumps(myTree, indent=4, sort_keys=True))  # It will print the keys in ascending order, not in descending

#print_tree(myTree)
#print("Najlepszy jest A{0}, ponieważ ma najwiekszy Gain: {1} ".format(best_gain(gain(read_file()))[0], best_gain(gain(read_file()))[1]))
