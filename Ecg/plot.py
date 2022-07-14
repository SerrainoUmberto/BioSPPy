import matplotlib.pyplot as plt
def plot_ecg(segnale,tempo):
    plt.figure(figsize=(10,8))
    plt.plot(tempo,segnale)
    plt.grid()
    plt.title('ECG')
    plt.xlabel('Tempo (Secondi)')
    plt.ylabel('d.d.p(Millivolt)')
    plt.show()
