class Entry:
    def __init__(self,idade,sexo,tensao,colesterol,batimento,temDoenca):
        self.age = idade
        self.sex = sexo
        self.tension = tensao
        self.cholesterol = colesterol
        self.pulse = batimento
        self.hasDisease = temDoenca

    def __str__(self):
        auxage = str(self.age)
        auxtension = str(self.tension)
        auxchol = str(self.cholesterol)
        auxpul = str(self.pulse)
        auxdesi = str(self.hasDisease)
        sep = ' | '
        res = auxage
        res += ' ' * (5-len(auxage))
        res += sep
        res += ' ' + self.sex + '  '
        res += sep
        res += auxtension
        res += ' ' * (6-len(auxtension))
        res += sep
        res += auxchol
        res += ' ' * (10-len(auxchol))
        res += sep
        res += auxpul
        res += ' ' * (9-len(auxpul))
        res += sep
        res += auxdesi
        res += ' ' * (9-len(auxdesi))
        res += sep
        return res