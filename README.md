# Finance Tracker

## Projektbeschreibung

Finance Tracker ist eine Webanwendung, die es Benutzern ermöglicht, ihre Ausgaben und Einnahmen zu protokollieren und zu visualisieren. Die Anwendung enthält ein Login-System zur Verwaltung der Benutzerdaten.

## Zweck

Der Zweck dieser Anwendung ist es, Benutzern zu helfen, ihre Finanzen zu protokollieren und zu visualisieren, um Trends zu erkennen und bessere finanzielle Entscheidungen zu treffen.

## Funktionen

Der Benutzer kann die folgenden Aktionen ausführen:

- **Ausgaben und Einnahmen hinzufügen**: Benutzer können ihre finanziellen Transaktionen hinzufügen und verwalten.
- **Finanzdaten visualisieren**: Benutzer können ihre Finanzdaten in Form von Diagrammen und Grafiken visualisieren.
- **Benutzer-Login und -Registrierung**: Benutzer können sich registrieren und anmelden, um ihre Daten sicher zu speichern.

## Verwendete Technologien

Dieses Projekt wurde mit den folgenden Technologien entwickelt:

- **Python**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **CSS**
- **Jinja**
- **FlaskForms**

## Bilder

Screenshots des Projekts:

![Bild 1](img/bild1.png)
_Bild 1: Hauptseite der Anwendung_

![Bild 2](img/bild2.png)
_Bild 2: Visualisierung der Finanzdaten_

![Bild 3](img/bild3.png)
_Bild 3: Benutzer-Login-Seite_

## Installation und Nutzung

Um dieses Projekt zu installieren und zu nutzen, folgen Sie diesen Schritten:

1. **Repository klonen**:
   ```bash
   git clone https://github.com/GregorPorsch/FinanceTracker.git
   ```
2. **In das Projektverzeichnis wechseln**:
   ```bash
   cd finance-tracker
   ```
3. **Virtuelle Umgebung erstellen und aktivieren**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Datenbank initialisieren**:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. **Projekt starten**:
   ```bash
   flask run
   ```
