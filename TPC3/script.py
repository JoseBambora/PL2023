import re
import json

data = []

def load_data(data):
    print('A carregar dados ...')
    file = open('processos.txt','r')
    lines = file.readlines()
    file.close()
    exp = r"(\d+)::(\d{4,4}-\d{2,2}-\d{2,2})::([A-Za-z\b\s]*)::([A-Za-z\b\s]*)::([A-Za-z\b\s]*)::([^::]*)::"
    regexp = re.compile(exp)
    for linha in lines:
        resultreg = regexp.match(linha)
        if resultreg:
            pasta = int(resultreg.group(1))
            date = resultreg.group(2)
            nome = resultreg.group(3)
            pai = resultreg.group(4)
            mae = resultreg.group(5)
            obs = resultreg.group(6)
            add = {
                'pasta':pasta,
                'data':date,
                'nome':nome,
                'pai':pai,
                'mae':mae,
                'obs':obs
            }
            data.append(add)
    print('Dados carregados')

def alinea_a(dados):
    expdata = r'(\d{4,4})-(\d{2,2})-(\d{2,2})'
    regdata = re.compile(expdata)
    res = {}
    for d in dados:
        data = d['data']
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
        nomes = [ d['nome'], d['pai'], d['mae'] ]
        data = d['data']
        resmatchdata = regdata.match(data)
        ano = resmatchdata.group(1)
        seculo = int(int(ano) / 100) + 1
        if not res.__contains__(seculo):
            res[seculo] = {'NP' : {}, 'NA' : {}}
        for nome in nomes:
            resmatch = regnomes.match(nome)
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
    exp = r'[A-Za-z\s]*,([A-Za-z\s]*)\.[\s]*Proc\.[\d]+\.'
    reexp = re.compile(exp)
    for d in dados:
        obs = d['obs']
        resexp = reexp.findall(obs)
        for g in resexp:
            if not res.__contains__(g):
                res[g] = 0
            res[g]+=1
    resl = []
    for grau in res.keys():
        resl.append((grau,res[grau]))
    resl.sort(key=lambda t: t[1],reverse=True)
    for grau in resl:
        print(f'Grau: {grau[0]}, frequência: {grau[1]}')
    

def alinea_d(dados, nomeficheiro):
    print(f'A guardar no ficheiro {nomeficheiro}')
    res = dados[:20]
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
