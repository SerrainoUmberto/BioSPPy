import os
import numpy as np
"""funzione che richiede in ingresso il numero del file
e il numero di campioni da far uscire, e da in uscita il numero definito di campioni del tempo e del segnale ecg"""
Fs=500 #frequenza di campionamento
def load_ecg(num_file,campioni): 
    os.chdir('C:/Users/dontw/OneDrive/Desktop/Tesi/Dati') #imposto come directory di lavoro la cartella dati
    
    if type(num_file)== int:     #controllo ingresso corretto
        if type(campioni)==int:
            if campioni > 10000:
                print('Il massimo di campioni ammissibili è 10000')
                return None,None
            elif campioni <=0:
                print(' Devi inserire un numero positivo di campioni')
                return None,None
            else:
                file= 'rec' + str(num_file) + '.txt'
                """x=pd.read_csv(file,header=None)  #prima utilizzavo questo script con pandas
                signal=x.loc[0:campioni-1,[1]]
                t=x.loc[0:campioni-1,[0]]
                ecg=signal.to_numpy()
                tempo=t.to_numpy()
                    """
                x=np.loadtxt(file)     #load del file scelto
                y=np.linspace(0,19.998,10000,endpoint= True)
                ecg=x[0:campioni]  #scelta della lunghezza dei campioni
                t=y[0:campioni]     #non metto il -1 alla lunghezza perchè l'ultimo elemento è escluso
                return t,ecg
        else:
            print('Metti un numero intero di campioni')
            return None,None
    else:
        print('Inserisci un numero intero per scegliere il file')
        return None,None
    
    
