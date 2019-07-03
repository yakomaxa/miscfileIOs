
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
            resn += [int(parsed[0])]
            aa += [str(parsed[1])]
            ss += [str(parsed[2])]
            abego += [str(parsed[3])]
            phi += [float(parsed[4])]
            psi += [float(parsed[5])]
            omega += [float(parsed[6])]
    rama=df(data={"resn":resn,
                  "aa":aa,
                  "ss":ss,
                  "abego":abego,
                  "phi":phi,
                  "psi":psi,
                  "omega":omega},
       columns=ramaheader)
    
    if(ignoreterms):
        rama=rama.drop(0)
        rama=rama.drop(rama["resn"].size)
        return  rama
    else:
        return rama
        
