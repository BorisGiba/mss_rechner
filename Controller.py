#Boris Giba
#02.09.2018
#MSS 12

from tkinter import *
from View import *
from Model import *


#------------------------------------------------
#Controller
#------------------------------------------------

class Controller(object):

    def __init__(self,model,view):
        self.m=model
        self.v=view
        self.ursprungswert=0
        self.abgezogeneKurse=0

    def getDropDownEinstellung(self):
        """

        Aktualisiert DropDown-Menü-Einstellungen.
        
        """
        
        try:
            self.m.dropDownEinstellung=self.v.dropDownStartCheckVar.get()
            
        #falls die Einstellungen unberührt blieben:
            
        except AttributeError:
            self.m.dropDownEinstellung=1
        
        self.v.dropDownEinstellung=self.m.dropDownEinstellung

    def getPunkteNEU(self):
        """

        Erfasst alle eingetragenen Punkte und speichert sie in einer Variablen (Model) ab.
        
        """
        
        self.m.gkpunkteListe=[]
        self.m.lkpunkteListe=[]
        inDieRechnungEinzubringendeMerknummern=[]
        kursAnzahlListe=[]
        entfernListe=[]
        vierKurse=[]
        
        
        for i in self.m.inDieRechnungEinzubringendeFeldnummern:
            inDieRechnungEinzubringendeMerknummern.append(i[0])
            
        for i in inDieRechnungEinzubringendeMerknummern:
            for j in self.v.pfListenListe:
                self.m.gkpunkteListe.append(j[i].punkte.get())

        for i in self.m.gkpunkteListe[:12]:
            self.m.lkpunkteListe.append(i)
            self.m.gkpunkteListe.remove(i)

        for i in self.m.inDieRechnungEinzubringendeFeldnummern[3:]:
            kursAnzahlListe.append(i[1])
            entfernListe.append(i[0])

        for i in kursAnzahlListe:
            index=kursAnzahlListe.index(i)
            gklisteKopie=self.m.gkpunkteListe[:]
            if i!=4:
                löschindex=0
                for j in self.m.inDieRechnungEinzubringendeFeldnummern:
                    if j[1]==i:
                        löschindex=self.m.inDieRechnungEinzubringendeFeldnummern.index(j)
                        self.m.inDieRechnungEinzubringendeFeldnummern.pop(löschindex)
                
                zähler=4*index-self.abgezogeneKurse

                while zähler>0:
                    gklisteKopie.pop(0)
                    zähler-=1
                if self.ursprungswert==0:
                    self.ursprungswert=1
                    vierKurse=[gklisteKopie[0],gklisteKopie[1],gklisteKopie[2],gklisteKopie[3]]
                else:
                    länge=len(gklisteKopie)
                    vierKurse=[gklisteKopie[länge-1],gklisteKopie[länge-2],gklisteKopie[länge-3],gklisteKopie[länge-4]]
                    
                    

                zähler2=i
                
                while zähler2<4:
                    self.m.gkpunkteListe.remove(min(vierKurse))
                    vierKurse.remove(min(vierKurse))
                    zähler2+=1

                    
                self.abgezogeneKurse+=4-i
                
        if len(self.m.übriggebliebenegkpunkte)==0:
            self.m.übriggebliebenegkpunkte=vierKurse

        elif len(self.m.übriggebliebenegkpunkte)!=0:
            for i in self.m.übriggebliebenegkpunkte:
                self.m.gkpunkteListe.append(i)


    def getStartLks(self):
        lks=[]
        lks.append(self.v.lk1.kurs.get().strip("\n"))
        lks.append(self.v.lk2.kurs.get().strip("\n"))
        lks.append(self.v.lk3.kurs.get().strip("\n"))

        self.m.lkSpeicher=lks
        
        return lks

    def lksUmschreiben(self):
        """

        Schreibt die LKs um.
        Bsp. :
        -'Mathematik' wird zu 'M'
        -'Informatik' zu 'INF'
        -'Englisch' zu 'FS'
        -'Chemie' zu 'NW'
        
        """
        eintrag1=self.v.lk1DropDownMenü.var.get()
        eintrag2=self.v.lk2DropDownMenü.var.get()
        eintrag3=self.v.lk3DropDownMenü.var.get()
        self.v.lk1.kurs.delete(0,END)
        self.v.lk1.kurs.insert(END,eintrag1)
        self.v.lk2.kurs.delete(0,END)
        self.v.lk2.kurs.insert(END,eintrag2)
        self.v.lk3.kurs.delete(0,END)
        self.v.lk3.kurs.insert(END,eintrag3)
        
        
        self.m.lks=self.getStartLks()
        korrekteEingabe=True

        for j in self.m.lks:
            if not j.strip("\n") in self.m.lkTabelle:
                korrekteEingabe=False

        if korrekteEingabe:
            for i in self.m.lks:
                self.m.lks[self.m.lks.index(i)] = self.m.lkUmgeformteTabelle[self.m.lkTabelle.index(i)]
        else:
            fehlermeldung=Meldung(self.v)
            fehler=Label(fehlermeldung,
                          bg="red",
                          text=("es liegt ein Fehler vor,bitte überprüfe deine Eingabe"))
            fehler.place(x=15,y=30)
                

                
        if korrekteEingabe:
            self.genaueAuswahlEinleiten()
        return self.m.lks

    def lksAuschreiben(self,lks):
        """

        Schreibt die übergebenen Kurse aus.
        Bsp.:
        -'D' wird zu 'Deutsch'
        -'NW' zu 'Naturwissenschaft'
        -'FS' zu 'Fremdsprache'
        
            
        """
        for i in lks:
            if i in self.m.lkUmgeformteTabelle:
                lks[lks.index(i)]=self.m.lkBasisTabelle[self.m.lkUmgeformteTabelle.index(i)]

        return lks
        


    def genaueAuswahlEinleiten(self):
        """

        Beschreibt die ersten Vorgänge,
        die nach der LK-Auswahl geschehen.
        d.h. generiert beispielsweise Textfelder und Dropdown-Menüs
        
        """
        self.m.lksAusgeschrieben=self.getStartLks()
        kombiNummer=self.m.kombiNummerFinden(self.m.lks[0],self.m.lks[1],self.m.lks[2])
        self.m.gks=self.m.getGks(kombiNummer)
            
        for i in self.m.lksAusgeschrieben:
            kopie=self.m.lksAusgeschrieben[:]
            kopie.remove(i)
            if i in kopie:
                self.m.gks=-1

        if self.m.gks==-1:
            fehlerMeldung=Meldung(self.v)
            fehler=Label(fehlerMeldung,
                      bg="red",
                      text="ungültige Kurskombination")
            fehler.place(x=75,y=30)
                 
        elif self.m.gks!=-1:
            self.getDropDownEinstellung()
            self.v.destroy()
            self.v=View(self.m.dropDownEinstellung)
            self.v.abstandEinstellen()
            self.v.configure(background=self.v.farbe)
            if self.m.dropDownEinstellung==0:
                self.v.geometry("640x480")
            else:
                self.v.geometry("680x620")
            self.v.kursfelderGenerieren()
            self.v.punktfelderGenerieren()
            self.v.punkteButtonGenerieren(self.genauereKursauswahl)
            self.v.kursCheckButtonsGenerieren()
            self.v.hilfeButtonGenerieren()
            self.v.einstellungsButtonGenerieren()
            
            self.punktFelderAusschalten()
            self.checkButtonsAusschalten()
            self.lksEintragen()
            self.gksEintragen()
            self.checkButtonsEinrichten()
            self.textFelderAnschalten()
            self.textFelderAusschalten()
            if self.m.dropDownEinstellung==1:
                self.dropDownsAktualisieren(self.dropDownCallBack)
                self.dropDownsAusschalten()
                        
    def lksEintragen(self):
        """

        Trägt die LKs in die LK-Felder ein.
        
        """
        self.v.kfListenListe[0].text.delete(1.0,END)
        self.v.kfListenListe[1].text.delete(1.0,END)
        self.v.kfListenListe[2].text.delete(1.0,END)
        self.v.kfListenListe[0].text.insert(END,self.m.lksAusgeschrieben[0])
        self.v.kfListenListe[0].text.configure(state="disabled")
        self.v.kfListenListe[1].text.insert(END,self.m.lksAusgeschrieben[1])
        self.v.kfListenListe[1].text.configure(state="disabled")
        self.v.kfListenListe[2].text.insert(END,self.m.lksAusgeschrieben[2])
        self.v.kfListenListe[2].text.configure(state="disabled")


    def gksEintragen(self):
        """

        Trägt die GKs in die GK-Felder ein.
        
        """

        self.m.gks=self.lksAuschreiben(self.m.gks)
        j=0
        for i in self.v.kfListenListe:
            if self.v.kfListenListe.index(i)>2 and self.v.kfListenListe.index(i)<10:
                i.text.delete(1.0,END)
                i.text.insert(END,self.m.gks[j])
                j+=1
            
        
    def checkButtonsZurücksetzen(self):
        for i in self.v.checkButtonListe:
            i.var.set(0)
        
    def checkButtonsEinrichten(self):
        """

        Setzt die Status der Checkbuttons (zum Bsp. werden Mathematik und Deutsch immer
        ausgewählt).
        
        """
        self.v.checkButtonListe[0].var.set(1)
        self.v.checkButtonListe[1].var.set(1)
        self.v.checkButtonListe[2].var.set(1)
        for i in self.v.checkButtonListe:
            i.box.configure(state="disabled")
        for i in self.v.kfListenListe[3:]:
            listenIndex = self.v.kfListenListe.index(i)
            if i.text.get("1.0", END) == "Mathematik\n" or i.text.get("1.0", END) == "Deutsch\n":
                self.v.checkButtonListe[listenIndex].var.set(1)
                self.v.checkButtonListe[listenIndex].box.configure(state="disabled")


    def textFelderAnschalten(self):
        for i in self.v.kfListenListe[3:]:
            if self.v.kfListenListe.index(i)!=len(self.v.kfListenListe)-1:
                if i.text.get("1.0",END)!= "Mathematik\n" and i.text.get("1.0",END)!="Deutsch\n" and i.text.get("1.0",END)!="Erdkunde/Sozialkunde\n" and i.text.get("1.0",END) in self.m.nichtEindeutigeKurse:
                    i.text.configure(state="normal")
                    i.text.configure(bg="white")
                    i.text.configure(fg="black")

        zwischenspeicher=self.lksAuschreiben(self.m.gks)
        j=0
        for i in self.v.kfListenListe:
            if self.v.kfListenListe.index(i)>2 and self.v.kfListenListe.index(i)<10:
                if self.m.gks[j].strip("\n") in self.m.nichtEindeutigeKurse:
                    i.text.configure(state="normal")
                    i.text.configure(bg="orange")
                    i.text.configure(fg="black")
                    if not self.v.kfListenListe.index(i) in self.m.uneindeutigeKursIndexListe:
                        self.m.uneindeutigeKursIndexListe.append(self.v.kfListenListe.index(i))
                j+=1
                    

    def textFelderAusschalten(self):
        for i in self.v.kfListenListe[3:]:
            i.text.configure(bg=self.v.ausgeschalteteFarbe)
            i.text.configure(state="disabled")
            i.text.configure(fg="white")

    def punktFelderAnschalten(self):
        for i in self.v.pfListenListe:

            if self.m.zusätzlicherGK:
                for j in i:
                    j.punkte.configure(state="normal")
                    j.punkte.configure(fg="black")
                    
                    if i.index(j)<3:
                        j.punkte.configure(bg=self.v.nebenFarbe)
                    else:
                        j.punkte.configure(bg="white")
            else:
                for j in i:
                    if not i.index(j)==len(i)-1:
                        j.punkte.configure(state="normal")
                        j.punkte.configure(fg="black")
                        
                        if i.index(j)<3:
                            j.punkte.configure(bg=self.v.nebenFarbe)
                        else:
                            j.punkte.configure(bg="white")

    def punktFelderAusschalten(self):
        for i in self.v.pfListenListe:
            for j in i:
                j.punkte.configure(fg="white")
                j.punkte.configure(state="disabled")

    def checkButtonsAnschalten(self):
        for i in self.v.checkButtonListe[3:]:
            
            listenIndex=self.v.checkButtonListe.index(i)
            
            if self.v.kfListenListe[listenIndex].text.get("1.0",END)!= "Mathematik\n" and self.v.kfListenListe[listenIndex].text.get("1.0",END)!="Deutsch\n" and self.v.kfListenListe[listenIndex].text.get("1.0",END)!="zusätzlicher GK\n":        
                i.box.configure(state="normal")
            

    def checkButtonsAusschalten(self):
        for i in self.v.checkButtonListe[3:]:
            i.box.configure(state="disabled")

    def dropDownsAusschalten(self):
        for i in self.v.dropDownMenüListe:
            i.configure(state="disabled")
            i.configure(bg=self.v.ausgeschalteteFarbe)
            i.configure(fg="white")

    def dropDownsAnschalten(self):
        for i in self.v.dropDownMenüListe:
            i.configure(state="normal")
            i.configure(bg="#4d3626")
            i.configure(fg="white")

    def dropDownsLöschen(self):
        for i in self.v.dropDownMenüListe:
            i.place_forget()
        
        

    def genauereKursauswahl(self):
        """

        leitet die Auswahl der weiteren GKs ein
        
        """
        if self.m.dropDownEinstellung==0:
            self.v.kursAuswahlHilfe(self.v)

        self.textFelderAnschalten()
        if self.m.dropDownEinstellung==1:
            self.dropDownsAnschalten()


        self.v.knopf.configure(text="weiter")
        self.v.knopf.configure(command=self.zusätzlichesFachEinleiten)

    def dropDownKurseInTextFelderEintragen(self):
        """
        Trägt die ausgewählten Kurse aus den Dropdowns in die Textfelder ein.
        """
        for i in self.v.dropDownMenüListe:
            index=i.kfIndex
            eintrag=i.var.get()
            self.v.kfListenListe[index].text.delete(0.0,END)
            self.v.kfListenListe[index].text.insert(END,eintrag)


    def kursKontrolle(self):
        """

        Kontrolliert die eingegebenen/ausgewählten Kurse.
        
        """
        vergleichsliste=[]
        duplikatenVergleichsListe=[]
        fehler=""
        
        korrekteEingabe=True

        for i in self.v.kfListenListe[3:]:
            if not self.v.kfListenListe.index(i) in self.m.nichtEindeutigeKurse and not self.m.dropDownEinstellung==1:
                fachindex=self.v.kfListenListe.index(i)
                kfListenLänge=len(self.v.kfListenListe)-1
                fach=i.text.get("1.0",END).strip("\n")

                
                if fach in self.m.lkTabelle  and fach!="zusätzlicher GK" and fachindex!=kfListenLänge-1:
                    listenIndex=self.m.lkTabelle.index(fach)
                    if self.m.lkBasisTabelle[listenIndex].strip("\n")=="Gesells.wissenschaft":
                        vergleichsliste.append(fach)
                    else:
                        vergleichsliste.append(self.m.lkBasisTabelle[listenIndex])
                        
                elif fach!="zusätzlicher GK" and fachindex!=kfListenLänge-1:
                    korrekteEingabe=False
                    fehler=fach
            

        for i in vergleichsliste:
            vergleichsIndex=vergleichsliste.index(i)
            
            if i==self.m.gks[vergleichsIndex] or self.m.gks[vergleichsIndex]=="Gesells.wissenschaft":
                pass
            elif self.m.gks[vergleichsIndex].strip("\n")=="FS/NW/INF":
                if i in self.m.fsnwinf:
                    pass
            elif self.m.gks[vergleichsIndex].strip("\n")=="FS/NW/INF/KF":
                if i in self.m.fsnwinfkf:
                    pass
            else:
                korrekteEingabe=False
                fehler="ungültige Eingabe eines Faches"


        for i in self.v.kfListenListe:
            if not self.v.kfListenListe.index(i) in self.m.uneindeutigeKursIndexListe:
                duplikatenVergleichsListe.append(i.text.get("1.0",END).strip("\n"))



        if self.m.dropDownEinstellung==1:
            for j in self.v.dropDownMenüListe:
                duplikatenVergleichsListe.append(j.var.get())
                
        for i in duplikatenVergleichsListe:
            kopie=duplikatenVergleichsListe[:]
            kopie.remove(i)

            if i in kopie:

                korrekteEingabe=False
                fehler="Ein Fach ist mehrfach enthalten",i


        if korrekteEingabe and self.m.dropDownEinstellung==1:
            self.dropDownKurseInTextFelderEintragen()


        if korrekteEingabe:
            alleKurse=[]
            for i in self.v.kfListenListe:
                alleKurse.append((i.text.get("1.0",END)).strip("\n"))

            nw=False
            for j in alleKurse:
                if j in self.m.nw:
                    alleKurse.remove(j)
                    nw=True
                    
            if not nw:
                korrekteEingabe=False
                fehler="Es fehlt eine Naturwissenschaft"


            fs=False
            for j in alleKurse:
                if j in self.m.fs:
                    alleKurse.remove(j)
                    fs=True

            if not fs:
                korrekteEingabe=False
                fehler="Es fehlt eine Fremdsprache"

            
                
        return [korrekteEingabe,fehler]

    def dropDownCallBack(self,auswahl):
        pass

    def dropDownMenüAuswahlFestlegen(self):
        """

        Legt die Kurse fest, die in den Drop-Down-Menüs ausgewählt werden können.
        
        """
        kickListe=[]

        alleAuswahlen=[]
        for i in self.m.uneindeutigeKursIndexListe:
            alleAuswahlen.append([""])

            
        auswahl=[self.m.lks+self.m.gks]

        lkListe=[]

        lkzähler=2

        while lkzähler>=0:
            lk=(self.v.kfListenListe[lkzähler].text.get("1.0",END)).strip("\n")
            lkListe.append(lk)
            lkzähler-=1


        zähler=0
        
        for j in self.v.kfListenListe:
            eintrag=(j.text.get("1.0",END)).strip("\n")

            
            if eintrag in self.m.nichtEindeutigeKurse:
                auswahl=self.m.getDropDownAuswahlListe(eintrag)
                for k in auswahl:
                    if not eintrag in self.m.nichtEindeutigeKurse:
                        auswahl.remove(k)

                for k in lkListe:
                    if k in auswahl:
                        auswahl.remove(k)
                alleAuswahlen[zähler]=auswahl
                zähler+=1

            if eintrag=="Sozialkunde":
                kickListe.append("Erdkunde/Sozialkunde")
                kickListe.append("Erdkunde")
                                 
            elif eintrag=="Erdkunde":
                kickListe.append("Erdkunde/Sozialkunde")
                kickListe.append("Sozialkunde")
                
            elif eintrag=="Geschichte":
                kickListe.append("Sozialkunde")
                kickListe.append("Erdkunde")
                
            elif eintrag=="Mathematik":
                kickListe.append("Mathematik")

            elif eintrag=="Deutsch":
                kickListe.append("Deutsch")

                

        for l in alleAuswahlen:
            for m in kickListe:
                if m in l:
                    l.remove(m)
             
        return alleAuswahlen

    def dropDownsAktualisieren(self,cbBefehl):
        alleAuswahlen=self.dropDownMenüAuswahlFestlegen()
        self.v.dropDownMenüsGenerieren(self.m.uneindeutigeKursIndexListe,alleAuswahlen,cbBefehl)


    def zusätzlichesFachEinleiten(self):
        kontrolle=self.kursKontrolle()
        if kontrolle[0]:
            if self.m.dropDownEinstellung==1:
                self.dropDownsAusschalten()
            for i in self.v.kfListenListe:
                self.textFelderAusschalten()
            meldungsfenster=Meldung(self.v,"nein")
            meldungsfenster.geometry("300x150")
            meldungsfenster.title("Aufforderung")
            meldung=Label(meldungsfenster,
                                  bg=self.v.nebenFarbe,
                                  font=self.v.verd,
                                  text=("hast du ein zusätzliches freiwilliges Fach?"))
            meldung.place(x=10,y=30)
            antwortknopf1=Button(meldungsfenster,
                                 text="ja, ich trage es nun ein",
                                 bg="#b48768",
                                 fg="white",
                                 font=self.v.verd,
                                 command=lambda:[self.zusätzlichesFachEintragen(),meldungsfenster.destroy()])
            antwortknopf2=Button(meldungsfenster,
                                 text="nein",
                                 bg="#b48768",
                                 fg="white",
                                 font=self.v.verd,
                                 command=lambda:[self.zusätzlichesFachVerwerfen(),meldungsfenster.destroy()])
            antwortknopf1.place(x=25,y=80)
            antwortknopf2.place(x=230,y=80)
            

        else:
            fehlermeldung=Meldung(self.v)
            fehlermeldung.geometry("400x125")
            fehler=Label(fehlermeldung,
                      bg="red",
                      text=("es liegt ein Fehler vor:",kontrolle[1]))
            fehler.place(x=15,y=30)


            
    def zusätzlichesFachEintragen(self):
        self.m.zusätzlicherGK=True

        self.v.kfListenListe[10].text.configure(state="normal")
        self.v.kfListenListe[10].text.configure(bg="white")
        self.v.kfListenListe[10].text.configure(fg="black")

        if self.m.dropDownEinstellung==1:
            self.dropDownsAusschalten()
            
            auswahl=self.m.lkTabelle[:]
            auswahl.remove("Katholische Religion")
            auswahl.remove("Evangelische Religion")
            auswahl.remove("Ethik")
            
            eigeneFächer=[]
            
            for i in self.v.kfListenListe:
                fach=(i.text.get("1.0",END)).strip("\n")
                eigeneFächer.append(fach)
                
                for j in auswahl:
                    auswahl[auswahl.index(j)]=j.strip(" ")
                if fach in auswahl:
                    auswahl.remove(fach)

            for i in eigeneFächer:
                if i in auswahl:
                    auswahl.remove(i)
                    
            if "Erdkunde/Sozialkunde" in eigeneFächer:
                auswahl.remove("Erdkunde")
                auswahl.remove("Sozialkunde")
                
            if "Sozialkunde" in eigeneFächer:
               auswahl.remove("Erdkunde")
               auswahl.remove("Erdkunde/Sozialkunde")

            if "Erdkunde" in eigeneFächer:
                auswahl.remove("Sozialkunde")
                auswahl.remove("Erdkunde/Sozialkunde")
                      
            self.v.zusätzlichesDropDownMenüGenerieren(auswahl)
            
        self.v.knopf.configure(text="zusätzliches Fach bestätigen")
        self.v.knopf.configure(command=self.zusätzlichesFachKontrollieren)

    def zusätzlichesFachVerwerfen(self):
        self.m.zusätzlicherGK=False
        self.v.kfListenListe[len(self.v.kfListenListe)-1].text.configure(state="disabled")
        self.v.knopf.configure(text="weiter")
        self.v.knopf.configure(command=self.punkteEintragen)
        self.v.pfListenListe[0][-1].configure(state="normal")
        

    def zusätzlichesFachKontrollieren(self):
        korrekteEingabe=True

        if self.m.dropDownEinstellung==1:
            zusätzlichesFach=self.v.zusätzlichesDropDownMenü.var.get()
            self.v.kfListenListe[10].text.configure(state="normal")
            self.v.kfListenListe[10].text.delete("1.0",END)
            self.v.kfListenListe[10].text.insert(END,zusätzlichesFach)
            self.v.kfListenListe[10].text.configure(state="disabled")
            
        for i in self.v.kfListenListe[:10]:
            if (
                self.v.kfListenListe[-1].text.get("1.0",END).strip("\n") == i.text.get("1.0",END) or
                self.v.kfListenListe[-1].text.get("1.0",END).strip("\n") not in self.m.lkTabelle
                ):
                        korrekteEingabe=False

            else:
                self.v.kfListenListe[-1].text.configure(state="disabled")
                self.v.knopf.configure(text="weiter")
                self.v.knopf.configure(command=self.punkteEintragen)
                if self.m.dropDownEinstellung==1:
                    self.v.zusätzlichesDropDownMenü.configure(state="disabled")
                    self.v.zusätzlichesDropDownMenü.configure(bg=self.v.ausgeschalteteFarbe)
                    self.v.zusätzlichesDropDownMenü["menu"].configure(fg="white")
                
        if not korrekteEingabe:
                        meldungsfenster=Meldung(self.v)
                        meldung=Label(meldungsfenster,
                                  bg="#b20000",
                                  text=("ungültiges Fach,Feld wurde zurückgesetzt"))
                        meldung.place(x=15,y=30)
                        self.v.kfListenListe[-1].text.delete(0.0,END)
                        self.v.kfListenListe[-1].text.insert(END,"zusätzlicher GK")
                        self.zusätzlichesFachEinleiten()
                
                    
    def punkteAuffüllen(self,index):
        """

        Wird bei Betätigen des 'Pfeilknopfs' ausgeführt.
        Vervollständigt die jeweilige Reihe an Punkten,
        falls die bisherige Eingabe stimmt.
        
        """
        if self.v.auffüllEinstellung==1:

            viertePunktzahl=self.v.pfListenListe[3][index].punkte.get()
            if viertePunktzahl=="" or not self.intKontrolle(viertePunktzahl):
                überschreibwert=0
                punktzahl=0
                
                drittePunktzahl=self.v.pfListenListe[2][index].punkte.get()
                
                if self.intKontrolle(drittePunktzahl):
                    drittePunktzahl=int(drittePunktzahl)
                    if drittePunktzahl<16 and drittePunktzahl>=0:
                        punktzahl=drittePunktzahl
                        überschreibwert=1
                          
                elif self.intKontrolle(self.v.pfListenListe[1][index].punkte.get()):
                    zweitePunktzahl=self.v.pfListenListe[1][index].punkte.get()
                    zweitePunktzahl=int(zweitePunktzahl)
                    if zweitePunktzahl<16 and zweitePunktzahl>=0:
                        punktzahl=zweitePunktzahl
                        überschreibwert=2
                            

                elif self.intKontrolle(self.v.pfListenListe[0][index].punkte.get()):
                    erstePunktzahl=self.v.pfListenListe[0][index].punkte.get()
                    erstePunktzahl=int(erstePunktzahl)
                    if erstePunktzahl<16 and erstePunktzahl>=0:
                        punktzahl=erstePunktzahl
                        überschreibwert=3
                
                if überschreibwert>=1:
                    self.v.pfListenListe[3][index].punkte.delete(0,END)
                    self.v.pfListenListe[3][index].punkte.insert(END,punktzahl)

                if überschreibwert>=2:
                    self.v.pfListenListe[2][index].punkte.delete(0,END)
                    self.v.pfListenListe[2][index].punkte.insert(END,punktzahl)
                    
                if überschreibwert==3:
                    self.v.pfListenListe[1][index].punkte.delete(0,END)
                    self.v.pfListenListe[1][index].punkte.insert(END,punktzahl)
        else:
            self.punkteAuffüllenSimpel(index)
        
            
    def punkteAuffüllenSimpel(self,index):
        """

        Eine simplere Version der oberen Funktion,
        Schreibt den Wert des ersten Feldes der Reihe in alle anderen Felder der Reihe.
        
        """
        
        erstePunktzahl=self.v.pfListenListe[0][index].punkte.get()
        if len(erstePunktzahl)==1 or len(erstePunktzahl)==2:
            erstePunktzahl=int(erstePunktzahl)
        
        if erstePunktzahl!="" and type(erstePunktzahl)!="str" and erstePunktzahl>=0 and erstePunktzahl<16:
            self.v.pfListenListe[1][index].punkte.delete(0,END)
            self.v.pfListenListe[1][index].punkte.insert(END,erstePunktzahl)
            self.v.pfListenListe[2][index].punkte.delete(0,END)
            self.v.pfListenListe[2][index].punkte.insert(END,erstePunktzahl)
            self.v.pfListenListe[3][index].punkte.delete(0,END)
            self.v.pfListenListe[3][index].punkte.insert(END,erstePunktzahl)
        


        
    def punkteEintragen(self):
        """

        Leitet das Eintragen der Punktzahlen ein.
        
        """
                
        kontrolle=self.kursKontrolle()
        if kontrolle[0]:
            if self.m.dropDownEinstellung==1:
                self.dropDownsLöschen()
                if self.m.zusätzlicherGK:
                    self.v.zusätzlichesDropDownMenü.place_forget()
                
            self.v.punkteAuffüllenButtonsGenerieren(self.punkteAuffüllen)
            self.v.kfListenListe[10].text.configure(state="disabled")
            self.v.kfListenListe[10].text.configure(bg=self.v.ausgeschalteteFarbe)
            self.v.kfListenListe[10].text.configure(fg="white")
            
            self.punktFelderAnschalten()
            meldungsfenster=Meldung(self.v)
            meldung=Label(meldungsfenster,
                          text="trage nun bitte alle deine erzielten Punkte ein",
                          font="Verdana 9",
                          bg=self.v.nebenFarbe)
            meldung.place(x=2,y=30)
            self.v.knopf.configure(text="Punkte bestätigen",command=self.abiKursAuswahl)

            
        else:
            fehlermeldung=Meldung(self.v)
            fehler=Label(fehlermeldung,
                      bg="#b20000",
                      text=("es liegt ein Fehler vor,"
                            "bitte kontrolliere deine Eingabe"))
            fehler.place(x=15,y=30)
            


    def punkteKontrolle(self):
        """
        
        Kontrolliert die eingetragenen Punkte.
        
        """
        korrekteEingabe=True
        
        for i in self.v.pfListenListe:
            for j in i:
                
                state = str(j.punkte["state"])
                if state!="disabled":
                    if self.intKontrolle(j.punkte.get()):
                        if int( j.punkte.get() ) >15:
                            korrekteEingabe=False
                            
                    elif not self.intKontrolle(j.punkte.get()) and not j.punkte.get()=="":
                        korrekteEingabe=False
                            
                if self.v.pfListenListe.index(i)==0:
                    if state!="disabled":
                        if j.punkte.get()=="" or not self.intKontrolle(j.punkte.get()):
                            korrekteEingabe=False

        for i in self.v.pfListenListe:
            for j in i[:3]:
                if j.punkte.get()=="0":
                    korrekteEingabe=False
                
                            
        if korrekteEingabe:
            for i in self.v.pfListenListe:
                for j in i:
                    if (j.punkte.get()).strip("\n")=="" and not self.m.prognose and korrekteEingabe and j.punkte["state"]!="disabled":
                                
                        if self.v.prognoseEinstellung==1 and not self.m.prognose:
                            if not self.prognose():
                                korrekteEingabe=False
                            else:
                                prognoseAbfrage=Meldung(self.v,button="nein",schließschutz="ja")
                                prognoseAbfrageText=Label(prognoseAbfrage,
                                                          bg="light blue",
                                                          text=("Es wurden nicht alle Punkte eingetragen.\n"
                                                                "Eine Prognose wird generiert."))
                                prognoseAbfrageText.place(x=30,y=30)
                                prognoseAbfrageBestätigungsKnopf=Button(prognoseAbfrage,
                                                                        text="ok!",
                                                                        font=self.v.verd,
                                                                        bg="#ae7d5b",
                                                                        fg="white",
                                                                        command= lambda : [self.setPrognose(1) , prognoseAbfrage.destroy()])
                                prognoseAbfrageAblehnKnopf=Button(prognoseAbfrage,
                                                                  text="nein,zurück zur Eingabe",
                                                                  font=self.v.verd,
                                                                  bg="#ae7d5b",
                                                                  fg="white",
                                                                  command= lambda : prognoseAbfrage.destroy())
                                        
                                prognoseAbfrageBestätigungsKnopf.place(x=35,y=80)
                                prognoseAbfrageAblehnKnopf.place(x=85,y=80)

                                self.v.wait_window(prognoseAbfrage)
                                
                                if self.m.prognose==1:
                                    self.prognose()
                                    self.v.prognoseTextHinzufügen()

                                else:

                                    korrekteEingabe=False
                                                                                                  

        return korrekteEingabe
        
    def prognose(self):
        """

        Erstellt eine Prognose der Noten,
        falls nicht alle Noten eingetragen wurden.
        Die restlichen Punktfelder werden gefüllt,
        falls kein Fehler in der Eingabe vorliegt.
        
        """
        korrekteEingabe=True
        aufzufüllendeListenIndizes=[]
        for i in self.v.pfListenListe:
            leer=False
            for j in i:
                if (j.punkte.get()).strip(" ") == "":
                    leer=True
                if leer:
                    if not i.index(j) in aufzufüllendeListenIndizes:
                        aufzufüllendeListenIndizes.append(i.index(j))
                        
        if self.m.zusätzlicherGK:
            reichweite=range(0,11)
        else:
            reichweite=range(0,10)
            
        for i in reichweite:
            for j in self.v.pfListenListe:
                
                ersterIndex=self.v.pfListenListe.index(j)
                zweiterIndex=i

                if ersterIndex==0:
                    ersterIndex=1
                


                punkte1=self.v.pfListenListe[ersterIndex][zweiterIndex].punkte.get()
                punkte2=self.v.pfListenListe[ersterIndex-1][zweiterIndex].punkte.get()


                kontrolle1=[ self.intKontrolle(punkte1) , punkte1=="" ]
                kontrolle2=[ self.intKontrolle(punkte2) ,punkte2=="" ]

                if (kontrolle1[0] and not kontrolle2[0]) or (not kontrolle1[1] and kontrolle2[1]):
                    korrekteEingabe=False
                

        if korrekteEingabe and self.m.prognose:

            if self.v.auffüllEinstellung==0:
                for i in aufzufüllendeListenIndizes:
                    self.punkteAuffüllenSimpel(i)

            else:
                for i in aufzufüllendeListenIndizes:
                    self.punkteAuffüllen(i)
        

        return korrekteEingabe
            
                

    def setPrognoseEinstellung(self,wert):
        self.v.prognoseEinstellung=wert


    def setPrognose(self,wert):
        self.m.prognose=wert
    

    def abiKursAuswahl(self):
        """

        Leitet das Auswählen der Kurse ein,
        die in die Abiturnote miteingehen sollen.

        """
            
        if self.punkteKontrolle():
            self.v.einstellungsBlock=1
            if not self.m.prognose:
                text=("bitte wählen Sie nun die zu wertenden Kurse aus.")
            elif self.m.prognose:
                text=("bitte wählen Sie nun die zu wertenden Kurse aus.\n"
                      "Die Prognosefunktion wurde aktiviert.")
                
            self.punktFelderAusschalten()
            self.checkButtonsAnschalten()
            meldungsfenster=Meldung(self.v)
            meldung=Label(meldungsfenster,
                          text=text,
                          bg=self.v.nebenFarbe)
            meldung.place(x=20,y=30)
            self.v.knopf.configure(text="Kurse bestätigen",
                                        command=self.berechnungEinleiten)
        else:
            fehlermeldung=Meldung(self.v)
            fehlermeldung.geometry("320x140")
            fehlermeldung.schließKnopf.place(x=120,y=100)
            fehler=Label(fehlermeldung,
                         bg="red",
                         text=("es liegt ein Fehler vor,\n"
                            "bitte kontrolliere deine Eingabe.\n"
                            "Es müssen mindestens die Noten von 11/1\n"
                            "eingetragen werden.\n"
                            "Die Punkte müssen zwischen 0 und 15 liegen\n"
                            "Ein LK-Kurs darf nie 0 Punkte haben."))
            fehler.place(x=35,y=0)
            

    def abiKursKontrolle(self):
        """

        Kontrolliert die Auswahl der ins Abitur einzubringenden Kurse.
        
        """
        
        eingebrachteKursAnzeige=Entry(self.v,width=10)
        anzeige35=Label(self.v,text="/35",bg=self.v.farbe,fg="white")
        if self.m.dropDownEinstellung==0:
            eingebrachteKursAnzeige.place(x=350,y=450)
            anzeige35.place(x=410,y=450)
        else:
            eingebrachteKursAnzeige.place(x=450,y=585)
            anzeige35.place(x=510,y=585)            
        eingebrachteKurseText=Label(self.v,
                                    text="Anzahl eingebrachter Kurse:",
                                    fg="white",
                                    bg=self.v.farbe,
                                    font="Arial 9")
        if self.m.dropDownEinstellung==0:
            eingebrachteKurseText.place(x=185,y=450)
        else:
            eingebrachteKurseText.place(x=285,y=585)
        korrekteEingabe=True
        eingebrachteKursAnzeige.delete(0,END)
        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
        zurücksetzenKnopf=Button(self.v,
                                 font=self.v.verd,
                                 text="zurücksetzen",
                                 command=self.kursWahlZurücksetzen,
                                 bg="#b48768",
                                 fg="white")
        if self.m.dropDownEinstellung==0:
            zurücksetzenKnopf.place(x=480,y=450)
        else:
            zurücksetzenKnopf.place(x=565,y=580)
    

        
        for j in self.m.checkListe:
            for i in self.v.kfListenListe:
                listenIndex=self.v.kfListenListe.index(i)
                fach=i.text.get(1.0,END).strip("\n")
                checkFeld=self.v.checkButtonListe[listenIndex].var.get()

                if fach=="Deutsch" and not self.m.checkListe[0][1] and not fach in self.m.gecheckteFächer:
                   if checkFeld==1:
                        self.m.checkListe[0][1]=True
                        self.m.eingebrachteKurse+=4
                        self.m.gecheckteFächer.append(fach)
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,4])

                        
                if fach in self.m.fs and not self.m.checkListe[1][1] and not fach in self.m.gecheckteFächer:
                    if checkFeld==1:
                        self.m.checkListe[1][1]=True
                        self.m.ersteFremdsprache=fach
                        self.m.gecheckteFächer.append(fach)
                        self.m.eingebrachteKurse+=4
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,4])
                        
                if fach=="Mathematik" and not self.m.checkListe[2][1] and not fach in self.m.gecheckteFächer:
                    if checkFeld==1:
                        self.m.checkListe[2][1]=True
                        self.m.gecheckteFächer.append(fach)
                        self.m.eingebrachteKurse+=4
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,4])
                        
                elif fach in self.m.nw and not self.m.checkListe[3][1] and not fach in self.m.gecheckteFächer:
                    if checkFeld==1:
                        self.m.checkListe[3][1]=True
                        self.m.ersteNaturwissenschaft=fach
                        self.m.gecheckteFächer.append(fach)
                        self.m.eingebrachteKurse+=4
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,4])
                        
                elif fach in self.m.gw and not self.m.checkListe[4][1] and not fach in self.m.gecheckteFächer:
                    if checkFeld==1:
                        self.m.checkListe[4][1]=True
                        self.m.gecheckteFächer.append(fach)
                        self.m.eingebrachteKurse+=4
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,4])

                elif (fach=="Bildende Kunst" or fach=="Musik" ) and not self.m.checkListe[6][1] and not fach in self.m.gecheckteFächer and not (fach in self.m.lkSpeicher):
                    if checkFeld==1:
                        self.m.checkListe[6][1]=True
                        self.m.gecheckteFächer.append(fach)
                        
                        self.abiKursKontrolleHilfsFunktion(fach)
                        
                        abfrageWert=self.m.kursAnzahl
                        abfrageWert=int(abfrageWert)
                        self.m.eingebrachteKurse+=abfrageWert
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,abfrageWert])



                elif ((fach in self.m.fs and fach!=self.m.ersteFremdsprache)or (fach in self.m.nw  and fach!=self.m.ersteNaturwissenschaft) or (fach=="Informatik")) and not (fach in self.m.gecheckteFächer) and not (self.m.checkListe[5][1]) and not (fach in self.m.lkSpeicher):
                    if checkFeld==1:
                        self.m.checkListe[5][1]=True
                        self.m.gecheckteFächer.append(fach)
                        
                        self.abiKursKontrolleHilfsFunktion(fach)
                        
                        abfrageWert=self.m.kursAnzahl
                        abfrageWert=int(abfrageWert)
                        self.m.eingebrachteKurse+=abfrageWert
                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,abfrageWert])

                            

                elif not fach in self.m.gecheckteFächer:
                    if checkFeld==1:
                        self.m.gecheckteFächer.append(fach)
                        if not fach in self.m.lkSpeicher:
                            
                            self.abiKursKontrolleHilfsFunktion(fach)
                        
                            abfrageWert=self.m.kursAnzahl
                            abfrageWert=int(abfrageWert)
                            self.m.eingebrachteKurse+=abfrageWert


                        else:
                            abfrageWert=4
                            self.m.eingebrachteKurse+=abfrageWert
                            if fach=="Informatik":
                                self.m.checkListe[5][1]=True


                        eingebrachteKursAnzeige.delete(0,END)
                        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)
                        self.v.checkButtonListe[self.v.kfListenListe.index(i)].box.configure(state="disabled")
                        if not listenIndex in self.m.inDieRechnungEinzubringendeFeldnummern:
                            self.m.inDieRechnungEinzubringendeFeldnummern.append([listenIndex,abfrageWert])

                if not self.m.checkListe[6][1]:
                    kfVorhanden=False
                    for k in self.v.kfListenListe:
                        if k.text.get("1.0",END).strip("\n")=="Bildende Kunst" or k.text.get("1.0",END).strip("\n")=="Musik":
                            kfVorhanden=True
                    if not kfVorhanden:
                        self.kfAbfragefenster=Meldung(self.v,"nein",schließschutz="ja")
                        self.kfAbfrage1=Entry(self.kfAbfragefenster)
                        self.kfAbfrage1.place(x=5,y=65)
                        self.kfAbfrage2=Entry(self.kfAbfragefenster)
                        self.kfAbfrage2.place(x=165,y=65)
                        abfrageText=Label(self.kfAbfragefenster,
                                          text=("anscheinend hast du ein künstlerisches Fach \n"
                                                "nur in der Jahrgangsstufe 12 belegt.Bitte trage \n"
                                                "hier die entsprechenden Punktzahlen ein"),
                                          font="Arial 8",
                                          fg="black",
                                          bg=self.v.nebenFarbe)


                        
                        abfrageText.place(x=30,y=5)
                        abfrageWert=0
                        abfrageBestätigungsKnopf=Button(self.kfAbfragefenster,
                                                        text="bestätigen",
                                                        font=self.v.verd,
                                                        bg="#b48768",
                                                        fg="white",
                                                        command=lambda:[self.kfAbfrageBestätigung(),self.kfAbfragefenster.destroy()])
                        abfrageBestätigungsKnopf.place(x=110,y=90)
                        self.v.wait_window(self.kfAbfragefenster)
                        
        eingebrachteKursAnzeige.delete(0,END)
        eingebrachteKursAnzeige.insert(0,self.m.eingebrachteKurse)

        kfSicherung=0
        
        for j in self.m.checkListe:
            if not j[1]:
                if j[0]=="KF":
                    if "KF" in self.m.lks:
                        kfSicherung=1

                if kfSicherung==0 or j[0]!="KF":
                    
                        fehlermeldungsfenster=Meldung(self.v)
                        fehlermeldung=Label(fehlermeldungsfenster,
                                            text=("Folgendes Fach fehlt:",j[0]),
                                            bg="red")
                        fehlermeldung.place(x=10,y=35)
                        korrekteEingabe=False
                        


        if not self.m.eingebrachteKurse==35:
            korrekteEingabe=False

        self.getPunkteNEU()
        return korrekteEingabe

    def abiKursKontrolleHilfsFunktion(self,fach):
        """

        Hilfsfunktion für 'abiKursKontrolle',
        die ein Fenster erstellt, in dem angegeben werden soll,
        wie viele Kurse eines Faches eingebracht werden sollen.

        """
        self.abfragefenster=Meldung(self.v,"nein",schließschutz="ja")
        self.abfrage=Entry(self.abfragefenster)
        self.abfrage.place(x=85,y=55)
        
        if fach.strip("\n")=="Bildende Kunst" or fach.strip("\n")=="Musik":
            text=(fach,": wie viele Kurse \n"
                                "möchtest du einbringen? (2-4)")
        elif fach=="Sport":
            text=(fach,": wie viele Kurse \n"
                                "möchtest du einbringen? (1-3)")
        else:
            text=(fach,": wie viele Kurse \n"
                                "möchtest du einbringen? (1-4)")
        
        abfrageText=Label(self.abfragefenster,
                                text=(text),
                                bg="#805a3f",
                                fg="white")

        abfrageText.place(x=50,y=5)
        abfrageWert=0
        abfrageBestätigungsKnopf=Button(self.abfragefenster,
                                        text="bestätigen",
                                        command=self.kursAnzahlAbfrageBefehl,
                                        bg="#b48768",
                                        fg="white")
        abfrageBestätigungsKnopf.place(x=120,y=90)
        self.v.wait_window(self.abfragefenster)
        

    def kfAbfrageBestätigung(self):
        """

        Relevant für eine Belegung eines künstlerischen Faches nur in der Jahrgangsstufe 12.
        Prüft und speichert genau diese Noten aus der 12.
        
        """
        korrekteEingabe=False
        kfpunktzahl1=self.kfAbfrage1.get()
        kfpunktzahl2=self.kfAbfrage2.get()
        if self.intKontrolle(kfpunktzahl1) and self.intKontrolle(kfpunktzahl2):
            kfpunktzahl1=int(kfpunktzahl1)
            kfpunktzahl2=int(kfpunktzahl2)
            if kfpunktzahl1>=0 and kfpunktzahl1<16 and kfpunktzahl2>=0 and kfpunktzahl2<16:
                korrekteEingabe=True

        if korrekteEingabe:
            self.m.checkListe[6][1]=True
            self.m.eingebrachteKurse+=2
            self.m.kfNurIn12PunkteListe=[kfpunktzahl1,kfpunktzahl2]
        
        

    def kursAnzahlAbfrageBefehl(self):
        """
        
        Befehl beim 'Schließen'-Knopf der Abfrage,
        bei der die Anzahl der einzubringenden Kurse festgelegt wird.
        Falls die Eingabe korrekt ist,
        wird das Fenster geschlossen.
        
        """
        self.setKursAnzahl(self.abfrage.get())
        if int(self.m.kursAnzahl)>0 and int(self.m.kursAnzahl)<5:
            self.abfragefenster.destroy()
        

    def setKursAnzahl(self,wert):
        self.m.kursAnzahl=wert

    def kursWahlZurücksetzen(self):
        """

        Setzt den Fortschritt bei der Auswahl
        der in die Abiturnote einzubringenden Kurse zurück.
        
        """
        self.checkButtonsZurücksetzen()
        self.checkButtonsEinrichten()
        self.checkButtonsAnschalten()
        self.m.checkListe=[ ["D",False], ["FS",False], ["M",False], ["NW",False], ["GW",False], ["FS/NW/INF",False], ["KF",False] ]
        self.m.gecheckteFächer=[]
        self.m.eingebrachteKurse=0
        self.m.ersteFremdsprache=""
        self.m.ersteNaturwissenschaft=""
        self.m.inDieRechnungEinzubringendeFeldnummern=[]
        self.abiKursKontrolle()
        self.v.knopf.configure(command=self.berechnungEinleiten)
        self.v.knopf.configure(text="Kurse bestätigen")
        
        
    def berechnungEinleiten(self):
        """

        Falls die abiKursKontrolle erfolgreich ist,
        kann nun das Fenster zum Eintragen der Abiturnoten
        aufgerufen werden.
        
        """
        if self.abiKursKontrolle():
            for i in self.v.checkButtonListe:
                i.box.configure(state="disabled")
            self.v.knopf.configure(text="Abiresultate eintragen",
                                   command=self.abiResultateAbfragen)


    def abiResultateAbfragen(self):
        """

        Leitet die Abfrage der Abiturnoten ein.
        
        """
        self.v.abiResultatAbfrageEinleiten(self.abiSchnittBerechnenNEU)

            

    def abiResultateKontrollieren(self):
        """

        Kontrolliert die Eingabe der schriftlichen und mündlichen Abiturpunktzahlen.
        
        """
        self.noten=[]
        korrekteEingabe=True
        self.noten.append(self.v.schriftlicheAbfrage1.get())
        self.noten.append(self.v.schriftlicheAbfrage2.get())
        self.noten.append(self.v.schriftlicheAbfrage3.get())
        self.noten.append(self.v.mündlicheAbfrage.get())
        
        for i in self.noten:
            
                if not self.intKontrolle(i):
                    korrekteEingabe=False
                    
                elif int(i)>15 or int(i)<=0:
                    korrekteEingabe=False
                
        return [korrekteEingabe,self.noten]
    

    def abiSchnittBerechnenNEU(self):
        """

        Setzt den Abischnitt zusammen und zeigt ihn an.
        
        """
        if self.abiResultateKontrollieren()[0]:
            
            block2=self.abiResultateKontrollieren()[1]

            facharbeit=self.v.facharbeitAbfrage.get()

            gesamtpunkte=self.m.abiSchnittZusammenstellen(facharbeit,block2)

            ergebnis=Entry(self.v.abfrageFenster)
            ergebnis.place(x=60,y=390)
            ergebnistext=Label(self.v.abfrageFenster,
                               bg=self.v.nebenFarbe,
                               text="dein Abischnitt:",
                               font=("Arial 8 italic"))
            ergebnistext.place(x=80,y=370)
            abischnitt=self.m.abischnittUmwandeln(gesamtpunkte)
            ergebnis.insert(END,abischnitt)
            
        else:
            fehlermeldung=Meldung(self.v)
            fehler=Label(fehlermeldung,
                          bg="red",
                          text=("es liegt ein Fehler vor,bitte überprüfe deine Eingabe"))
            fehler.place(x=15,y=30)

    def intKontrolle(self,wert):
        """

        input : ...
        output : input==int?
        
        """
        
        try:
            int(wert)
            korrekteEingabe=True
        except ValueError:
            korrekteEingabe=False

        return korrekteEingabe
            
        
    
if __name__=="__main__":
    m=Model()
    root=View(0)
    C=Controller(m,root)
    root.startEinrichten(C.lksUmschreiben,m.lkTabelle)
    root.mainloop()
