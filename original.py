import re

class Lister:
    
    def __init__(self,path):
        self.path = path
        
    def write(self,F,text):
        with open(self.path,'a') as f:
            f.write(F+" "+text+"\n")

lister = Lister("./out.txt")

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
    f = f.replace("&","*") 
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
    while "|" in f:
        n = -1
        for i in f.split("|")[0]:
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
            if body[kol] == "|" and shet == 0:
                body = body[:kol]+"+1)*(1+"+body[(kol+1):]
                shet = 1
        body = "1+(("+body+"))"
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
    lister.write(C, "Modus ponens for "+A+" and "+B)
    return C

def acs_A1(F,G):
    Res = "("+F+"@"+"("+G+"@"+F+"))"
    lister.write(Res,"A1 for "+F+" and "+G)
    return Res

def acs_A2(F,G,H):
    Res = "(("+F+"@"+"("+G+"@"+H+"))"+"@(("+F+"@"+G+")@("+F+"@"+H+")))"
    lister.write(Res,"A2 for "+F+" and "+G+" and "+H)
    return Res

def acs_A3(A,B):
    Res = "("+A+"@("+A+"|"+B+"))"
    lister.write(Res,"A3 for "+A+" and "+B)
    return Res

def acs_A4(A,B):
    Res = "("+B+"@("+A+"|"+B+"))"
    lister.write(Res,"A4 for "+A+" and "+B)
    return Res

def acs_A5(A,B,C):
    Res = "(("+A+"@"+C+")@(("+B+"@"+C+")@(("+A+"|"+B+")@"+C+")))"
    lister.write(Res,"A5 for "+A+" and "+B+" and "+C)
    return Res

def acs_A6(A,B):
    Res = "(("+A+"&"+B+")@"+A+")"
    lister.write(Res,"A6 for "+A+" and "+B)
    return Res

def acs_A7(A,B):
    Res = "(("+A+"&"+B+")@"+B+")"
    lister.write(Res,"A7 for "+A+" and "+B)
    return Res

def acs_A8(A,B,C):
    Res = "(("+A+"@"+B+")@(("+A+"@"+C+")@("+A+"@"+"("+B+"&"+C+"))))"
    lister.write(Res,"A8 for "+A+" and "+B+" and "+C)
    return Res

def acs_A9(A,B):
    Res = "(("+A+"@"+B+")@(("+A+"@($"+B+"))@($"+A+")))"
    lister.write(Res,"A9 for "+A+" and "+B)
    return Res

def acs_A10(A):
    Res = "(($($"+A+"))@"+A+")"
    lister.write(Res,"A10 for "+A)
    return Res

def teor_L(F):
    F1 = acs_A2(F,"("+F+"@"+F+")",F)
    F2 = acs_A1(F,"("+F+"@"+F+")")
    F3 = MP(F2, F1)
    F4 = acs_A1(F,F)
    F5 = MP(F4,F3)
    return F5

def teor_deduc(Gamma,F,G,Vivod):
    _Vivod = []
    for i in range (len(Vivod)):
        if i == 0:
            if Vivod[i] == F:
                D = teor_L(F)
                _Vivod.append(D)
            else:
                F11 = acs_A1(Vivod[i],F)
                D = MP(Vivod[i],F11)
                _Vivod.append(F11)
                _Vivod.append(D)
        else:
            Param = True
            for p in range (i):
                for q in range (i):
                    if Vivod[i] == MP(Vivod[p],Vivod[q]):
                        F12 = acs_A2(F,Vivod[p],Vivod[i])
                        F22 = MP("("+F+"@"+Vivod[q]+")",F12)
                        D = MP("("+F+"@"+Vivod[p]+")",F22)
                        _Vivod.append(F12)
                        _Vivod.append(F22)
                        _Vivod.append(D)
                        Param = False
            if Param:
                if Vivod[i] == F:
                    D = teor_L(F)
                    _Vivod.append(D)
                else:
                    F11 = acs_A1(Vivod[i],F)
                    D = MP(Vivod[i],F11)
                    _Vivod.append(F11)
                    _Vivod.append(D)
    return [Gamma,D,_Vivod]

def alpha_sp(arn):
    alphasp = []
    for j in range (2**(arn)):
        alpha = [0]*arn
        v = str(bin(j))[2:]
        for i in range (len(v)):
            alpha[i] = int(v[len(v)-i-1])
        alpha = list(reversed(alpha))
        alphasp.append(alpha)
    return alphasp

def f_alpha(f, a):
    if calc(f,a) == 1:
        return f
    return "($"+f+")"

def teor_T2(A):
    F1 = A
    F2 = acs_A1(A,"($"+A+")")
    F3 = MP(F1,F2)
    F4 = teor_L("($"+A+")")
    F5 = acs_A9("($"+A+")",A)
    F6 = MP(F3,F5)
    F7 = MP(F4,F6)
    F8 = teor_deduc([],A,F7,[F1,F2,F3,F4,F5,F6,F7])
    return [[],F8[1]]

def shtuka(F,G):
    F1 = F
    F2 = "($"+F+")"
    F3 = acs_A1(F1,"($"+G+")")
    F4 = acs_A1(F2,"($"+G+")")
    F5 = MP(F1,F3)
    F6 = MP(F2,F4)
    F7 = acs_A9("($"+G+")",F1)
    F8 = MP(F5,F7)
    F9 = MP(F6,F8)
    F10 = acs_A10(G)
    F11 = MP(F9,F10)
    F12 = teor_deduc(["($"+G+")","($"+F+")"],F,G,[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11])
    return [F12[0],F12[1]]

def shtuka2(F,G):
    F1 = F
    F2 = "($"+F+")"
    F3 = acs_A1(F1,"($"+G+")")
    F4 = acs_A1(F2,"($"+G+")")
    F5 = MP(F1,F3)
    F6 = MP(F2,F4)
    F7 = acs_A9("($"+G+")",F1)
    F8 = MP(F5,F7)
    F9 = MP(F6,F8)
    F10 = acs_A10(G)
    F11 = MP(F9,F10)
    T = teor_deduc([F2],F1,F11,[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11])
    F12 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F13 = teor_deduc([],Gamma,F12,Vivod)[1]
    return [[],F13]

def vprava_2(A,B):
    F1 = acs_A9("("+A+"|"+B+")",A)
    F2 = shtuka(B,A)[1]
    F3 = acs_A5(A,B,A)
    F4 = teor_L(A)
    F5 = MP(F4,F3)
    F6 = MP(F2,F5)
    F7 = MP(F6,F1)
    F8 = acs_A1("($"+A+")","("+A+"|"+B+")")
    F9 = "($"+A+")"
    F10 = MP(F9,F8)
    F11 = MP(F10,F7)
    T = teor_deduc(["($"+A+")"],"($"+B+")",F11,[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11])
    F12 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F13 = teor_deduc([],Gamma,F12,Vivod)[1]
    return [[],F13]

def priklad_2(A,B):
    F1 = acs_A1("($"+B+")",A)
    F2 = "($"+B+")"
    F3 = MP(F2,F1)
    F4 = acs_A9(A,B)
    F5 = "("+A+"@"+B+")"
    F6 = MP(F5,F4)
    F7 = MP(F3,F6)
    T = teor_deduc([F5],F2,"($"+A+")",[F1,F2,F3,F4,F5,F6,F7])
    F8 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6,F7]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F9 = teor_deduc([],Gamma,F8,Vivod)[1]
    return [[],F9]

def vprava_3(A,B):
    F1 = "("+A+"@"+B+")"
    F2 = "(($"+A+")@"+B+")"
    F3 = acs_A9("($"+B+")","($"+A+")")
    F4 = priklad_2(A,B)[1]
    F5 = MP(F1,F4)
    F6 = MP(F5,F3)
    F7 = priklad_2("($"+A+")",B)[1]
    F8 = MP(F2,F7)
    F9 = MP(F8,F6)
    F10 = acs_A10(B)
    F11 = MP(F9,F10)
    T = teor_deduc([F1],F2,F11,[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11])
    F12 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F13 = teor_deduc([],Gamma,F12,Vivod)[1]
    return [[],F13]
    
def vprava_4(A,B):
    F1 = acs_A8(A,A,B)
    F2 = teor_L(A)
    F3 = MP(F2,F1)
    F4 = acs_A1(B,A)
    F5 = A
    F6 = B
    F7 = MP(F6,F4)
    F8 = MP(F7,F3)
    F9 = MP(F5,F8)
    T = teor_deduc([F5],F6,F9,[F1,F2,F3,F4,F5,F6,F7,F8,F9])
    F10 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6,F7,F8,F9]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F11 = teor_deduc([],Gamma,F10,Vivod)[1]
    return [[],F11]

def priklad_k_kal(A,B):
    F1 = A
    F2 = "("+A+"@"+B+")"
    F3 = acs_A1("("+A+"@"+B+")",A)
    F4 = MP(F2,F3)
    F5 = MP(F1,F4)
    F6 = MP(F1,F5)
    T = teor_deduc([F1],F2,F6,[F1,F2,F3,F4,F5,F6])
    F7 = T[1]
    Vivod = [F1,F2,F3,F4,F5,F6]
    Vivod.extend(T[2])
    Gamma = T[0][0]
    F8 = teor_deduc([],Gamma,F7,Vivod)[1]
    return [[],F8]

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
        if F[posit+2] == "@":
            return [[G,H],1]
        elif F[posit+2] == "&":
            return [[G,H],3]
        elif F[posit+2] == "|":
            return [[G,H],4]


def lema_Kal(F, alpha):
    out = []
    if razbit(F)[1] == 2:
        out.extend([f_alpha(F,alpha)])
    else:
        if razbit(F)[1] == 0:
            if calc(replac(F),alpha) == 1:
                out.extend(lema_Kal(razbit(F)[0][0],alpha))
            else:
                out.extend(lema_Kal(razbit(F)[0][0],alpha))
                out.append(teor_T2(out[len(out)-1])[1])
        elif razbit(F)[1] == 1:
            A = razbit(F)[0]
            if calc(replac(A[0]),alpha) == 0:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                F2 = shtuka2(A[0],A[1])[1]
                F3 = MP(F1,F2)
                out.append(F2)
                out.append(F3)
            elif calc(replac(A[1]),alpha) == 1:
                out.extend(lema_Kal(A[1],alpha))
                F1 = out[len(out)-1]
                F2 = acs_A1(F1,A[0])
                out.append(F2)
                F3 = MP(F1,F2)
                out.append(F3)
            else:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                out.extend(lema_Kal(A[1],alpha))
                F2 = out[len(out)-1]
                F3 = priklad_k_kal(A[0],A[1])[1]
                F4 = MP(F1,F3)
                F5 = priklad_2("("+A[0]+"@"+A[1]+")",A[1])[1]
                F6 = MP(F4,F5)
                F7 = MP(F2,F6)
                out.extend([F3,F4,F5,F6,F7])

        elif razbit(F)[1] == 3:
            A = razbit(F)[0]
            if calc(replac(A[0]),alpha) == 1 and calc(replac(A[1]),alpha) == 1:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                out.extend(lema_Kal(A[1],alpha))
                F2 = out[len(out)-1]
                F3 = vprava_4(F1,F2)[1]
                F4 = MP(F1,F3)
                F5 = MP(F2,F4)
                out.extend([F3,F4,F5])
            if calc(replac(A[0]),alpha) == 0:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                F2 = acs_A6(A[0],A[1])
                F3 = priklad_2("("+A[0]+"&"+A[1]+")",A[0])[1]
                F4 = MP(F2,F3)
                F5 = MP(F1,F4)
                out.extend([F2,F3,F4,F5])
            if calc(replac(A[1]),alpha) == 0:
                out.extend(lema_Kal(A[1],alpha))
                F1 = out[len(out)-1]
                F2 = acs_A7(A[0],A[1])
                F3 = priklad_2("("+A[0]+"&"+A[1]+")",A[1])[1]
                F4 = MP(F2,F3)
                F5 = MP(F1,F4)
                out.extend([F2,F3,F4,F5])
        elif razbit(F)[1] == 4:
            A = razbit(F)[0]
            if calc(replac(A[0]),alpha) == 0 and calc(replac(A[1]),alpha) == 0:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                out.extend(lema_Kal(A[1],alpha))
                F2 = out[len(out)-1]
                F3 = vprava_2(A[0],A[1])[1]
                F4 = MP(F1,F3)
                F5 = MP(F2,F4)
                out.extend([F3,F4,F5])
            if calc(replac(A[0]),alpha) == 1:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                F2 = acs_A3(A[0],A[1])
                F3 = MP(F1,F2)
                out.extend([F2,F3])
            if calc(replac(A[1]),alpha) == 1:
                out.extend(lema_Kal(A[1],alpha))
                F1 = out[len(out)-1]
                F2 = acs_A4(A[0],A[1])
                F3 = MP(F1,F2)
                out.extend([F2,F3]) 
    return out
            
def adekvat(F):
    if not glavnaya(F):
        return False
    arn = kolvo_per(F)
    out = [0]*arn
    alphasp = alpha_sp(arn+1)
    for i in range (arn):
        out[i] = lema_Kal(F,alphasp[i])
    while arn != -1:
        alphasp = alpha_sp(arn+1)
        for i in range (arn):
            alphasp[i][len(alphasp[i])-1] = 1
            Gamma = []
            for j in range (arn-1):
                Gamma.append(f_alpha("(x["+str(j)+"])",alphasp[i]))
            vrem = teor_deduc(Gamma,f_alpha("(x["+str(arn)+"])",alphasp[i]),F,out[i])
            F1 = vrem[1]
            vivod_F1 = vrem[2]
            alphasp[i][len(alphasp[i])-1] = 0
            vrem = teor_deduc(Gamma,f_alpha("(x["+str(arn)+"])",alphasp[i]),F,out[i])
            F2 = vrem[1]
            vivod_F2 = vrem[2]
            F3 = vprava_3("(x["+str(arn)+"])",F)[1]
            F4 = MP(F1,F3)
            F5 = MP(F2,F4)
            res = vivod_F1
            res.extend(vivod_F2)
            res.append(F4)
            res.append(F5)
            out[i] = res
        arn -= 1
    return res








while True:
    logik = input("Введите выражение(@ - импликация, $ - заперечення,\nпеременную под номером n обозначать xn, все брать в скобки): ")
    #logik = format_per(logik)
    print(adekvat(logik))
    '''if glavnaya(logik):
        print("Тавтология")
    else:
        print("Не тавтология")'''
