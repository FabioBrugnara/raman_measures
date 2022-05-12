#  LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import os
import copy


##########################################################
######################## FUNZIONI ########################
##########################################################

def _raman_labels():
    plt.figure(figsize=(10,5))
    plt.xlabel(r'Raman shift [$cm^{-1}$]')
    plt.ylabel('Counts')


def merge_spectra(folder = 'raw_data', plot=False):
    # CERCO I FILE NELLLA CARTELLA folder E LI RAGRUPPO
    dir = sorted(os.listdir(folder))
    name = ''
    files=[]
    n_file=-1
    for rep in dir:
        if rep[-4:]=='.txt':
            if rep[:-6]!=name:
                name = rep[:-6]
                files.append([rep])
                n_file +=1
            else:
                files[n_file].append(rep)

    for i in range(len(files)):
        # CARICO TUTTI GLI SPETTRI DI UNA RIPETIZIONE IN UNA LISTA
        spectras_raw=[]
        for j in files[i]:
            spectras_raw.append(np.transpose(np.loadtxt(folder+'/'+j)))

        spectras = copy.deepcopy(spectras_raw)


        for a in range(len(spectras)-1):
            b = a+1
            # CALCOLO REGIONE COMUNE AGLI SPETTRI A E B
            na,nb = (0,0)
            while spectras[a][0][na]<spectras[b][0][0]:
                na+=1
            while spectras[b][0][nb]<spectras[a][0][-1]:
                nb+=1

            # CALCOLO OFFSET A-B
            offset = np.mean(spectras[a][1][na:]) - np.mean(spectras[b][1][:nb])

            # AGGIUNGO OFFSET A SPETTRO B
            spectras[b][1] += offset

        merged = np.concatenate(spectras, axis=1)

        if plot==True:
            plt.figure(figsize=(10,5))
            for a in range(len(spectras_raw)):
                plt.plot(spectras_raw[a][0],spectras_raw[a][1])

            plt.plot(merged[0], merged[1])
            plt.title(files[i][0][0:-7])
            plt.show()
            
        np.savetxt(files[i][0][0:-7]+'.txt', np.transpose(merged))

def ls():
    files = [j for j in os.listdir() if (j[-4:]=='.txt' and j[0:6]!='README')]
    for i in enumerate(files):
        print(i[0], ' -> ', i[1])

def plot(S):

    if type(S)==str:
        S = np.transpose(np.loadtxt(S))
    elif type(S)==np.ndarray:
        S = S
    elif type(S)==int:
        S = np.transpose(np.loadtxt([j for j in os.listdir() if (j[-4:]=='.txt' and j[0:6]!='README')][S]))
    else:
        print('Type error!')
        return 

    _raman_labels()
    plt.plot(S[0], S[1])
    plt.show()

def loadtxt(file):
    return np.transpose(np.loadtxt(file))

def bkg_subtraction(S):
    BKG = np.zeros(len(S[0]))
    S_nobkg = np.ones(len(S[0]))
    return BKG, S_nobkg


################################################################
######################## CLASSE SPECTRA ########################
################################################################

class spectra:

    def __init__(self, S):
        
        if type(S)==str:
            self.info = S[:-4]
            self.S = np.transpose(np.loadtxt(S))
        
        elif type(S)==np.ndarray:
            self.S = S
            self.info = 'No uploaded info about this spectra. Save info in this variable'
        elif type(S)==int:
            S = [j for j in os.listdir() if (j[-4:]=='.txt' and j[0:6]!='README')][S]
            self.info = S[:-4]
            self.S = np.transpose(np.loadtxt(S))
        else:
            print('Type error!')

    def plot(self):
        _raman_labels()
        if self.info!='No uploaded info about this spectra. Save info in this variable':
            plt.title(self.info)

        plt.plot(self.S[0], self.S[1])
        plt.show()

    def bkg_subtraction(self):
        self.BKG, self.S_nobkg = bkg_subtraction(self.S)

    
