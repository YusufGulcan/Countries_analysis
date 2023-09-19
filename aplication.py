import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.set_page_config(layout = "wide", initial_sidebar_state="expanded")
path = "World_economy.csv"
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def kendi_inflectim(x):
    if abs(x) > 1000000000000:
        rez = x/1000000000000
        return "{:.2f} T".format(rez)
    elif abs(x) > 1000000000:
        rez = x/1000000000
        return "{:.2f} B".format(rez)
    elif abs(x) > 1000000:
        rez = x/1000000
        return "{:.2f} M".format(rez)
    else: 
        return "{:,.2f}".format(x)

df = pd.read_csv(path)
df["Net Trade"]= df["Export"] - df["Import"]
df["R&D"] = (df["R&D"] * df["GDP"])/100



countries_dict = {
"Europe" : df[df['Continent Name']=="Europe"]["Country Name"].unique(),
"Africa" : df[df['Continent Name']=="Africa"]["Country Name"].unique(),
"North America" : df[df['Continent Name']=="North America"]["Country Name"].unique(),
"South America" : df[df['Continent Name']=="South America"]["Country Name"].unique(),
"Asia" : df[df['Continent Name']=="Asia"]["Country Name"].unique(),
"Ocenia" : df[df['Continent Name']=="Ocenia"]["Country Name"].unique()}
cc = list(df["Country Name"].unique())
cc.extend(countries_dict.keys())
st.markdown("<h3 style='text-align: center;'> Distribution on The World Map </h3>", unsafe_allow_html=True)



#### Choropleth MAP Starts ## 
item1, item2 = st.columns([2,8])
with item1:
    metric_choro = st.selectbox(
        'Select The Metric:',
        [x for x  in df.columns[3:] if x!= "Continent Name"])


chorodata = df[df[metric_choro].isna()==False]
highest = chorodata[chorodata.Year==2022][metric_choro].max()
previous = chorodata[chorodata.Year==2021][metric_choro].max()
vl = chorodata[chorodata.Year==2022][metric_choro].max()
country_highest = chorodata[(chorodata.Year==2022)&(chorodata[metric_choro]==vl)]["Country Name"].values[0]
delta_h = ((highest - previous)/previous)*100

lowest = chorodata[chorodata.Year==2022][metric_choro].min()
prev_lowest = chorodata[chorodata.Year==2021][metric_choro].min()
vl = chorodata[chorodata.Year==2022][metric_choro].min()
country_lowest = chorodata[(chorodata.Year==2022)&(chorodata[metric_choro]==vl)]["Country Name"].values[0]
delta_l = ((lowest - prev_lowest) / prev_lowest) * 100

avg_mt = chorodata[chorodata.Year==2022][metric_choro].mean()
previous_avg = chorodata[chorodata.Year==2021][metric_choro].mean()
delta_avg = ((avg_mt - previous_avg)/previous_avg)*100

mdian_mt = chorodata[chorodata.Year==2022][metric_choro].median()
mdian_prev = chorodata[chorodata.Year==2021][metric_choro].median()
delta_median = ((mdian_mt - mdian_prev)/mdian_prev)*100


metrics, choro_map, data_df = st.columns([1.8,6,2.2])
with metrics:
    st.metric("a", "","",label_visibility="hidden")
    st.metric("a", "","",label_visibility="hidden")
    st.metric("a", "","",label_visibility="hidden")
    with st.container():
        st.metric(f"Highest {metric_choro} - {country_highest}", "{}".format(kendi_inflectim(highest)), "{}%".format(kendi_inflectim(delta_h)))
        st.metric(f"Lowest {metric_choro} - {country_lowest}", "{}".format(kendi_inflectim(lowest)), "{}%".format(kendi_inflectim(delta_l)))
        st.metric(f"Average {metric_choro} in 2022", "{}".format(kendi_inflectim(avg_mt)), "{}%".format(kendi_inflectim(delta_avg)))
        st.metric(f"Median {metric_choro} in 2022", "{}".format(kendi_inflectim(mdian_mt)), "{}%".format(kendi_inflectim(delta_median)))
with choro_map:
    fig5 = px.choropleth(chorodata , locations ="Country Code", color = metric_choro, 
                    width = 1400, height = 800, range_color= [int(np.quantile(chorodata[metric_choro],0.10)),int(np.quantile(chorodata[metric_choro],0.97)) ],
                color_continuous_scale="Bluered",animation_frame="Year",title = f'{metric_choro} Values In The World',hover_data="Country Name" )
    fig5.update_layout(title= {"x":0.2,"y":0.95}, geo= dict(bgcolor = "#F5F8FA"),coloraxis_showscale=False)
    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

with data_df:
    st.metric("a", "","",label_visibility="hidden")
    st.metric("a", "","",label_visibility="hidden")
    st.metric("a", "","",label_visibility="hidden")
    df_use = chorodata[chorodata.Year==2022][["Country Name", metric_choro]].sort_values(metric_choro,ascending = False).drop_duplicates()
    df_use[metric_choro] = df_use[metric_choro].apply(lambda x : kendi_inflectim(x))
    st.dataframe(df_use,height=480)
    

#### Choropleth MAP Ends ## 

st.divider()

st.markdown("<h3 style='text-align: center;'> Time Series Analysis</h3>", unsafe_allow_html=True)

c1 , c2, c3 = st.columns((1.5,7,1.5))

with c1:
    metric = st.selectbox(
        'Metric:',
        ('Agriculture (% GDP)',
       'Ease of Doing Business', 'Education Expenditure (% GDP)', 'Export (% GDP)', 'GDP',
       'Health Expenditure (% GDP)', 'Import (% GDP)', 'Industry (% GDP)', 'Inflation Rate',
       'R&D', 'Service (% GDP)', 'Unemployment', 'Population',
        'Education Expenditure', 'Health Expenditure',
       'Net Trade', 'GDP Per Capita'))
    
with c2:
    country_selection = st.multiselect(
        'Country or Continent:',
        options = (cc),default = ["United States", "China","United Kingdom", "Germany", "Japan", "Spain","Italy", "Canada", "France"])
    flattened = []
    continents = [x for x in country_selection if x in countries_dict.keys()]
    countries = [x for x in country_selection if x not in countries_dict.keys()]

    for item in continents:
        for co in countries_dict[item]:
            flattened.append(co)
    for co1 in countries:
        flattened.append(co1)

df_to_use = df[df["Country Name"].isin(flattened)]
df_to_use1 = df_to_use.groupby(["Continent Name","Year"])[metric].mean().reset_index()

All_continents = df["Continent Name"].unique()
All_countries = df["Country Name"].unique()


chart1, chart2 = st.columns(2)

with chart1:
    df_to_use = df_to_use[df_to_use["Population"].isna()==False]
    fig = px.scatter(df_to_use, x = "Continent Name", y = metric, color = "Country Name", animation_frame="Year",
                 height=800, title = f'{metric} Statistics per Country For The Last 20 Years',
                 range_y=[df_to_use[metric].min(),df_to_use[metric].max()*1.05],size="Population",size_max=55)
    fig.update_layout(width = 1500,height = 600, showlegend=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with chart2:
    fig2 = px.line(df_to_use1, x = "Year", y = metric, markers=True, height=600,color="Continent Name",title = f'Average {metric} Statistics per Continent For The Last 20 Years')
    fig2.update_layout(width = 1500,height = 600)
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


st.divider()

st.markdown("<h3 style='text-align: center;'>Correlation of Metrics</h3>", unsafe_allow_html=True)



scatter_col1 , scatter_col2,scatter_col3 = st.columns([1.5,1.5,7])
with scatter_col1:
    metric3 = st.selectbox("Year:",(df.Year.unique()))
with scatter_col2:
    metric1 = st.selectbox(
        'Compare:',
        ('Agriculture (% GDP)',
       'Ease of Doing Business', 'Education Expenditure (% GDP)', 'Export (% GDP)', 'GDP',
       'Health Expenditure (% GDP)', 'Import (% GDP)', 'Industry (% GDP)', 'Inflation Rate',
       'R&D', 'Service (% GDP)', 'Unemployment', 'Population',
        'Education Expenditure', 'Health Expenditure',
       'Net Trade'))
with scatter_col3:
    st.metric("a", "","",label_visibility="hidden")

chc1, chc2 = st.columns([4,6])
with chc2:
    chc_data = df[(df[metric1].isna()==False)&(df["GDP Per Capita"].isna()==False)]
    chc_data = chc_data.groupby(["Year"])[[metric1,"GDP Per Capita"]].mean().reset_index()

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Scatter(x = chc_data["Year"], y = chc_data[metric1],name = metric1, mode = "markers+lines",
                                line=dict(color = "Lightgreen")), secondary_y = False)
    fig4.add_trace(go.Scatter(x = chc_data["Year"], y = chc_data["GDP Per Capita"], name = "GDP Per Capita",mode = "markers+lines",
                                line=dict(color = "Cyan")),secondary_y = True)
    fig4.add_vrect(x0=metric3-0.5, x1=metric3+0.5, 
              annotation_text=str(metric3), annotation_position="bottom",
              fillcolor="green", opacity=0.20, line_width=0)
    fig4.update_layout(
    title_text=f"<b>{metric1}</b> vs <b>GDP Per Capita Comparison</b> In Time", height = 600,legend=dict(x=0.5,y= 1)
    )
    # Set x-axis title
    fig4.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig4.update_yaxes(title_text= f"Average {metric1}", secondary_y=False)
    fig4.update_yaxes(title_text= "Average GDP Per Capita", secondary_y=True)
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)
with chc1:
    sector_data = df[(df[metric1].isna()==False)&(df["GDP Per Capita"].isna()==False)&(df["Year"]==metric3)]

    fig3 = px.scatter(sector_data, x = "GDP Per Capita", y = metric1,
                size = "Population", color = "Country Name",height = 600, size_max= 55, title= f"<b>{metric1}</b> vs <b>GDP Per Capita Comparison</b> By Country")
    fig3.update_layout(showlegend=False, )
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

st.divider()

