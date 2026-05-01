import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Liste de tes actions
tickers = {
    'Mastercard': 'MA',
    'Amazon': 'AMZN',
    'Microsoft': 'MSFT',
    'Constellation Software': 'CSU.TO',
    'ASML': 'ASML',
    'Google': 'GOOGL',
    'Fair Isaac': 'FICO',
    'Booking': 'BKNG',
    'Intuit': 'INTU',
    'Salesforce' : "CRM"
}

# Titre et navigation — TOUJOURS affichés
st.title("📈 Mon Portfolio Boursier")
st.sidebar.title("Navigation")
pages = ["Vue globale", "Détail par action", "News"]
page = st.sidebar.radio("Aller vers", pages)

# Fonction cache
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'prix': info.get('currentPrice', 'N/A'),
        'variation': info.get('regularMarketChangePercent', 'N/A'),
        'devise': info.get('currency', 'USD')
    }

# Page 1 - Vue Globale
if page == pages[0]:
    st.write("### Vue globale")
    cols = st.columns(3)
    for i, (nom, ticker) in enumerate(tickers.items()):
        data = get_stock_data(ticker)
        col = cols[i % 3]
        variation = data['variation']
        if variation != 'N/A':
            delta = f"{variation:.2f}%"
        else:
            delta = "N/A"
        col.metric(
            label=nom,
            value=f"{data['prix']} {data['devise']}",
            delta=delta
        )

# Page 2 - Détail par action
if page == pages[1]:
    st.write("### Détail par action")
    
    # Sélection de l'action
    action_selectionnee = st.selectbox('Choisir une action', list(tickers.keys()))
    ticker = tickers[action_selectionnee]
    
    # Période
    periode = st.radio('Période', ['1mo', '3mo', '6mo', '1y'], horizontal=True)
    
    # Récupérer l'historique
    @st.cache_data(ttl=300)
    def get_history(ticker, periode):
        stock = yf.Ticker(ticker)
        return stock.history(period=periode)
    
    hist = get_history(ticker, periode)
    
    # Graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['Close'],
        name=action_selectionnee,
        line=dict(color='#00b2ee', width=2)
    ))
    fig.update_layout(
        title=f'Evolution de {action_selectionnee}',
        xaxis_title='Date',
        yaxis_title='Prix de clôture'
    )
    st.plotly_chart(fig, use_container_width=True)

#Page 3 - News

from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("NEWS_API_KEY")

if page == pages[2]:
    st.write("### 📰 News")
    
    action_news = st.selectbox('Choisir une action', list(tickers.keys()), key='news')
    
    @st.cache_data(ttl=1800)  # Cache 30 minutes
    def get_news(query, api_key):
        url = f"https://newsapi.org/v2/everything?q={query}&language=fr&sortBy=publishedAt&pageSize=10&apiKey={api_key}"
        response = requests.get(url)
        return response.json()
    
    news = get_news(action_news, api_key)
    
    if news['status'] == 'ok':
        for article in news['articles']:
            st.write(f"**{article['title']}**")
            st.write(f"*{article['publishedAt'][:10]}* — {article['source']['name']}")
            st.write(article['description'])
            st.write(f"[Lire l'article]({article['url']})")
            st.divider()
    else:
        st.error("Erreur lors de la récupération des news")
