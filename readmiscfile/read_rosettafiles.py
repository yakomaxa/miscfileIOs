
def read_rama(filename, ignoreterms=True):
    from pandas import  DataFrame as df
    ramafile=open(filename)
    lines=ramafile.readlines()
    #df.append()
    ramaheader = ["resn","aa","ss","abego","phi","psi","omega"]
    #df=df(columns=ramaheader)

    resn=[]
    aa=[]
    ss=[]
    abego=[]
    phi=[]
    psi=[]
    omega=[]

    for line in lines:
        parsed=list(map(str, line.split()))
        if ( parsed[0] == "#"):
            print("header ignored")
            print(parsed)
        else:
            resn += [parsed[0]]
            aa += [parsed[1]]
            ss += [parsed[2]]
            abego += [parsed[3]]
            phi += [parsed[4]]
            psi += [parsed[5]]
            omega += [parsed[6]]
    rama=df(data={'resn':resn,
              'aa':aa,
              'ss':ss,
              'abego':abego,
              'phi':phi,
               "psi":psi,
               "omega":omega},
       columns=ramaheader)
    
    if(ignoreterms):
        rama=rama.drop(0)
        rama=rama.drop(rama["resn"].size)
        return  rama
    else:
        return rama
        
