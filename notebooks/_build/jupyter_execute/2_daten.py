#!/usr/bin/env python
# coding: utf-8

# # 2 Quellengrundlage & Daten: Bundestagsprotokolle & Open Discourse
# Im Folgenden werden die Plenarprotokolle, die der Bundestag als Open Data bereitstellt, sowie das Open-Discourse-Korpus vorgestellt und ersten quellenkritischen Untersuchungen unterzogen. Dabei liegt der Fokus sowohl auf der Entstehung als Quelle, als auch auf deren Digitalisierung und weiterer Verarbeitung. Zudem werden die Modellierung und Strukturierung der Daten untersucht, wobei auf die daraus resultierenden Schwierigkeiten eingegangen wird. Dies bildet die notwendige Vorbereitung für die Durchführung der Goldstandard-Korpus-Analyse.
# 
# <a id="2-1"></a>
# ## 2.1 Plenarprotokolle des Bundestags als Open Data
# Im Deutsche Bundestag kommen die demokratisch gewählten Abgeordneten zusammen, um Gesetze zu diskutieren und zu verabschieden. Dieser Prozess findet zu einem großen Teil in verschiedenen Unterausschüssen statt, die Abstimmungen und wichtigen Diskussionen passieren dagegen in den Plenarsitzungen. Aus diesem Grund sind die Protokolle eine äußerst wichtige Quelle für die Geschichte der Bundesrepublik.
# 
# ### 2.1.1 Plenarsitzungen und -Protokolle
# Die Verhandlungen des Deutschen Bundestags finden öffentlich statt, nur mit einer Zweidrittelmehrheit kann die Öffentlichkeit ausgeschlossen werden.[[1]](#ref_1) Zu jeder Sitzung wird ein Plenarprotokoll erstellt.[[2]](#ref_2) Diese Protokolle werden von dem hauseigenen stenografischen Dienst des Deutschen Bundestags angefertigt. Ein Protokoll „entspricht in der Regel nicht völlig dem Wortlaut einer Rede. Mit Blick auf die Schriftsprache findet eine gewisse sprachlich-stilistische Glättung des mündlich Gesprochenen statt bis hin zur Korrektur offensichtlicher Versprecher.“[[3]](#ref_3) Nach einer Debatte haben die Sprecher:innen zwei Stunden Zeit, um die Niederschriften zu prüfen und Fehler vor der Veröffentlichung des Protokolls korrigieren zu lassen. Bereits veröffentlichte Fehler können allerdings auch in späteren Protokollen noch richtig gestellt werden.[[4]](#ref_4) 
# 
# Die grundsätzliche Struktur eines Plenarprotokolls hat sich seit 1949 nicht geändert und steht in einer direkten Tradition der Protokolle des Reichstags in der Weimarer Republik:
# 1. **Inhaltsverzeichnis:** Auflistung der Tagesordnungspunkte
# 2. **Hauptteil**: Redebeiträge
# 3. **Anlagen zum Stenografischen Bericht:** Die erste Anlage bildet die Anwesenheitsliste beziehungsweise die Liste entschuldigter Abgeordneter, weitere Anhänge sind beispielsweise schriftliche Antworten in Fragestunden.
# 
# Im Bundestag dürfen dem Grundgesetz folgend nur Abgeordnete sowie Vertreter:innen der Bundesregierung und des Bundesrats sprechen. Sofern Gäste im Bundestag eine Rede halten, wie beispielsweise Wladimir Putin im September 2001, findet dies offiziell außerhalb der Plenarsitzung statt und ist inzwischen auch nicht mehr Teil der Plenarprotokolle.[[5]](#ref_5) Obwohl es hierfür keine Rechtsgrundlage gab, sind in den Protokollen jedoch einige Beispiele für Reden ausländischer Gäste vorhanden, z. B. die des britischen Abgeordneten Arthur Woodburn 1951 oder des französischen Präsidenten François Mitterrand 1983 [(01163, S. 6603)](https://dserver.bundestag.de/btp/01/01163.pdf) oder des französischen Präsidenten François Mitterrand 1983 [(09142, S. 8978)](https://dserver.bundestag.de/btp/09/09142.pdf).
# 
# In dieser Arbeit bezeichnen die Begriffe Bundestagsprotokoll, Plenarprotokoll und Protokoll synonymhaft jeweils ein einzelnes Protokoll einer Plenarsitzung (oder Session) des Deutschen Bundestags. Hauptsächlich wird der Begriff Redebeitrag anstatt Rede verwendet, da auch die meist kurzen Moderationsbeiträge der Sitzungsleitung darin enthalten sind. Zwischenrufe sind keine Redebeiträge, sondern bilden eine eigene Kategorie. Diese sind erlaubt, als Redebeitrag zählt jedoch nur, wenn der:die Redner:in offiziell das Wort hat. Für den Verweis auf die einzelnen Protokolle wird die fünfstellige Nummerierung des Bundestags verwendet. Dabei kennzeichnen die ersten beiden Ziffern die (Legislatur-)Periode und die letzten drei Ziffern die Protokollnummer innerhalb der Periode. So steht beispielsweise die Referenznummer 01001 für die erste Sitzung der ersten Wahlperiode, 13145 für die 145. Sitzung in der 13. Periode.
# 
# ### 2.1.2 Open Data
# Seit spätestens 2017 stellt der Bundestag auf einem Open-Data-Portal alle seit 1949 entstandenen Protokolle im PDF- und XML-Format bereit.[[6]](#ref_6) Zu diesem Zweck hat der Bundestag bereits seit Januar 1996 eine eigene Website.[[7]](#ref_7) In der *Wayback Machine* des Internet Archive findet sich der erste Crawl der Bundestagswebsite für den 19. Oktober 1996, zu diesem Zeitpunkt sind neun Protokolle (das erste für den 13. September 1996) online abrufbar.[[8]](#ref_8) Seitdem wurden die Protokolle weiter ergänzt, seit Februar 2006 ließen sich Protokolle ab Juni 1975 (7. Periode) als PDF-Datei abrufen.[[9]](#ref_9) Seit März 2013 ist ein PDF-Zugriff auf sämtliche Plenarprotokolle möglich.[[10]](#ref_10) Vorausgegangen war die Verabschiedung des E-Government-Gesetzes, dass einerseits die Bereitstellung von Regierungs-Dokumenten und -Daten von öffentlichen Interesse in maschinenlesbarer Form vorgibt, wie auch deren uneingeschränkte Nutzung und Verwertung erlaubt.[[11]](#ref_11) Der erste Snapshot im Internet Archive der heute verfügbaren Open-Data-Seite des Bundestages mit allen Protokollen im PDF- und XML-Format ist von Oktober 2017. Diese Seite wird fortlaufend um aktuelle Protokolle erweitert.
# 
# An dieser Stelle ist ein Blick in die Meta-Daten der Dateien spannend, um mehr über deren Entstehung herauszufinden, hier an einer Stichprobe je zweier Protokolle aus den Perioden 1-19:

# In[1]:


from PyPDF2 import PdfReader
import pandas as pd
from datetime import datetime as dt
from IPython.display import display, HTML
import os

# Funktion um PDF-Metadaten auszulesen
def get_pdf_meta_data(minute):
    reader = PdfReader("../data/evaluation/pdf/" + minute + ".pdf")
    return reader.metadata

# Erstellung der Tabelle mit den Protokoll-Metadaten
# Zeitangaben in UTC
meta_data_columns = ['Protokoll', 'PDF erstellt', 'PDF zuletzt geändert', 'PDF Anwendung', 'PDF erstellt mit', 'XML zuletzt geändert']
df_meta_data =  pd.DataFrame(columns = meta_data_columns)

# Iteriere über die einzelnen Protokolle (eng. Minute) aus der Stichprobe
minute_sample = ["01020", "01229", "02087", "02202", "03018", "03103", "04015", "04184", "05101", "05158", 
                 "06017", "06185", "07118", "07140", "08025", "08080", "09014", "09126", "10061", "10213", 
                 "11102", "11124", "12037", "12152", "13176", "13217", "14145", "14150", "15058", "15077", 
                 "16002", "16133", "17036", "17248", "18014", "18088", "19021", "19180"]

for minute in minute_sample:
    metadata = get_pdf_meta_data(minute)
    metadata = pd.DataFrame([[minute, 
                              dt.strptime(metadata.getText("/CreationDate").replace("'", "")[:16], "D:%Y%m%d%H%M%S"),
                              dt.strptime(metadata.getText("/ModDate").replace("'", "")[:16], "D:%Y%m%d%H%M%S"),
                              metadata.getText("/Creator"),
                              metadata.getText("/Producer"),
                              dt.utcfromtimestamp(int(os.path.getmtime("../data/evaluation/raw/" + minute + ".xml"))).strftime('%Y-%m-%d %H:%M:%S')
                             ]], columns=meta_data_columns)
    df_meta_data = pd.concat([df_meta_data, metadata], ignore_index=True)

display(HTML("<div style='height: 500px; overflow:scroll-y'>"+df_meta_data.to_html()+"</div>"))


# Bei den Protokollen der Perioden 1-13 liegt das Erstellungsdatum für die PDFs zwischen Mitte 2011 und Mitte 2012, die letzte Änderung in der Regel bis Mitte 2012, teils auch im Jahr 2014. Dabei wurden die Dateien sukzessive von der 13. Periode aus zurückgehend bearbeitet. Das hierfür benutzte Programm ist stets die Software OmniPage 17. Während für die PDFs die Zeitstempel-Meta-Daten in die Datei eingebettet sind, ist dies bei den XML-Dateien nicht der Fall. Dementsprechend ist diese Information mit Vorsicht zu handhaben, da sie beispielsweise durch einen Kopier- oder Downloadvorgang neu gesetzt werden kann.
# 
# Die Protokolle ab der 14. Periode liegen hinsichtlich ihres Erstellungsdatums nah am ursprünglichen Tag der Sitzung, wobei häufig Bearbeitungen vorgenommen wurden; interessant ist auch das Fortschreiten der benutzten Tools beispielsweise durch die verschiedenen Adobe Distiller Versionen von 4.0 bis 10.1.2.

# #### 2.1.2.1 Datei-Struktur
# Die Bereitstellung der Daten im XML-Format bedeutet nur sehr eingeschränkt eine zusätzliche Datenqualität: Für Protokolle bis 2017 enthalten diese, abgesehen von einigen Meta-Informationen, den technisch komplett unstrukturierten Text. Die Dokumente besitzen damit keinerlei technische Abgrenzungen in die verschiedenen Bestandteile wie Inhaltsverzeichnis, Hauptteil, Anhang oder die einzelnen Tagesordnungspunkte und Reden. So ähneln alle XML-Dokumente der Perioden 1 - 18, diesem Ausschnitt des 3. Protokolls der ersten Periode [(01003)](https://dserver.bundestag.de/btp/01/01003.pdf):
# 
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE DOKUMENT SYSTEM "BUNDESTAGSDOKUMENTE.dtd">
# <DOKUMENT>
#   <WAHLPERIODE>1</WAHLPERIODE>
#   <DOKUMENTART>PLENARPROTOKOLL</DOKUMENTART>
#   <NR>01/3</NR>
#   <DATUM>15.09.1949</DATUM>
#   <TITEL>Plenarprotokoll vom 15.09.1949</TITEL>
#   <TEXT>Deutscher Bundestag — 3. Sitzung. Bonn, Donnerstag, den 15. September 1949	13
# 3. Sitzung.
# Bonn, Donnerstag, den 15. September 1949. Mitteilungen:
# Geschäftliches 	 13B, 14A
# Schreiben des Bundespräsidenten, betreffend Verzicht auf seinen Sitz als
# Abgeordneter im Bundestag . . . 	 13B
# Eintritt der Frau Abgeordneten Hütter
# in den Bundestag 	 13B
# Bildung der Gruppe „Nationale Rechte"
# im Bundestag 	 13B
# Wahl des Bundeskanzlers 	 13C
# Dr. Adenauer nimmt die Wahl als Bundeskanzler an 	 14C
# Nächste Sitzung 	 14C
# Die Sitzung wird um 11 Uhr 6 Minuten durch den Präsidenten Dr. Köhler eröffnet.
# Präsident Dr. Köhler: Meine Damen und Herren! Ich eröffne die 3. Sitzung des Deutschen Bundestags.
# Die Tagesordnung liegt Ihnen vor. Wir treten in die Tagesordnung ein. Punkt 1:
# Mitteilungen.
# ```
# 
# Seit 2017, respektive Periode 19, werden die Plenarprotokolle im XML-Format mit einer eigens entwickelten Dokumenttypdefinition (DTP) angelegt. Für jeden Sitzungstag liegt weiterhin eine XML-Datei vor. Die verschiedenen Arten von Redebeiträgen sind in diesem Format nun voneinander abgegrenzt und mit den Metadaten des:der Redner:in versehen. Wie diese Struktur definiert ist, lässt sich in der als Open Data bereitgestellten Dokumentation dieser Plenarprotokoll-DTD nachlesen.[[13]](#ref_13) Die DTD unterscheidet sich dabei von der in der in den Geisteswissenschaften und Archiven verbreiteten DTD der Text Encoding Initiative (TEI). 
# 
# Die ersten 25 Zeilen der ersten Sitzung in der 19. Periode sehen etwas anders aus als die früherer Perioden:
# ```xml
# <?xml version="1.0" encoding="UTF-8"?>
# <?xml-stylesheet href="dbtplenarprotokoll.css" type="text/css" charset="UTF-8"?>
# <!DOCTYPE dbtplenarprotokoll SYSTEM "dbtplenarprotokoll.dtd">
# <dbtplenarprotokoll herstellung="Satz: Satzweiss.com Print, Web, Software GmbH, Mainzer Straße 116, 66121 Saarbrücken, www.satzweiss.com, Druck: Printsystem GmbH, Schafwäsche 1-3, 71296 Heimsheim, www.printsystem.de" sitzung-datum="24.10.2017" sitzung-ende-uhrzeit="17:03" sitzung-naechste-datum="22.11.2017" sitzung-nr="1" sitzung-start-uhrzeit="11:00" start-seitennr="1" vertrieb="Bundesanzeiger Verlagsgesellschaft mbH, Postfach 1 0 05 34, 50445 Köln, Telefon (02 21) 97 66 83 40, Fax (02 21) 97 66 83 44, www.betrifft-gesetze.de" wahlperiode="19">
#   <vorspann>
#     <kopfdaten>
#       <plenarprotokoll-nummer>Plenarprotokoll <wahlperiode>19</wahlperiode>/<sitzungsnr>1</sitzungsnr></plenarprotokoll-nummer>
#       <herausgeber>Deutscher Bundestag</herausgeber>
#       <berichtart>Stenografischer Bericht</berichtart>
#       <sitzungstitel><sitzungsnr>1</sitzungsnr>. Sitzung</sitzungstitel>
#       <veranstaltungsdaten><ort>Berlin</ort>, <datum date="24.10.2017">Dienstag, den 24. Oktober 2017</datum></veranstaltungsdaten>
#     </kopfdaten>
#     <inhaltsverzeichnis>
#       <ivz-titel>Inhalt:</ivz-titel>
#       <ivz-eintrag>
#         <ivz-eintrag-inhalt><redner id="11002190"><name><vorname>Alterspräsident Dr. Hermann</vorname><nachname>Otto Solms</nachname><rolle><rolle_lang>Alterspräsident</rolle_lang><rolle_kurz>Alterspräsident</rolle_kurz></rolle></name></redner>Alterspräsident Dr. Hermann Otto Solms</ivz-eintrag-inhalt>
#         <xref div="A" pnr="1" ref-type="rede" rid="ID19100100">
#           <a href="S1" typ="druckseitennummer"><seite>1</seite> <seitenbereich>A</seitenbereich></a>
#         </xref>
#       </ivz-eintrag>
#       <ivz-block>
#         <ivz-block-titel>Tagesordnungspunkt 1:</ivz-block-titel>
#         <ivz-eintrag>
#           <ivz-eintrag-inhalt>Eröffnung der Sitzung durch den Alterspräsidenten Drucksache 19/2 </ivz-eintrag-inhalt>
#           <a href="S1" typ="druckseitennummer"><seite>1</seite> <seitenbereich>C</seitenbereich></a>
# ```
# 
# Dabei hat jede Rede eine eigene ID, der einleitende Redner ist mit Meta-Informationen versehen, hier illustriert an den ersten drei XML-Zeilen der Rede von Carsten Schneider in der gleichen Sitzung:
# 
# ```xml
# <rede id="ID19100300">
#     <p klasse="redner"><redner id="11003218"><name><vorname>Carsten</vorname><nachname>Schneider</nachname><fraktion>SPD</fraktion><ortszusatz>(Erfurt)</ortszusatz></name></redner>Carsten Schneider (Erfurt) (SPD):</p>
#     <p klasse="J_1">Sehr geehrter Herr Präsident! Sehr geehrte Kolleginnen und Kollegen! Mit der heutigen Konstituierung nimmt der Deutsche Bundestag zum 19. Mal seine Arbeit auf. Er ist die wichtigste Institution im Parlamentarismus in Deutschland, und er ist zugleich die Herzkammer unserer Demokratie; denn nur wir Abgeordneten sind vom Volk gewählt und damit unmittelbar legitimiert.</p>
# ```
# 
# Genau diese Informationen fehlen in den Protokollen bis 2017 und machen es in dieser Form unmöglich, die Reden hinsichtlich bestimmter Personen oder Fraktionen statistisch zu untersuchen: Abgesehen von grundsätzlichen Meta-Daten im XML-Header wie das Datum und die Nummer der Sitzung, liegen nur unstrukturierte Texte vor. Einzelne Redebeiträge lassen sich nicht durch die technische Struktur der Datei erkennen und es lässt sich nicht automatisiert verarbeiten, wer was gesagt hat. Für Menschen, die den Fließtext lesen, ist dies kein Problem; jede Rede beginnt mit Namen, Titel, Partei und Funktion der sprechenden Person. Automatisierte Analysen gelangen dadurch jedoch schnell an ihre Grenzen. So ließe sich zwar nach Schlagwörtern suchen, aber nicht nach Person, Partei, Funktion oder Eigenschaften der Personen (z. B. Alter, Beruf, Geschlecht, Wohnort) filtern.
# 
# #### 2.1.2.2 OCR & PDF-Extraktion
# Neben dem bereits beschriebenen Unterschied zwischen den Perioden hinsichtlich ihrer XML-Auszeichnung variieren die Protokolle bis 2017 zusätzlich angesichts ihres Ausgangsmaterials. Zwar sind alle Rohtexte aus PDF-Dokumenten extrahiert, für die erste Periode 1949 bis zum Ende der 13. Periode im Herbst 1998 basieren diese PDF-Dokumente jedoch auf Scans. Seit der 14. Periode liegen hierfür born-digital PDF-Dokumente zugrunde.
# 
# Dies führt zu einem entscheidenden Unterschied: Die früheren Protokolle sind mithilfe von automatischer Texterkennung (OCR) auf Basis der Scans entstanden. Leider ist der Entstehungsprozess der XML-Dateien und damit auch das OCR nicht öffentlich dokumentiert worden, trotzdem lassen sich aus den bestehenden Daten Rückschlüsse auf die Vorgehensweise ziehen. Die Dokumenteigenschaften der Scan-PDFs weisen als Erstellungssoftware das OCR-Programm OmniPage 17 aus.

# Das 2009 erschienene OmniPage 17 konnte einerseits bestehende Bild- und Scandateien importieren oder direkt scannen und automatisiert mit OCR- und Layouterkennung verarbeiten. Die offizielle Feature-Liste des Herstellers erklärt selbstbewusst „OmniPage delivers unprecedented accuracy at a level greater than 99% for over 120 different languages.“[[13]](#ref_13) In der Bedienungsanleitung der Software zeigen sich umfangreiche Funktionen, von automatisierten OCR-Scans bis hin zu umfangreichen Korrekturfunktionen bei unklaren Stellen in den OCR-Texten. Neben vorhandenen Wörterbüchern lässt sich auch ein eigenes Wörterbuch ergänzen, um die Erkennung zu verbessern.[[14]](#ref_14) Eine unabhängige und vergleichbare Evaluation der OCR-Qualität von OmniPage gibt es leider nicht.[[15]](#ref_15) Hinzu kommt, dass ohne die vorliegende Dokumentation des Entstehungskontextes, beispielsweise ob eine Korrektur stattgefunden hat, solche Leistungszahlen wenig aussagekräftig wären.
# 
# 
# Es gibt starke Hinweise darauf, dass ein eigenes Wörterbuch mit den Namen der Abgeordneten ergänzt wurde. Der später in dieser Arbeit erläuterte Zuordnungsprozess von Reden zu den Abgeordneten auf Basis der OCR gescannten Namensangabe hat nur wenige Probleme, dennoch gibt es einige Fehlerkennungen und auch Sonderfälle, die auf dieses Wörterbuch-Vorgehen zurückzuführen ist: So wird der Name des Abgeordneten *Kißlinger* in der Stichprobe an einer Stelle fälschlich als *Kißiinger* erkannt ([(10213, S. 16408)](https://dserver.bundestag.de/btp/10/10213.pdf)). In den Stammdaten wird der Abgeordnete als *Karl Kisslinger* geführt, die Version *Kißlinger* war offenbar nicht in dem Wörterbuch enthalten. Bei den 65 weiteren Abgeordneten mit einem Eszett im Namen gab es in der Stichprobe keine derartigen Schwierigkeiten. Die häufigsten OCR-Fehler betreffen die Unterscheidung zwischen den Buchstaben i und l, beispielsweise wird *Dr. Spöri (SPD)* [(10213, S. 16305)](https://dserver.bundestag.de/btp/10/10213.pdf), fälschlich als *Spörl* erkannt, der Name eines Abgeordneten der CSU; im gleichen Dokument [(10213, S. 16424)](https://dserver.bundestag.de/btp/10/10213.pdf) erhielt der CDU-Abgeordnete *Broll* den neuen Nachnamen *Broil* im OCR-Text.
# 
# 
# Auch die Unterscheidung zwischen Umlauten und deren korrespondierenden Vokalen ist ein Fehlerfeld, beispielsweise bei Staatssekretär *Bölling*, der einmal als *Boiling* [(08025, S. 1704)](https://dserver.bundestag.de/btp/08/08025.pdf) und *Balling* erkannt wird [(08025, S. 1705)](https://dserver.bundestag.de/btp/08/08025.pdf). Der Staatssekretär *Hopf* fällt ebenfalls einem Wort aus dem englischen Wortschatz zum Opfer und erhält im OCR-Text den Namen der nordamerikanischen indigenen Gruppe der *Hopi* [(04105, S. 446)](https://dserver.bundestag.de/btp/04/04015.pdf). Der Staatssekretär Schütz wird bei seinen neun Redebeiträgen als Schutz erkannt [(05101, S. 4683ff.)](https://dserver.bundestag.de/btp/05/05101.pdf). Das sich die Beobachtungen von OCR-Fehlern hier auf Staatssekretäre fokussieren, ist kein Zufall, da diese nicht in den Abgeordneten-Stammdaten des Bundestags enthalten sind, sofern sie nicht gleichzeitig Abgeordnete sind.
# 
# Analog zu der zuverlässigen Erkennung von Namen, die in dem Zusatz-Wörterbuch enthalten sind, ist auch die allgemeine Textqualität recht hoch. Während im weiteren Verlauf dieser Arbeit zwar die Namenserkennung systematisch untersucht wird, wird der Text selbst nicht entsprechend bearbeitet. Dabei dürften innerhalb der Redebeiträge vor allem Namen von Personen, Unternehmen, Organisationen und Orten nicht immer richtig erkannt werden aufgrund der dargelegten Wörterbuchthematik. Dies hat beispielsweise für Untersuchungen, die ausschließlich nach Erwähnungen dieser Begriffe suchen wie auch für Anwendungen, in denen Named-Entity-Recognition-Techniken zum Einsatz kommen sollen, Auswirkungen.
# 
# In der Stichprobe funktioniert die Layouterkennung allgemein sehr gut, die Dokumente sind in der Regel zweispaltig formatiert, allerdings gibt es auch Probleme. So wurde in Protokoll 14145 die zentrierte Überschrift über der Eröffnung der Sitzung durch Vizepräsident Dr. Solms fälschlich der rechten Spalte zugeordnet und findet sich damit im Fließtext der Rede von Kurt Bodewig. Da diese Überschrift ansonsten ein guter Marker ist, um das Inhaltsverzeichnis von dem Hauptteil abzugrenzen, hat dies potenziell direkten Einfluss auf die daraus generierten Daten, da beispielsweise die ersten Redebeiträge abgeschnitten werden können.
# 
# #### 2.1.2.3 Allgemeine Datenqualität
# Um eine gute Datenqualität sicherzustellen, müssen auch die Meta-Daten stimmen und es dürfen keine Dubletten, in diesem Fall also doppelte Protokolle, in den Daten vorhanden sein. Die Meta-Daten in den vorliegenden XML-Dateien sind dabei nicht besonders umfangreich: die Wahlperiode, die Sitzungsnummer, das Sitzungsdatum und der Sitzungstitel – wobei Letzterer aus dem Sitzungsdatum generiert ist. Bei den Wahlperioden und den Sitzungsnummern gab es in der Untersuchung keine Auffälligkeiten, bei diesen scheinen keine Fehler vorzuliegen.
# 
# Zur Untersuchung der Datumsangabe und Dubletten sowie um Anomalien zu finden, kann die Gesamtheit der Datumsangaben automatisiert miteinander verglichen werden. Hierzu wird mit dem folgenden Code eine Tabelle aller Protokolle aus den Roh-XML-Dateien erstellt:

# In[2]:


import os, os.path
import pandas as pd
from lxml import etree
import datetime
from IPython.display import display, HTML

# Erstelle einer Übersichtstabelle
minutes_columns = ['period','nr','date','len', 'date_anomaly', 'datum_duplicate']
minutes = pd.DataFrame(columns=minutes_columns)

# Iteriere über alle Perioden
for period in range(1, 19):
    period_string = str(period).zfill(2)
    path = '../data/raw' + '/' + period_string
    count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])     
    
    # Iteriere über alle Protokolle innerhalb einer Periode
    for number in range (1, count + 1):
        number_string = str(number).zfill(3)
        file_path = path + '/' + period_string + number_string + '.xml'
        
        # Füge Informationen zu dem DataFrame hinzu
        if os.path.exists(file_path):
            root = etree.parse(file_path).getroot()
            date = datetime.datetime.strptime(root.find('DATUM').text, '%d.%m.%Y').date()
            len_xml = len(root.find('TEXT').text)
            
            minutes = pd.concat([minutes, 
                              pd.DataFrame([[period, number, date, len_xml, False, False]], columns=minutes_columns) ], 
                             ignore_index=True)


# Diese Tabelle aller Protokolle wird dann hinsichtlich Datums-Anomalien und -Dubletten untersucht:

# In[3]:


# Startvariable setzen
date = minutes.head(1).date.values[0]

# Iteriere über alle Protokolle
for index, minute in minutes.iterrows():
    # Untersuche alle Protokolle außer dem Ersten und Letzten
    if index > 0 and index < len(minutes) - 1:
        date_previous = date
        date = minute.date
        date_next = minutes.iloc[[index + 1]].date.values[0]
               
        if date < date_previous or date > date_next:
            minutes.at[index,'date_anomaly'] = True

        if date == date_previous or date == date_next:
            minutes.at[index,'datum_duplicate'] = True

# Tabelle nach Anomalien filtern
minutes_anomaly_filtered = minutes[minutes['date_anomaly']==True]
display(HTML(minutes_anomaly_filtered.to_html()))


# Eine Anomalie definiert sich hierbei dadurch, dass ein Protokoll entweder vor dem Datum des vorherigen oder nach dem Datum des darauffolgenden Protokolls liegt. Beides darf durch die Logik der Sitzungen, die jeweils zeitlich chronologisch folgen, nicht vorkommen. Dadurch konnten acht Protokolle mit Anomalien identifiziert werden. Bei diesen acht Protokollen handelt es sich jeweils um Paare, von denen je nur eines der beiden wirklich eine Anomalie ist, da ein falsches Datum durch den im Code angelegten Vergleich immer auch eine zweite Datei betrifft. Nach einem Blick in die Rohdaten zeigt sich, dass vier Protokolle ein falsches Datum in den Meta-Daten enthalten: 
# 
# |     Nummer    |     Angebendes Datum    |     Korrektes Datum    |     Abweichung    |
# |---------------|-------------------------|------------------------|-------------------|
# |     [01195](https://dserver.bundestag.de/btp/01/01195.pdf)     |     21.02.1952          |     21.02.1951         |     1 Jahr        |
# |     [02176](https://dserver.bundestag.de/btp/02/02176.pdf)     |     05.12.1956          |     05.11.1956         |     1 Monat       |
# |     [14021](https://dserver.bundestag.de/btp/14/14021.pdf)     |     24.02.1999          |     14.02.1999         |     10 Tage       |
# |     [15028](https://dserver.bundestag.de/btp/15/15028.pdf)     |     20.02.2003          |     20.12.2003         |     10 Monate     |
# 
# 
# Hinsichtlich der Dubletten wird es schwieriger, diese lassen sich nicht allein durch das Datum des Tages identifizieren:

# In[4]:


minutes_duplicates_filtered = minutes[minutes['datum_duplicate']==True]
print('Anzahl von Sitzung, die am gleichen Tag wie eine andere Sitzung stattfand (die Zahl zählt beide): ', len(minutes_duplicates_filtered))
display(HTML(minutes_duplicates_filtered.head(5).to_html()))


# Es gibt neunzig Protokolle für Sitzungen, die an Tagen mit mehr als einer Sitzung stattfanden. Ein Blick auf die Zahl der in der Datei enthaltenen Zeichen zeigt, dass eben nicht alle Dubletten sind, sondern sich einige lediglich den Tag mit einer weiteren Sitzung teilen. Die Sitzungen [01020](https://dserver.bundestag.de/btp/01/01021.pdf) und [01021](https://dserver.bundestag.de/btp/01/01020.pdf) sind dagegen tatsächlich Duplikate. Trotz der abweichenden Zeichenzahl und obwohl sie offenbar auf den gleichen Scans basieren, fehlen in Nr. 21 lediglich die Kopfzeilen, ansonsten sind beide identisch. Sie sind identisch, weil die Sitzungen zusammengehören: Die Überschrift in der gedruckten Version lautet „20. und 21. Sitzung“, der Grund in diesem Fall war eine fehlende Beschlussfähigkeit und eine darauffolgende Einberufung einer neuen Sitzung wenige Minuten später. In den XML-Dateien wurde in diesen Fällen – analog zu den PDF-Dateien – jeweils das komplette Dokument beider Sitzungen eingefügt. 
# 
# Um weiter herauszufinden, welche Sitzungen als Duplikate vorliegen, lässt sich die Liste filtern:

# In[5]:


minutes_duplicates_filtered.insert(5, 'len_duplicate',minutes_duplicates_filtered['len'])
minutes_duplicates_filtered.insert(2, 'nr_duplicate',minutes_duplicates_filtered['nr'])

# Groupieren nach Tag und Berechnung der relativen Abweichung
minutes_duplicates_filtered = minutes_duplicates_filtered.groupby(['date'], as_index=False).agg({'period': 'first', 'nr': 'first', 'nr_duplicate': 'last', 'date': 'first', 'len': 'first', 'len_duplicate': 'last'})
minutes_duplicates_filtered.insert(6, 'diff',minutes_duplicates_filtered['len']/minutes_duplicates_filtered['len_duplicate'])

# Filtern nach Abweichung
threshold = 0.025
minutes_duplicates_filtered = minutes_duplicates_filtered[(minutes_duplicates_filtered['diff'] < 1 + threshold) & (minutes_duplicates_filtered['diff'] > 1 - threshold)]
minutes_duplicates_filtered


# Die iterativ gefundene Maximalabweichung von 2,5 % hinsichtlich der Zeichenzahl zweier Dokumente führt zu einer Liste von 14 Tagen und damit 28 Protokollen, die doppelt vorhanden sind. Für all diese 14 Tage und 28 Protokolle kann mit einem  Blick in die Rohdaten verifiziert werden, dass diese tatsächlich Dubletten sind.
# 
# Die Dubletten sind für Close-Reading-Anwendungen kein Problem, da sich beim Lesen direkt erschließt, wo die neue Sitzung beginnt und auch eine genaue Abgrenzung in die eine oder die andere Nummer wohl zweitrangig ist. Als Rohdaten für eine automatisierte Verarbeitung ist hierbei jedoch Vorsicht geboten. Bei insgesamt 4106 Protokolle bis Ende 2017, haben diese 28 Protokolle nur einen geringen Anteil, in der ersten Periode betreffen sie aber immerhin über 4 % der Protokolle.
# 
# Ein schmales Fehlerfeld betrifft zudem Protokolle für Debatten, die über mehr als einen Tag andauern. Während ein Überziehen bis nach Mitternacht, eine Praxis, die nach der zweiten Periode nur noch vereinzelt vorkommt, meist nur durch die entsprechende Schlussuhrzeit erkennbar ist, wurde in einigen wenigen Fällen der zweite Tag in den Titel aufgenommen, dadurch wurden folgende drei Protokolle mit einem falschen Datum versehen:[[16]](#ref_16)
# 
# * [01018](https://dserver.bundestag.de/btp/01/01018.pdf): 24.11.1949 (anstatt 25.11.1949, Ende: 25.11. 6.23 Uhr)
# * [03158](https://dserver.bundestag.de/btp/03/03158.pdf): 04.05.1961 (anstatt 05.05.1961, Ende: 05.05. 0.19 Uhr)
# * [03164](https://dserver.bundestag.de/btp/03/03164.pdf): 28.06.1961 (anstatt 29.06.1961, Ende: 29.06. 0.07 Uhr.)
# 
# Ein weiteres fehlerhaftes Datum findet sich für das Protokoll 07208, hier wurde der 11.12.1975 eingetragen, die Sitzung fand jedoch einen Tag davor, am 10.12.1975 statt. Diese falsche Datierung wurde auch im Zuge der Prüfung von doppelt vorkommenden Daten erkannt, da die Sitzung 07209 tatsächlich am 11.12.1975 stattfand. Alle 90 Protokolle, die dort Erwähnung fanden, wurden entsprechend geprüft. Das bedeutet jedoch auch, dass wahrscheinlich noch weitere unentdeckte fehlerbehaftete Datumsangaben in dem Korpus vorkommen, die sich in dem Plausibilitätsbereich zwischen der vorherigen und darauffolgenden Sitzung bewegen. Die hier gefundenen acht von 4106 Protokolle liegen im Promillebereich und dürften für breitere Untersuchungen kein größeres Problem darstellen. Trotzdem führen sie dazu, dass an die tausend Redebeiträge mit einem falschen Datum versehen sind.
# 
# Daneben gibt es kleinere Tipp- und Formfehler, die nur einzelne Redebeiträge betreffen. In der Stichprobe finden sich beispielsweise zwei Parteienfehler, so wurde Konrad Porzner der nicht existenten Partei SDP anstatt der SPD zugeordnet [(04184, S. 9260)](https://dserver.bundestag.de/btp/04/04184.pdf). Schwerwiegender ist, dass Klaus W. Lippold der SPD zugeordnet wurde, obwohl er CDU-Abgeordneter war [(12152, S. 13019)](https://dserver.bundestag.de/btp/12/12152.pdf). In den 36 Protokollen gibt es auch eine interessante Zahl von Tippfehlern im Präsidententitel:
# 
# * "Vizeräsident Dr. Dehler:" [(04184, S. 9244)](https://dserver.bundestag.de/btp/04/04184.pdf)
# * "Vizepräsidennt Frau Dr. Probst:" [(05101, S. 4701)](https://dserver.bundestag.de/btp/05/05101.pdf)
# * "Viezepräsident Wurbs:" [(09014, S. 458)](https://dserver.bundestag.de/btp/09/09014.pdf)
# * "Vizpräsident Frau Renger:" [(10213, S. 16414)](https://dserver.bundestag.de/btp/10/10213.pdf)
# 
# Seltene Formfehler sind für die automatisierte Weiterverarbeitung zu beachten. So gibt es klare Regeln, wann eckige und wann runde Klammern genutzt werden: Bei Redebeiträgen steht die Partei in runden Klammern, bei Zwischenrufen in eckigen Klammern. In mehreren Instanzen werden jedoch eckige Klammern fälschlich bei Redebeiträgen genutzt. Insgesamt lassen sich diese Form- und Tippfehler bei den Namen und Titeln innerhalb der Stichprobe zwar an zwei Händen abzählen, führen bei einer reinen regelbasierten automatisierten Verarbeitung jedoch mit hoher Wahrscheinlichkeit zu Erkennungsfehler dieser einzelnen Redebeiträge. In den folgenden Kapiteln wird darauf ausführlicher eingegangen werden.
# 
# Ein weiterer Fehler, der einmal aufgefallen ist, ist eine fehlende Seite; diese fehlt bereits in dem zugrundliegenden PDF-Dokument [(14192: S. 18818)](https://dserver.bundestag.de/btp/14/14192.pdf). Es ist plausibel, dass dieser Fehler häufiger vorkommt, in der Stichprobe ist dies allerdings nicht der Fall. Dies könnte systematisch untersucht werden indem die Seitenzahl aller Seiten extrahiert und jeweils ein Vergleich mit der vorherigen durchgeführt wird; in dieser Arbeit wird dem jedoch nicht weiter nachgegangen.

# In[6]:


# Variablen für das nächste Kapitel speichern
get_ipython().run_line_magic('store', 'minutes minutes_duplicates_filtered')


# ***
# <a id="ref_1"></a>[1] Grundgesetz für die Bundesrepublik Deutschland, Artikel 42 Abs. 1.
# 
# <a id="ref_2"></a>[2] §116 Abs. 1, Geschäftsordnung des Deutschen Bundestages, o. D., https://www.bundestag.de/parlament/aufgaben/rechtsgrundlagen/go_btg (abgerufen: 13.10.2021).
# 
# <a id="ref_3"></a>[3] Heike Schweitzer, AW: Fragen zu Plenarprotokollen, 14.10.2021.
# 
# <a id="ref_4"></a>[4] § 117 Abs. 1 in der Geschäftsordnung des Deutschen Bundestages (s. Anm. 2).
# 
# <a id="ref_5"></a>[5] Deutscher Bundestag - Gastredner, Deutscher Bundestag, o. D., https://www.bundestag.de/services/glossar/glossar/G/gastredner-857066 (abgerufen: 26.06.2023).
# 
# <a id="ref_6"></a>[6] Der erste Eintrag im Internet Archive für die Open-Data-Seite ist von März 2017, zu diesem Zeitpunkt noch mit dem Titel „Offene Daten“:
# Deutscher Bundestag - Offene Daten, 27.10.2017, https://web.archive.org/web/20171027122855/http://www.bundestag.de/service/opendata (abgerufen: 05.05.2023).
# Zum aktuellen Zeitpunkt ist das Webarchiv des Bundestags nur bis 2016 freigeschaltet, eine genaue zeitliche Einordnung der Veröffentlich dadurch nicht möglich, vgl. Deutscher Bundestag - Webarchiv, o. D., https://webarchiv.bundestag.de/ (abgerufen: 29.06.2023).
# 
# <a id="ref_7"></a>[7] Volker Müller, Deutscher Bundestag - 20 Jahre Deutscher Bundestag im Internet, Deutscher Bundestag, o. D., https://www.bundestag.de/webarchiv/textarchiv/2016/kw04-20-jahre-bundestag-im-internet-403918 (abgerufen: 29.06.2023).
# 
# <a id="ref_8"></a>[8] Deutscher Bundestag - Plenarprotokolle Übersicht, Wayback Machine, 19.10.1996, https://web.archive.org/web/19961019120016/http://www.bundestag.de/aktuell/113.htm (abgerufen: 26.06.2023).
# 
# <a id="ref_9"></a>[9] Deutscher Bundestag - Dokumentenserver PARFORS, Wayback Machine, 06.02.2006, https://web.archive.org/web/20060206121510/http://dip.bundestag.de/parfors/parfors.htm (abgerufen: 26.06.2023).
# 
# <a id="ref_10"></a>[10] Drucksachen und Plenarprotokolle des Bundestages - 1949 bis 2005, Wayback Machine, 20.03.2013, https://web.archive.org/web/20130320135845/http://pdok.bundestag.de/ (abgerufen: 29.06.2023).
# 
# <a id="ref_11"></a>[11] § 12a EGovG - Einzelnorm, o. D., S. 12, https://www.gesetze-im-internet.de/egovg/__12a.html (abgerufen: 26.06.2023).
# 
# <a id="ref_12"></a>[12] Bundestags-Plenar-Protokolle im XML-Format: Aufbau der Strukturdefinition – DTD, Deutscher Bundestag, 07.02.2022, https://www.bundestag.de/resource/blob/577234/4c8091d8650fe417016bb48e604e3eaf/dbtplenarprotokoll_kommentiert-data.pdf.
# 
# <a id="ref_13"></a>[13] Nuance - standard - Convert scanned paper and digital documents into editable files - OmniPage 17 Standard, Wayback Machine, 18.03.2011, https://web.archive.org/web/20110318193528/http://www.nuance.com/for-business/by-product/omnipage/standard/index.htm (abgerufen: 29.06.2023).
# 
# <a id="ref_14"></a>[14] Der ursprüngliche Hersteller Nuance hat 2019 OmniPage an Kofax Inc. verkauft, die originale Anleitung lässt sich leider auch nicht über das Internet Archive finden, sondern nur über diese Drittseite.
# OmniPage 17 User’s Guide - Nuance, yumpu.com, o. D., https://www.yumpu.com/en/document/read/3266704/omnipage-17-users-guide-nuance (abgerufen: 29.06.2023).
# 
# <a id="ref_15"></a>[15] Martin Volk, Torsten Marek, Rico Sennrich, Reducing OCR errors by combining two OCR systems in, s.n., 16.08.2010, https://doi.org/10.5167/UZH-35259.
# In diesem Paper wird OmniPage-OCR-Output hinsichtlich Ausgangsmaterial aus dem 19. und 20. Jahrhundert evaluiert, dieses ist jedoch multilingual und OmniPage ist vor allem im Bereich französischer Texterkennung fehlerbehaftet (S. 5).
# 
# <a id="ref_16"></a>[16] Um diese zu finden, lassen sich per Regex die Dateien nach `Bonn, den [\d]{1,2}. und` durchsuchen; das geht in Python, aber auch beispielsweise bei geöffnetem Ordner in Visual Studio Code.

# In[ ]:




