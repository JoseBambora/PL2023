from ply.lex import lex
import sys
import re

# Expressões regulares uteis
expmoedas = r'(\d+[ce])'
regmoedas = re.compile(expmoedas)
expnum = r'(\d+)'
regnum = re.compile(expnum)

# Saldo do telefone
saldo = 0

# Moedas a introduzir e o respetivo valor em cêntimos
coins = {
    '1c' : 1,
    '2c' : 2,
    '5c' : 5,
    '10c' : 10,
    '20c' : 20,
    '50c' : 50,
    '1e' : 100,
    '2e' : 200
}

# Números a contactar e o respetivo valor (-1 é erro)
numeros = [
    (r'601\d+', -1),
    (r'641\d+', -1),
    (r'00\d+', 150),
    (r'2\d+', 25),
    (r'800\d+', 0),
    (r'808\d+', 10)
]

# Tokens, CHAMADA <=> T=(...) MOEDA<=> MOEDA (...)
tokens = [
    'POUSAR',
    'CHAMADA',
    'LEVANTAR',
    'MOEDA',
    'ABORTAR'
]

# 3 Grupos, o inicial, o de inserir as moedas e o de efetuar chamadas
states = (
    ('MOEDA', 'inclusive'),
    ('CHAMADA', 'inclusive')
)
# Automate: 
# 
# Qualquer carater que não seja compativel com o estado atual do programa, esse mesmo estado não é alterado.          
#
#    ____(LEVANTAR)_____  MOEDA
#   /                    /  |
# INICIAL ___(POUSAR)___    | MOEDA (...)
#   \                       |
#     ____(POUSAR)______  CHAMADA __T=(...)
#                                 \___|

t_ignore  = ' \t'

def t_ANY_ABORTAR(t):
    r'ABORTAR'
    print(calcula_troco())
    print('A desligar máquina')
    sys.exit()

def getSaldo(saldo):
    s = str(saldo)
    if(saldo > 100):
        s = s[:-2] + 'e' +  s[-2:] + 'c'
    else:
        s += 'c'
    p = f'saldo = {s}'
    return p

# 'Ativar' maquina
def t_INITIAL_LEVANTAR(t):
    r'LEVANTAR'
    print("Introduza moedas.")
    t.lexer.begin('MOEDA')

# Pousar sem ter introduzido moedas
def t_MOEDA_POUSAR(t):
    r'POUSAR'
    print('Volte sempre!')
    t.lexer.begin('INITIAL')

# Introdução de moedas
def t_MOEDA_MOEDA(t):
    r'MOEDA(\s*\d+[ce][,.])*'
    global saldo
    cs = t.value[6:]
    mi = regmoedas.findall(cs)
    p = ''
    for c in mi:
        if coins.__contains__(c):
            saldo += coins[c]
        else:
            p += f'{c} moeda inválida; '
    p+=getSaldo(saldo)
    print(p)
    t.lexer.begin('CHAMADA')
    return t

# Realizar chamada
def t_CHAMADA_CHAMADA(t):
    r'T\s*=\s*(\d+)'
    global saldo
    num = regnum.search(t.value).group(1)
    aux = list(filter(lambda e: re.match(e[0],num),numeros))
    if len(aux) == 1:
        reduz = aux[0][1]
        if reduz == -1:
            print('Esse número não é permitido neste telefone. Queira discar novo número!')
        elif saldo < reduz:
            print('Saldo insuficiente')
        else:
            saldo -= reduz
            print(getSaldo(saldo))
    else:
        print('Número desconhecido!')
    return t

def calcula_troco():
    global saldo
    troco = saldo
    m = '2e'
    i = 1
    contador = {}
    coinlist = list(coins.keys())
    coinlist.sort(key = lambda e: -coins[e])
    for c in coinlist:
        contador[c] = 0
    while troco != 0:
        valor = coins[m]
        if troco >= valor:
            troco -= valor
            contador[m] += 1
        else:
            m = coinlist[i]
            i+=1
    p = 'troco='
    coinlist = filter(lambda k: contador[k] > 0,coinlist)
    for k in coinlist:
        p+= ' ' + str(contador[k]) + 'x' + k + ','
    p = p[:-1]
    return p

# Pousar telefone
def t_CHAMADA_POUSAR(t):
    r'POUSAR'
    global saldo
    p = calcula_troco() + '; Volte sempre!'
    saldo = 0
    print(p)
    t.lexer.begin('INITIAL')
    return t

# Qualquer carater que não seja compativel com o estado atual do programa, esse mesmo estado não é alterado.          

def t_INITIAL_ANY(t):
    r'.+'
    print('Máquina Desligada')

def t_MOEDA_ANY(t):
    r'.+'
    print('Erro. Introduza Moedas.')

def t_CHAMADA_ANY(t):
    r'.+'
    print('Erro, introduza um número ou pouse o telefone')

def t_error(t):
    t.lexer.skip(1)

def t_ANY_newline(t):
    r'\n+'
    return t

lexer = lex()

for s in sys.stdin:
    lexer.input(s)
    t = lexer.token()
    while(t):
        t = lexer.token()
        