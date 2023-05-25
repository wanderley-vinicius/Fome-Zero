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

st.set_page_config( page_title='Visão Tipos de Cusinhas', page_icon='🍽', layout='wide')

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
#=-=
def top_restaurant_italiana_v( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Italian', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    df_aux2 = df_aux

    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux2 = (df_aux2.loc[df_aux2['aggregate_rating']==4.9, cols]
                      .groupby('restaurant_name')
                      .max()
                      .sort_values(['restaurant_id'], ascending=True)
                      .reset_index())
    
    valor = df_aux2.iloc[0,2]
    
    return valor

def top_restaurant_italiana_n( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Italian', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    df_aux2 = df_aux

    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux2 = (df_aux2.loc[df_aux2['aggregate_rating']==4.9, cols]
                      .groupby('restaurant_name')
                      .max()
                      .sort_values(['restaurant_id'], ascending=True)
                      .reset_index())
    
    nome = df_aux2.iloc[0,0]
    
    return nome
#=-=
def top_restaurant_american_n(df):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='American', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())

    df_aux2 = df_aux

    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux2 = (df_aux2.loc[df_aux2['aggregate_rating']==4.9, cols]
                      .groupby('restaurant_name')
                      .max()
                      .sort_values(['restaurant_id'], ascending=True)
                      .reset_index())
    nome = df_aux2.iloc[0,0]
    return nome

def top_restaurant_american_v(df):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='American', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())

    df_aux2 = df_aux

    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux2 = (df_aux2.loc[df_aux2['aggregate_rating']==4.9, cols]
                      .groupby('restaurant_name')
                      .max()
                      .sort_values(['restaurant_id'], ascending=True)
                      .reset_index())
    valor = df_aux2.iloc[0,2]
    return valor

#=-=
def top_restaurant_arabe_n( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Arabian', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    nome = df_aux.iloc[0,1]
    return nome

def top_restaurant_arabe_v( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Arabian', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    valor = df_aux.iloc[0,2]
    return valor

#=-=
def top_restaurant_japanese_n( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Japanese', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    nome = df_aux.iloc[0,1]
    return nome

def top_restaurant_japanese_v( df ):
    cols = ['restaurant_name', 'restaurant_id', 'aggregate_rating']
    df_aux = (df.loc[df['cuisines']=='Japanese', cols]
                 .groupby(['restaurant_id', 'restaurant_name'])
                 .mean()
                 .sort_values(['aggregate_rating', 'restaurant_id'], ascending=False)
                 .reset_index())
    valor = df_aux.iloc[0,2]
    return valor

#=-=
def top_10_types_cuisines( df, top_asc ): 
    df_aux = (df.loc[:, ['cuisines', 'aggregate_rating']]
                .groupby('cuisines')
                .mean()
                .sort_values(['aggregate_rating'], ascending=top_asc)
                .reset_index())
    # Gráfico de Barras
    fig = px.bar(df_aux.head(7), x='cuisines', y='aggregate_rating')
    
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

st.write( "# Visão Tipos de Cusinhas" )
st.write( "## Melhores Restaurantes dos Principais tipos Culinários")

with st.container():

    col1, col2, col3, col4 = st.columns( 4, gap='large' )
    with col1:
        valor = top_restaurant_italiana_v( df )
        nome = top_restaurant_italiana_n( df )
        col1.metric( nome, valor )

    with col2:
        valor = top_restaurant_american_v( df )
        nome = top_restaurant_american_n( df )
        col2.metric( nome, valor )

    with col3:
        nome = top_restaurant_arabe_n( df )
        valor = top_restaurant_arabe_v( df )
        col3.metric( nome, valor )

    with col4:
        nome = top_restaurant_japanese_n( df )
        valor = top_restaurant_japanese_v( df )
        col4.metric( nome, valor )

with st.container():
    st.write( "Top 10 Restaurantes" )
    cols = ['restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    df_aux1 = df.loc[df['restaurant_id'] == 6102616, cols]
    df_aux2 = df.loc[df['restaurant_id'] == 6107336, cols]
    df_aux3 = df.loc[df['restaurant_id'] == 6116563, cols]
    df_aux4 = df.loc[df['restaurant_id'] == 6501298, cols]
    df_aux5 = df.loc[df['restaurant_id'] == 6801374, cols]
    df_aux6 = df.loc[df['restaurant_id'] == 7300004, cols]
    df_aux7 = df.loc[df['restaurant_id'] == 7300955, cols]
    df_aux8 = df.loc[df['restaurant_id'] == 7302898, cols]
    df_aux9 = df.loc[df['restaurant_id'] == 7700796, cols]
    df_aux10 = df.loc[df['restaurant_id'] == 16587684, cols]
    data = pd.concat([df_aux1, df_aux2, df_aux3, df_aux4, df_aux5, df_aux6, df_aux7, df_aux8, df_aux9, df_aux10])
    
    st.dataframe(data)

pd.concat([df_aux1, df_aux2, df_aux3, df_aux4, df_aux5, df_aux6, df_aux7, df_aux8, df_aux9, df_aux10])

with st.container():
    col1, col2 = st.columns( 2, gap='large' )
    with col1:  
        fig = top_10_types_cuisines(df, top_asc=False)
        st.markdown( '##### Top 10 Melhores Tipos de Culinárias' )
        st.plotly_chart(fig, use_container_with=True)
        
        
    with col2:
        fig = top_10_types_cuisines(df, top_asc=True)
        st.markdown( '##### Top 10 Piores Tipos de Culinárias' )
        st.plotly_chart(fig, use_container_with=True)
