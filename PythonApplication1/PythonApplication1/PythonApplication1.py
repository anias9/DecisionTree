from math import log

def read_file():
    with open('test2.txt', 'r') as file:
        element = [line.strip() for line in file]

    lista = [el.split(',') for el in element]
    return lista

kolumna = {}

decyzja = [row[len(read_file()[0])-1] for row in read_file()] #wyodrębniona tabela decyzyjna
atrrNumber = len(read_file()[0])-1 #odjąć decyzyjna
rowNumber = len([row[0] for row in decyzja])
unikatoweD = list(set([row[0] for row in decyzja])) #unikatowe w decyzji

def unique_values(dataSet, col):
    counts = {} 
    for row in dataSet:
        label = row[col]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def propability(dataSet, dictoniary_values):
    prob = []
    suma = sum(dictoniary_values.values())
    for i in dictoniary_values.keys():
        p = dictoniary_values[i]/ suma
        prob.append(p)
    return prob
        
    
def entropy(dataSet, dictoniary_values):
    entropy = 0
    for i in dictoniary_values.keys():
        p = dictoniary_values[i]/ rowNumber
        entropy += -p * log(p,2)
    return entropy


print("=====")
print(unique_values(read_file(), atrrNumber))
print(propability(read_file(),unique_values(read_file(), atrrNumber)))
print("Entropia (dec): ", entropy(read_file(),unique_values(read_file(), atrrNumber)))
print("=====")

def best_gain(dataSet):
    bestGain = 0
    bestAtt = 0 
    for el in range(atrrNumber): # dla każdej kolumny
        actualCol = [row[el] for row in dataSet]
        atrr = unique_values(dataSet, el)
        sumAtrr = sum(atrr.values())
        p={}
        entr = entropy(dataSet,atrr) #entropia
        
        print("A", el+ 1)
        print(atrr)
        print(sumAtrr)
                
        for row_number, row in enumerate(actualCol):#po wartosciach w danej kolumnie
            temp = [decyzja[rowNb] for rowNb, row2 in enumerate(actualCol) if row2 == row]
            p[row] = {a:  temp.count(a) for wart in temp for a in decyzja}

        info=0
        split = 0
        
        for k in sorted(p.keys()): 
            print("Decyzje")
            d = p[k]
            suma2 = sum(d.values())
            prop = propability(dataSet, d)
            print("\t", d)            
            print("\t", prop)
            print("\t", (-1)*sum([p * log(p,2) for p in prop if p!=0]),'*', suma2/sumAtrr)
            
        info += (suma2/sumAtrr * (-1)*sum([p * log(p,2) for p in prop if p!=0]))
        split += (suma2/sumAtrr * (-1)*sum([suma2/sumAtrr * log(suma2/sumAtrr,2) for p in prop if p!=0]))
        gain = entropy(dataSet,unique_values(dataSet, atrrNumber)) - info
            
        print("Info A{0}: {1}".format(el + 1, info))
        print("Gain: ", gain)
        print("Split: ", split)
        print("Gain Ratio: ", gain/split)
        print("\n")

        if gain > bestGain:
            bestGain = gain
            bestAtt = el + 1
            
        kolumna[el+1] = p
            
    #return "Wybrany atrybut A{0}, bo w tym przypadku najwyższa jest wartość Gain: {1}".format(bestAtt, bestGain)
    return bestAtt, bestGain


def split_dataSet(dataSet, row_nb):
    newSet = []
    pass
        
    
def build_tree(dataSet):
    att, gain = best_gain(dataSet)
    
    if gain == 0:
        return end_of_tree()
    
    return [att, gain]

def end_of_tree(dataSet):
    pass

#print builded tree
def print_tree(node):
    pass

print(build_tree(read_file()))

    

    
    

    










    
    

