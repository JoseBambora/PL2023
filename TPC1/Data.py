from Entry import Entry

class Data:
    def __init__(self):
        self.header = []
        self.data = []
        self.maxs = {}
        self.mins = {}
    def add(self, entry):
        self.patients.__add__(entry)
    def readFile(self, filename):
        file = open(filename,"r")
        line = file.readline()
        self.header = line.replace('\n','').split(',')
        while line:
            line = file.readline()
            if(len(line) > 0):
                content = line.replace('\n','').split(',')
                age = int(content[0])
                sex = content[1]
                ten = int(content[2])
                col = int(content[3])
                pul = int(content[4])
                hde = int(content[5])
                self.data.append(Entry(age,sex,ten,col,pul,hde))
        self.maxs['age'] = max(self.data,key=lambda e: e.age).age
        self.mins['age'] = min(self.data,key=lambda e: e.age).age
        self.maxs['col'] =  max(self.data,key=lambda e: e.cholesterol).cholesterol
        self.mins['col'] =  min(self.data,key=lambda e: e.cholesterol).cholesterol

    def distr_sex(self):
        res = {
            'M': 0,
            'F': 0
        }
        for entry in self.data:
            res[entry.sex]+=1
        return res

    def distr_esceta(self):
        m = self.maxs['age']
        i = self.mins['age']
        aux = {}
        res = {}
        while i < m:
            t = (i,i+4)
            res[t] = 0
            for k in range(0,5):
                aux[i+k] = t
            i +=5
        for entry in self.data:
            t = aux[entry.age]
            res[t] +=1
        return res

    def distr_collev(self):
        m = self.maxs['col']
        i = self.mins['col']
        aux = {}
        res = {}
        while i < m:
            t = (i,i+9)
            res[t] = 0
            for k in range(0,10):
                aux[i+k] = t
            i +=10
        for entry in self.data:
            t = aux[entry.cholesterol]
            res[t] +=1
        return res

    def __str__(self):
        res = '| index | '
        sep = ' | '
        for h in self.header:
            res += h
            res += sep
        l = len(res)-3
        res += '\n'
        auxres = '+' + ('-' * l) + '+'
        res = auxres + '\n' + res
        res += auxres
        res += '\n'
        index = 1
        for entry in self.data:
            auxindex = str(index)
            res += '| '
            res += auxindex
            res += ' ' * (5-len(auxindex))
            res += sep
            res += str(entry)
            res += '\n'
            index += 1
        return res + auxres

    def apresenta_tabela(self):
        return str




