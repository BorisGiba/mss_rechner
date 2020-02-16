#Boris Giba
#02.09.2018
#MSS 12

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox
from tkinter import font

#------------------------------------------------
#View
#------------------------------------------------


class View(Tk):
    
    def __init__(self,dropDownEinstellung):
        
        Tk.__init__(self)

        try:
            self.verdbold = font.Font(family="Verdana", size=10, weight="bold")
            self.verd = font.Font(family="Verdana", size=10)
        except:
            self.verdbold = "Arial 10 bold"
            self.verd="Arial 10"

        self.dropDownEinstellung=dropDownEinstellung

        self.abstand=25
        
        self.farbe="#6f4e37"

        self.ausgeschalteteFarbe= "#5e422e"

        self.nebenFarbe= "light blue"
        
        self.configure(background=self.farbe)

        self.title("MSS-Rechner (Kaffeebraune Edition)")
        
        self.geometry("640x480")

        self.pfListenListe= [ [],[],[],[] ]

        self.kfListenListe = []

        self.checkButtonListe = []

        self.auffüllEinstellung=1

        self.prognoseEinstellung=1

        self.einstellungsBlock=0

        self.prognose=False

        self.protocol("WM_DELETE_WINDOW", self.schließBestätigung)

    def schließBestätigung(self):
        if messagebox.askyesno("Programm beenden", "Willst du das Programm wirklich beenden?"):
            self.destroy()


    def startEinrichten(self,cbBefehl,fächerListe):
        """

        Richtet das erste Fenster ein (LK-Auswahl).

        """
        fächerListeKopie=fächerListe[:]
        StartLkFrame=Frame(self,width=640,
                       height=45,
                       bg="#4d3626")
        StartLkFrame.place(x=0,y=210)
        Startanleitung=Label(self,
                             fg="white",
                             font="Arial 15",
                             text=("Gebe deine Leistungskurse in die unteren Felder ein"
                                 "\n Achte auf korrekte Rechtschreibung (Anfang großgeschrieben)"))

        self.lk1=StartLkFeld(30,220,"Informatik",self)
        self.lk2=StartLkFeld(250,220,"Mathematik",self)
        self.lk3=StartLkFeld(480,220,"Englisch",self)

        ungültigeLKs=["Sport","Katholische Religion","Evangelische Religion","Ethik","Erdkunde/Sozialkunde"]
    
        for i in ungültigeLKs:
            if i in fächerListeKopie:
                fächerListeKopie.remove(i)

        self.lk1DropDownMenü=LKAuswahlDropDownMenü(self,
                                                   fächerListeKopie,
                                                   20,217)
        
        self.lk2DropDownMenü=LKAuswahlDropDownMenü(self,
                                                   fächerListeKopie,
                                                   240,217)
        
        self.lk3DropDownMenü=LKAuswahlDropDownMenü(self,
                                                   fächerListeKopie,
                                                   465,217)


        
        self.startbutton=Button(self,
                                bg="#b48768",
                                fg="white",
                                text="Start",
                                font=self.verdbold,
                                command=cbBefehl)
        self.startbutton.place(x=290,y=300)
        
        Startanleitung.place(x=30,
                         y=100)
        Startanleitung.configure(background=self.farbe)


        kaffeeBild=PhotoImage(file="coffeemug3.png")

        bildLabel=Label(self,image=kaffeeBild,borderwidth=0, highlightthickness=0)
        bildLabel.image=kaffeeBild

        bildLabel.place(x=525,y=350)

        bildText=Label(self,
                       text="jetzt mit noch mehr Kaffee",
                       font="Arial 10 italic",
                       fg="white",
                       bg=self.farbe)
        
        bildText.place(x=395,y=460)

        self.dropDownStartEinstellungsButton=Button(self,
                                       command=self.startDropDownEinstellungen,
                                       text="⚙",
                                       bg="#4d3626",
                                       fg="white")
        self.dropDownStartEinstellungsButton.place(x=605,y=5)
        

    def startDropDownEinstellungen(self):
        """

        beschreibt die Einstellungsmöglichkeit im Startmenü,
        in welcher der (alte) textbasierte Eingabemodus ohne
        die Drop-Down-Menüs aktiviert werden kann.
        
        """
        
        dropDownStartEinstellung=Toplevel(bg=self.farbe)
        dropDownStartEinstellung.geometry("300x125")
        self.dropDownStartFrage=Label(dropDownStartEinstellung,
                                 fg="white",
                                 bg=self.farbe,
                                 text="Drop-Down-Menüs beibehalten?\n"
                                 "Warnung : falls ausgeschaltet, können Fehler auftreten.")

        self.dropDownStartFrage.place(x=0,y=20)
        
        self.dropDownStartCheckVar=IntVar(self)
    
        self.dropDownStartCheckVar.set(1)
        
        self.dropDownStartFrageCheckButton=Checkbutton(dropDownStartEinstellung,var=self.dropDownStartCheckVar,onvalue=1,offvalue=0)
        self.dropDownStartFrageCheckButton.configure(borderwidth=0)
        self.dropDownStartFrageCheckButton.configure(relief="groove")
        self.dropDownStartFrageCheckButton.configure(bg=self.farbe)
        
        self.dropDownStartFrageCheckButton.place(x=140,y=55)

        self.dropDownStartAktualisierButton=Button(dropDownStartEinstellung,
                                                         text="Einstellungen \n"
                                                         "speichern",
                                                         font="Arial 8",
                                                         bg="#4d3626",
                                                         fg="white",
                                                         command=self.dropDownStartEinstellungenAktualisieren)
        self.dropDownStartAktualisierButton.place(x=113,y=78)

    def dropDownStartEinstellungenAktualisieren(self):
        self.dropDownEinstellung=self.dropDownStartCheckVar.get()
        
                                   
    def abstandEinstellen(self):
        """

        Legt Abstand zwischen den einzelnen Kurs- und Punktefeldern fest.
        
        """
        if self.dropDownEinstellung==0:
            self.abstand=25
            
        else:
            self.abstand=40
        

    def kursfelderGenerieren(self):
        y=100
        nummer=0
        for i in Kursfeld.liste:
            self.kfListenListe.append(Kursfeld(50,y,nummer,self))
            y+=self.abstand
            nummer+=1

        for i in self.kfListenListe:
            if self.kfListenListe.index(i)<3:
                i.text.configure(bg="light blue")

        return self.kfListenListe

    def punktfelderGenerieren(self):
        x=250
        y=100
        nummer=0
        index=0
        for i in range(0,4):
            for i in Kursfeld.liste:
                self.pfListenListe[index].append(Punktefeld(x,y,nummer,self))
                y+=self.abstand
                nummer+=1
            index+=1
            x+=100
            y=100
            nummer+=1
            
        self.punktfelderBeschriften()
        return self.pfListenListe

    def punktfelderBeschriften(self):
        """

        Beschriftet die Punktfelderspalten mit den einzelnen Halbjahreszahlen (11/2 - 13/1).
        
        """
        self.beschriftung1=Label(self,
                            text="11/2",
                            bg=self.farbe,
                            fg="white")
        self.beschriftung2=Label(self,
                            text="12/1",
                            bg=self.farbe,
                            fg="white")
        self.beschriftung3=Label(self,
                            text="12/2",
                            bg=self.farbe,
                            fg="white")
        self.beschriftung4=Label(self,
                            text="13/1",
                            bg=self.farbe,
                            fg="white")
        self.beschriftung1.place(x=250,y=75)
        self.beschriftung2.place(x=350,y=75)
        self.beschriftung3.place(x=450,y=75)
        self.beschriftung4.place(x=550,y=75)

    def punkteButtonGenerieren(self,cbclick):
        self.knopf=Button(self,
                          text="Auswahl beginnen",
                          font=self.verd,
                          command=cbclick,
                          bg="#b48768",
                          fg="white")
        if self.dropDownEinstellung==0:
            self.knopf.place(x=280,y=400)
        else:
            self.knopf.place(x=280,y=550)

    def kursCheckButtonsGenerieren(self):
        y=100
        for i in Kursfeld.liste:
            self.checkButtonListe.append(kursCheckButton(10,y,self))
            y+=self.abstand

        for i in self.checkButtonListe:
            if self.checkButtonListe.index(i)<3:
                i.box.configure(selectcolor="light blue")

    def hilfeButtonGenerieren(self):
        self.hilfeButton=Button(self,
                                command=self.hilfe,
                                text="?",
                                bg="#4d3626",
                                fg="white")
        if self.dropDownEinstellung==0:
            self.hilfeButton.place(x=620,y=10)
        else:
            self.hilfeButton.place(x=655,y=10)

    def hilfe(self):
        """

        Beschreibt das Fenster, das erscheint, falls die Hilfe (?) aufgerufen wird.

        """
        
        hilfe=Toplevel(self)
        hilfe.geometry("450x375")
        hilfe.configure(bg=self.farbe)
        
        textLang=("du musst folgende Kurse einbringen:\n"
                        "\n"
                        "-vier Kurse in Deutsch\n"
                        "-vier Kurse in einer fortgeführten Fremdsprache\n"
                        "-vier Kurse in Mathematik\n"
                        "-vier Kurse in einer Naturwissenschaft\n"
                        "-vier Kurse in einem gesellschaftswissenschaftlichen Fach\n"
                        "\n"  
                        "-ein Kurs aus der Jahrgangsstufe 13 in einer zweiten Fremdsprache\n"
                        " oder in einer zweiten Naturwissenschaft oder in Informatik\n"
                        "\n"
                        "-zwei Kurse in einem künstlerischen Fach (Ist innerhalb der Pflicht-\n"
                        " stundenzahl kein künstlerisches Fach durchgehend belegt worden,\n"
                        " so sind die Kurse im künstlerischen Fach aus den Halbjahren 12/1\n"
                        " und 12/2 einzubringen\n"
                        "\n"
                        "-in allen drei Leistungsfächern jeweils die vier Kurse der Qualifikationsphase\n"
                        "\n"
                        "-insgesamt sind 35 Kurse einzubringen")

        textKurz=("Diese Knöpfe erleichtern dir das Eintragen der Punkte.\n"
                  "Wenn du den Knopf betätigst,\n"
                  "wird die Reihe in der sich der Knopf befinden\n"
                  "automatisch aufgefüllt, falls sie noch nicht ganz voll ist.\n"
                  "\n"
                  "Dafür muss die Eingabe korrekt sein\n"
                  "und es darf kein 'Sprung' zwischen Notenfeldern bestehen.\n"
                  "D.h. falls die Noten von 12/1 eingetragen wurden,\n"
                  "müssen auch die Noten von 11/2 eingetragen sein.\n"
                  "In den Einstellungen kannst du die Art des Auffüllens verändern")
        
        if self.dropDownEinstellung==0:
            
            hilfetext=Label(hilfe,
                            bg="light blue",
                            text=textLang)
            hilfetext.place(x=25,y=40)
            
            kursAuswahlHilfeButton=Button(hilfe,
                                      font=self.verd,
                                      text="Kursauswahlhilfe anzeigen",
                                      command= lambda : self.kursAuswahlHilfe(self))
            kursAuswahlHilfeButton.place(x=135,y=335)
            
        else:
            hilfe.geometry("400x225")
            hilfetext=Label(hilfe,
                            bg="light blue",
                            text=textKurz,
                            font="Arial 9")
            
            hilfetext.place(x=25,y=40)
            
            hilfeButton=Button(hilfe,
                               text="→",
                               bg="#b48768",
                               fg="white")
            hilfeButton.place(x=200,y=5)
            
            


    def kursAuswahlHilfe(self,root):
        """

        Hilfetext, der erscheint, falls man sich gegen die DropDown-Menüs entscheidet.
        Er soll das Arbeiten mit den textbasierten Eingabefeldern erklären.
        
        """

        abfrageFenster=Meldung(root,"nein")
        abfrageFenster.geometry("575x500")
        abfrage=Label(abfrageFenster,
                      bg="light blue",
                      text="bitte trage nun deine restlichen Kurse in die dafür\n"
                      "vorgesehenen Felder ein\n"
                      "\nhier ein paar Hinweise:\n"
                      "-Schreibe bitte alle Kurse ausgeschrieben auf\n"
                      "und achte auf korrekte Rechtschreibung.\n"
                      "\n-Die Kurse müssen eindeutig sein,\n"
                      "uneindeutige Kurse wurden orange markiert."
                      "\n"
                      "\n"
                      "Hier eine Liste mit den kniffligsten uneindeutigen Kursen:\n"
                      "\n"
                      "Gesells.wissenschaft:\n"
                      "hier kannst du 'Erdkunde' oder 'Sozialkunde' oder 'Geschichte' eintragen.\n"
                      "\n"
                      "Künstlerisches Fach:\n"
                      "hier kannst du 'Bildende Kunst' oder 'Musik' eintragen\n"
                      "\n"
                      "Religion/Ethik:\n"
                      "hier kannst du 'katholische Religion' oder 'evangelische Religion' oder 'Ethik' eintragen.\n"
                      "\n"
                      "FS/NW/INF:\n"
                      "hier kannst du eine Fremdsprache oder Naturwissenschaft oder 'Informatik' eintragen.\n"
                      "\n"
                      "FS/NW/INF/KF:\n"
                      "genau wie das Beispiel darüber, allerdings kannst du hier auch ein künstlerisches Fach eintragen.")
        
        abfrage.place(x=25,y=30)

        hinweisRahmen=Frame(abfrageFenster,
                            width=512,
                            height=25,
                            bg="red")
        
        hinweisRahmen.place(x=25,y=175)

        hinweisText=Label(abfrageFenster,
                          bg="red",
                          fg="white",
                          text="Hier eine Liste mit den kniffligsten uneindeutigen Kursen:")
        hinweisText.place(x=135,y=175)

        wiederAufrufenHinweis=Label(abfrageFenster,
                                    fg="white",
                                    bg=root.farbe,
                                    text="diese Meldung kannst du auch wieder über die Hilfe (rechts oben) aufrufen",
                                    font="Arial 8 italic")
        wiederAufrufenHinweis.place(x=95,y=480)

        pflichtKursMeldung=Label(abfrageFenster,
                                 text="alle grau hinterlegten Kurse müssen belegt werden",
                                 bg="red",
                                 fg="white")
        pflichtKursMeldung.place(x=150,y=427)


    def einstellungsButtonGenerieren(self):
        self.einstellungsButton=Button(self,
                                       command=self.einstellungen,
                                       text="⚙",
                                       bg="#4d3626",
                                       fg="white")
        if self.dropDownEinstellung==0:
            self.einstellungsButton.place(x=585,y=10)
        else:
            self.einstellungsButton.place(x=625,y=10)

    def einstellungen(self):
        """

        Beschreibt das Fenster, das erscheint, wenn die Einstellungen (⚙) aufgerufen werden.
        Hier werden auch die verschiedenen Einstellungswerkzeuge generiert.

        """
        #Fenster
        einstellungen=Toplevel(self)
        einstellungen.title("Einstellungen")
        einstellungen.geometry("450x250")
        einstellungen.configure(bg="#6f4e37")
        
        #Hauptfarbe
        
        einstellungsButton=Button(einstellungen,
                                  text="Hauptfarbe ändern",
                                  bg="#4d3626",
                                  fg="white",
                                  command=self.setFarbe)
        einstellungsButton.place(x=70,y=80)
        einstellungsfarbhinweis=Label(einstellungen,
                                      bg="#6f4e37",
                                      fg="white",
                                      text="aktuelle Hauptfarbe:")
        einstellungsfarbhinweis.place(x=0,y=50)
        einstellungsfarbe=Label(einstellungen,
                                bg=self.farbe,
                                borderwidth=2,
                                relief="groove",
                                text="   ")
        einstellungsfarbe.place(x=120,y=50)

        #Zweitfarbe

        einstellungsButtonAusgeschalteteFarbe=Button(einstellungen,
                                  text="Zweitfarbe ändern",
                                  bg="#4d3626",
                                  fg="white",
                                  command=self.setausgeschalteteFarbe)
        einstellungsButtonAusgeschalteteFarbe.place(x=220,y=80)
        einstellungsAusgeschalteteFarbhinweis=Label(einstellungen,
                                      bg="#6f4e37",
                                      fg="white",
                                      text="aktuelle Zweitfarbe:")
        einstellungsAusgeschalteteFarbhinweis.place(x=150,y=50)
        einstellungsAusgeschalteteFarbe=Label(einstellungen,
                                bg=self.ausgeschalteteFarbe,
                                borderwidth=2,
                                relief="groove",
                                text="   ")
        einstellungsAusgeschalteteFarbe.place(x=270,y=50)

        #AuffüllEinstellungen

        auffüllEinstellungsLabel=Label(einstellungen,
                                       text="erweitertes Auffüllen",
                                       fg="white",
                                       bg="#6f4e37")
        auffüllEinstellungsLabel.place(x=30,y=120)

        self.auffüllEinstellungsCheckButtonVar=IntVar(einstellungen)
        self.auffüllEinstellungsCheckButtonVar.set(self.auffüllEinstellung)
        self.auffüllEinstellungsCheckButton=Checkbutton(einstellungen,
                                                        var=self.auffüllEinstellungsCheckButtonVar,
                                                        onvalue=1,
                                                        offvalue=0,
                                                        bg="#6f4e37")
        self.auffüllEinstellungsCheckButtonVar.set(self.auffüllEinstellung)
        self.auffüllEinstellungsCheckButton.place(x=150,y=120)
        
        self.auffüllEinstellungsHilfeButton=Button(einstellungen,
                                                   text="?",
                                                   font="Arial 8",
                                                   bg="#4d3626",
                                                   fg="white",
                                                   command=self.auffüllEinstellungsHilfe)
        self.auffüllEinstellungsHilfeButton.place(x=10,y=120)

        #Aktualisierknopf
        
        self.auffüllEinstellungsAktualisierButton=Button(einstellungen,
                                                         text="Auffülleinstellungen \n"
                                                         "speichern",
                                                         font="Arial 9",
                                                         bg="#4d3626",
                                                         fg="white",
                                                         command=self.auffüllEinstellungenAktualisieren)
        
        self.auffüllEinstellungsAktualisierButton.place(x=100,y=190)


        #Prognoseeinstellungen

        prognoseEinstellungsLabel=Label(einstellungen,
                                       text="Prognose",
                                       fg="white",
                                       bg="#6f4e37")
        prognoseEinstellungsLabel.place(x=30,y=150)

        self.prognoseEinstellungsCheckButtonVar=IntVar(einstellungen)
        self.prognoseEinstellungsCheckButtonVar.set(self.prognoseEinstellung)
        self.prognoseEinstellungsCheckButton=Checkbutton(einstellungen,
                                                        var=self.prognoseEinstellungsCheckButtonVar,
                                                        onvalue=1,
                                                        offvalue=0,
                                                        bg="#6f4e37")

        self.prognoseEinstellungsCheckButtonVar.set(self.prognoseEinstellung)
        self.prognoseEinstellungsCheckButton.place(x=150,y=150)

        self.prognoseEinstellungsHilfeButton=Button(einstellungen,
                                                   text="?",
                                                    font="Arial 8",
                                                    bg="#4d3626",
                                                    fg="white",
                                                   command=self.prognoseEinstellungsHilfe)
        self.prognoseEinstellungsHilfeButton.place(x=10,y=150)
        
        self.prognoseEinstellungsCheckButton.configure(state="disabled")
        
        if self.einstellungsBlock==1:
            self.auffüllEinstellungsCheckButton.configure(state="disabled")

        

        

    def auffüllEinstellungenAktualisieren(self):
        self.auffüllEinstellung=self.auffüllEinstellungsCheckButtonVar.get()


    def auffüllEinstellungsHilfe(self):
        hilfe=Meldung(self,"nein")
        hilfeText=Label(hilfe,
                        bg="light blue",
                        font="Arial 9",
                        text=("Füllt bei einer geschlossenen\n"
                        "Notenfolge die nicht befüllten Felder\n"
                        "mit der zuletzt eingetragenen Note ein.\n"
                        "\n"
                        "Falls ausgeschaltet, wird die Note aus 11/1,\n"
                        "falls valide, in alle Felder eingetragen\n"
                        "(bei Betätigen des Knopfes.)"))
        hilfeText.place(x=30,y=10)

    def prognoseEinstellungsHilfe(self):
        hilfe=Meldung(self,"nein")
        hilfe.geometry("320x230")
        hilfeText=Label(hilfe,
                        bg="light blue",
                        font="Arial 9",
                        text=("nutzt die erweiterte Auffüllfunktion,\n"
                        "um (bei ansonsten korrekter Eingabe) alle\n"
                        "nicht vollständig gefüllten Reihen aufzufüllen\n"
                        "und so die Berechnung fortzuführen.\n"
                        "\n"
                        "Nur möglich, falls keine Lücke in den Reihen\n"
                        "vorherrscht\n"
                        "(Bsp. für Lücke: Noten von 12/1 sind\n"
                        "eingetragen, aber Noten von 11/1 nicht.)\n"
                        "Ebenso müssen die Noten zwischen 0 und 15 liegen,\n"
                        "ein LK darf nie 0 Punkte haben und es müssen\n"
                        "mindestens die Noten von 11/1 eingetragen werden."))
        hilfeText.place(x=10,y=10)
        
        


    
    def setFarbe(self):
        """

        Fragt eine Farbe ab und ändert dann die Hauptfarbe im Interface in die ausgewählte Farbe.
        
        """
        self.farbe=askcolor()[1]
        self.hauptfarbeAktualisieren()

    def setausgeschalteteFarbe(self):
        """

        Fragt eine Farbe ab und ändert dann die Zweitfarbe im Interface in die ausgewählte Farbe.
        
        """
        self.ausgeschalteteFarbe=askcolor()[1]
        self.ausgeschalteteFarbeAktualisieren()
        

    def hauptfarbeAktualisieren(self):
        """

        Erneuert die Hauptfarbe im Interface (dort, wo sie verwendet wird).
        
        """
        self.configure(bg=self.farbe)
        self.beschriftung1.configure(bg=self.farbe)
        self.beschriftung2.configure(bg=self.farbe)
        self.beschriftung3.configure(bg=self.farbe)
        self.beschriftung4.configure(bg=self.farbe)
        for i in self.checkButtonListe:
            i.box.configure(bg=self.farbe)


    def ausgeschalteteFarbeAktualisieren(self):
        """

        Erneuert die Zweitfarbe im Interface (dort, wo sie verwendet wird).
        
        """
        
        for i in self.kfListenListe[3:]:
            if i.text["state"]=="disabled":
                i.text.configure(bg=self.ausgeschalteteFarbe)

                
        for i in self.pfListenListe:
            for j in i:
                if j.punkte["state"]=="disabled":
                    j.punkte.configure(disabledbackground=self.ausgeschalteteFarbe)

        for i in self.dropDownMenüListe:
            if i["state"]=="disabled":
                i.configure(bg=self.ausgeschalteteFarbe)
                    
        
        

    def punkteAuffüllenButtonsGenerieren(self,cbBefehl):
        self.punkteAuffüllButtonListe=[]
        index=0
        if self.dropDownEinstellung==0:
            x=600
        else:
            x=620
        y=100
        for i in self.kfListenListe:
            self.punkteAuffüllButtonListe.append(PunkteAuffüllButton(x,y,cbBefehl,index))
            y+=self.abstand
            index+=1


    def dropDownMenüsGenerieren(self,indexListe,auswahl,cbBefehl):
        self.dropDownMenüListe=[]
        x=50
        auswahlcounter=0
        for i in indexListe:
            y=100
            y+= i*self.abstand-3
            self.dropDownMenüListe.append(KursAuswahlDropDownMenü(self,auswahl[auswahlcounter],x,y,i))
            auswahlcounter+=1

    def zusätzlichesDropDownMenüGenerieren(self,auswahl):
        """

        Betrifft den zusätzlichen (/freiwilligen) Grundkurs.
        
        """
        self.zusätzlichesDropDownMenü=KursAuswahlDropDownMenü(self,auswahl,50,500,10)


    def prognoseTextHinzufügen(self):
        """

        Fügt einen kleinen Text in das Interface ein, der auf die Erstellung einer Prognose hinweisen soll.
        
        """
        
        self.prognose=True
        self.prognoseText=Label(self,
                                text="Prognose",
                                fg="white",
                                bg=self.farbe,
                                font="Arial 8 italic")
        self.prognoseText.place(x=5,y=600)
        
    def abiResultatAbfrageEinleiten(self,cbBefehl):
        
        """

        Öffnet und gestaltet ein neues Fenster, in dem die Abiturnoten eingetragen werden können
        (in diesem Fenster können, falls eine Prognose vorliegt, auch Informationen zu Facharbeiten abgerufen werden).
        
        """

        self.abfrageFenster=Tk()
        self.abfrageFenster.title("Abiturnotenabfrage")
        self.abfrageFenster.configure(bg=self.nebenFarbe)
        self.abfrageFenster.geometry("250x420")
        abfrageText=Label(self.abfrageFenster,bg=self.nebenFarbe,
                          text=("trage hier nun bitte\n"
                                "deine erhaltenen Noten im Abitur ein"),
                          )
        abfrageText.place(x=20,y=35)
        self.schriftlicheAbfrage1=Entry(self.abfrageFenster)
        self.schriftlicheAbfrage2=Entry(self.abfrageFenster)
        self.schriftlicheAbfrage3=Entry(self.abfrageFenster)
        self.schriftlicheAbfrage1.place(x=60,y=100)
        self.schriftlicheAbfrage2.place(x=60,y=125)
        self.schriftlicheAbfrage3.place(x=60,y=150)
        self.schriftlicheAbfrage1.insert(END,"erste Prüfung")
        self.schriftlicheAbfrage2.insert(END,"zweite Prüfung")
        self.schriftlicheAbfrage3.insert(END,"dritte Prüfung")

            
        self.mündlicheAbfrage=Entry(self.abfrageFenster)
        self.mündlicheAbfrage.place(x=60,y=200)
        self.mündlicheAbfrage.insert(END,"mündliche Prüfung")

        self.facharbeitAbfrage=Entry(self.abfrageFenster)
        self.facharbeitAbfrage.place(x=60,y=250)
        self.facharbeitAbfrage.insert(END,"Facharbeit (optional)")

        self.bestätigungsKnopf=Button(self.abfrageFenster,text="bestätigen",
                                      fg="white",
                                      bg="#9bc2cf",
                                      command=cbBefehl)
        self.bestätigungsKnopf.place(x=85,y=335)

        if self.prognose:
            facharbeitHilfeButton=Button(self.abfrageFenster,
                                         text="lohnt sich eine Facharbeit?",
                                         command=self.facharbeitHilfe,
                                         font="Arial 8",
                                         bg="#9bc2cf",
                                         fg="white",
                                         relief="sunken")
            facharbeitHilfeButton.place(x=55,y=275)
            
    def facharbeitHilfe(self):
        """

        Stellt einen Hilfetext dar, der aufgerufen werden kann,
        falls eine Prognose vorliegt.
        Er erklärt, ob sich eine Facharbeit lohnt.

        """
        hilfeFenster=Meldung(self,"nein")
        hilfeFenster.configure(bg="light blue")
        hilfeFenster.geometry("370x260")
        hilfe=Label(hilfeFenster,
                    bg="#9bc2cf",
                    fg="white",
                    text=("eine Facharbeit lohnt sich immer!\n",
                    "\n"
                    "denn die bei der Facharbeit erbrachte Punktzahl\n"
                    "(falls sie mindestens 5 Punkte beträgt)\n"
                    "fließt immer additiv in deine Abiturnote mit ein!\n"
                    "\n"
                    "d.h. eine Verschlechterung ist ausgeschlossen!\n"
                    "\n"
                    "Also nur Mut! Notfalls kannst du die Arbeit auch abbrechen.\n"
                    "Sprich am besten mit einem deiner Leistungskurs-Lehrer\n"
                    "oder der Oberstufenleitung über das Thema,\n"
                    "falls du mehr Informationen benötigst.\n"
                    "Viel Erfolg!"))
        
        hilfe.place(x=25,y=30)
            
            
            

class kursCheckButton(Checkbutton):
    
    def __init__(self,x,y,root):
        self.var=IntVar(root)
        Checkbutton.__init__(self)
        self.box=Checkbutton(root,var=self.var,onvalue=1,offvalue=0)
        self.box.configure(borderwidth=0)
        self.box.configure(relief="groove")
        self.box.configure(bg=root.farbe)
        self.box.configure(highlightthickness=0)
        self.box.configure(disabledforeground="white")
        self.box.place(x=x,y=y)

    


            

class Kursfeld(Text):

    liste=["lk1","lk2","lk3","gk1","gk2","gk3",
           "gk4","gk5","gk6","gk7","zusätzlicher GK"]

    def __init__(self,x,y,nummer,root):
        Text.__init__(self)
        self.text=Text(root,
                        width=20,
                        height=1,
                        bg="grey")
        self.text.place(x=x,
                        y=y)

        self.text.insert(END,
                    Kursfeld.liste[nummer])


class Punktefeld(Entry):

    def __init__(self,x,y,nummer,root):
        Entry.__init__(self)
        self.nummer=nummer
        self.punkte=Entry(root,
                          width=4,
                          disabledbackground=root.ausgeschalteteFarbe)
        self.punkte.place(x=x,
                         y=y)
        self.bind('<Tab>', lambda e, self=self: focusNext(self))
        

class StartLkFeld(Entry):

    def __init__(self,x,y,text,root):
        Entry.__init__(self)
        self.kurs = Entry(root,width=20)
        self.kurs.place(x=x,y=y)
        self.kurs.insert(END,text)
        self.kurs.configure(justify="center")
        self.bind('<Tab>', lambda e, self=self: focusNext(self))


class Meldung(Toplevel):
    def __init__(self,root,button="ja",schließschutz="nein"):
        Toplevel.__init__(self,bg=root.farbe)
        self.geometry("300x125")
        self.title("Meldung")
        if button=="ja":
            self.schließKnopf=Button(self,
                                     bg="#ae7d5b",
                                     fg="white",
                                     text="schließen",
                                     font=root.verd,
                                     command=self.destroy)
            self.schließKnopf.place(x=120,y=70)
            
        if schließschutz=="ja":
            self.protocol("WM_DELETE_WINDOW", self.schließBestätigung)

    def schließBestätigung(self):
        messagebox.showwarning("Fehler", "Meldung bitte nicht ungewollt schließen.")



class PunkteAuffüllButton(Button):
                                           
    def __init__(self,x,y,cbBefehl,index):
        Button.__init__(self)
        self.configure(text="→")
        self.configure(bg="#b48768")
        self.configure(fg="white")
        self.index=index
        self.configure(command= lambda : cbBefehl(index))
        self.place(x=x,y=y)


class KursAuswahlDropDownMenü(OptionMenu):

    def __init__(self,root,dropDownAuswahlListe,x,y,kfIndex):
        self.var=StringVar(root)
        self.var.set(dropDownAuswahlListe[0])
        OptionMenu.__init__(self,
                            root,
                            self.var,
                            *dropDownAuswahlListe)
        self.configure(width=20)
        self.place(x=x,y=y)
        self.fach=(root.kfListenListe[kfIndex].text.get("1.0",END)).strip("\n")
        self.kfIndex=kfIndex
        self.configure(bg="#4d3626")
        self.configure(fg="white")
        self["menu"].configure(bg="#4d3626")
        self["menu"].configure(fg="white")
        self.configure(activebackground="#b48768")
        self.configure(activeforeground="white")
        self["menu"].configure(activebackground="#b48768")

class LKAuswahlDropDownMenü(OptionMenu):

    def __init__(self,root,fächerListe,x,y):

        self.var=StringVar(root)
        self.var.set(fächerListe[-1])
        OptionMenu.__init__(self,
                            root,
                            self.var,
                            *fächerListe)
        self.configure(width=18)
        self.configure(bg="#4d3626")
        self.configure(fg="white")
        self.place(x=x,y=y)
        self["menu"].configure(bg="#4d3626")
        self["menu"].configure(fg="white")
        self.configure(activebackground="#b48768")
        self.configure(activeforeground="white")
        self["menu"].configure(activebackground="#b48768")
