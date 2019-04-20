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
    #f = format_per(f)
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

def MP(A,B):
    A = str(A)
    B = str(B)
    D = B[1:(len(A)+1)]
    if A != D:
        return False
    C = B[(len(A)+2):(len(B)-1)]
    return C

def acs_A1(F,G):
    return "("+F+"@"+"("+G+"@"+F+"))"

def acs_A2(F,G,H):
    return "(("+F+"@"+"("+G+"@"+H+"))"+"@(("+F+"@"+G+")@("+F+"@"+H+")))"

def acs_A3(F,G):
    return "((($"+G+")@($"+F+"))@((($"+G+")@"+F+")@"+G+"))"

def teor_L(F):
    F1 = acs_A2(F,"("+F+"@"+F+")",F)
    F2 = acs_A1(F,"("+F+"@"+F+")")
    F3 = MP(F2, F1)
    F4 = acs_A1(F,F)
    F5 = MP(F4,F3)
    return F5

def teor_deduc(Gamma,F,G,Vivod):
    if Vivod == True: return[Gamma,"("+F+"@"+G+")"]
    for i in range (len(Vivod)):
        if i == 0:
            if Vivod[i] == F:
                D = teor_L(F)
            else:
                F11 = acs_A1(Vivod[i],F)
                D = MP(Vivod[i],F11)
        else:
            Param = True
            for p in range (i):
                for q in range (i):
                    if Vivod[i] == MP(Vivod[p],Vivod[q]):
                        F12 = acs_A2(F,Vivod[p],Vivod[i])
                        D = MP("("+F+"@"+Vivod[q]+")",F12)
                        D = MP("("+F+"@"+Vivod[p]+")",D)
                        Param = False
            if Param:
                if Vivod[i] == F:
                    D = teor_L(F)
                else:
                    F11 = acs_A1(Vivod[i],F)
                    D = MP(Vivod[i],F11)
    return [Gamma,D]
        
def nasl_S1(F,G,H):
    Gamma = ["("+F+"@"+G+")","("+G+"@"+H+")"]
    Vivod = []
    for g in Gamma:
        Vivod.append(g)
    Vivod.append(F)
    Vivod.append(MP(Vivod[2],Vivod[0]))
    Vivod.append(MP(Vivod[3],Vivod[1]))
    return teor_deduc(Gamma,F,H,Vivod)

def nasl_S2(F,G,H):
    Gamma = ["("+F+"@("+G+"@"+H+"))",G]
    Vivod = []
    for g in Gamma:
        Vivod.append(g)
    Vivod.append(F)
    Vivod.append(MP(Vivod[2],Vivod[0]))
    Vivod.append(MP(Vivod[1],Vivod[3]))
    return teor_deduc(Gamma,F,H,Vivod)

def teor_T1(F):
    Vivod = []
    Vivod.append(acs_A3("($"+F+")",F))
    Vivod.append(teor_L("($"+F+")"))
    Vivod.append(nasl_S2("(($"+F+")@($($"+F+")))","(($"+F+")@($"+F+"))",F))
    Vivod.append(acs_A1("($($"+F+"))","($"+F+")"))
    Vivod.append(nasl_S1("($($"+F+"))","(($"+F+")@($($"+F+")))",F))
    return [[],Vivod[4][1]]

def teor_T2(F):
    return [[],"("+F+"@($($"+F+")))"]

def teor_T3(F,G):
    return [[],"(($"+F+")@("+F+"@"+G+"))"]

def teor_T6(F,G):
    return [[],"("+F+"@(($"+G+")@($("+F+"@"+G+"))))"]

def teor_T7(F,G):
    return [[],"(("+F+"@"+G+")@((($"+F+")@"+G+")@"+G+"))"]

def razbit(F):
    shab = r'\d+'
    per = re.findall(shab,F)
    if len(per) == 1 and F[1] != "$":
        return [[F],2]
    elif F[1] == "$":
        return [[F[2:(len(F)-1)]],0]
    else:
        nymer_skob = skobki(F)
        for elem in nymer_skob:
            if 1 in elem:
                nomer = elem[1]
        j = 0
        for i in range (len(F)):
            if F[i] == "(" or F[i] == ")":
                j+=1
            if j == nomer:
                posit = i
        G = F[1:posit+2]
        H = F[posit+3:(len(F)-1)]
        return [[G,H],1]    

def lema_Kal(F, alpha):
    shab = r'\d+'
    ult = re.findall(shab,F)
    ult = sorted(list(set(ult)))
    x=[]
    for i in range (len(ult)):
        if alpha[i] == 1:
            x.append("(x["+str(ult[i])+"])")
        if alpha[i] == 0:
            x.append("($(x["+str(ult[i])+"]))")
    razb = razbit(F)
    if razb[1] == 2:
        return [x,F,alpha]
    if razb[1] == 0:
        f = replac(F)
        if calc(f,alpha) == 1:
            return [x,F,alpha]
        else:
            G = lema_Kal(razb[0][0],alpha)[1]
            F1 = teor_T2(G)[1]
            F2 = MP(G,F1)
            return [x,F2[2:(len(F2)-1)],alpha]
    if razb[1] == 1:
        G = razb[0][0]
        H = razb[0][1]
        G = lema_Kal(G,alpha)[1]
        H = lema_Kal(H,alpha)[1]
        if calc(replac(G),alpha) == 0:
            F1 = teor_T3(G,H)[1]
            F2 = MP("($"+G+")",F1)
            return [x,F2,alpha]
        elif calc(replac(H),alpha) == 1:
            F1 = acs_A1(H,G)
            F2 = MP(H,F1)
            return [x,F2,alpha]
        else:
            F1 = teor_T6(G,H)[1]
            F2 = MP(G,F1)
            F3 = MP("($"+H+")",F2)
            return [x,F3[2:(len(F3)-1)],alpha]
            
def adekvat(F):
    if not glavnaya(F):
        return False
    arn = kolvo_per(F)+1
    for j in range (arn):
        Dlya_ind = []
        for i in range (2**(j+1)):
            alpha = [0]*arn
            v = str(bin(i))[2:]
            for k in range (len(v)):
                alpha[k]=int(v[len(v)-k-1])
            alpha = list(reversed(alpha))
            Kal = lema_Kal(F,alpha)
            Dlya_ind.append(teor_deduc(Kal[0][:(arn-j-1)],Kal[0][(arn-j-1)],F,True)[1])
        ded = list(set(Dlya_ind))
        ded = list(sorted(ded))
        F1 = teor_T7("(x["+str((arn-j-1))+"])",F)[1]
        F2 = MP(ded[1],F1)
        F3 = MP(ded[0],F2)
    return [[],F3]




while True:
    logik = input("Введите выражение(@ - импликация, $ - заперечення,\nпеременную под номером n обозначать xn, все брать в скобки): ")
    logik = format_per(logik)

    print(logik)
    if glavnaya(logik):
        print("Тавтология")
    else:
        print("Не тавтология")

    print(adekvat(logik))
