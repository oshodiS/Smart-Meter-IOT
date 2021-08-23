# Progetto programmazione di reti: Traccia 1
## Shola Oshodi - Daniel Guariglia 


Gli aspetti di analisi e progettazione sono approfonditi nella relazione in formato pdf all'interno della seguente repository git:  
https://github.com/oshodiS/progetto-reti.git

# Informazioni personali
### Daniel Guariglia
Mail: daniel.guariglia@studio.unibo.it \
Matricola: 0000916433

### Shola Oshodi
Mail: shola.oshodi@studio.unibo.it \
Matricola: 0000915434

## Librerie esterne necessarie
Durante lo sviluppo del progetto abbiamo importato diverse librerie estene tra cui:

* Time
* Thread
* colorama  (colori per console)
* termcolor (colori per console)
* json
* datatime

Tra le sopracitate è probabile che sia necessario installare le seguenti, consigliamo l'uso di pip: 
```bash
pip install colorama
pip install termcolor
pip install json
```

## Utilizzo
Nella cartella della repositiory [GIT](https://github.com/oshodiS/progetto-reti.git) saranno presenti 4 file .py 
* Device.py
* Server.py
* Gateway.py
* Test.py  

Per avviare una simulazione da riga di comando è necessario eseguire il seguente comando:
```bash
python test.py
```

Una volta avviato test.py richiederà in console in quanti secondi si vogliono simulare 24 ore di campionamenti, successivamente istanzia con valori di prova e avvia i thread di Device, Server e Gateway.
Per migliorare la leggibilità della console abbiamo usato 2 colori; Giallo per le informazini di sistema e Blu per l'output del server.

Per terminare la simulazione su console windows è consigliato usate il comando di interruzione ctrl+c.

