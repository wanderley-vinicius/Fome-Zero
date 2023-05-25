# Bibliotecas
import pandas as pd
import folium
import re
import plotly.express as px
from haversine import haversine
import plotly.graph_objects as go
import inflection
from streamlit_folium import folium_static

# Bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Visão Cidades', page_icon='🏙', layout='wide')

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Funções
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

def clean_code( df ):
    # Removendo colunas com poucos valores
        #df1.pop("Is delivering now")
        #df1.pop("Switch to order menu")

    # Removendo linhas col valor nulo
    linhas_selecionadas = df['cuisines'].notnull()
    df = df.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df['aggregate_rating'].notnull()
    df = df.loc[linhas_selecionadas, :].copy()

    # Categorizar, todos os restaurantes somente por um tipo de culinária.
    df['cuisines'] = df.loc[:, 'cuisines'].apply( lambda x: x.split( ',' )[0] )
    
    # Preenchimento do nome dos países

    COUNTRIES = {
                1: "India",
                14: "Australia",
                30: "Brazil",
                37: "Canada",
                94: "Indonesia",
                148: "New Zeland",
                162: "Philippines",
                166: "Qatar",
                184: "Singapure",
                189: "South Africa",
                191: "Sri Lanka",
                208: "Turkey",
                214: "United Arab Emirates",
                215: "England",
                216: "United States of America",
                }

    def country_name(country_id):
        dataframe.loc[:, ''].apply( lambda x: x )
        return COUNTRIES[country_id]

    for linha in df['country_code']:
        if linha == 1:
            df['country_code'] = df['country_code'].replace({linha: 'India'})
        elif linha == 14:
            df['country_code'] = df['country_code'].replace({linha: 'Australia'})
        elif linha == 30:
            df['country_code'] = df['country_code'].replace({linha: 'Brazil'})    
        elif linha == 37:
            df['country_code'] = df['country_code'].replace({linha: 'Canada'})
        elif linha == 94:
            df['country_code'] = df['country_code'].replace({linha: 'Indonesia'})    
        elif linha == 148:
            df['country_code'] = df['country_code'].replace({linha: 'New Zeland'})
        elif linha == 162:
            df['country_code'] = df['country_code'].replace({linha: 'Philippines'})    
        elif linha == 166:
            df['country_code'] = df['country_code'].replace({linha: 'Qatar'})
        elif linha == 184:
            df['country_code'] = df['country_code'].replace({linha: 'Singapure'}) 
        elif linha == 189:
            df['country_code'] = df['country_code'].replace({linha: 'South Africa'})
        elif linha == 191:
            df['country_code'] = df['country_code'].replace({linha: 'Sri Lanka'})    
        elif linha == 208:
            df['country_code'] = df['country_code'].replace({linha: 'Turkey'})
        elif linha == 214:
            df['country_code'] = df['country_code'].replace({linha: 'United Arab Emirates'})
        elif linha == 215:
            df['country_code'] = df['country_code'].replace({linha: 'England'})
        elif linha == 216:
            df['country_code'] = df['country_code'].replace({linha: 'United States of America'}) 

    
    return df

def top_10_restaurants_by_cities( df ):
    cols = ['city', 'restaurant_id']
    df_aux = (df.loc[:, cols]
                  .groupby('city')
                  .count()
                  .sort_values( ['restaurant_id'], ascending=False)
                  .reset_index())
    # Gráfico de Barras
    fig = px.bar( df_aux.head(10), x='city', y='restaurant_id' )

    return fig

def top_7_cities_by_restaurants_avg_above_4( df ):
    cols = ['city', 'restaurant_id']
    df_aux = (df.loc[df['aggregate_rating'] > 4.0, cols]
              .groupby('city')
              .count()
              .sort_values(['restaurant_id'], ascending=False)
              .reset_index())
    # Gráfico de Barras
    fig = px.bar( df_aux.head(7), x='city', y='restaurant_id' )
    
    return fig

def top_7_cities_by_restaurants_avg_below_2( df ):
    cols = ['city', 'restaurant_id']
    df_aux = (df.loc[df['aggregate_rating'] < 2.5, cols]
              .groupby('city')
              .count()
              .sort_values(['restaurant_id'], ascending=False)
              .reset_index())
    # Gráfico de Barras
    fig = px.bar(df_aux.head(7), x='city', y='restaurant_id')
    
    return fig

def top_10_cities_by_restaurants_types_cuisines_different( df ):
    cols = ['city', 'cuisines']
    df_aux = (df.loc[:, ['city', 'cuisines']]
              .groupby('city')
              .nunique()
              .sort_values(['cuisines'],ascending=False)
              .reset_index())
    # Gráfico de Barras
    fig = px.bar(df_aux.head(10), x='city', y='cuisines')

    return fig
# _-_-_-_-_-_- Inicío da Estrutura lógica do código _-_-_-_-_-_-

# =-=-=-=-=-=-=-=-=-==-=-=-=-=
# Import dataset
# =-=-=-=-=-=-=-=-=-==-=-=-=-=

dataframe = pd.read_csv( 'zomato.csv' )

# =-=-=-=-=-=-=-=-=-==-=-=-=-=
# Limpando os dados
# =-=-=-=-=-=-=-=-=-==-=-=-=-=
dataframe = rename_columns(dataframe)

df = clean_code( dataframe )

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#     Barra Lateral
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#image_path = r'C:\Users\Wanderley\Documents\repos\ftc_programacao_python\ciclo_8'

st.sidebar.markdown( '## Filtros' )

traffic_options = st.sidebar.multiselect(
        'Escolha os Paises que Deseja visualizar os Restaurantes',
        ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
        default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])


# Filtro Países
linhas_selecionadas = df['country_code'].isin( traffic_options )
df = df.loc[linhas_selecionadas, :]


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#     Layout no Streamlit
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=

with st.container():
    
    fig = top_10_restaurants_by_cities( df )
    st.markdown( '##### Top 10 cidades com mais restaurantes na base de dados' )
    st.plotly_chart(fig, use_container_with=True)

with st.container():
    col1, col2 = st.columns( 2, gap='large' )
    with col1:
        fig = top_7_cities_by_restaurants_avg_above_4(df)
        st.markdown( '##### Top 7 cidades com restaurantes com média de avaliações acima de 4' )
        st.plotly_chart(fig, use_container_with=True)
        
    with col2:
        fig = top_7_cities_by_restaurants_avg_below_2(df)
        st.markdown( '##### Top 7 cidades com restaurantes com média de avaliações abaixo de 2.5' )
        st.plotly_chart(fig, use_container_with=True)
        
with st.container(): 
        fig = top_10_cities_by_restaurants_types_cuisines_different( df )
        st.markdown( '##### Top 10 cidades com restaurantes com tipos de culinárias distintas' )
        st.plotly_chart(fig, use_container_with=True)
