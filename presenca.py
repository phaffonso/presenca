#!/usr/bin/python
# coding=utf-8

import sys
import csv
import os
import codecs
import re

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
    return [entrada == 0 and saida >= 0, entrada <= 1 and saida >= 1, entrada <= 2 and saida == 2]
    
def leArq(in_fn, nomes, dias, pres):
    with open(in_fn, "r") as fin:
        next(fin)#pula primeira linha
        for line in fin :
            fields = line.split(";")
            try:
                data,hora,evento,codigo,nome,matricula,portal,null = fields
            except ValueError as e:
                print "Erro na linha: "+line
                raise
            nomes.add(normalizaNome(nome))
            dias.add(data)
            key = (data, normalizaNome(nome))
            if(key in pres):
                pres[key].add(hora)
            else:
                pres[key] = set([hora])
    
class Aluno:
    def __init__(self, row):
        self.inscricao = row[0];
        self.nome = row[1].decode('utf-8').upper();
        self.sala = row[3];
        
        
def carregaAlunos(in_fn):
    alunos = [];
    with open(in_fn, "r") as csvfile:
        reader = csv.reader(csvfile);
        reader.next(); #descarta cabecalho
        for row in reader:
            alunos.append(Aluno(row));
    return alunos;

    
def converteArq(in_fn, out_fn):
    nomes = set()
    dias = set()
    pres = dict()
    leArq(in_fn, nomes, dias, pres);
    escreveArq(out_fn, nomes, dias, pres);


def escreveArq(out_fn, nomes, dias, pres, alunos):       
    with codecs.open(out_fn, "w", encoding='utf8') as fout:
        #encontrar perdidos - nomes não associados a alunos cadastrados
        perdidos = [];
        for nome in nomes:
            if(not nome in alunos):
                perdidos.append(nome);
                
        alunos_ord = sorted(list(alunos.values()), key=lambda a:(a.sala, a.nome))
        dias_ord = sorted(list(dias), key = lambda dia: dia.split('/')[::-1])  
        #escrever cabecalho
        fout.write('"insrcicao", "nome","sala"')
        for dia in dias_ord:
            fout.write(',"'+str(dia)+'"')
        fout.write(',"presencas normais","presencas extra"\n');
        
        for aluno in alunos_ord:
            soma_extra = 0
            soma = 0

            fout.write(aluno.inscricao+',"' + aluno.nome + '","'+aluno.sala+'"')

            for dia in dias_ord:
                key = (dia, normalizaNome(aluno.nome))
                presenca = [False,False,False]
                if(key in pres):
                    presenca = calcPresenca(pres[key])
                fout.write(','+str(sum(presenca)))
                soma = soma + sum(presenca[1:])
                soma_extra = soma_extra + sum(presenca[0:1])
            fout.write(',' + str(soma) + ',' + str(soma_extra) + '\n')
            
        #escrever totais
        if(len(perdidos) > 0):
            print "Alunos nao presentes na listagem:"
            for p in perdidos:
                print p
        #fout.write('"Totais/médias"')
        #fout.write('\n')

def normalizaNome(nome):
    return re.sub("[^a-zA-Z0-9 ]", "", nome)[:23].upper()
    


def main():
    alunos = carregaAlunos("alunos.csv");
    dic_alunos = {};
    for aluno in alunos:
        dic_alunos[normalizaNome(aluno.nome)] = aluno
    fn_in = next(os.walk('./in'))[2]
    nomes = set()
    dias = set()
    pres = dict()
    for fn in fn_in:
        leArq('in/'+fn, nomes, dias, pres)
    nomes = set([nome.decode('utf-8') for nome in nomes])
    for nome in [aluno.nome for aluno in alunos]:
        nomes.add(nome);
    nomes = set([normalizaNome(nome) for nome in nomes])
    escreveArq('relatorio_consolidado.csv', nomes, dias, pres, dic_alunos)
    print u"Relatório criado com sucesso"

if __name__ == "__main__":
    main()

        
        
            