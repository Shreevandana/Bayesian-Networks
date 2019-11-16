import xml.etree.ElementTree as ET
import copy 
import random
import sys 
import time
import matplotlib.pyplot as plt

## parse the xml file to get variable names and probability distributions. 
## Generated a nested dictionary that saves parents, children and true probabilities of variables.
def parse(tree):
    net = {}
    variables = []
    root = tree.getroot()

    for var in root.findall('.//VARIABLE/NAME'):
        net[var.text] = {'parents':[], 'children':[], 'prob':[], 'cond_prob':[]}
        variables.append(var.text)

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

## generate a random sample 
def prior_sample(net, variables):

    prior_values = {}

    x = ['True', 'False']

    for i in variables:
        
        prior_values[i] = random.choice(x)

    return prior_values 

## function to generate samples that are consistent with the evidence 
def rejection_sampling(q,e,net,n_sample,variables):
    N = {'True':0, 'False':0}
    for i in range(0,n_sample):
        sample_values = prior_sample(net,variables)

        ## check for consistency 

        for j in sample_values:
            if j in e and sample_values[j] == e[j]:
                    N[sample_values[q]] += 1

    total = float(N['True'] + N['False'])
    
    QX = {'True': N['True']/total, 'False': N['False']/total}

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

e={}
n = int(input("Enter number of evidence variables"))
n_sample = int(sys.argv[1])
q = sys.argv[3]

if n == 1:
    a = sys.argv[4]
    a_val = sys.argv[5]
    e[a]=a_val

if n == 2:
    a = sys.argv[4]
    a_val = sys.argv[5]
    e[a]=a_val
  

    b = sys.argv[6]
    b_val = sys.argv[7]
    e[b]=b_val

if n == 3:
    a = sys.argv[4]
    a_val = sys.argv[5]
    e[a]=a_val

    b = sys.argv[6]
    b_val = sys.argv[7]
    e[b]=b_val

    c = sys.argv[8]
    c_val = sys.argv[9]
    e[c]=c_val

if n == 4:
    a = sys.argv[4]
    a_val = sys.argv[5]
    e[a]=a_val

    b = sys.argv[6]
    b_val = sys.argv[7]
    e[b]=b_val

    c = sys.argv[8]
    c_val = sys.argv[9]
    e[c]=c_val

    d = sys.argv[10]
    d_val = sys.argv[11]
    e[d]=d_val

tree = ET.parse("aima-alarm.xml")
start = time.time()
bn,var = parse(tree)

x = rejection_sampling(q,e,bn,n_sample,var)
print(x)