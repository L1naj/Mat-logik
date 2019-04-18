import re

def skobki(f):
    a=[]
    for i in f:
        if i == "(" or i == ")":
            a.append(i)
    nymer_skob = []
    k = 0
    for i in range (len(a)):
        if a[i] == ")":
            for k in range (i):
                if a[k] == "(":
                    m = k
            nymer_skob.append((m,i))
            a[i] = " "
            a[m] = " "
    return nymer_skob

def format_per(f):
    shab = r'\w+'
    per = re.findall(shab,f)
    for i in per:
        f = f.replace(i,"(x["+i[1:]+"])")
    return f

def replac(f):
    f = format_per(f)
    f = f.replace("$","1+") 
    while "@" in f:
        n = -1
        for i in f.split("@")[0]:
            if i == "(" or i == ")":
                n += 1
        nymer_skob = skobki(f)
        for e in nymer_skob:
            if n in e:
                skobka_ot = e[0]-1
            if n+1 in e:
                skobka_za = e[1]
        nom0 = -1
        slice_ot = 0
        slice_za = 0
        for i in f:
            if nom0 < skobka_za:
                if nom0 < skobka_ot:
                    if i == "(" or i == ")":
                        nom0 += 1
                    slice_ot += 1
                    slice_za += 1
                else:
                    if i == "(" or i == ")":
                        nom0 += 1
                    slice_za += 1
        body = f[slice_ot:slice_za]
        shet = 0
        for kol in range (len(body)):  
            if body[kol] == "@" and shet == 0:  
                body = body[:kol]+"*(1+"+body[(kol+1):]
                shet = 1
        body = "1+("+body+"))"
        f = f[:slice_ot]+body+f[slice_za:]
    return f

def calc(f,x):
    return eval(f)%2

def kolvo_per(f):
    shab = r'\d+'
    ult = re.findall(shab,f)
    ult = map(int,ult)
    arn = max(list(ult))
    return arn

def glavnaya(f):
    arn = kolvo_per(f)+1
    f = replac(f)
    for i in range(2**(arn)):
        x = [0]*(arn)
        v = str(bin(i))[2:]
        for k in range (len(v)):
            x[k]=int(v[len(v)-k-1])  
        if calc(f,x) == 0:
            print("Принимает 0 на векторе "+str(x))
            return False
    return True


while True:
    logik = input("Введите выражение(@ - импликация, $ - заперечення,\nпеременную под номером n обозначать xn, все брать в скобки): ")

    if glavnaya(logik):
        print("Тавтология")
    else:
        print("Не тавтология")
    









