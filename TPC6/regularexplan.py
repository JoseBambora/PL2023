from ply.lex import lex
import re

tokens = (
    'COMML',
    'COM',
    'VAR',
    'FUN',
    'WHILE',
    'COND1',
    'OPE',
    'PROGRAM',
    'FOR',
    'COND2',
    'CALLFUN',
    'ARRAY',
    'IF',
    'END'
)

estados = ['INITIAL']
estadosnivel = 0

def t_IF(t):
    r'if'
    global estados,estadosnivel
    estados.append(f'IF #{estadosnivel}')
    estadosnivel += 1
    return t

def t_END(t):
    r'\}'
    global estados,estadosnivel
    s = estados.pop()
    estadosnivel-=1

def t_ARRAY(t):
    r'\w+\[\d+\]\s*=\s*\{\d+(,\d+)*\}'
    return t

def t_CALLFUN(t):
    r'\w+\([\w,\s\(\)]*\)' # Fazer melhor (chamadas de funções nos argumentos)
    return t

def t_COND2(t):
    r'\w+\s+in\s+\[\d+\.\.\d+\]'
    return t

def t_FOR(t):
    r'for\s+'
    global estados, estadosnivel
    estados.append(f'FOR #{estadosnivel}')
    estadosnivel+=1
    return t

def t_PROGRAM(t):
    r'program\s+\w+'
    global estados,estadosnivel
    estados.append('PROGRAM')
    estadosnivel+=1
    return t

def t_OPE(t):
    r'(int\s+)?\w+(\[(\d+|\w+)\])?\s*=\s*(\w+(\[(\d+|\w+)\])?|\d+)(\s*(\+|\*|\-|\/)\s*(\w+(\[(\d+|\w+)\])?|\d+))*'
    return t

def t_COND1(t):
    r'(\w+|\d+|\w+\[(\d+|\w+)\])\s*(<|>|==|<=|>=)\s*(\w+(\[(\d+|\w+)\])?|\d+)'
    return t

def t_WHILE(t):
    r'while'
    global estados, estadosnivel
    estados.append(f'WHILE #{estadosnivel}')
    estadosnivel+=1
    return t


def t_FUN(t):
    r'function\s+\w+\([\w,\s]*\)'
    global estados,estadosnivel
    estados.append('FUN')
    estadosnivel+=1
    return t

def t_VAR(t):
    r'int\s+\w+;'
    return t

def t_COMML(t):
    r'\/\*[\w\s\-\.\:\b]*\*\/'
    return t

def t_COM(t):
    r'\/\/[^\n]*'
    return t

def t_error(t):
    t.lexer.skip(1)


def t_ANY_newline(t):
    r'\n+'

p1 = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
    int res2 = res * n + 1;
    while res > 3 {
        res = res + 1
    }
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}'''


p2 = '''
/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}'''

lexer = lex()

l = []
lexer.input(p1 + p2)
t = lexer.token()
while t:
    l.append((t.type,t.value))
    print(f'Estado: {estados[-1]}, token: {t}')
    t = lexer.token()
# for tu in l:
#     print(tu)