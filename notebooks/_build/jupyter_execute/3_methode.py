#!/usr/bin/env python
# coding: utf-8

# # 3 Methode: Goldstandard-Korpus-Evaluation
# 
# Ein Goldstandard-Korpus bezeichnet im NLP-Kontext eine manuell annotierte Textsammlung, die teils von mehreren Expert:innen unabhängig voneinander bearbeitet wurde.[[1]](#ref_1) Die Nutzung von Goldstandard-Korpora als Evaluationsgrundlage ist im Bereich der OCR-Qualität und deren Implikationen für nachgelagerte Aufgaben wie Information Retrieval, Autorenschaftsanalyse, Named-Entity-Recognition und Topic-Modelling bereits in mehreren Studien angewendet worden.[[2]](#ref_2)
# 
# Dieser Prozess lässt sich für die Geschichtswissenschaften adaptieren. Ursprünglich werden die Daten komplett gespiegelt und sollen beispielhaft für ähnliche Datensätze stehen. In dem adaptierten Ansatz wird dagegen eine Stichprobe genommen, die nur für das Korpus repräsentativ ist. Der Untersuchungsgegenstand ist hier die automatisierte Annotation und Erkennung, nicht das OCR, dass den häufigsten Anwendungsfall eines Goldstandard-Korpus darstellt. Als solcher Prozess der Quellenkritik lässt sich die Goldstandard-Korpus-Evaluation in folgende fünf Schritte strukturieren:
# 
# 1. Festlegung der Untersuchungskriterien
# 2. Stichprobe der Quelle
# 3. Annotation der Stichprobe hin zu einem Goldstandard
# 4. Matching beider Korpora
# 5. Analyse
# 
# ## 3.1 Untersuchungskriterien
# 
# Die Untersuchungskriterien schließen für dieses Korpus dort an, wo die bisherige Analyse der äußeren Faktoren der Rohdaten und des Open-Discourse-Korpus endete: Inwieweit die eigentlichen Redebeiträge innerhalb der Protokolle durch das Korpus repräsentiert werden. Hierbei gibt es mehrere zentrale Fragen, die zu beantworten sind:
# 
# 1. Sind alle Redebeiträge erkannt worden? Ist das Korpus also vollständig? 
# 2. Sind die Redebeiträge mit dem richtigen Umfang repräsentiert? Ist deren Text vollständig und enthält auch keinen zusätzlichen Text?
# 3. Sind fälschlich als Redebeiträge erkannte Fragmente vorhanden?
# 4. Sind die Redebeiträge den (richtigen) Personen zugeordnet?
# 
# Eine weitere Frage betrifft die OCR-Qualität. Dies wurde aus Gründen des Umfangs in dieser Arbeit aber ausgeblendet. Open Discourse nutzt den Rohtext aus den Open Data des Bundestags und bearbeitete diesen sehr leicht durch die Filterung von Kopfzeilen und Layoutartefakten.
# 
# ## 3.2 Stichprobe
# 
# Für die Stichprobe wurden jeweils zwei Protokolle für die Perioden 1-18 randomisiert ausgewählt.  Das bedeutet, dass die Redebeiträge bei der Auswahl zweifach geclustert sind: nach Periode und Protokoll. Dies erlaubt zwar die Repräsentation möglicher Textkonventions-Änderungen, kann aber auch einen Bias einer Überrepräsentation bestimmter Perioden aufgrund der abweichenden Anzahl der Protokolle je Periode induzieren; hinsichtlich der Clusterung in Protokollen könnten die unterschiedlichen Sitzungslängen ebenfalls ein Bias verursachen. Dem wurde in dieser Arbeit dadurch begegnet, dass eine abschließende Messung der erkannten Fehlursachen innerhalb des Gesamtkorpus erfolgte.

# In[1]:


import random
import os
minutes_sample = []

# Iteriere über alle Perioden
for period in range(1, 19):
    period_string = str(period).zfill(2)
    path = '../data/raw' + '/' + period_string
    
    # Zähle die XML-Dateien in dem entsprechenden Perioden-Rohdaten-Ordner
    count = len([name for name in os.listdir(path) if name.endswith('.xml') and os.path.isfile(os.path.join(path, name))])     
    # Ziehe nacheinander zwei zufällige Zallen aus der Anzahl der Protokolle der Periode
    min_samples = random.sample(range(1, count + 1), 2)
    
    # Baue die Strings, die die beiden Protokolle repräsentieren und hänge sie an die Liste der Samples an
    minutes_sample += [period_string + str(min_sample).zfill(3) for min_sample in min_samples]


# Bei jedem Abruf des Skripts wird ein eigenes Sample erzeugt. Das folgende Sample ist das Ergebnis des Zufallsskripts und lag der weiteren Untersuchung zugrunde:

# In[2]:


minutes_sample = ['01020', '01229', '02087', '02202', '03018', '03103', '04015', '04184', '05101', '05158', 
                 '06017', '06185', '07118', '07140', '08025', '08080', '09014', '09126', '10061', '10213', 
                 '11102', '11124', '12037', '12152', '13176', '13217', '14145', '14150', '15058', '15077', 
                 '16002', '16133', '17036', '17248', '18014', '18088']


# ***
# <a id="ref_1"></a>[1] Lars Wissler, Mohammed Almashraee, Dagmar Monett, u. a., The Gold Standard in Corpus Annotation, in: Proceedings of the 5th IEEE Germany Students Conference 2014, ResearchGate 2014, https://doi.org/10.13140/2.1.4316.3523, S. 2.
# 
# <a id="ref_2"></a>[2] D. van Strien, K. Beelen, M. C. Ardanuy, u. a., Assessing the impact of OCR quality on downstream NLP tasks, in: Proceedings of the 12th International Conference on Agents and Artificial Intelligence, 2020, https://doi.org/10.5220/0009169004840496, S. 2.

# In[ ]:




