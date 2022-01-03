# physik_schaltkreise
Ein "simmulationsprogramm" um die Fehlenden Werte einer Schaltung aus Widerständen mithilfe des Omschen Gesetztes, der Ketten- und Machenregel zu berechnen.

Die Projektseite ist hier: https://ln.topdf.de/physik/

Die Datei, die die Schaltkreise beschreibt, muss wievolgt aufgebaut sein:
```
// Eingerückt wird mit tab oder 4 leerzeichen
//
// Typ:
// R/r = resistor
// S/s = series connection
// P/p = parallel
//
//
// {name}, {Typ}
//     U: {Spannung}
//     R: {Widerstand}
//     I: {Stromstärke}
// {namen aller zugehörigen Komponenten getrennt von einem Umbruch}
//
Uges, S
  U: 5
  R: -1
  I: 3
U123
U5
U6

U123, P
U1
U2
U3
```
