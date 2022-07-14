from biosppy.signals import ecg
def filtro_ecg(segnale):
    out=ecg.ecg(signal=segnale, show=False)
    return out[1]
    
    
