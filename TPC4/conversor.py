import re
import json

# Processa o cabeçalho do csv. O resultado já determina se há lista / funções e etc
# Número,Nome,Curso = [['Número'], ['Nome'], ['Curso']]
# Número,Nome,Curso,Notas{3,5},,,,, = [['Número'], ['Nome'], ['Curso'], ['Notas', ['3', '5']]]
# Número,Nome,Curso,Notas{3,5}::max,,,,, = [['Número'], ['Nome'], ['Curso'], ['Notas', ['3', '5'], 'max']]
# Número,Nome,Curso,Notas{2,6}::sum,,,,,, = [['Número'], ['Nome'], ['Curso'], ['Notas', ['2', '6'], 'sum']]
def processa_header(header):
    res = []
    exp = r"(\w+)({\d+,?\d*})?(::\w+)?"
    regex = re.compile(exp)
    componentes = regex.findall(header)
    for tuple in componentes:
        t1 = tuple[0]
        t2 = tuple[1][1:][:-1].split(',')
        t3 = tuple[2][2:]
        if(t2[0] == '' and len(t3) == 0):
            t2 = []
        l = [t1,t2,t3]
        l = list(filter(lambda str: len(str) > 0,l))
        res.append(l)
    return res

# Processa partes de {número,número} ou {número}
def process_max_min(hcom,componentes,k):
    add = []
    minvalue = 1
    maxvalue = 1
    lim = hcom[1]
    llim = len(lim)
    if(llim > 0):
        minvalue = int(lim[0])
    if(llim > 1):
        maxvalue = int(lim[1])
    w = 0
    lc = len(componentes)
    while k < lc and (w < minvalue or (w >= minvalue and w < maxvalue)):
        add.append(componentes[k])
        k += 1
        w += 1
    add = filter(lambda s: len(s) > 0, add)
    add = list(map(lambda s: int(s),add))
    return (k,add)

# Processa funções
def processa_func(add,hcom,aux):
    fun = hcom[2]
    str = f'{hcom[0]}_{fun}'
    addres = 0
    if(fun == 'sum'):
        addres = sum(add)
    elif(fun == 'media'):
        addres = sum(add) / len(add)
    elif(fun == 'min'):
        addres = min(add)
    elif(fun == 'max'):
        addres = max(add)
    aux[str] = addres

# Processa um elemento de uma linha, com base no cabeçalho
def processa_elem(aux,hcom,componentes,k):
    if len(hcom) == 1:
        aux[hcom[0]] = componentes[k]
        k += 1
    else:
        k, add = process_max_min(hcom,componentes,k)
        if len(hcom) == 3:
            processa_func(add,hcom,aux)
        else:
            aux[hcom[0]] = add
    return k

# Processa uma linha
def processa_line(line,header):
    aux = {}
    lh = len(header)
    exp = r","
    reg = re.compile(exp)
    componentes = reg.split(line)
    if(len(componentes[-1]) < 1):
        componentes = componentes[:-1]
    elif(componentes[-1][-1] == '\n'):
        componentes[-1] = componentes[-1][:-1]
    k = 0
    for j in range(0,lh):
        hcom = header[j]
        k = processa_elem(aux,hcom,componentes,k)
    return aux

# Processa todas as linhas
def processa_lines(header,lines):
    res = []
    ll = len(lines)
    for i in range(1,ll):
        line = lines[i]
        aux = processa_line(line,header)
        res.append(aux)
    return res

# Função que escreve em .json. Não usei a json.dump por causa das listas.
def write_manually(file,res):
    string = '[\n'
    for e in res:
        string += '\t{\n'
        for elem in e.keys():
            string += f'\t\t"{elem}": '
            if isinstance(e[elem],str):
                string += f'"{e[elem]}",\n'
            else:
                string += f'{e[elem]},\n'
        string = string[:-2]
        string += '\n\t},\n'
    string = string[:-2]
    string += '\n]'
    file.write(string)

def save_info(file,res):
    file = open(file,mode="w",encoding="utf-8")
    write_manually(file,res)
    # json.dump(res,file,indent=4,ensure_ascii=False)
    file.close()

def load_info(file):
    file = open(file,mode="r",encoding="utf-8")
    lines = file.readlines()
    file.close()
    return lines

def processa_csv(file):
    lines = load_info("csv/" + file + '.csv')
    header = processa_header(lines[0])
    res = processa_lines(header,lines)
    save_info("json/" + file + '.json', res)

def testes():
    for i in range(1,8):
        processa_csv(f'alunos{i}')
testes()