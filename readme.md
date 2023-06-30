# Goldstandard-Korpus-Evaluation als Methode digitaler Quellenkritik in den Geschichtswissenschaften am Beispiel des Open-Discourse-Korpus der Bundestagsprotokolle

tl;dr: Die in dieser Arbeit entwickelte Goldstandard-Korpus-Evaluation ermöglicht eine teil-automatisierte Stichproben-Untersuchung, die starke strukturelle Mängel im Bundestags-Redebeitrags-Korpus Open Discourse offenbart und die Relevanz neuer Methoden digitaler Quellenkritik zeigt.

Das vollständige Jupyter Book gibt es hier: http://paulramisch.github.io/gold-standard-corpus-evaluation  


## Datenvorbereitung
Auf der [Open-Data-Seite](https://www.bundestag.de/services/opendata) des Bundestags müssen die Stammdaten heruntergeladen werden und in `data/raw/MDB_STAMMDATEN.XML`gelegt werden.

Um die verschiedenen Open-Discourse-Analysen durchzuführen, werden deren [Feather-Dateien benötigt. Diese sind im Havard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/FIKIBO) abgelegt und müssen im Ordner `data/open_discourse` abgelegt werden.

Danach sieht die Datenstruktur folgendermaßen aus:

data/
├── open_discourse/
│   ├── contributions_extended.pkl
│   ├── contributions_simplified.pkl
│   ├── factions.feather
│   ├── politicians.feather
│   ├── speeches.feather
│   └── speeches.pkl
└── raw/
    └── MDB_STAMMDATEN.XML

## Durchführung
Alle weiteren 