import matplotlib.pyplot as plt
def plot_ecg(segnale,tempo):
    plt.figure(figsize=(10,8)) #definisco la misura della pagina che presenta il grafico
    plt.plot(tempo,segnale)
    plt.grid() #decido che il grafico contenga righe e colonne
    plt.title('ECG') #imposto titolo
    plt.xlabel('Tempo (Secondi)') #imposto nome delle ascisse
    plt.ylabel('d.d.p(Millivolt)') #imposto nome delle ordinate
    plt.show()
