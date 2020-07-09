import torch
class fragmentsets:
    def __init__(self):
        self.fragments = []
        self.ssetype = []
        #self.fragments_now = []
        self.resindex = []
    def readfile(self,filename=None,fragsize=3,fragnum=200):
        with open(filename) as f:
            c=0
            for line in f:
                if (line[0] == "\n"):
                    print("new")
                    cc=0
                elif (line==" "):
                    print("boid")
                    cc=1
                elif (line[0]==" "):
                    pos=line[1:10]
                    if (pos == "position:"):
                        numfrag = int(line[-14:-1])
                        fragid = int(line[10:23])
                        #print(fragid)
                        self.fragments_now = []
                        self.ssetype_now = []
                        writeflag=0
                    else:
                        #print(line)
                        #print(slices(line, 3, 3, 5))
                        pdbid = line[1:5]
                        chainid = line[6]
                        position=line[10:13]
                        resname=line[14:15]
                        ssetype=str(line[16:17])
                        phi = float(line[18:26])
                        psi = float(line[27:35])
                        omega = float(line[36:44])
                        #ppo=[phi,psi,omega]
                        #c=1
                        if (c==0):
                            phis=[phi]
                            psis=[psi]
                            omegas=[omega]
                            sses=[ssetype]
                            c=c+1
                        else:
                            phis.append(phi)
                            psis.append(psi)
                            omegas.append(omega)
                            sses.append(ssetype)
                            c=c+1
                            if(c == fragsize):
                                print("hello"+str(c))
                                c=0
                                self.fragments_now.append([(phis),
                                                           (psis),
                                                           (omegas)])
                                self.ssetype_now.append(sses)
                                writeflag=writeflag+1
                                if (writeflag == fragnum):
                                    self.fragments.append(self.fragments_now)
                                    self.ssetype.append(self.ssetype_now)

        self.tensorfragments=torch.tensor(self.fragments).permute([0,1,3,2])

    def set_resindex(self):
        for i in range(0,len(self.fragments)):
            self.resindex.append(slice(i, i+len(self.fragments[0][0][0])))

    def set_tensorfragments(self):
        self.tensorfragments=torch.tensor(self.fragments).permute([0,1,3,2])
        #return fragments

    def writefragment(self,outname=None,write_sse=False):
        frags = self.tensorfragments
        if (write_sse):
            sses = self.ssetype
        # assume frags has N batch, M residue, L dim  (L=3dim: phi psi omega)
        # dummy strings
        left = ' xxxx A     0 V '
        middle = '    0.000    0.000     0.000 0     0.000'
        right = 'P  1 F  1'
        #####
        fragsize = frags.size(2)
        fragnum = frags.size(1)
        regionnum = frags.size(0)
        nei = "% 8s" % str(fragnum)
        newline = " \n"
        f = open(file=outname, mode="w")
        import numpy as np
        # phis_all = np.ndrray(frags[:,:,0])
        # psis_all = np.adrray(frags[:,:, 1])
        # omegas_all = np.array(frags[:,:, 2])
        #fragnumber = frags.size(0) - fragsize + 1
        for iregion in range(0, regionnum, 1):
            print(iregion)
            pos = "% 7s" % str(iregion + 1)
            header = " position:" + pos + " " + "neighbors:" + nei
            f.write(header + "\n")
            f.write(newline)
            resis = slice(iregion, iregion + fragsize - 1 + 1, 1)
            # sstypes=list(rama.ss[resis])
            for i in range(0, fragnum, 1):
                phis = frags[iregion,i,:, 0]
                psis = frags[iregion,i,:, 1]
                omegas = frags[iregion, i, :, 2]
                if (write_sse):
                    sse = sses[iregion][i][:]

                #print(phis.size())
                for iline in range(0, fragsize, 1):
                    PP = "% 3s" % str(iregion + 1)
                    FF = "% 3s" % str(i + 1)
                    right = " " + "P" + PP + " " + "F" + FF
                    phi = phis[iline]  # + 5 * np.random.randn()
                    phi_str = "%9.3f" % phi
                    psi = psis[iline]  # + 5 * np.random.randn()
                    psi_str = "%9.3f" % psi
                    omega = omegas[iline]  # + 2 * np.random.randn()
                    omega_str = "%9.3f" % omega
                    # fragmain=left+sstypes[iline]+phi_str+psi_str+omega_str+middle+right
                    if (write_sse):
                        fragmain = left + str(sse[iline]) + phi_str + psi_str + omega_str + middle + right
                    else:
                        fragmain = left + "L" + phi_str + psi_str + omega_str + middle + right

                    f.write(fragmain + "\n")
                f.write(newline)
        f.close()

