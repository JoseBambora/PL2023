from functools import reduce

def fun(str):
    res = []
    add = ""
    for ch in str:
        if ch.isdigit() or ch == '.':
            add += ch
        else:
            if(len(add) > 0):
                res.append(add)
                add = ""
            if ch == '=':
                res.append('=')
    if(len(add) > 0):
        res.append(add)
    return res

def concat(l):
    return  [elem for lst in l for elem in lst]

def funaux(l):
    return list(filter(lambda str: str == '=',l[0])) + l[1:]

def funtakeon(l):
    return map(lambda str: funaux(str.split('on')),l)

def auxreduce(acc):
    print(acc)
    return acc

inputuser = input()
lowerin = inputuser.lower()
splitoff = lowerin.split('off')
splitoffon = splitoff[:1] + concat(funtakeon(splitoff[1:]))
splitoffon = concat(map(fun,splitoffon))
print(f'Partes a considerar: {splitoffon}')
res = reduce(lambda acc, str: auxreduce(acc) if str == '=' else acc + float(str), splitoffon, 0)
# for str in splitoffon:
#     if str == '=':
#         print(res)
#     else:
#         res += int(str)
print(res)