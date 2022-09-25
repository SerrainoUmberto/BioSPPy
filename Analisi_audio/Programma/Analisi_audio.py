import os,shutil
import numpy as np
import scipy as sp
from scipy.io import wavfile as wv
from scipy.fftpack import fft,fftfreq
import simpleaudio as sa
from pylab import *
import matplotlib.pyplot as plt
import biosppy

''' Funzioni di controllo e gestione del segnale audio per renderlo compatibile con
    istruzioni utilizzate'''
def controllo_audio(file_name,op=''):
    try:
        file = np.load('../../Analisi_audio/Work/'+file_name+'/'+file_name+op+'.npz')
        audio = file['amp']
        fs = file['fs']
    except FileNotFoundError:
        print('\nIl file non esiste!\n')
    return audio,fs

'''def stereo_to_mono(audio):
    if np.size(audio.shape) == 2: # Campioni per file a due canali
        rr,vv = audio.shape
        amp = np.zeros(rr)
        for i in range(rr):
            amp[i] = sum(audio[:][i])/2
    else:
        amp = np.array(audio)
        rr = np.size(amp)
    return amp,rr'''

def stereoToMono(audiodata):
    newaudiodata = []
    for i in range(int(len(audiodata)/2)):
        d = (audiodata[i][0]/2 + audiodata[i][1]/2)
        newaudiodata.append(d)

    return np.array(newaudiodata, dtype='int16')

# --------------- LOAD ---------------- #
""" Funzione iniziale da eseguire sempre, esegue ogni check sulla validità dei dati inseriti
    a monte, così da avere un procedura più snella per le funzioni successive
"""
def audio_load(fin,N):
    Nmax = 50000
    while N>Nmax or N<0: # controllo di avere un numero corretto di campioni
        if N>50000:
            N = int(input('Inserire numero di campioni minore di {}: '.format(Nmax)))
        elif N<=0:
            N = int(input('Inserire numero positivo di campioni: '))
    fini = '../../Analisi_audio/Dati/'+fin+'.wav' 
    try:
        file = open(fini,'r')
    except FileNotFoundError:
        print('\nIl file non esiste!\n')
            
    file.close()    
    (fs,audio) = wv.read(fini,True) # tupla di 2 elementi
    #audio = np.array(audio)

    #amp,rr = stereo_to_mono(audio) # Campioni per file a un canale

    #print(fs)
    #print(amp_audio)
    #print(len(amp_audio)
    #print(rr)
    if np.size(audio.shape) == 2: # Campioni per file a due canali
        audio = stereoToMono(audio)
#        rr,vv = audio.shape
#    else:
    rr = np.size(audio)
        
    if N>0 and N<rr:    # analisi degli ultimi N campioni
        audio = audio[:N]
    else:
        audio = audio[:rr]
        N = rr

    try:
        os.makedirs('../../Analisi_audio/Work/'+fin)
    except FileExistsError:
        print('Directory già esistente, i file saranno salvati al suo interno')

    np.savez('../../Analisi_audio/Work/'+fin+'/'+fin+'.npz',amp=audio,fs=fs)
    print('Frequenza di campionamento: {} Hz'.format(fs))
    print(audio)

# --------------- PLOT ---------------- #
"""Funzione per stampare tutti gli elementi generati dal sistema"""
def audio_plot_time(file_name,op=''):

    audio,fs = controllo_audio(file_name,op)
    
    #t = (np.arange(np.size(audio)))/fs #vettore temporale    
    durata = len(audio)
    t = np.arange(0,durata)/fs

    plt.figure(figsize=(10,8)) # Dimensione della pagina che presenta il grafico
    plt.plot(t,20*log(audio))
    plt.grid() # Formazione della griglia
    plt.title('Segnale audio '+file_name) #imposto titolo
    plt.xlabel('t [s]') #imposto nome delle ascisse
    plt.ylabel('Ampiezza [dB]') #imposto nome delle ordinate
    plt.show()


def audio_plot_freq(file_name,op=''):

    audio,fs = controllo_audio(file_name,op)
    durata = np.size(audio)
    FFT = abs(fft(audio))
    #t = (np.arange(np.size(audio)))/fs #vettore temporale    
    freqs = fftfreq(durata,1/fs)
    L = len(FFT)

    plt.figure(figsize=(10,8)) # Dimensione della pagina che presenta il grafico
    plt.plot(freqs[:int(L/2)],20*log(FFT[:int(L/2)]))
    plt.grid() # Formazione della griglia
    plt.title('TdF '+file_name+' '+op) #imposto titolo
    plt.xlabel('f [Hz]') #imposto nome delle ascisse
    plt.ylabel('Ampiezza [dB]') #imposto nome delle ordinate
    plt.show()

    np.savez('../../Analisi_audio/Work/'+file_name+'/'+file_name+'TDF.npz',amp=FFT,fs=fs)
    print('Il file '+file_name+'TDF.npz è stato salvato\n')



# --------------- PLAY ---------------- #
def audio_play(file_name,op=''):
    # eseguo il file generato
    audio,fs = controllo_audio(file_name,op)

    wv.write('../../Analisi_audio/Work/'+file_name+'/'+file_name+op+'.wav',fs,audio)
    wave_obj = sa.WaveObject.from_wave_file('../../Analisi_audio/Work/'+file_name+'/'+file_name+'.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()
    
    
# --------------- STOP ---------------- #
def audio_stop(file_name,op=''):
    wave_obj = sa.WaveObject.from_wave_file('../../Analisi_audio/Work/'+file_name+'/'+file_name+'.wav')
    stop_obj = wave_obj.stop()
    
    
# ------------ SPECTRE ---------------- #
def audio_spec(file_name,T=0,wind='hann',op=''):
    # T durata in secondi
    audio,fs = controllo_audio(file_name,op)
    if T == 0: T = int(len(audio)/10)
    #audio,rr = stereo_to_mono(audio) # Campioni per file a un canale
    
    freq,power=biosppy.signals.tools.welch_spectrum(signal=audio,sampling_rate=fs,size=T,window=wind,decibel=True)

    plt.figure(figsize=(10,8)) 
    plt.plot(freq,power)
    plt.grid() 
    plt.title('Spettro di densità di potenza') # titolo
    plt.xlabel('Frequenza [Hz]') # nome delle ascisse
    plt.ylabel('Ampiezza [dB]') # nome delle ordinate
    plt.show()

# ------------- FILTRO ---------------- #
def audio_filtro(file_name,fL=0,fH=0,op=''):

    audio,fs = controllo_audio(file_name,op)
       
    durata = np.size(audio) # Campioni per file a un canale
    
    t = np.arange(0,durata,1/fs)
    segnale,k,l=biosppy.signals.tools.filter_signal(signal=audio, ftype='butter',order=4 ,band='bandpass',frequency=[fL,fH], sampling_rate=fs)

    np.savez('../../Analisi_audio/Work/'+file_name+'/'+file_name+'fil.npz',amp=segnale,fs=fs)
    print('Il file '+file_name+'fil.npz è stato salvato\n')


# ------------ ADD SIN --------------- #
def audio_addsin (file_name,A,f0,op=''):

    audio,fs = controllo_audio(file_name,op)
    #audio,rr = stereo_to_mono(audio) # Campioni per file a un canale
    
    t = np.arange(np.size(audio))/fs
    y = A * np.sin(2 * math.pi * f0 * t)
    audio_sin = audio + y

    np.savez('../../Analisi_audio/Work/'+file_name+'/'+file_name+'sin.npz',amp=audio_sin,fs=fs)

    print('\nIl disturbo sinusoidale è stato aggiunto \n')
    print('Il file '+file_name+'sin.npz è stato salvato\n')


    
  
