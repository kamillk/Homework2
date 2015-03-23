import sys
import xml.dom.minidom
import time
from matrixops import floyd_warshall
from copy import deepcopy

doc = xml.dom.minidom.parse(sys.argv[1])

elements = doc.getElementsByTagName('net')
number = elements.length;
d = [[float("+inf") for x in range(number+1)] for y in range(number+1)]

for i in range(1,number+1):
    d[i][i] = 0;

capactor = doc.getElementsByTagName('capactor')
resistor = doc.getElementsByTagName('resistor')
diode = doc.getElementsByTagName('diode')

for i in range(capactor.length):
    res = float(capactor[i].attributes['resistance'].value)
    a = int(capactor[i].attributes['net_from'].value)
    b = int(capactor[i].attributes['net_to'].value)
    d[a][b] = 1/ (1/d[a][b] + 1/res)
    d[b][a] = 1/ (1/d[b][a] + 1/res)

for i in range(resistor.length):
    res = float(resistor[i].attributes['resistance'].value)
    a = int(resistor[i].attributes['net_from'].value)
    b = int(resistor[i].attributes['net_to'].value)
    d[a][b] = 1/ (1/d[a][b] + 1/res)
    d[b][a] = 1/ (1/d[b][a] + 1/res)

for i in range(diode.length):
    res = float(diode[i].attributes['resistance'].value)
    res_rev = float(diode[i].attributes['reverse_resistance'].value)
    a = int(diode[i].attributes['net_from'].value)
    b = int(diode[i].attributes['net_to'].value)
    d[a][b] = 1/ (1/d[a][b] + 1/res)
    d[b][a] = 1/ (1/d[b][a] + 1/res_rev)

cur_d = deepcopy(d)
start_python = time.time()

for k in range(1,number+1):
    for i in range(1,number+1):
        for j in range(1,number+1):
            if d[i][j] == 0 or d[i][k] == 0 and d[k][j] == 0:
                d[i][j] = 0
            elif d[i][j] == float("+inf") and d[i][k] == float("+inf") or d[i][j] == float("+inf") and d[k][j] == float("+inf"):
                d[i][j] = float("+inf")
            else:
                d[i][j] = 1/ (1/d[i][j]+ 1/(d[i][k]+d[k][j]))

finish_python = time.time()


start_c = time.time()
d = floyd_warshall(cur_d)
finish_c = time.time()

cur_f = sys.argv[2]
f = open(cur_f, 'w')
for i in range(1,number+1):
    for j in range(1,number+1):
        f.write("{},".format(round(d[i][j],6)))
    f.write("\n")
f.close()

print((finish_python - start_python)/(finish_c - start_c))


    
            


    
