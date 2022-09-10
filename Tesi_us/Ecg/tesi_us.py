import os
import numpy as np
import matplotlib.pyplot as plt
import math
import biosppy
import random
"""funzione che richiede in ingresso il numero del file
e il numero di campioni da far uscire, e salva l'array ecg nella cartella work sotto il nome di ecg.npy"""
Fs=500 #frequenza di campionamento
def load_ecg(num_file,campioni): 
    
    if type(num_file)== int:     #controllo ingresso corretto #devo ancora mettere il controllo sui file
        if type(campioni)==int:
            if campioni > 10000:
                print('Il massimo di campioni ammissibili è 10000')
            elif campioni <=0:
                print(' Devi inserire un numero positivo di campioni')
            else:
                file='../../Tesi_us/Dati/rec'+str(num_file)+ '.txt'
                x=np.loadtxt(file)     #load del file scelto
                ecg=x[0:campioni]  #scelta della lunghezza dei campioni
                np.save('../../Tesi_us/Wrk/ecg.npy', ecg)
                
        else:
            print('Metti un numero intero di campioni')
            
    else:
        print('Inserisci un numero intero per scegliere il file')
        

"""Funzione che preleva in ingresso l'array del segnale ECG salvato come ecg.npy nella sottocartella Wrk,
e da in uscita un grafico nel tempo del segnale ECG"""
def plot_ecg(nome_file_da_plottare):
    segnale=np.load('../../Tesi_us/Wrk/' + nome_file_da_plottare + '.npy')
    t=np.arange(np.size(segnale)) #Definisco un array del tempo che va da 0 fino alla dimensione dell'array
    #segnale -1 in quanto la funzione non inserisce l'ultimo elemento
    tempo=t/Fs #Definisco il periodo di campionamento del segnale ECG
    plt.figure(figsize=(10,8)) #definisco la misura della pagina che presenta il grafico
    plt.plot(tempo,segnale)
    plt.grid() #decido che il grafico contenga righe e colonne
    plt.title('ECG') #imposto titolo
    plt.xlabel('Tempo (Secondi)') #imposto nome delle ascisse
    plt.ylabel('d.d.p(mV)') #imposto nome delle ordinate
    plt.show()
    
"""
La funzione riceve in ingresso l'array x del segnale ECG, l'ampiezza a e la frequenza fo del segnale sinusoidale.
La sinusoide si somma all'array ECG, e questa funzione da in uscita il vettore somma dei campioni del segnale ECG
e della sinusoide, intesa come rumore.
"""
def ecg_add_sin0(x,a,fo ):
    t=np.arange(np.size(x)) #Definisco Definisco un array del tempo che va da 0 fino alla dimensione dell'array
    #segnale -1 in quanto la funzione non inserisce l'ultimo elemento
    t=t/Fs #Definisco il periodo di campionamento del segnale ECG
    d = a* np.sin( 2 * math.pi * fo * t )
    y= x + d
    return y
"""
Questa funzione riceve in ingresso il numero del file da cui prelevare i campioni del segnale ECG, quanti campioni utilizzare
del segnale ECG, l'ampiezza a della sinusoide da sommare al segnale ECG e la sua frequenza fo.
Questa funzione darà luogo a un vettore somma del segnale ECG e del rumore sinusoidale, e la salverà
nella sottocartella Wrk, con il nome di 'ecg_seno.npy'
"""
def ecg_add_sin(n_file,n_campioni,a,fo):
    if type(n_file)== int:     #Protezione da cosa metto in ingresso
        #if n_file >=1 and <= ? :
        if type(n_campioni)==int:
            if n_campioni > 10000:
                print('Il massimo di campioni ammissibili è 10000')
            elif n_campioni <=0:
                print(' Devi inserire un numero positivo di campioni')
            else:
                load_ecg(n_file,n_campioni) #Uso la funzione load_ecg 
                segnale=np.load('../../Tesi_us/Wrk/ecg.npy')#Prelevo il vettore ecg salvato
                #come ecg.npy nella sottocartella Wrk
                ecg_seno=ecg_add_sin0(segnale,a,fo)
                np.save('../../Tesi_us/Wrk/ecg_seno.npy', ecg_seno)#Salvo il nuovo vettore
                #ecg più rumore dato dalla sinuoside col nome ecg_seno nella sottocartella Wrk
        else:
            print('Metti un numero intero di campioni')        

    else:
        print('Inserisci un numero intero per scegliere il file')
"""
La funzione riceve in ingresso x,vettore che rappresenta il file ecg,
lo azzera nell'intervallo temporale t1-to e restituisce il segnale
modificato sotto forma di vettore.
"""
def ecg_zero0(x,to,t1 ): #Essendo Fs=500, il segnale ECG ha periodo di campionamento Ts pari a 0.002
    Ts=1/Fs
    Tmax= Ts * 9999
    if t1 > Tmax:
        print('Abbiamo acquisito il segnale fino a '+ str(Tmax)+ ' secondi')

    else:
        to=math.floor(to)
        t1=math.floor(t1)
        t0=to*Fs #campione n-esimo all'istante to
        t11=t1*Fs #campione n-esimo all'istante t1
        x[t0:t11+1]=0
        return x

"""
La funzione riceve in ingresso il numero del file da cui prelevare il segnale ecg, preleva questi campioni
e azzera il segnale ECG nell'intervallo temporale t1-to e salva il segnale modificato nella sottocartella Wrk
"""
def ecg_zero(nu_file,to,t1):
    if type(nu_file)== int:
        #if n_file >=1 and <= ? :
        load_ecg(nu_file,10000) #Uso la funzione load_ecg 
        segnale=np.load('../../Tesi_us/Wrk/ecg.npy')#Prelevo il vettore ecg salvato
        #come ecg.npy nella sottocartella Wrk
        if to>t1:
            print('Intervallo di tempo errato')
        else:
            z=ecg_zero0(segnale,to,t1)
            np.save('../../Tesi_us/Wrk/ecg_zero.npy',z)#Salvo il nuovo vettore
            #ecg azzerato nell'istante temporale t1-t0 col nome ecg_zero nella sottocartella Wrk
        
    else:
        print('Inserisci un numero intero per scegliere il file')
"""
La funzione riceve in ingresso i campioni del segnale ECG, la frequenza f0, la frequenza f1 e SNR in dB.
Essa somma al segnale ECG un rumore bianco filtrato con un filtro passa-banda alle frequenze fo e f1, in maniera tale
che il rapporto segnale-rumore del segnale uscente sia pari al SNR in dB indicato all'ingresso della funzione.
"""

def ecg_noise0(x,f0,f1,SNRdB):
    SNR=10**(SNRdB/20) 
    rum=np.random.standard_normal(np.size(x)) #Definisco il rumore bianco
    rumf,k,l=biosppy.signals.tools.filter_signal(signal=rum, ftype='butter',order=4 ,band='bandpass',frequency=[f0,f1], sampling_rate=500)
    #Filtro il rumore bianco e lascio passare solo la banda compresa tra f0 e f1
    rmsx=math.sqrt(np.mean(x**2)) #Calcolo il root mean square del segnale ECG
    rmsr=math.sqrt(np.mean(rumf**2)) #Calcolo il root mean square del processo bianco
    a=rmsx/(rmsr*SNR) #Definisco la costante a, che moltiplicata con il rumore filtrato, mi da luogo al SNR desiderato
    y=a*rumf
    z=x+y
    return z
"""
La funzione riceve in ingresso il numero del file del segnale ECG, quanti campioni utilizzare, la banda
in cui vogliamo che il rumore sia contenuto,e il rapporto segnale-rumore che vogliamo ottenere nel segnale risultante
la somma del segnale ECG e del rumore bianco. Questa funzione produce il segnale somma del segnale ECG e del rumore
bianco, e lo salva nella sottocartella Wrk con il nome di ecg_noise.
"""
def ecg_noise(n_file,n_campioni,f0,f1,SNRdB):
    if type(n_file)== int:     #Protezione da cosa metto in ingresso
        #if n_file >=1 and <= ? :
        if type(n_campioni)==int:
            if n_campioni > 10000:
                print('Il massimo di campioni ammissibili è 10000')
            elif n_campioni <=0:
                print(' Devi inserire un numero positivo di campioni')
            else:
                load_ecg(n_file,n_campioni) #Uso la funzione load_ecg 
                segnale=np.load('../../Tesi_us/Wrk/ecg.npy')#Prelevo il vettore ecg salvato
                #come ecg.npy nella sottocartella Wrk
                ecgn=ecg_noise0(segnale,f0,f1,SNRdB)
                np.save('../../Tesi_us/Wrk/ecg_noise.npy', ecgn)#Salvo il nuovo vettore
                #ecg più rumore dato dalla sinuoside col nome ecg_noise nella sottocartella Wrk
        else:
            print('Metti un numero intero di campioni')        

    else:
        print('Inserisci un numero intero per scegliere il file')
"""
Funzione che chiede quale vettore salvato prelevato e quale finestra utilizzare, e produce in uscita
il grafico della densità di potenza del segnale in ingresso
"""
def graf_spettro(nome_file_segnale,finestra):
    x=np.load('../../Tesi_us/Wrk/' + nome_file_segnale + '.npy')
    freq,power=biosppy.signals.tools.welch_spectrum(signal=x,sampling_rate=500,window=finestra,decibel=True)
    plt.figure(figsize=(10,8)) #definisco la misura della pagina che presenta il grafico
    plt.plot(freq,power)
    plt.grid() #decido che il grafico contenga righe e colonne
    plt.title('Spettro di densità di potenza') #imposto titolo
    plt.xlabel('Frequenza (Hz)') #imposto nome delle ascisse
    plt.ylabel('densità di potenza (mV^2/Hz)in dB') #imposto nome delle ordinate
    plt.show()

"""
La funzione riceve in ingresso il numero del file che rappresenta il file ecg, e ha il 50% di applicare
in modo casuale tre disturbi e di modificare il file restituendo in uscita il
file modificato sotto il nome di ecg_distuba, contenuto nella sottocartella Wrk. k è un parametro che cambia il seme
per k=0 il seme cambia, per k>1 il seme rimane quello del numero scelto.
"""
def ecg_disturba(n_file, k):
    if type(n_file)== int:
        #if n_file >=1 and <= ? :
        load_ecg(n_file,10000) #Uso la funzione load_ecg 
        segnale=np.load('../../Tesi_us/Wrk/ecg.npy')#Prelevo il vettore ecg salvato
        #come ecg.npy nella sottocartella Wrk
        if k>0:
            random.seed(k)
            x=random.random()
        else:
            x=random.random()

        if x>0.5:
            c=0
            d=np.size(segnale)/Fs
            to=math.floor(c+(d-c)*random.random())
            e=0
            t1=math.floor(e+(d-e)*random.random())

            while t1>19.998:
                t1=math.floor(e+(d-e)*random.random())

            if to>t1: #ribalto l'intervallo
                t2=t1
                t1=to
                to=t2
                
            ecg_d=ecg_zero0(segnale,to,t1 )
            print('La funzione ha azzerato il segnale ECG tra to=' +str(to)+ ' e t1='+ str(t1)+'. \n')
        else:
            print('La funzione non ha azzerato il segnale ECG in un intervallo t1-to')

        if x>0.5:
            ss=np.std(segnale)
            c=0.05*ss
            d=0.5*ss;
            a=c+(d-c)*random.random()
            e=0.01
            f=(Fs/2)-0.01
            f0=math.floor(e+(f-e)*random.random())
            ecg_d2=ecg_add_sin0(ecg_d,a,f0)
            print('La funzione ha aggiunto un disturbo sinusoidale di ampiezza a='+str(a)+' e frequenza f='+str(f0)+' Hz al segnale ECG.\n')

        else:
            print('La funzione non ha aggiunto nessun disturbo sinusoidale.\n')

        if x>0.5:
            c=0.001
            d =(Fs/2)-0.01
            fo=math.floor(c+(d-c)*random.random())
            e=5
            f=(Fs/2)-0.01
            f1=math.floor(e+(f-e)*random.random())
            if f1<fo:
                f2=f1
                f1=fo
                fo=f2
            g=10
            h =30
            SNRdB=math.floor(g+(h-g)*random.random())
            ecg_d3=ecg_noise0(ecg_d2,fo,f1,SNRdB)
            print('La funzione ha aggiunto un rumore passa banda tra la frequenza fo='+str(fo)+' Hz e la frequenza f1='+str(f1)+' Hz al segnale ECG.Il rapporto segnale-rumore in dB vale '+str(SNRdB)+'. \n')
            np.save('../../Tesi_us/Wrk/ecg_disturba.npy',ecg_d3)#Salvo il nuovo vettore
                #ecg più rumore col nome ecg_disturba nella sottocartella Wrk
        else:
            print('La funzione non ha aggiunto nessun rumore bianco.\n')

    else:
        print('Inserisci un numero intero per scegliere il file')    
    

       
        
