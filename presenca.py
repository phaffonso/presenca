#!/usr/bin/python

import sys
import csv

def time2f(time):
    h,m,s = time.split(':')
    return int(h) + int(m)/60.0
    
def calcPresenca(lista):
    horamin = [17.5, 18.5, 20.25, 22]
    horamax = [18.25, 19.35, 21, 23]
    horarios = [False, False, False, False]
    for horario in range(3):
        for hora in lista:
            if(time2f(hora) <= horamax[horario] and time2f(hora) >= horamin[horario]):
                horarios[horario] = True
    return [horarios[0] and horarios[1],horarios[1] and horarios[2],horarios[2] and horarios[3]]
    

if(len(sys.argv) != 3):
    print 'Uso correto: python presenca.py arq_entrada.csv arq_saida.csv'
    sys.exit(0)
in_fn = sys.argv[1]
out_fn = sys.argv[2]

nomes = set()
dias = set()
pres = dict()

print 'leitura'

with open(in_fn, "r") as fin:
    next(fin)#pula primeira linha
    for line in fin :
        fields = line.split(";")
        data,hora,evento,codigo,nome,matricula,portal,null = fields
        nomes.add(nome)
        dias.add(data)
        key = (data, nome)
        if(key in pres):
            pres[key].add(hora)
        else:
            pres[key] = set([hora])
    
print 'escrita'    
    
with open(out_fn, "w") as fout:
    fout.write('"nome","presencas","presencas extra"\n');
#header
    nomes_ord = sorted(list(nomes))
   
    for nome in nomes_ord:
        soma_extra = 0
        soma = 0
        for dia in dias:
            key = (dia, nome)
            presenca = [False,False,False]
            if(key in pres):
                presenca = calcPresenca(pres[key])
            soma = soma + sum(presenca[1:])
            soma_extra = soma_extra + sum(presenca[0:1])
        fout.write('"' + nome + '",' + str(soma) + ',' + str(soma_extra) + '\n')
        
        
            