import xml.etree.ElementTree as ET
import copy 
import sys 
import time

## parse the xml file to get variable names and probability distributions. 
## Generated a nested dictionary that saves parents, children and true probabilities of variables.
def parse(tree,name):
    
    net = {}
    variables = []
    root = tree.getroot()

    for var in root.findall('.//VARIABLE/NAME'):
        net[var.text] = {'parents':[], 'children':[], 'prob':[], 'cond_prob':[]}
        if name != "dog-problem.xml":
            variables.append(var.text)
        else:
            variables = ["bowel-problem","family-out","dog-out","light-on","hear-bark"]
   
    for item in root.findall('.//DEFINITION'):

        variable = item.find('FOR')
        
        if item.findall('.//GIVEN'):
            for element in item.findall('.//GIVEN'):

                net[variable.text]['parents'].append(element.text)
                net[element.text]['children'].append(variable.text)

                probDistrTable = item.find('TABLE')
                k = probDistrTable.text.split()

                prob = []
                prob_append = []
                
                if len(k) == 8:
                    prob.append(k[0])
                    prob.append(k[2])
                    prob.append(k[4])
                    prob.append(k[6])
            

                if len(k) == 4:

                    prob.append(k[0])
                    prob.append(k[2])

            for j in prob:
                if j not in prob_append:
                    prob_append.append(j)



            net[variable.text]['cond_prob'].append(prob_append)
           
        else:
            
            probDistrTable = item.find('TABLE')
            k = probDistrTable.text.split()
            net[variable.text]['prob'].append(k[0])

    return net, variables

## function to normalize true and false counts and returns probability
def normalize(QX):
    total = 0
    
    for val in QX.values():
        total = total + val 
    for key in QX.keys():
        QX[key] = QX[key]/total

    return QX

# inputs query variable, evidence and bayesian network
# outputs a singular probability value given certain value of query variable
def querygiven(y,e,net):

    value = 0
    if net[y]['parents'] == []:
        if e[y] == 'True':
            value = float(net[y]['prob'][0])
        else:
            value = 1 - float(net[y]['prob'][0])

    else:
        parent = []
        n = len(net[y]['parents'])
        for p in net[y]['parents']:
            parent.append(e[p])


        if n == 1:
            if e[y] == 'True':
                if parent[0] == 'True':
                    value = float(net[y]['cond_prob'][0][0])
                else:
                    value = float(net[y]['cond_prob'][0][1])
            else:
                if parent[0] == 'True':
                    value = 1 - float(net[y]['cond_prob'][0][0])
                else:
                    value = 1 - float(net[y]['cond_prob'][0][1])

        elif n == 2:
        
            if e[y] == 'True':
                if parent[0] == 'True' and parent[1] == 'True':
                    value = float(net[y]['cond_prob'][0][0])
                elif parent[0] == 'True' and  parent[1] == 'False':
                    value = float(net[y]['cond_prob'][0][1])
                elif  parent[0] == 'False' and parent[1] == 'True' :
                    value = float(net[y]['cond_prob'][0][2])
                elif  parent[0] == 'False' and  parent[1] == 'False':
                    value = float(net[y]['cond_prob'][0][3])

            else:
                if parent[0] == 'True' and parent[1] == 'True':
                    value = 1 - float(net[y]['cond_prob'][0][0])
                elif parent[0] == 'True' and  parent[1] == 'False':
                    value = 1 - float(net[y]['cond_prob'][0][1])
                elif  parent[0] == 'False' and parent[1] == 'True' :
                    value = 1 - float(net[y]['cond_prob'][0][2])
                elif  parent[0] == 'False' and  parent[1] == 'False':
                    value = 1 - float(net[y]['cond_prob'][0][3])

  
    return value 

##assigns both True False values to query variable and then call enumeration_all
def enumeration_ask(q,e,variables,net):
    QX = {}
    for x in ['True', 'False']:
        e1 = copy.deepcopy(e)
        e1[q]= x
        QX[x] = enumeration_all(variables,e1,net)

    return normalize(QX)

##calculates the probability value given evidence by 
##summation of non evidence variables over product of the probability distribution.
def enumeration_all(variables,e,net):
    e2 = copy.deepcopy(e)
    
    if len(variables) == 0:
        return 1
    Y = variables[0]
   
    if Y in e:
        a = querygiven(Y,e,net)
        ret = a*enumeration_all(variables[1:],e,net)
       
        return ret
    else:
       
        probability = []
        #total = 0
        e2[Y] = 'True'
        b = querygiven(Y,e2,net)
        
        ans = b*enumeration_all(variables[1:],e2,net) 
        probability.append(ans)
        e2[Y] = 'False'
        c = querygiven(Y,e2,net)
        
        ans1 = c*enumeration_all(variables[1:],e2,net) 
        probability.append(ans1)
       
        total = sum(probability)
        return total

e={}

n = int(input("Enter number of evidence variables"))

xml_name= sys.argv[1]
q = sys.argv[2]


if n == 1:
    a = sys.argv[3]
    a_val = sys.argv[4]
    e[a]=a_val

if n == 2:
    a = sys.argv[3]
    a_val = sys.argv[4]
    e[a]=a_val
  

    b = sys.argv[5]
    b_val = sys.argv[6]
    e[b]=b_val

if n == 3:
    a = sys.argv[3]
    a_val = sys.argv[4]
    e[a]=a_val

    b = sys.argv[5]
    b_val = sys.argv[6]
    e[b]=b_val

    c = sys.argv[7]
    c_val = sys.argv[8]
    e[c]=c_val

if n == 4:
    a = sys.argv[3]
    a_val = sys.argv[4]
    e[a]=a_val

    b = sys.argv[5]
    b_val = sys.argv[6]
    e[b]=b_val

    c = sys.argv[7]
    c_val = sys.argv[8]
    e[c]=c_val

    d = sys.argv[9]
    d_val = sys.argv[10]
    e[d]=d_val


start = time.time()
tree = ET.parse("aima-alarm.xml")
bn,var = parse(tree, xml_name)
dist = enumeration_ask(q,e,var,bn)
end = time.time()

print("FINAL ANSWER", dist)


