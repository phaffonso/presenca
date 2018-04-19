#!/usr/bin/python

import sys
import csv
import os

def time2f(time):
    h,m,s = time.split(':')
    return int(h) + int(m)/60.0
    
def calcPresenca(lista):
    horaminsaida = [18.6, 20.25, 22]
    horamaxentrada = [18.25, 19.35, 21]
    horarios = [False, False, False, False]
    entrada = 3
    saida = -1
    for horario in range(3):
        for hora in lista:
            if(time2f(hora) <= horamaxentrada[horario]):
                entrada = min(horario, entrada)
    for horario in range(3):
        for hora in lista:
            if(time2f(hora) <= horaminsaida[horario]):
                saida = max(horario, saida)
    print (entrada, saida)
    return [entrada == 0 and saida >= 0, entrada <= 1 and saida >= 1, entrada <= 2 and saida == 2]

def converteArq(in_fn, out_fn):

    nomes = set()
    dias = set()
    pres = dict()

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
            
# if(len(sys.argv) != 3):
    # print 'Uso correto: python presenca.py arq_entrada.csv arq_saida.csv'
    # sys.exit(0)
# in_fn = sys.argv[1]
# out_fn = sys.argv[2]            

def main():
    fn_in = next(os.walk('./in'))[2]
    for fn in fn_in:
        converteArq('in/'+fn, 'out/'+fn)
        

if __name__ == "__main__":
    main()

        
        
            