# Dashboard Boursier

## Description
Application web interactive construite avec Streamlit pour suivre un portfolio boursier en temps réel.

## Fonctionnalités
- Vue globale du portfolio avec KPIs (prix actuel, variation du jour)
- Graphique d'évolution historique par action (1 mois / 3 mois / 6 mois / 1 an)
- Flux de news financières par action

## Stack technique
- **Python** — pandas, plotly
- **Streamlit** — interface web interactive
- **yfinance** — données boursières en temps réel
- **NewsAPI** — actualités financières

## Actions suivies
Mastercard, Amazon, Microsoft, Constellation Software, ASML, Google, Fair Isaac, Booking, Intuit

## Installation
N/A

### Prérequis
bash
```
pip install streamlit yfinance plotly pandas python-dotenv requests
```

### Configuration
Créer un fichier ⁠.env à la racine du projet :
```
 NEWS_API_KEY=ta_clé_newsapi
```
 Lancement
 ```
 streamlit run bourse.py
```

 Auteur
Maxime Sarton
 
Colle ça dans ton README sur GitHub et commit ! 😊
 
