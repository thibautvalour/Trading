"""
# Simulateur investissement PEA
"""

import streamlit as st
import datetime

from src.config import params
from src.price_loader import StockLoader
from src.strategy import DCAStrategy

# Menu
col_start, col_end = st.columns(2)
with col_start:
    starting_year = st.number_input("Année de départ", 1994, 2024, 1994)
with col_end:
    ending_year = st.number_input("Année de fin d'investissement", 1995, 2024, 2024)

col1, col2, col3 = st.columns(3)
with col1:
    initial_investment = st.number_input(
        "Investissement Initial",
        min_value=0,
        max_value=params["Global"]["PEA_limit"],
        value=10_000,
    )
with col2:
    initial_monthly_contribution = st.number_input(
        "Versement mensuel", min_value=0, value=100
    )
with col3:
    yearly_bump = st.number_input(
        "Augmentation du versement annuelle",
        min_value=0,
        max_value=10_000,
        value=10,
    )


ticker = "SPY"
start = datetime.datetime(starting_year, 1, 1)
end = datetime.datetime(ending_year, 1, 1)
# # end = datetime.datetime.now() - datetime.timedelta(days=1) # Yesterday

strategy = DCAStrategy(
    ticker,
    start,
    end,
    initial_cash=initial_investment,
    initial_monthly_contribution=initial_monthly_contribution,
    yearly_bump=yearly_bump,
)

monthly_prices = StockLoader(ticker=ticker).get_monthly_prices(
    start, end, include_dividends=True, yearly_fee=params[ticker]["yearly_fee"]
)
strategy.simulate_investment_strategy(monthly_prices)
invested_cash = strategy.total_invested_cash[-1]
exit_value = strategy.exit_values[-1]


fig = strategy.create_portfolio_visualization(monthly_prices)
st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Montant total investi : **{invested_cash:,.0f} $**")
st.subheader(f"Valeur nette de sortie : **{exit_value:,.0f} $**")
st.write("")
st.write(
    "La stratégie d'investissement présentée ici est basée sur le principe du **Dollar Cost Averaging (DCA)** via un PEA. Cette méthode consiste à investir une somme fixe à intervalle régulier, dans notre cas tous les mois, dans un ETF suivant l'indice S&P 500."
)
st.write(
    "L'ETF sélectionné réplique la performance des 500 plus grandes entreprises américaines cotées en bourse. La répartition sectorielle de l'indice est visualisable [ici](https://finviz.com/map.ashx). Les détails de fonctionnement de l'ETF reproduisant cet indice sont disponibles dans [ce document](https://doc.morningstar.com/Document/127c37e75a3252469991ea9641a63266.msdoc/?key=20e84eb11f96a433746b6c63912632d0da6d46c213a26195acbdbe8df5afb0d5)."
)
st.write(
    "Les montants indiqués tiennent compte des frais de gestion annuels de l'ETF (0,153%), ainsi que des frais d'entrée (3%) et de sortie (3%) de l'ETF, et de l'impôt sur les plus-values du PEA (17,2%). Les versements sur le PEA sont plaffonés à 160 500 $ (150k €). Tous les montants sont exprimés en $ USD"
)
