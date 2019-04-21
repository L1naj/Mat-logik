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

def acs_A3(F,G):
    Res = "((($"+G+")@($"+F+"))@((($"+G+")@"+F+")@"+G+"))"
    lister.write(Res,"A3 for "+F+" and "+G)
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
    Vivod.append(nasl_S2("(($"+F+")@($($"+F+")))",Vivod[1],F)[1])
    Vivod.append(acs_A1("($($"+F+"))","($"+F+")"))
    Vivod.append(nasl_S1("($($"+F+"))","(($"+F+")@($($"+F+")))",F)[1])
    return [[],Vivod[4]]

def teor_T2(F):
    Vivod = []
    Vivod.append(acs_A3(F,"($($"+F+"))"))
    Vivod.append(teor_T1("($"+F+")")[1])
    Vivod.append(MP(Vivod[1],Vivod[0]))
    Vivod.append(acs_A1(Vivod[1],Vivod[0]))
    Vivod.append(nasl_S1(F,"(($($($"+F+")))@"+F+")","($($"+F+"))")[1])
    return [[],Vivod[4]]

def teor_T3(F,G):
    Vivod = []
    Vivod.append("($"+F+")")
    Vivod.append(acs_A1(F,"($"+G+")"))
    Vivod.append(MP(F,Vivod[1]))
    Vivod.append(acs_A1(Vivod[0],"($"+G+")"))
    Vivod.append(MP(Vivod[0],Vivod[3]))
    Vivod.append(acs_A3(F,G))
    Vivod.append(MP(Vivod[4],Vivod[5]))
    Vivod.append(MP(Vivod[2],Vivod[6]))
    out = teor_deduc([Vivod[0]],F,Vivod[7],[Vivod[0],Vivod[1],Vivod[2],Vivod[2],Vivod[3],Vivod[4],Vivod[5],Vivod[6],Vivod[7]])
    out = teor_deduc([],Vivod[0],out[1],out[2])
    return [[],out[1]]

def teor_T4(F,G):
    Vivod = []
    Vivod.append(acs_A3(F,G))
    Vivod.append("(($"+G+")@($"+F+"))")
    Vivod.append(MP(Vivod[1],Vivod[0]))
    Vivod.append(acs_A1(F,"($"+G+")"))
    Vivod.append(nasl_S1(F,"(($"+G+")@"+F+")",G)[1])
    not_out = nasl_S1(F,"(($"+G+")@"+F+")",G)[2]
    out = [Vivod[0],Vivod[1],Vivod[2],Vivod[3]]
    out.extend(not_out)
    out = teor_deduc([],Vivod[1],Vivod[4],out)
    return [[],out[1]]

def teor_T5(F,G):
    Vivod = []
    Vivod.append(acs_A3("($"+G+")","($"+F+")"))
    Vivod.append("("+F+"@"+G+")")
    Vivod.append(teor_T2(G)[1])
    Vivod.append(nasl_S1(F,G,"($($"+G+"))")[1])
    out = nasl_S1(F,G,"($($"+G+"))")[2]
    Vivod.append(teor_T1(F)[1])
    Vivod.append(nasl_S1("($($"+F+"))",F,"($($"+G+"))")[1])
    out.extend(nasl_S1("($($"+F+"))",F,"($($"+G+"))")[2])
    Vivod.append(MP(Vivod[5],Vivod[0]))
    Vivod.append(acs_A1("($"+G+")","($($"+F+"))"))
    Vivod.append(nasl_S1("($"+G+")","(($($"+F+"))@($"+G+"))","($"+F+")")[1])
    out.extend(nasl_S1("($"+G+")","(($($"+F+"))@($"+G+"))","($"+F+")")[2])
    out = teor_deduc([],Vivod[1],Vivod[8],out)
    return [[],out[1]]

def teor_T6(F,G):
    out = []
    Vivod = []
    Vivod.append(teor_T5("("+F+"@"+G+")",G)[1])
    Vivod.append(teor_deduc([],"("+F+"@"+G+")",G,[F,"("+F+"@"+G+")",MP(F,"("+F+"@"+G+")")])[1])
    out.extend(teor_deduc([],F,"("+F+"@"+G+")",[F,"("+F+"@"+G+")",MP(F,"("+F+"@"+G+")")])[2])
    Vivod.append(MP(Vivod[1],Vivod[0]))
    out.append(Vivod[2])
    out = teor_deduc([],F,Vivod[2],out)
    return [[],out[1]]

def lema_kT7(F,G):
    Vivod = []
    Vivod.append("($"+F+")")
    Vivod.append("(($"+F+")@"+G+")")
    Vivod.append(MP(Vivod[0],Vivod[1]))
    Vivod.append(teor_T2(G)[1])
    Vivod.append(MP(Vivod[2],Vivod[3]))
    Vivod.append(teor_deduc([Vivod[1],Vivod[2],Vivod[3]],Vivod[0],"($($"+G+"))",[Vivod[0],Vivod[1],Vivod[2],Vivod[3],Vivod[4]])[1])
    out = teor_deduc([Vivod[1],Vivod[2],Vivod[3]],Vivod[0],"($($"+G+"))",[Vivod[0],Vivod[1],Vivod[2],Vivod[3],Vivod[4]])[2]
    out = teor_deduc([],Vivod[1],Vivod[5],out)
    return [[],out[1]]

def teor_T7(F,G):
    Vivod = []
    Vivod.append("("+F+"@"+G+")")
    Vivod.append(teor_T5(F,G)[1])
    Vivod.append(acs_A3(F,G))
    Vivod.append(nasl_S1(Vivod[0],"(($"+G+")@($"+F+"))","((($"+G+")@"+F+")@"+G+")")[1])
    out = nasl_S1(Vivod[0],"(($"+G+")@($"+F+"))","((($"+G+")@"+F+")@"+G+")")[2]
    Vivod.append(MP(Vivod[0],Vivod[3]))
    Vivod.append(teor_T4("($"+G+")",F)[1])
    Vivod.append(lema_kT7(F,G))
    Vivod.append(nasl_S1("(($"+F+")@"+G+")","(($"+F+")@($($"+G+")))","(($"+G+")@"+F+")")[1])
    out.extend(nasl_S1("(($"+F+")@"+G+")","(($"+F+")@($($"+G+")))","(($"+G+")@"+F+")")[2])
    Vivod.append(nasl_S1("(($"+F+")@"+G+")","(($"+G+")@"+F+")",G)[1])
    out.extend(nasl_S1("(($"+F+")@"+G+")","(($"+G+")@"+F+")",G)[2])
    out = teor_deduc([],Vivod[0],Vivod[8],out)
    return [[],out[1]]

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
        else:
            A = razbit(F)[0]
            if calc(replac(A[0]),alpha) == 0:
                out.extend(lema_Kal(A[0],alpha))
                F1 = out[len(out)-1]
                out.append(teor_T3(A[0],A[1])[1])
                F2 = out[len(out)-1]
                F3 = MP(F1,F2)
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
                out.append(teor_T6(A[0],A[1])[1])
                F3 = out[len(out)-1]
                F4 = MP(F1,F3)
                out.append(F4)
                F5 = MP(F2,F4)
                out.append(F5)
    return out
            
def adekvat(F):
    if not glavnaya(F):
        return False
    arn = kolvo_per(F)
    out = [0]*arn
    alphasp = alpha_sp(arn+1)
    for i in range (arn):
        out[i] = lema_Kal(F,alphasp[i])
    while arn != 0:
        arn -= 1
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
            F3 = teor_T7("(x["+str(arn)+"])",F)[1]
            F4 = MP(F1,F3)
            F5 = MP(F2.F4)
            res = vivod_F1
            res.extend(vivod_F2)
            res.append(F4)
            res.append(F5)
            out[i] = res
    alphasp = [[0],[1]]
    alpha = alphasp[1]
    Gamma = []
    vrem = teor_deduc(Gamma,f_alpha("(x[0])",alpha),F,out[0])
    F1 = vrem[1]
    vivod_F1 = vrem[2]
    alpha = alphasp[0]
    vrem = teor_deduc(Gamma,f_alpha("(x[0])",alpha),F,out[0])
    F2 = vrem[1]
    vivod_F2 = vrem[2]
    F3 = teor_T7("(x[0])",F)[1]
    F4 = MP(F1,F3)
    F5 = MP(F2,F4)
    res = vivod_F1
    res.extend(vivod_F2)
    res.append(F4)
    res.append(F5)
    out[0] = res
    return res








while True:
    logik = input("Введите выражение(@ - импликация, $ - заперечення,\nпеременную под номером n обозначать xn, все брать в скобки): ")
    logik = format_per(logik)

    print(logik)
    if glavnaya(logik):
        print("Тавтология")
    else:
        print("Не тавтология")

    print(adekvat(logik))
