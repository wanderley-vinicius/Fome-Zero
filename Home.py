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

st.set_page_config(
    page_title='Main Page',
    page_icon='📊',
    layout='wide'
)

def country_maps( df ):
    """  
        Essa função faz uma maração de pontos em um mapa localizando cada cidade por tráfego

        Sequência de passos:
        1. Criação da várivael dataplot para criar o filtro de cada cidade por tráfego
        2. Criação da váriavel map_ para criar o mapa
        3. Criação do for para fazer a interação do dataplot no map_ para fazer a marção de pontos

        Input: Dataframe
        Output: Map   
    """
    # len(df.loc[:, 'country_code'].unique())
    # Localização central de cada cidade por tipo de tráfego
    data_plot = (df.loc[:, ['city', 
                              'restaurant_id',
                              'latitude',
                              'longitude']]
                      .groupby( ['city', 'restaurant_id'])
                      .median()
                      .reset_index())

    # Desenhar o mapa
    map_ = folium.Map()
    for index, location_info in data_plot.iterrows(): 
        folium.Marker( 
                [location_info['latitude'],
                location_info['longitude']],
                popup=location_info[
                ['city', 'restaurant_id']] ).add_to( map_ )

    folium_static( map_, width=1024, height=600 )

    return None


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

image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Fome Zero' )
st.sidebar.markdown( '## Filtros' )

traffic_options = st.sidebar.multiselect(
        'Escolha os Paises que Deseja visualizar os Restaurantes',
        ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
        default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])


st.sidebar.markdown( '# Dados Tratados' )

#+_+_+_+_+_+
# Text files

df.to_csv('df.csv', index=False)
with open('df.csv', encoding="utf-8") as f:
       st.sidebar.download_button('Download CSV', f, 'df.csv')  # Defaults to 'text/plain'

#+_+_+_+_+_+

# Filtro Países
linhas_selecionadas = df['country_code'].isin( traffic_options )
df = df.loc[linhas_selecionadas, :]

st.write( "# Fome Zero!" )
st.write( "## O Melhor lugar para encontrar seu mais novo restaurante favorito!" )
st.write( "### Temos as seguintes marcas dentro da nossa plataforma:" )

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#     Layout no Streamlit
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=
with st.container():         
    col1, col2, col3, col4, col5 = st.columns( 5, gap='large' )
    with col1:
        restaurantes_cadastrados = len(df.loc[:, 'restaurant_id'].unique())
        col1.metric( 'Restaurantes Cadastrados', restaurantes_cadastrados )

    with col2:
        paises_cadastrados = len(df.loc[:, 'country_code'].unique())
        col2.metric( 'Paises Cadastrados', paises_cadastrados )

    with col3:
        cidades_cadastrados = len(df.loc[:, 'city'].unique())
        col3.metric( 'Cidades Cadastrados', cidades_cadastrados )

    with col4:
        total_avg_plataforma = len(df.loc[:, 'aggregate_rating'])
        col4.metric( 'Avaliações Feitas na Plataforma', total_avg_plataforma )

    with col5:
        total_tipos_culinarias = len(df.loc[:, 'cuisines'].unique())
        col5.metric( 'Tipos de Culinárias Oferecidas', total_tipos_culinarias )

with st.container():
    st.markdown( '# Country Maps' )
    country_maps( df )