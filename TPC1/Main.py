from Data import Data
import matplotlib.pyplot as plt

def graphic(dist,xstr,ystr,title,tuple):
    plt.figure(figsize=[18, 9.3])
    plt.subplots_adjust(top=0.95, bottom=0.05)
    x_coords = [str(key) for key in dist.keys()]
    if tuple:
     x_coords = [i for i in range(len( dist.keys()))]
    display = [t[0] for t in dist.values()]
    plt.barh(x_coords,display,color=['red','black'], height=1.0)
    if tuple:
        xtick_labels = [f"{i[0]}-{i[1]}" for i in dist.keys()]
        plt.yticks(x_coords, xtick_labels)
    plt.xlabel(xstr)
    plt.ylabel(ystr)
    plt.title(title)
    plt.show()

def print_dist(xstr,ystr,dist):
    x1 = len(xstr)
    x2 = len(ystr)
    x3 = len('Probabilidade')
    h = f'| {xstr} | {ystr} | Probabilidade |'
    l = len(h)
    sep = '+'
    sep += '-' * (l-2)
    sep += '+'
    print(sep)
    print(h)
    print(sep)
    for t in dist.items():
        s1 = str(t[0])
        s2 = str(t[1][0])
        s3 = str(round(t[1][1],3)*100)
        p1 = ' ' * (x1-len(s1))
        p2 = ' ' * (x2-len(s2))
        p3 = ' ' * (x3-len(s3)-1)
        print(f"| {s1} {p1}| {s2} {p2}| {s3}% {p3}|")
    print(sep)

def show_dist(dist,xstr,ystr,title,tuple):
    print('Qual a opção?')
    print('1 - Gráfico')
    print('2 - Formato Textual')
    op = input()
    option = 0
    while option != 1 and option != 2:
        if op.isdigit():
            option = int(op)
            if option > 0 and option < 3:
                if option == 1: graphic(dist,xstr,ystr,title,tuple)
                else: print_dist(xstr,ystr,dist)
            else:
                print('Opção Inválida')
        else:
            print('Input Inválido')


def distr_sex(dados):
    res = dados.distr_sex()
    show_dist(res,"Sexo","Valor","Distribuição por sexo",False)

def distr_sesceta(dados):
    res = dados.distr_esceta()
    show_dist(res,"Escalões etários","Valor","Distribuição por escalões etários",True)

def distr_collev(dados):
    res = dados.distr_collev()
    show_dist(res,"Níveis de colestrol","Valor","Distribuição por níveis de colestrol",True)


dados = Data()
filename = 'myheart.csv'
print('Ler do ficheiro csv: ' + filename)
dados.readFile(filename)
print('Dados lidos')
option = 0
while option != 5:
    print('Qual a opção?')
    print('1 - Tabela dados')
    print('2 - Distribuição por sexo')
    print('3 - Distribuição por escalões etários')
    print('4 - Distribuição por níveis de colestrol')
    print('5 - Sair')
    op = input()
    if op.isdigit():
        option = int(op)
        if option > 0 and option < 6:
            if option == 1: print(dados)
            elif option == 2 : distr_sex(dados)
            elif option == 3 : distr_sesceta(dados)
            elif option == 4 : distr_collev(dados)
        else:
            print('Opção Inválida')
    else:
        print('Input Inválido')