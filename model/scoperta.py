import numpy as np
from collections import Counter
import pandas as pd

def scoperta(measure_sensibilit):
    distanza_finale=[]
    week_individuazione_np=np.array([['B.1',11],['B.1.1 ',10],['B.1.177',44],['B.1.2',47],['B.1.1.7',56],['AY.44',82],['AY.43',105], ['AY.4',79],['AY.103',84],['B.1.617.2',87],['BA.1',107],['BA.2',111],['BA.2.9',111],['BA.2.3',121],['BA.2.12.1',126],['BA.5.1',134],['CH.1.1',156],['XBB.1.5',159]])
    measure_sensibilit_np = np.array(measure_sensibilit) #lo trasformo in un array np
    Varianti = measure_sensibilit_np[:, 0] #seleziono le varianti
    variant_dict = Counter(Varianti) #costruisco un dizionario con le varianti
    for k in variant_dict.keys(): #ciclo sulle varianti
        if k == 'unknown':
            continue
        i_k = np.where(measure_sensibilit_np == k)[0] # trovo gli indici in cui c'è la variante
        i_w = np.where(week_individuazione_np == k)[0]
        Settimana_riconosciuta= np.array(list(map(int, week_individuazione_np[i_w, 1]))) # settimane riconoscite
        predetti = np.array(list(map(int, measure_sensibilit_np[i_k, 2]))) #predetti
        week_an = np.array(list(map(int, measure_sensibilit_np[i_k, 3]))) #settimana (ricordiamo che dobbiamo aggiungere ad 1 per la differenza delle settimne )
        Indice_prima_predizione=np.where(predetti>0)[0] #vado a prendere il minimo degli indici in cui le predizioni sono maggiore di 0
        if len(Indice_prima_predizione)==0:
            continue
        settimana_prima_predizione=min(list(week_an[Indice_prima_predizione]))
        settimana_prima_predizione_true=settimana_prima_predizione+1
        distanza=np.array(Settimana_riconosciuta-settimana_prima_predizione_true)
        riassunto=[k,distanza]
        distanza_finale.append(riassunto)
    return distanza_finale,