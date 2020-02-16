#Boris Giba
#02.09.2018
#MSS 12

import json


#------------------------------------------------
#Model
#------------------------------------------------

class Model(object):

    kurstabelle=open("lkKombinationen.json")
    kurstabelle=kurstabelle.read()
    kurstabelle=json.loads(kurstabelle)
    from faecherListen import (lkTabelle,lkUmgeformteTabelle,lkBasisTabelle,
                          fsnwinf,fsnwinfkf,fs,nw,gw,
                          nichtEindeutigeKurse,
                          abischnittTabelle)

    def __init__(self):
        self.punkteListe=[ [],[],[],[] ]
        self.lks=[]
        self.gks=[]
        self.gkpunkteListe=[]
        self.lkpunkteListe=[]
        self.checkListe=[ ["D",False], ["FS",False], ["M",False], ["NW",False], ["GW",False], ["FS/NW/INF",False], ["KF",False] ]
        self.gecheckteFächer=[]
        self.eingebrachteKurse=0
        self.ersteFremdsprache=""
        self.ersteNaturwissenschaft=""
        self.inDieRechnungEinzubringendeFeldnummern=[]
        self.übriggebliebenegkpunkte=[]
        self.kursAnzahl=0
        self.kfNurIn12PunkteListe=[]
        self.lksAusgeschrieben=[]
        self.zusätzlicherGK=False
        self.kfNurIn12=False
        self.lkSpeicher=[]
        self.uneindeutigeKursIndexListe=[]
        self.dropDownEinstellung=0
        self.prognose=False


    def kombiNummerFinden(self,lk1,lk2,lk3):
        """

        input: 3 strings (die LKs)
        output: int (die Kombinationsnummer, oder -1, falls nicht gefunden)
        
        """
        if lk1=="SK" or lk1=="EK" or lk1=="G":
            lk1="GW"
        if lk2=="SK" or lk2=="EK" or lk2=="G":
            lk2="GW"
        if lk3=="SK" or lk3=="EK" or lk3=="G":
            lk3="GW"
        gesuchteNummer=-1
        for bandNummer,gesamtKurse in self.kurstabelle.items():
            for kursArt, kurse in gesamtKurse.items():
                if len(kurse)==3:
                    if lk1 in kurse and lk2 in kurse and lk3 in kurse:

                        if lk1 != lk2 and lk1 != lk3 and lk2 != lk3:
                            gesuchteNummer=bandNummer

                        else:
                            
                            kopie=kurse[:]
                            kopie.remove(lk1)
                                         
                            if lk2 in kopie:
                                kopie.remove(lk2)
                                
                                if lk3 in kopie:
                                    kopie.remove(lk3)
                                    gesuchteNummer=bandNummer
        return gesuchteNummer


    def getGks(self,kombiNummer):
        """

        input: int (Kombinationsnummer)
        output: list of str (Grundkurse der jeweiligen Kombination)
        
        """
        gks=-1
        
        try:
            gks=self.kurstabelle[kombiNummer]["gks"]
            
        except KeyError:
            gks=-1
           
        return gks

    def abiSchnittZusammenstellen(self,facharbeit,block2):
        """

        input: zwei ints (Facharbeitsnote,Punkte in Block2)
        output: int (Gesamtpunktzahl (final))
    
        """
        block1punkte=0
        gkpunkte=0
        lkpunkte=self.lkPunkteBerechnenNEU()
        
        for i in self.gkpunkteListe:
            if i!="":
                gkpunkte+=int(i)


        block1punkte+= lkpunkte
        block1punkte+= gkpunkte
        try:
            facharbeit=int(facharbeit)
            if facharbeit<16 and facharbeit>=0:
                block1punkte+=facharbeit
        except ValueError:
            pass


        if len(self.kfNurIn12PunkteListe)==2:
            block1punkte+=int(self.kfNurIn12PunkteListe[0])
            block1punkte+=int(self.kfNurIn12PunkteListe[1])



        block1punkte= block1punkte / 44
        block1punkte= block1punkte * 40

        block2punkte=0
        for i in block2:
            block2punkte+=int(i)

        block2punkte*=5

        gesamtpunkte=block1punkte+block2punkte

        return gesamtpunkte

    def lkPunkteBerechnenNEU(self):
        """

        output: int (Gesamtpunktzahl der LKs)

        """
        lk1punkte=int(self.lkpunkteListe[0])+int(self.lkpunkteListe[1])+int(self.lkpunkteListe[2])+int(self.lkpunkteListe[3])
        lk2punkte=int(self.lkpunkteListe[4])+int(self.lkpunkteListe[5])+int(self.lkpunkteListe[2])+int(self.lkpunkteListe[6])
        lk3punkte=int(self.lkpunkteListe[7])+int(self.lkpunkteListe[1])+int(self.lkpunkteListe[8])+int(self.lkpunkteListe[9])

        gesamtpunkteListe=[lk1punkte,lk2punkte,lk3punkte]
        gesamtpunkteListe.remove(min(gesamtpunkteListe))

        if not lk1punkte in gesamtpunkteListe:
            lk2punkte*=2
            lk3punkte*=2
        elif not lk2punkte in gesamtpunkteListe:
            lk1punkte*=2
            lk3punkte*=2
        else:
            lk1punkte*=2
            lk2punkte*=2

        gesamtpunkteListe=[lk1punkte,lk2punkte,lk3punkte]
        
        gesamtpunkte=0
        for i in gesamtpunkteListe:
            gesamtpunkte+=int(i)
        
        return gesamtpunkte

    def abischnittUmwandeln(self,punkte):
        """
        
        input: int (Rohpunkte)
        output: int (Abiturschnitt)
            
        """
        schnitt=""
        punkte=round(punkte,0)
        
        if punkte<300:
            schnitt="nicht bestanden"
        else:
            for i in self.abischnittTabelle:
                if punkte<=i[0] and punkte>=i[1]:
                    schnitt=i[2]
        return schnitt


    def getDropDownAuswahlListe(self,fach):
        """

        input: str (Fachbezeichnung, z.B. Naturwissenschaft)
        output: list (alle Fächer dieser Bezeichnung, z.B. [Physik,Chemie,Biologie])

        """
        
        auswahl=[]
        
        if fach=="FS/NW/INF/KF":
            auswahl=self.fsnwinfkf[:]
        elif fach=="FS/NW/INF":
            auswahl=self.fsnwinf[:]
        elif fach=="Fremdsprache":
            auswahl=self.fs[:]
        elif fach=="Naturwissenschaft":
            auswahl=self.nw[:]
        elif fach=="Gesells.wissenschaft":
            auswahl=self.gw[:]
        elif fach=="Künstlerisches Fach":
            auswahl=["Bildende Kunst","Musik"]
        elif fach=="Religion/Ethik":
            auswahl=["Katholische Religion","Evangelische Religion","Ethik"]

        return auswahl


        
