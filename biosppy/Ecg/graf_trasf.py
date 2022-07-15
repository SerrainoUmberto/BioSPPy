from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np

def mod_fft(ecg_signal):
    Fs=500 #frequenza campionamento
    fourier=fft(ecg_signal) #faccio la trasformata di Fourier discreta
    n=np.size(ecg_signal)
    fx=fftfreq(n,1/Fs) # Restituisce le componenti in frequenza corrispondente all'array della trasformata 
    fy=np.abs(fourier) #faccio il modulo della trasformata del segnale
    plt.figure(figsize=(10,8))
    plt.plot(fx,fy)
    plt.grid()
    plt.title('Modulo FFT')
    plt.xlabel('Frequenza (Hz)')
    plt.ylabel('Modulo (Void)')
    plt.show()
    
    
