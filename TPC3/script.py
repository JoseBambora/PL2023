import re
import json

data = []

def load_data(data):
    print('A carregar dados ...')
    file = open('processos.txt','r')
    lines = file.readlines()
    file.close()
    exp1 = r"(\d+)::(\d{4,4}-\d{2,2}-\d{2,2})::"
    exp2 = r"([A-Za-z][A-Za-z\b\s]{5,})(,[A-Za-z][A-Za-z\b\s]{5,}\. )?(Proc.[\d]+)?[:|.]"
    regexp1 = re.compile(exp1)
    regexp2 = re.compile(exp2)
    ids = set()
    for linha in lines:
        num_data = regexp1.search(linha)
        nomes = regexp2.findall(linha)
        nomes = list(map(lambda tup: (tup[0],tup[1][1:-2],tup[2]),nomes))
        if num_data and len(nomes) > 0:
            num = int(num_data.group(1))
            if not num in ids:
                date = num_data.group(2)
                ids.add(num)
                data.append((num,date,nomes))
    print('Dados carregados')

def alinea_a(dados):
    expdata = r'(\d{4,4})-(\d{2,2})-(\d{2,2})'
    regdata = re.compile(expdata)
    res = {}
    for d in dados:
        data = d[1]
        resmatch = regdata.match(data)
        ano = resmatch.group(1)
        if not res.__contains__(ano):
            res[ano] = 0
        res[ano] += 1
    resb = []
    for ano in res.keys():
        resb.append((ano,res[ano]))
    resb.sort(key=lambda t: t[0])
    for ano in resb:
        print(f'Ano: {ano[0]}, frequência {ano[1]}')

def aux_alinea_b(nomes,str):
    nres = []
    for n in nomes.keys():
        nres.append((n,nomes[n]))
    nres.sort(key = lambda t: t[1],reverse=True)
    ntop5 = nres[0:5]
    print(f'\t{str}:')
    for n in ntop5:
        print(f'\t\t{n[0]}:{n[1]}')

def alinea_b(dados):
    expdata = r'(\d{4,4})-(\d{2,2})-(\d{2,2})'
    regdata = re.compile(expdata)
    expnomes = r'([A-Za-z]+) .* ([A-Za-z]+)'
    regnomes = re.compile(expnomes)
    res = {}
    for d in dados:
        nomes = d[2]
        data = d[1]
        resmatchdata = regdata.match(data)
        ano = resmatchdata.group(1)
        seculo = int(int(ano) / 100) + 1
        if not res.__contains__(seculo):
            res[seculo] = {'NP' : {}, 'NA' : {}}
        for nome in nomes:
            resmatch = regnomes.match(nome[0])
            if resmatch:
                np = resmatch.group(1)
                na = resmatch.group(2)
                nps = res[seculo]['NP']
                nas = res[seculo]['NA']
                if not nps.__contains__(np):
                    nps[np] = 0
                if not nas.__contains__(na):
                    nas[na] = 0
                nps[np] += 1
                nas[na] += 1
    resl = []
    for seculo in res.keys():
        resl.append((seculo,res[seculo]))
    resl.sort(key=lambda t: t[0],reverse=True)
    for seculo in resl:
        print(f'Século {seculo[0]}')
        aux_alinea_b(seculo[1]['NP'],'Nomes próprios')
        aux_alinea_b(seculo[1]['NA'],'Apelidos')

def alinea_c(dados):
    res = {}
    for d in dados:
        nomes = d[2]
        for nome in nomes:
            p = nome[1]
            if len(p) > 0:
                if not res.__contains__(p):
                    res[p] = 0
                res[p] += 1
    resl = []
    for grau in res.keys():
        resl.append((grau,res[grau]))
    resl.sort(key=lambda t: t[1],reverse=True)
    for grau in resl:
        print(f'Grau: {grau[0]}, frequência: {grau[1]}')
    

def alinea_d(dados, nomeficheiro):
    print(f'A guardar no ficheiro {nomeficheiro}')
    p20 = dados[:20]
    res = []
    for t in p20:
        l = []
        conversion = {
            'id' : t[0],
            'data' : t[1],
            'nomes' : l
        }
        for n in t[2]:
            l.append({
                'nome': n[0],
                'grau parentesco' : n[1],
                'processo' : n[2]
            })
        res.append(conversion)
    file = open(nomeficheiro,'w')
    json.dump(res,file,indent=4)
    file.close()
    print('Save completo')

load_data(data)
b = True
while b:
    print('Qual a alinea? (a-d)')
    print('e - sair')
    str = input()
    if str == 'a':
        alinea_a(data)
    elif str == 'b':
        alinea_b(data)
    elif str == 'c':
        alinea_c(data)
    elif str == 'd':
        alinea_d(data,'data.json')
    elif str == 'e':
        b = False
