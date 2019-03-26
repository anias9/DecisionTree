from math import log

def read_file():
    with open('tes.txt', 'r') as file:
        element = [line.strip() for line in file]

    return [el.split(' ') for el in element]    

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
    entropy = 0
    for i in dictoniary_values.keys():
        p = dictoniary_values[i]/ rowNumber
        entropy += -p * log(p,2)
    return entropy

atrrNumber = len(read_file()[0])-1 #odjąć decyzyjna
decyzja = [row[len(read_file()[0])-1] for row in read_file()] #wyodrębniona tabela decyzyjna
rowNumber = len([row[0] for row in decyzja])



print("=====")
print(unique_values(read_file(), atrrNumber))
print(propability(unique_values(read_file(), atrrNumber)))
print("Entropia (dec): ", entropy(unique_values(read_file(), atrrNumber)))
print("=====")
    

def gain(dataSet):
    all_gains= []
    decyzja = [row[len(dataSet[0])-1] for row in dataSet] #wyodrębniona tabela decyzyjna
    atrrNumber = len(dataSet[0])-1 #odjąć decyzyjna
    rowNumber = len([row[0] for row in decyzja])
    
    for el in range(atrrNumber): # dla każdej kolumny
        actualCol = [row[el] for row in dataSet]
        atrr = unique_values(dataSet, el)
        sumAtrr = sum(atrr.values())
        p={}
        entr = entropy(atrr) #entropia
        
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
            prop = propability(d)
            print("\t", d)            
            print("\t", prop)
            print("\t", (-1)*sum([p * log(p,2) for p in prop if p!=0]),'*', suma2/sumAtrr)
            
            info += (suma2/sumAtrr * (-1)*sum([p * log(p,2) for p in prop if p!=0]))
            split += (suma2/sumAtrr * (-1)*sum([suma2/sumAtrr * log(suma2/sumAtrr,2) for p in prop if p!=0]))

        gain = entropy(unique_values(dataSet, atrrNumber)) - info
        all_gains.append(gain)
        """
        print("Info A{0}: {1}".format(el + 1, info))
        print("Gain: ", gain)
        print("Split: ", split)
        if split > 0:
            print("Gain Ratio: ", gain/split)
        print("\n")"""
                        
    return all_gains

def best_gain(gains):
    bestGain = 0
    for gain in gains:
        if gain > bestGain:
            bestGain = gain
            att = gains.index(gain) + 1
    
    return att, bestGain


#dataSet without rows contain value on node
def new_dataSet(dataSet, row_nb):
    newSetG, newSetL  = []

    for row in dataSet:
        if dataSetG.index(row) != row_nb:
            newSetG.append(row)
        else:
            newSetL.append(row)
        
    return newSetG, newSetL

     
def build_tree(dataSet):
    att, gain = best_gain(gain(dataSet))

    #If S is empty, return a single node with value Failure;

    if not dataSet:
        return "Empty data"

    """
    function ID3 (R: a set of non-categorical attributes,
		 C: the categorical attribute,
		 S: a training set) returns a decision tree;
       begin
	If S is empty, return a single node with value Failure;
	If S consists of records all with the same value for 
	   the categorical attribute, 
	   return a single node with that value;
	If R is empty, then return a single node with as value
	   the most frequent of the values of the categorical attribute
	   that are found in records of S; [note that then there
	   will be errors, that is, records that will be improperly
	   classified];
	Let D be the attribute with largest Gain(D,S) 
	   among attributes in R;
	Let {dj| j=1,2, .., m} be the values of attribute D;
	Let {Sj| j=1,2, .., m} be the subsets of S consisting 
	   respectively of records with value dj for attribute D;
	Return a tree with root labeled D and arcs labeled 
	   d1, d2, .., dm going respectively to the trees 

	     ID3(R-{D}, C, S1), ID3(R-{D}, C, S2), .., ID3(R-{D}, C, Sm);
   end ID3;
    """
          
    build_tree(new_dataSet(dataSet, att))
    
    return [att, gain]


def end_of_tree(dataSet):
    pass


#print builded tree
def print_tree(node):
    pass


#print(build_tree(read_file()))
print("Najlepszy jest A{0}, ponieważ ma najwiekszy Gain: {1} ".format(best_gain(gain(read_file()))[0], best_gain(gain(read_file()))[1]))

