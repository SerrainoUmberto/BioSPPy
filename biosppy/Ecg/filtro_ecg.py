from biosppy.signals import ecg
def filtro_ecg(segnale):
    out=ecg.ecg(signal=segnale,sampling_rate=500, show=False)
    return out[1]
    
    
