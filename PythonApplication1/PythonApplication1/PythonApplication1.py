from math import log

def read_file():
    with open('test2.txt', 'r') as file:
        element = [line.strip() for line in file]

    lista = [el.split(',') for el in element]
    return lista

kolumna = {}

decyzja = [row[len(read_file()[0])-1] for row in read_file()] #wyodrębniona tabela decyzyjna
ileKolumn = len(read_file()[0])-1 #odjąć decyzyjna
ileWierszy = len([row[0] for row in decyzja])
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
        p = dictoniary_values[i]/ ileWierszy
        entropy += -p * log(p,2)
    return entropy


print("=====")
print(unique_values(read_file(), ileKolumn))
print(propability(read_file(),unique_values(read_file(), ileKolumn)))
print("Entropia (dec): ", entropy(read_file(),unique_values(read_file(), ileKolumn)))
print("=====")
bestGain = 0 



def decisions(dataSet):
    bestGain = 0
    bestAtt = 0 
    for el in range(ileKolumn): # dla każdej kolumny
        danaKolumna = [row[el] for row in lista]
        atrybuty = unique_values(dataSet, el)
        sumaAtrybutow = sum(atrybuty.values())
        p={}
        entr = entropy(lista,atrybuty) #entropia
        
        print("A", el+ 1)
        print(atrybuty)
        print(sumaAtrybutow)
                
        for row_number, row in enumerate(danaKolumna):#po wartosciach w danej kolumnie
            temp = [decyzja[rowNb] for rowNb, row2 in enumerate(danaKolumna) if row2 == row]
            p[row] = {a:  temp.count(a) for wart in temp for a in decyzja}

        info=0
        split = 0
        
        for k in sorted(p.keys()): 
            print("Decyzje")
            d = p[k]
            suma2 = sum(d.values())
            prop = propability(lista, d)
            print("\t", d)            
            print("\t", prop)
            print("\t", (-1)*sum([p * log(p,2) for p in prop if p!=0]),'*', suma2/sumaAtrybutow)
            info += (suma2/sumaAtrybutow * (-1)*sum([p * log(p,2) for p in prop if p!=0]))
            split += (suma2/sumaAtrybutow * (-1)*sum([suma2/sumaAtrybutow * log(suma2/sumaAtrybutow,2) for p in prop if p!=0]))

        gain = entropy(lista,unique_values(lista, ileKolumn)) - info
            
        print("Info A{0}: {1}".format(el + 1, info))
        print("Gain: ", gain)
        print("Split: ", split)
        print("Gain Ratio: ", gain/split)
        print("\n")

        if gain > bestGain:
            bestGain = gain
            bestAtt = el + 1
            
        kolumna[el+1] = p
            
    return "Wybrany atrybut A{0}, bo w tym przypadku najwyższa jest wartość Gain: {1}".format(bestAtt, bestGain)

print(decisions(lista))

