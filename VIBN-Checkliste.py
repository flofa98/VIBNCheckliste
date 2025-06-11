import tkinter as tk
from tkinter import messagebox

# Fragenstruktur
bereiche = {
    "Mechanik": [
        "Sind mechanische Modelle vollständig und aktuell?",
        "Werden CAD-Daten in die Simulation integriert?",
        "Sind Mechanik-Modelle für digitale Zwillinge geeignet?",
        "Ist die mechanische Simulation ausreichend detailliert?",
        "Gibt es eine konsistente Abstraktionsebene für mechanische Modelle?",
        "Sind die mechanischen Modelle mit anderen Disziplinen kompatibel?",
        "Unterstützen die Tools Standards wie STEP oder AutomationML?",
        "Wurde die mechanische Simulation mit realen Daten überprüft?",
        "Gibt es ein Testprotokoll für mechanische Validierungen?"
    ],
    "Elektronik": [
        "Sind elektrische Schaltpläne und Layouts aktuell und digital verfügbar?",
        "Unterstützen die Modelle Datenstandards wie EPLAN?",
        "Ist die elektrische Simulation detailliert genug?",
        "Sind Signalflüsse und Stromlasten simuliert?",
        "Sind die elektronischen Modelle kompatibel mit mechanischen und steuerungstechnischen Modellen?",
        "Werden standardisierte Schnittstellen genutzt (z. B. OPC UA)?",
        "Sind reale Elektronik-Komponenten in die Tests integriert?",
        "Gibt es Tests für die elektromechanische Interaktion?"
    ],
    "Steuerung": [
        "Sind Steuerungsprogramme vollständig und getestet?",
        "Unterstützen die Steuerungssysteme Standards wie IEC 61131-3?",
        "Ist die Steuerungslogik in einer Simulationsumgebung ausführbar?",
        "Werden HIL-Tests (Hardware-in-the-Loop) verwendet?",
        "Sind die Steuerungssysteme mit mechanischen und elektronischen Modellen verbunden?",
        "Unterstützen die Steuerungen industrielle Kommunikationsprotokolle (z. B. Profinet, EtherCAT)?",
        "Wurden Steuerungssysteme in realitätsnahen Szenarien getestet?",
        "Gibt es ein Fehlerprotokoll für die Steuerungsvalidierung?"
    ]
}

class VIBNAuswertungApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtuelle Inbetriebnahme – Checkliste")

        self.antworten = {}
        self.gewichtungen = {}
        self.vars = {}

        row = 0
        for bereich, fragen in bereiche.items():
            tk.Label(root, text=bereich, font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w")
            row += 1
            self.gewichtungen[bereich] = tk.DoubleVar(value=1.0)
            tk.Label(root, text="Gewichtung:").grid(row=row, column=0, sticky="e")
            tk.Entry(root, textvariable=self.gewichtungen[bereich], width=5).grid(row=row, column=1, sticky="w")
            row += 1
            self.vars[bereich] = []
            for frage in fragen:
                var = tk.BooleanVar()
                tk.Checkbutton(root, text=frage, variable=var, wraplength=600).grid(row=row, column=0, columnspan=2, sticky="w")
                self.vars[bereich].append(var)
                row += 1
            row += 1

        tk.Button(root, text="Auswertung", command=self.auswerten).grid(row=row, column=0, pady=10)
        self.ergebnis_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.ergebnis_label.grid(row=row, column=1)

    def auswerten(self):
        gesamt_score = 0
        gesamt_gewicht = 0
        text_ergebnis = ""

        for bereich in bereiche:
            antworten = [v.get() for v in self.vars[bereich]]
            score = sum(antworten) / len(antworten)
            gewicht = self.gewichtungen[bereich].get()
            gesamt_score += score * gewicht
            gesamt_gewicht += gewicht
            prozent = round(score * 100)
            text_ergebnis += f"{bereich}: {prozent}%\n"

        if gesamt_gewicht > 0:
            gesamt_prozent = round((gesamt_score / gesamt_gewicht) * 100)
            text_ergebnis += f"\nGesamtbewertung: {gesamt_prozent}%"
            self.ergebnis_label.config(text=f"{gesamt_prozent}%")
            messagebox.showinfo("Auswertung", text_ergebnis)
        else:
            messagebox.showwarning("Fehler", "Gewichtungen dürfen nicht alle 0 sein.")

# Start
root = tk.Tk()
app = VIBNAuswertungApp(root)
root.mainloop()
