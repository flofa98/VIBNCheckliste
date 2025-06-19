import tkinter as tk
from tkinter import messagebox

# Fragenstruktur für Mechanik, Elektronik, Steuerung 
fragenbereiche = {
    "Mechanik": [
        ("Sind mechanische Modelle vollständig und aktuell?", [
            "Wurden die Modelle gegen reale Messdaten geprüft?",
            "Existiert ein Versionierungssystem für Modelländerungen?",
            "Werden Variantenmodelle unterstützt?"
        ]),
        ("Werden CAD-Daten in die Simulation integriert?", [
            "Ist der CAD-Import automatisiert?",
            "Werden STEP- oder AutomationML-Standards verwendet?",
            "Gibt es Schnittstellen zu Simulationssoftware?"
        ]),
        ("Sind Mechanik-Modelle für digitale Zwillinge geeignet?", [
            "Enthalten die Modelle Verhaltensdaten (z. B. Federwege)?",
            "Sind Modelle direkt mit Steuerung/Simulation verknüpfbar?"
        ]),
        ("Ist die mechanische Simulation ausreichend detailliert?", [
            "Werden reale Bewegungsabläufe abgebildet?",
            "Beinhaltet die Simulation Kollisionserkennung?",
            "Gibt es eine dynamische Massen-/Kraftberechnung?"
        ]),
        ("Gibt es eine konsistente Abstraktionsebene für mechanische Modelle?", [
            "Existieren vereinheitlichte Modellrichtlinien?",
            "Wird die Abstraktion projektspezifisch angepasst?"
        ]),
        ("Sind die mechanischen Modelle mit anderen Disziplinen (Elektronik, Steuerung) kompatibel?", [
            "Gibt es gemeinsame Koordinatensysteme?",
            "Werden Multidomain-Schnittstellen verwendet?"
        ]),
        ("Unterstützen die Tools Standards wie STEP oder AutomationML?", [
            "Sind Standardformate projektweit vorgeschrieben?",
            "Gibt es automatisierte Konvertierungspfade?"
        ]),
        ("Wurde die mechanische Simulation mit realen Daten überprüft?", [
            "Existieren Abgleich-Protokolle mit Prüfdaten?",
            "Wird Validierung regelmäßig durchgeführt?"
        ]),
        ("Gibt es ein Testprotokoll für mechanische Validierungen?", [
            "Ist das Testprotokoll versioniert und dokumentiert?",
            "Wird es bei Änderungen automatisch aktualisiert?"
        ])
    ],
    "Elektronik": [
        ("Sind elektrische Schaltpläne und Layouts aktuell und digital verfügbar?", [
            "Sind alle Komponenten im System modelliert?",
            "Gibt es einen digitalen Zwilling für die Elektrik?"
        ]),
        ("Unterstützen die Modelle Datenstandards wie EPLAN?", [
            "Werden EPLAN-Standards projekteinheitlich verwendet?",
            "Gibt es eine automatisierte Prüfung auf Normkonformität?"
        ]),
        ("Ist die elektrische Simulation detailliert genug für die virtuelle Inbetriebnahme?", [
            "Werden Störungen und Fehlerfälle simuliert?",
            "Gibt es eine Lasten-/Stromanalyse?"
        ]),
        ("Sind Signalflüsse und Stromlasten simuliert?", [
            "Werden diese Simulationen regelmäßig aktualisiert?",
            "Existieren Grenzwert-Überprüfungen?"
        ]),
        ("Sind die elektronischen Modelle kompatibel mit mechanischen und steuerungstechnischen Modellen?", [
            "Werden elektrische Signale synchron mit anderen Domänen simuliert?",
            "Gibt es gemeinsame Simulationsplattformen?"
        ]),
        ("Werden standardisierte Schnittstellen genutzt (z. B. OPC UA)?", [
            "Werden Protokolle wie OPC UA oder MQTT produktiv genutzt?",
            "Sind Kommunikationsfehler Teil der Simulation?"
        ]),
        ("Sind reale Elektronik-Komponenten in die Tests integriert?", [
            "Gibt es HIL-Tests für Elektronik?",
            "Werden reale Steuergeräte eingebunden?"
        ]),
        ("Gibt es Tests für die elektromechanische Interaktion?", [
            "Wird das Zusammenspiel mit Mechanik aktiv simuliert?",
            "Existieren Kopplungstests mit Bewegung und Aktorik?"
        ])
    ],
    "Steuerung": [
        ("Sind Steuerungsprogramme vollständig und getestet?", [
            "Gibt es Unit-Tests und Integrationstests?",
            "Werden automatisierte Tests bei Änderungen ausgeführt?"
        ]),
        ("Unterstützen die Steuerungssysteme Standards wie IEC 61131-3?", [
            "Werden alle Programmbausteine standardkonform umgesetzt?",
            "Gibt es eine Prüfung durch externe Tools?"
        ]),
        ("Ist die Steuerungslogik in einer Simulationsumgebung ausführbar?", [
            "Werden reale Szenarien simuliert?",
            "Gibt es Simulationsmodelle für alle Steuerfunktionen?"
        ]),
        ("Werden HIL-Tests (Hardware-in-the-Loop) verwendet?", [
            "Gibt es automatisierte HIL-Testpläne?",
            "Werden reale Steuergeräte über Simulation angesteuert?"
        ]),
        ("Sind die Steuerungssysteme mit mechanischen und elektronischen Modellen verbunden?", [
            "Laufen alle Systeme synchronisiert?",
            "Wird Timingverhalten realistisch abgebildet?"
        ]),
        ("Unterstützen die Steuerungen industrielle Kommunikationsprotokolle (z. B. Profinet, EtherCAT)?", [
            "Werden mehrere Protokolle simultan getestet?",
            "Sind Protokolle konfigurierbar und dokumentiert?"
        ]),
        ("Wurden Steuerungssysteme in realitätsnahen Szenarien getestet?", [
            "Existieren automatisierte Testszenarien?",
            "Gibt es Regressionstests für Updates?"
        ]),
        ("Gibt es ein Fehlerprotokoll für die Steuerungsvalidierung?", [
            "Werden Fehler automatisch erkannt und protokolliert?",
            "Existieren Maßnahmenvorschläge im Protokoll?"
        ])
    ]
}

class ChecklisteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkliste VIBN – Scrollbar-Version")

        # Scrollbar Setup
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variablen vorbereiten
        self.haupt_vars = {}
        self.folge_vars = {}
        self.folgewidgets = {}
        self.gewichtungen = {}

        row = 0
        for bereich, fragen in fragenbereiche.items():
            frame = tk.LabelFrame(self.scroll_frame, text=f"Bereich: {bereich}", padx=10, pady=5)
            frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            self.haupt_vars[bereich] = []
            self.folge_vars[bereich] = []
            self.folgewidgets[bereich] = []

            tk.Label(frame, text="Gewichtung (z. B. 1.0):").pack(anchor="w")
            gewicht_var = tk.DoubleVar(value=1.0)
            tk.Entry(frame, textvariable=gewicht_var, width=5).pack(anchor="w")
            self.gewichtungen[bereich] = gewicht_var

            for frage, folgen in fragen:
                rahmen = tk.Frame(frame)
                rahmen.pack(anchor="w", fill="x")
                var = tk.BooleanVar()
                cb = tk.Checkbutton(rahmen, text=frage, variable=var,
                                    command=lambda v=var, f=folgen, b=bereich, r=rahmen: self.toggle_folge(v, f, b, r))
                cb.pack(anchor="w")
                fvars = [tk.BooleanVar() for _ in folgen]
                self.haupt_vars[bereich].append(var)
                self.folge_vars[bereich].append(fvars)
                self.folgewidgets[bereich].append([])

            row += 1

        tk.Button(self.scroll_frame, text="Auswertung", command=self.auswerten).grid(row=row, column=0, pady=10)

        # Optional: Maus-Scroll aktivieren (nur Windows/Mac)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def toggle_folge(self, hauptvar, folgetexte, bereich, rahmen):
        index = [i for i, v in enumerate(self.haupt_vars[bereich]) if v == hauptvar][0]
        if hauptvar.get():
            for i, ftext in enumerate(folgetexte):
                cb = tk.Checkbutton(rahmen, text="   ↪ " + ftext, variable=self.folge_vars[bereich][index][i], wraplength=600)
                cb.pack(anchor="w", padx=20)
                self.folgewidgets[bereich][index].append(cb)
        else:
            for cb in self.folgewidgets[bereich][index]:
                cb.destroy()
            self.folgewidgets[bereich][index].clear()

    def auswerten(self):
        summary = ""
        gesamt_score = 0
        gesamt_gewicht = 0

        for bereich in fragenbereiche:
            erreicht = 0
            gesamt = 0
            for i, var in enumerate(self.haupt_vars[bereich]):
                if var.get():
                    erreicht += 1
                gesamt += 1
                for fvar in self.folge_vars[bereich][i]:
                    gesamt += 1
                    if fvar.get():
                        erreicht += 1

            gewicht = self.gewichtungen[bereich].get()
            prozent = round((erreicht / gesamt) * 100) if gesamt > 0 else 0

            if prozent >= 80:
                stufe = 5
            elif prozent >= 60:
                stufe = 4
            elif prozent >= 40:
                stufe = 3
            elif prozent >= 20:
                stufe = 2
            else:
                stufe = 1

            summary += f"{bereich}: {prozent}% (Gewichtung: {gewicht}) → Stufe {stufe}\n"
            gesamt_score += prozent * gewicht
            gesamt_gewicht += gewicht

        if gesamt_gewicht > 0:
            gesamt_prozent = round(gesamt_score / gesamt_gewicht)
            messagebox.showinfo("Gesamtauswertung", f"{summary}\nGesamtbewertung: {gesamt_prozent}%")
        else:
            messagebox.showwarning("Fehler", "Keine Gewichtung gesetzt.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklisteApp(root)
    root.mainloop()
