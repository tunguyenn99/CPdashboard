import os
import io
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from PIL import Image
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import datetime as dt
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#############################################################################################################################################

st.set_page_config(page_title = "Dashboard")

# #Input text box
# path1 = st.text_input("Input Data file URL:",)
# path2 = st.text_input("Input Campaign Station URL:",)

#Upload files
path1 = st.file_uploader("Input Data file URL:",)
path2 = st.file_uploader("Input Campaign Station URL:",)


st.header("Campaign Landing page")

#############################################################################################################################################

# Loading CSV
# df = pd.read_csv("C:/Users/nguyen.minh.tu/Desktop/PYTHON/Jan2023/Feb_2023_all.csv",encoding="utf-8-sig")
# df1 = pd.read_csv("C:/Users/nguyen.minh.tu/Desktop/PYTHON/Jan2023/Jan_CP Station.csv")

# Use this when have input text box
df = pd.read_csv(path1)
df1 = pd.read_csv(path2)

# st.dataframe(df)
# st.dataframe(df1)


df["GMV"] = df["GMV"].round(0)
df["ADO"] = df["ADO"].round(0)

st.subheader("Filter")

source_selection = st.multiselect('Source:',
                                set(df["Seller Source"]),
                                default = set(df["Seller Source"])
                                )

batch_selection = st.multiselect('Batch:',
                                set(df["Batch"]),
                                default = set(df["Batch"])
                                )

lkam_selection = st.multiselect('LKAM:',
                                set(df["LKAM"]),
                                default = set(df["LKAM"])
                                )

ado_selection = st.slider("ADO range:",
                          min_value = min(df["ADO"]),
                          max_value = max(df["ADO"]),
                          value = (min(df["ADO"]),max(df["ADO"]))
                          )

mask = (df["Seller Source"].isin(source_selection))&(df["Batch"].isin(batch_selection))&(df["LKAM"].isin(lkam_selection))&(df["ADO"].between(*ado_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Kết quả: {number_of_result}*')

#number formatting
def billions(x, pos):
    return '%1.0f B' % (x*1e-9)
formatter_billions = FuncFormatter(billions)

def millions(x, pos):
    return '%1.0f M' % (x*1e-6)
formatter_millions = FuncFormatter(millions)

def thousands(x, pos):
    return '%1.0f K' % (x*1e-3)
formatter_thousands = FuncFormatter(thousands)


# Grouping data

## Group by ADO
ADO_byCP = dict(df[mask].groupby(by="Campaign name")["ADO"].sum().sort_values(ascending=False))

ADO_byLKAM = dict(df[mask].groupby(by="LKAM")["ADO"].sum().sort_values(ascending=False))
ADO_byLKAM_AtoZ = dict(df[mask].groupby(by="LKAM")["ADO"].sum().sort_values(ascending=True))

ADO_byBatch = dict(df[mask].groupby(by="Batch")["ADO"].sum().sort_values(ascending=False))
ADO_byCAT = dict(df[mask].groupby(by="CAT Data Go")["ADO"].sum().sort_values(ascending=False))
ADO_byGCAT = dict(df[mask].groupby(by="CAT Final")["ADO"].sum().sort_values(ascending=False))
ADO_bySource = dict(df[mask].groupby(by="Seller Source")["ADO"].sum().sort_values(ascending=False))
ADO_byTier = dict(df[mask].groupby(by="Tier")["ADO"].sum().sort_values(ascending=False))
ADO_byTiersource = dict(df[mask].groupby(by="Tier source")["ADO"].sum().sort_values(ascending=False))

## Group by GMV
GMV_byCP = dict(df[mask].groupby(by="Campaign name")["GMV"].sum().sort_values(ascending=False))
GMV_byLKAM = dict(df[mask].groupby(by="LKAM")["GMV"].sum().sort_values(ascending=False))
GMV_byBatch = dict(df[mask].groupby(by="Batch")["GMV"].sum().sort_values(ascending=False))
GMV_byCAT = dict(df[mask].groupby(by="CAT Data Go")["GMV"].sum().sort_values(ascending=False))
GMV_byGCAT = dict(df[mask].groupby(by="CAT Final")["GMV"].sum().sort_values(ascending=False))
GMV_bySource = dict(df[mask].groupby(by="Seller Source")["GMV"].sum().sort_values(ascending=False))
GMV_byTier = dict(df[mask].groupby(by="Tier")["GMV"].sum().sort_values(ascending=False))
GMV_byTiersource = dict(df[mask].groupby(by="Tier source")["GMV"].sum().sort_values(ascending=False))

## Group by ADO/slot
ADOperslot_byCP = dict((df[mask].groupby(by="Campaign name")["ADO"].sum()/df[mask].groupby(by="Campaign name")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byLKAM = dict((df[mask].groupby(by="LKAM")["ADO"].sum()/df[mask].groupby(by="LKAM")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byBatch = dict((df[mask].groupby(by="Batch")["ADO"].sum()/df[mask].groupby(by="Batch")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byCAT = dict((df[mask].groupby(by="CAT Data Go")["ADO"].sum()/df[mask].groupby(by="CAT Data Go")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byGCAT = dict((df[mask].groupby(by="CAT Final")["ADO"].sum()/df[mask].groupby(by="CAT Final")["ADO"].count()).sort_values(ascending=False))
ADOperslot_bySource = dict((df[mask].groupby(by="Seller Source")["ADO"].sum()/df[mask].groupby(by="Seller Source")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byTier = dict((df[mask].groupby(by="Tier")["ADO"].sum()/df[mask].groupby(by="Tier")["ADO"].count()).sort_values(ascending=False))
ADOperslot_byTiersource = dict((df[mask].groupby(by="Tier source")["ADO"].sum()/df[mask].groupby(by="Tier source")["ADO"].count()).sort_values(ascending=False))

## Group by ADO/item
ADOperitem_byCP = dict((df[mask].groupby(by="Campaign name")["ADO"].sum()/df[mask].groupby(by="Campaign name")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byLKAM = dict((df[mask].groupby(by="LKAM")["ADO"].sum()/df[mask].groupby(by="LKAM")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byBatch = dict((df[mask].groupby(by="Batch")["ADO"].sum()/df[mask].groupby(by="Batch")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byCAT = dict((df[mask].groupby(by="CAT Data Go")["ADO"].sum()/df[mask].groupby(by="CAT Data Go")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byGCAT = dict((df[mask].groupby(by="CAT Final")["ADO"].sum()/df[mask].groupby(by="CAT Final")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_bySource = dict((df[mask].groupby(by="Seller Source")["ADO"].sum()/df[mask].groupby(by="Seller Source")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byTier = dict((df[mask].groupby(by="Tier")["ADO"].sum()/df[mask].groupby(by="Tier")["ADO"].nunique()).sort_values(ascending=False))
ADOperitem_byTiersource = dict((df[mask].groupby(by="Tier source")["ADO"].sum()/df[mask].groupby(by="Tier source")["ADO"].nunique()).sort_values(ascending=False))

## Group by ADO/slot
GMVperslot_byCP = dict((df[mask].groupby(by="Campaign name")["GMV"].sum()/df[mask].groupby(by="Campaign name")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byLKAM = dict((df[mask].groupby(by="LKAM")["GMV"].sum()/df[mask].groupby(by="LKAM")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byBatch = dict((df[mask].groupby(by="Batch")["GMV"].sum()/df[mask].groupby(by="Batch")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byCAT = dict((df[mask].groupby(by="CAT Data Go")["GMV"].sum()/df[mask].groupby(by="CAT Data Go")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byGCAT = dict((df[mask].groupby(by="CAT Final")["GMV"].sum()/df[mask].groupby(by="CAT Final")["GMV"].count()).sort_values(ascending=False))
GMVperslot_bySource = dict((df[mask].groupby(by="Seller Source")["GMV"].sum()/df[mask].groupby(by="Seller Source")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byTier = dict((df[mask].groupby(by="Tier")["GMV"].sum()/df[mask].groupby(by="Tier")["GMV"].count()).sort_values(ascending=False))
GMVperslot_byTiersource = dict((df[mask].groupby(by="Tier source")["GMV"].sum()/df[mask].groupby(by="Tier source")["GMV"].count()).sort_values(ascending=False))

# Merge data

## Merge by LKAM
df_ADO_byLKAM = pd.DataFrame(ADO_byLKAM.items(),columns = ['LKAM','ADO']) #tạo DF gồm LKAM và ADO
df_ADOperslot_byLKAM = pd.DataFrame(ADOperslot_byLKAM.items(),columns = ['LKAM','ADO/slot']) #tạo DF gồm LKAM và ADO/slot
df_GMV_byLKAM = pd.DataFrame(GMV_byLKAM.items(),columns = ['LKAM','GMV']) #tạo DF gồm LKAM và GMV
df_GMVperslot_byLKAM = pd.DataFrame(GMVperslot_byLKAM.items(),columns = ['LKAM','GMV/slot']) #tạo DF gồm LKAM và GMV
df_ADO_GMV_byLKAM = df_ADO_byLKAM.merge(df_ADOperslot_byLKAM).merge(df_GMV_byLKAM).merge(df_GMVperslot_byLKAM) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_byLKAM["ADO"] = df_ADO_GMV_byLKAM["ADO"].round(1)
df_ADO_GMV_byLKAM["ADO/slot"] = df_ADO_GMV_byLKAM["ADO/slot"].round(1)
df_ADO_GMV_byLKAM["GMV/slot"] = df_ADO_GMV_byLKAM["GMV/slot"].round(1)


## Merge by CAT
df_ADO_byCAT = pd.DataFrame(ADO_byCAT.items(),columns = ['CAT','ADO']) #tạo DF gồm CAT và ADO
df_ADOperslot_byCAT = pd.DataFrame(ADOperslot_byCAT.items(),columns = ['CAT','ADO/slot']) #tạo DF gồm CAT và ADO/slot
df_GMV_byCAT = pd.DataFrame(GMV_byCAT.items(),columns = ['CAT','GMV']) #tạo DF gồm CAT và GMV
df_GMVperslot_byCAT = pd.DataFrame(GMVperslot_byCAT.items(),columns = ['CAT','GMV/slot']) #tạo DF gồm CAT và GMV
df_ADO_GMV_byCAT = df_ADO_byCAT.merge(df_ADOperslot_byCAT).merge(df_GMV_byCAT).merge(df_GMVperslot_byCAT) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_byCAT["ADO"] = df_ADO_GMV_byCAT["ADO"].round(1)
df_ADO_GMV_byCAT["ADO/slot"] = df_ADO_GMV_byCAT["ADO/slot"].round(1)
df_ADO_GMV_byCAT["GMV/slot"] = df_ADO_GMV_byCAT["GMV/slot"].round(1)


## Merge by Campaign
df_ADO_byCP = pd.DataFrame(ADO_byCP.items(),columns = ['Campaign name','ADO']) #tạo DF gồm CAT và ADO
df_ADOperslot_byCP = pd.DataFrame(ADOperslot_byCP.items(),columns = ['Campaign name','ADO/slot']) #tạo DF gồm CAT và ADO/slot
df_GMV_byCP = pd.DataFrame(GMV_byCP.items(),columns = ['Campaign name','GMV']) #tạo DF gồm CAT và GMV
df_GMVperslot_byCP = pd.DataFrame(GMVperslot_byCP.items(),columns = ['Campaign name','GMV/slot']) #tạo DF gồm CAT và GMV
df_ADO_GMV_byCP = df_ADO_byCP.merge(df_ADOperslot_byCP).merge(df_GMV_byCP).merge(df_GMVperslot_byCP) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_byCP["ADO"] = df_ADO_GMV_byCP["ADO"].round(1)
df_ADO_GMV_byCP["ADO/slot"] = df_ADO_GMV_byCP["ADO/slot"].round(1)
df_ADO_GMV_byCP["GMV/slot"] = df_ADO_GMV_byCP["GMV/slot"].round(1)

## Merge by Batch
df_ADO_byBatch = pd.DataFrame(ADO_byBatch.items(),columns = ['Batch','ADO']) #tạo DF gồm CAT và ADO
df_ADOperslot_byBatch = pd.DataFrame(ADOperslot_byBatch.items(),columns = ['Batch','ADO/slot']) #tạo DF gồm CAT và ADO/slot
df_GMV_byBatch = pd.DataFrame(GMV_byBatch.items(),columns = ['Batch','GMV']) #tạo DF gồm CAT và GMV
df_GMVperslot_byBatch = pd.DataFrame(GMVperslot_byBatch.items(),columns = ['Batch','GMV/slot']) #tạo DF gồm CAT và GMV
df_ADO_GMV_byBatch = df_ADO_byBatch.merge(df_ADOperslot_byBatch).merge(df_GMV_byBatch).merge(df_GMVperslot_byBatch) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_byBatch["ADO"] = df_ADO_GMV_byBatch["ADO"].round(1)
df_ADO_GMV_byBatch["ADO/slot"] = df_ADO_GMV_byBatch["ADO/slot"].round(1)
df_ADO_GMV_byBatch["GMV/slot"] = df_ADO_GMV_byBatch["GMV/slot"].round(1)


## Merge by Source
df_ADO_bySource = pd.DataFrame(ADO_bySource.items(),columns = ['Source','ADO']) #tạo DF gồm CAT và ADO
df_ADOperslot_bySource = pd.DataFrame(ADOperslot_bySource.items(),columns = ['Source','ADO/slot']) #tạo DF gồm CAT và ADO/slot
df_GMV_bySource = pd.DataFrame(GMV_bySource.items(),columns = ['Source','GMV']) #tạo DF gồm CAT và GMV
df_GMVperslot_bySource = pd.DataFrame(GMVperslot_bySource.items(),columns = ['Source','GMV/slot']) #tạo DF gồm CAT và GMV
df_ADO_GMV_bySource = df_ADO_bySource.merge(df_ADOperslot_bySource).merge(df_GMV_bySource).merge(df_GMVperslot_bySource) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_bySource["ADO"] = df_ADO_GMV_bySource["ADO"].round(1)
df_ADO_GMV_bySource["ADO/slot"] = df_ADO_GMV_bySource["ADO/slot"].round(1)
df_ADO_GMV_bySource["GMV/slot"] = df_ADO_GMV_bySource["GMV/slot"].round(1)


## Merge by Tier
df_ADO_byTier = pd.DataFrame(ADO_byTier.items(),columns = ['Tier','ADO']) #tạo DF gồm CAT và ADO
df_ADOperslot_byTier = pd.DataFrame(ADOperslot_byTier.items(),columns = ['Tier','ADO/slot']) #tạo DF gồm CAT và ADO/slot
df_GMV_byTier = pd.DataFrame(GMV_byTier.items(),columns = ['Tier','GMV']) #tạo DF gồm CAT và GMV
df_GMVperslot_byTier = pd.DataFrame(GMVperslot_byTier.items(),columns = ['Tier','GMV/slot']) #tạo DF gồm CAT và GMV
df_ADO_GMV_byTier = df_ADO_byTier.merge(df_ADOperslot_byTier).merge(df_GMV_byTier).merge(df_GMVperslot_byTier) #tạo DF gồm LKAM và ADO và ADO/slot và GMV
df_ADO_GMV_byTier["ADO"] = df_ADO_GMV_byTier["ADO"].round(1)
df_ADO_GMV_byTier["ADO/slot"] = df_ADO_GMV_byTier["ADO/slot"].round(1)
df_ADO_GMV_byTier["GMV/slot"] = df_ADO_GMV_byTier["GMV/slot"].round(1)
df_ADO_GMV_byTier = df_ADO_GMV_byTier.sort_values(by="Tier") #sort by Tier name

## Merge by Campaign Station

df1["Date"] = pd.to_datetime(df1["Date"],dayfirst=True)
df1["Date"] = df1["Date"].dt.date

Visitor_byDate = dict(df1.groupby(by="Date")["Unique Visitor"].sum()) 
Click_byDate = dict(df1.groupby(by="Date")["Click"].sum())
Pageview_byDate = dict(df1.groupby(by="Date")["Page View"].sum())
Impression_byDate = dict(df1.groupby(by="Date")["Impression"].sum())

df_Visitor_byDate  = pd.DataFrame(Visitor_byDate.items(),columns = ['Date','Unique Visitor']) #tạo DF gồm CAT và ADO
df_Click_byDate = pd.DataFrame(Click_byDate.items(),columns = ['Date','Click']) #tạo DF gồm CAT và ADO/slot
df_Pageview_byDate = pd.DataFrame(Pageview_byDate.items(),columns = ['Date','Page View']) #tạo DF gồm CAT và GMV
df_Impression_byDate = pd.DataFrame(Impression_byDate.items(),columns = ['Date','Impression']) #tạo DF gồm CAT và GMV

df_Traffic_byDate = df_Visitor_byDate.merge(df_Click_byDate).merge(df_Pageview_byDate).merge(df_Impression_byDate)


st.subheader("Traffic on Landing Pages")
df_Traffic_byDate

#############################################################################################################################################
fig, ax = plt.subplots(2,2,figsize = (15,10),gridspec_kw={'height_ratios':[2,2]})

#set range
range = np.arange(1,len(df_Traffic_byDate["Date"])+1,1)

    #CHART 1: Traffic by Visitor
ax[0,0].plot(range,
             df_Traffic_byDate["Unique Visitor"],
             color = "#f78357",
             marker='o')
ax[0,0].set_title("Visitor",size = 15,fontweight = "bold")
ax[0,0].set_ylabel("Unique Visitor",fontweight = "bold")
ax[0,0].set_xlabel("Date",fontweight = "bold")
ax[0,0].yaxis.set_major_formatter(formatter_thousands)
ax[0,0].locator_params(nbins=60, axis='x')
ax[0,0].set_xticks(range)
ax[0,0].grid()

    #CHART 2: Traffic by Click
ax[0,1].plot(range,
             df_Traffic_byDate["Click"],
             color = "#519544",
             marker='o')
ax[0,1].set_title("Click",size = 15,fontweight = "bold")
ax[0,1].set_ylabel("Click",fontweight = "bold")
ax[0,1].set_xlabel("Date",fontweight = "bold")
ax[0,1].yaxis.set_major_formatter(formatter_thousands)
ax[0,1].locator_params(nbins=60, axis='x')
ax[0,1].set_xticks(range)
ax[0,1].grid()

    #CHART 3: Traffic by Impression
ax[1,0].plot(range,
             df_Traffic_byDate["Impression"],
             color = "#fbd35c",
             marker='o')
ax[1,0].set_title("Impression",size = 15,fontweight = "bold")
ax[1,0].set_ylabel("Impression",fontweight = "bold")
ax[1,0].set_xlabel("Date",fontweight = "bold")
ax[1,0].yaxis.set_major_formatter(formatter_thousands)
ax[1,0].locator_params(nbins=60, axis='x')
ax[1,0].set_xticks(range)
ax[1,0].grid()

    #CHART 4: Traffic by PageView
ax[1,1].plot(range,
             df_Traffic_byDate["Page View"],
             color = "#5482ce",
             marker='o',
             linewidth=1.0)
ax[1,1].set_title("Page View",size = 15,fontweight = "bold")
ax[1,1].set_ylabel("Pageview",fontweight = "bold")
ax[1,1].set_xlabel("Date",fontweight = "bold")
ax[1,1].yaxis.set_major_formatter(formatter_thousands)
ax[1,1].set_xticks(range)
ax[1,1].grid()

    #Set title for bigchart
fig.suptitle('TRAFFIC ON LANDING PAGE', size = 26, fontweight = "bold", x = 0.6)
fig.tight_layout()

plt.subplots_adjust(right = 1.2, top = 0.9 , wspace = 0.1, hspace = 0.3)

st.pyplot(fig)


#############################################################################################################################################


## Traffic charts
bar_visitor = px.line(df_Traffic_byDate,x = "Date", y = "Unique Visitor", title = "Visitor",markers=True)
bar_visitor.update_traces(line_color='#f78357')
bar_visitor.update_xaxes(tickangle=300)
bar_visitor.update_layout(xaxis_tickformat = '%d %B (%a)')
bar_visitor.update_layout(xaxis = dict(tickmode = 'linear'))
st.plotly_chart(bar_visitor)

bar_click = px.line(df_Traffic_byDate,x = "Date", y = "Click", title = "Click",markers=True)
bar_click.update_traces(line_color='#519544')
bar_click.update_xaxes(tickangle=300)
bar_click.update_layout(xaxis_tickformat = '%d %B (%a)') #%d %B (%a)<br>%Y là có cả năm
bar_click.update_layout(xaxis = dict(tickmode = 'linear')) #show all date
st.plotly_chart(bar_click)

bar_impression = px.line(df_Traffic_byDate,x = "Date", y = "Impression", title = "Impression",markers=True)
bar_impression.update_traces(line_color='#fbd35c')
bar_impression.update_xaxes(tickangle=300)
bar_impression.update_layout(xaxis_tickformat = '%d %B (%a)')
bar_impression.update_layout(xaxis = dict(tickmode = 'linear'))
st.plotly_chart(bar_impression)

bar_pageview = px.line(df_Traffic_byDate,x = "Date", y = "Page View", title = "Page View",markers=True)
bar_pageview.update_traces(line_color='#5482ce')
bar_pageview.update_xaxes(tickangle=300)
bar_pageview.update_layout(xaxis_tickformat = '%d %B (%a)')
bar_pageview.update_layout(xaxis = dict(tickmode = 'linear'))
st.plotly_chart(bar_pageview)

#############################################################################################################################################

## Performance charts
st.subheader("Deals")

df

#Data grouping for CAT-Treemap
ADO_byCAT1 = df[mask].groupby(by="CAT Data Go")["ADO"].sum()
GMV_byCAT1 = df[mask].groupby(by="CAT Data Go")["GMV"].sum().to_list()
Slot_byCAT1 = df[mask].groupby(by="CAT Data Go")["Item id"].count()
Item_byCAT1 = df[mask].groupby(by="CAT Data Go")["Item id"].nunique() #count unique
ADOperslot_byCAT1 = (ADO_byCAT1/Slot_byCAT1).to_list()
ADOperitem_byCAT1 = (ADO_byCAT1/Item_byCAT1).to_list()

#Plot CAT-Treemap
fig = px.treemap(data_frame=df[mask], names = df[mask]["CAT Final"], values = df[mask]["ADO"].round(1), path=[px.Constant("<b>ALL CLUSTER</b>"),"CAT Final","CAT Data Go"],width = 705, height = 500)

fig.update_layout(
    title_text = "<b>BREAKDOWN BY G-CAT</b>", title_font = dict(color = "Black", size = 15),title_xanchor = "center",title_xref = "container", title_x = 0.5,
    paper_bgcolor = "White",
    font_color="White", #Đổi màu px.constant
    font_size = 15,
    hoverlabel_bordercolor = "White", #Đổi màu text của hover
    margin = dict(t=50, l=50, r=50, b=20),
    treemapcolorway = ["#df979e", "#e4bcad","#98d1d1","#a7b0e1"]
    )

fig.update_traces(root_color="#dedad2",insidetextfont = dict(color = "White",size = 15)) #Đổi màu px.constant

fig.data[0].customdata = np.column_stack([ADOperslot_byCAT1, ADOperitem_byCAT1,GMV_byCAT1])
fig.data[0].texttemplate = "%{label}<br>ADO: %{value:.2s}<br>ADO/slot: %{customdata[0]:.1f}<br>ADO/item: %{customdata[1]:.1f}<br>GMV: %{customdata[2]:.3s} VND"
fig.data[0].hovertemplate = "%{label}<br>ADO: %{value:.2s}<br>ADO/slot: %{customdata[0]:.1f}<br>ADO/item: %{customdata[1]:.1f}<br>GMV: %{customdata[2]:.3s} VND"

st.plotly_chart(fig)

#############################################################################################################################################

#Color whee
parachute = ["#3A63AD", "#3BB58F", "#3AA5D1", "#A86BD1","#E65F8E","#bcbcbc"] #parachute color
sunset = ["#FFCA3E", "#FF6F50", "#D03454", "#9C2162", "#772F67"] #sunset color
rainforest = ["#323B81", "#005FAA", "#0087AC", "#00A88F", "#82C272","#bcbcbc"] #rainforest color
rainforest_3 = ["#323B81", "#0087AC", "#82C272"] #rainforest-3-color
ocean = ["#003870", "#0A579E", "#1578CF", "#249CFF", "#77C2FE"] #ocean color
ocean_3 = ["#003870" , "#1578CF", "#77C2FE"] #ocean-3-color
foam = ["#d7658b","#df979e", "#e4bcad","#98d1d1", "#badbdb", "#dedad2"] #Foam
foam_3 = ["#df979e","#98d1d1", "#dedad2"]


#Plot big chart
fig, ax = plt.subplots(3,3,figsize = (18,20),gridspec_kw={'height_ratios':[3,2,2]})

    #CHART 1: ADO by Batch
ax[0,0].pie(ADO_byBatch.values(), autopct = "%1.1f%%", counterclock = False, startangle = 90, pctdistance = 1.15,wedgeprops ={'width': 0.5}, colors = foam_3)
ax[0,0].set_title("ADO by Batch",weight = "bold",size = 15)
ax[0,0].legend(ADO_byBatch.keys(),loc = "best", bbox_to_anchor=(1.1,1.1), title = "Batches")

    #CHART 2: ADO by Source
ax[0,1].pie(ADO_bySource.values(), autopct = "%1.1f%%", counterclock = False, startangle = 90, pctdistance = 1.15,wedgeprops ={'width': 0.5}, colors = foam)
ax[0,1].set_title("ADO by Source",weight = "bold",size = 15)
ax[0,1].legend(ADO_bySource.keys(),loc = "best", bbox_to_anchor=(1.1,1.1), title = "Sources")

    #CHART 3: ADO by Source
ax[0,2].pie(ADO_byTier.values(), autopct = "%1.1f%%", counterclock = False, startangle = 90, pctdistance = 1.15,wedgeprops ={'width': 0.5}, colors = foam_3)
ax[0,2].set_title("ADO by Tier",weight = "bold",size = 15)
ax[0,2].legend(ADO_byTier.keys(),loc = "best", bbox_to_anchor=(1.2,1.1), title = "Tier slot")

###############################################

    #CHART 4: ADO-ADO/slot by LKAM
ax[1,0].bar(df_ADO_GMV_byLKAM["LKAM"],df_ADO_GMV_byLKAM["ADO"],color = "#df979e")
ax[1,0].set_title("ADO & ADO/slot by LKAM",weight = "bold",size = 15)

ax[1,0].set_xticks(df_ADO_GMV_byLKAM["LKAM"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[1,0].set_xticklabels(df_ADO_GMV_byLKAM["LKAM"],rotation = 60, ha = "right")

ax[1,0].set_ylabel("ADO",fontweight = "bold")
ax[1,0].yaxis.set_major_formatter(formatter_thousands)
        #plot 2nd axis
ax2 = ax[1,0].twinx()
ax2.plot(df_ADO_GMV_byLKAM["LKAM"],df_ADO_GMV_byLKAM["ADO/slot"],color = "#c80064",marker='o')
ax2.set_ylabel("ADO/slot",fontweight = "bold")

    #CHART 5: ADO by CP
ax[1,1].bar(df_ADO_GMV_byCP["Campaign name"],df_ADO_GMV_byCP["ADO"],color = "#98d1d1")
ax[1,1].set_title("ADO & ADO/slot by CP",weight = "bold",size = 15)

ax[1,1].set_xticks(df_ADO_GMV_byCP["Campaign name"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[1,1].set_xticklabels(df_ADO_GMV_byCP["Campaign name"],rotation = 60, ha = "right")

ax[1,1].set_ylabel("ADO",fontweight = "bold")
ax[1,1].yaxis.set_major_formatter(formatter_thousands)
        #plot 2nd axis
ax2 = ax[1,1].twinx()
ax2.plot(df_ADO_GMV_byCP["Campaign name"],df_ADO_GMV_byCP["ADO/slot"],color = "#54bebe",marker='o')
ax2.set_ylabel("ADO/slot",fontweight = "bold")

    #CHART 6: ADO by CAT
ax[1,2].bar(df_ADO_GMV_byCAT["CAT"],df_ADO_GMV_byCAT["ADO"],color = "#a7b0e1")
ax[1,2].set_title("ADO & ADO/slot by CAT",weight = "bold",size = 15)

ax[1,2].set_xticks(df_ADO_GMV_byCAT["CAT"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[1,2].set_xticklabels(df_ADO_GMV_byCAT["CAT"],rotation = 60, ha = "right") #UserWarning:FixedFormatter should only be used together with FixedLocator

ax[1,2].set_ylabel("ADO",fontweight = "bold")
ax[1,2].yaxis.set_major_formatter(formatter_thousands)
        #plot 2nd axis
ax2 = ax[1,2].twinx()
ax2.plot(df_ADO_GMV_byCAT["CAT"],df_ADO_GMV_byCAT["ADO/slot"],color = "#4e60c9",marker='o')
ax2.set_ylabel("ADO/slot",fontweight = "bold")

###############################################


    #CHART 7: GMV-GMV/slot by LKAM
ax[2,0].bar(df_ADO_GMV_byLKAM["LKAM"],df_ADO_GMV_byLKAM["GMV"],color = "#ffd0b5")
ax[2,0].set_title("GMV & GMV/slot by LKAM",weight = "bold",size = 15)

ax[2,0].set_xticks(df_ADO_GMV_byLKAM["LKAM"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[2,0].set_xticklabels(df_ADO_GMV_byLKAM["LKAM"],rotation = 60, ha = "right")

ax[2,0].set_ylabel("GMV (VNĐ)",fontweight = "bold")
ax[2,0].yaxis.set_major_formatter(formatter_billions)
        #plot 2nd axis
ax2 = ax[2,0].twinx()
ax2.plot(df_ADO_GMV_byLKAM["LKAM"],df_ADO_GMV_byLKAM["GMV/slot"],color = "#A75D5D",marker='o')
ax2.set_ylabel("GMV/slot",fontweight = "bold")
ax2.yaxis.set_major_formatter(formatter_thousands)


    #CHART 8: GMV-GMV/slot by CP
ax[2,1].bar(df_ADO_GMV_byCP["Campaign name"],df_ADO_GMV_byCP["GMV"],color = "#a3d5ef")
ax[2,1].set_title("GMV & GMV/slot by CP",weight = "bold",size = 15)

ax[2,1].set_xticks(df_ADO_GMV_byCP["Campaign name"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[2,1].set_xticklabels(df_ADO_GMV_byCP["Campaign name"],rotation = 60, ha = "right")

ax[2,1].set_ylabel("GMV (VNĐ)",fontweight = "bold")
ax[2,1].yaxis.set_major_formatter(formatter_billions)
        #plot 2nd axis
ax2 = ax[2,1].twinx()
ax2.plot(df_ADO_GMV_byCP["Campaign name"],df_ADO_GMV_byCP["GMV/slot"],color = "#1984c5",marker='o')
ax2.set_ylabel("GMV/slot",fontweight = "bold")
ax2.yaxis.set_major_formatter(formatter_millions)


    #CHART 9: GMV-GMV/slot by CAT
ax[2,2].bar(df_ADO_GMV_byCAT["CAT"],df_ADO_GMV_byCAT["GMV"],color = "#dedad2")
ax[2,2].set_title("GMV & GMV/slot by CAT",weight = "bold",size = 15)

ax[2,2].set_xticks(df_ADO_GMV_byCAT["CAT"]) #This will fix below warning (UserWarning:FixedFormatter should only be used together with FixedLocator)
ax[2,2].set_xticklabels(df_ADO_GMV_byCAT["CAT"],rotation = 60, ha = "right")

ax[2,2].set_ylabel("GMV (VNĐ)",fontweight = "bold")
ax[2,2].yaxis.set_major_formatter(formatter_billions)
        #plot 2nd axis
ax2 = ax[2,2].twinx()
ax2.plot(df_ADO_GMV_byCAT["CAT"],df_ADO_GMV_byCAT["GMV/slot"],color = "#74726c",marker='o')
ax2.set_ylabel("GMV/slot",fontweight = "bold")
ax2.yaxis.set_major_formatter(formatter_thousands)


    #Set title for bigchart
fig.suptitle('CAMPAIGN BREAKDOWN', size = 26, fontweight = "bold", x = 0.65)
fig.tight_layout()

plt.subplots_adjust(right = 1.2, top = 0.9 , wspace = 0.3, hspace = 0.6)

st.pyplot(fig)
###################################################################
st.subheader("Breakdown by Batch")
df_ADO_GMV_byBatch
pie_Batch = px.pie(df_ADO_GMV_byBatch,values = "ADO",names = "Batch",color_discrete_sequence = foam_3,hole = 0.3) #color_discrete_sequence để chỉnh màu
st.plotly_chart(pie_Batch)


st.subheader("Breakdown by Source")
df_ADO_GMV_bySource
pie_Source = px.pie(df_ADO_GMV_bySource,values = "ADO",names = "Source",color_discrete_sequence = foam,hole = 0.3)
st.plotly_chart(pie_Source)

st.subheader("Breakdown by Tier")
df_ADO_GMV_byTier
pie_Tier = px.pie(df_ADO_GMV_byTier,values = "ADO",names = "Tier",color_discrete_sequence = foam_3,hole = 0.3) #color_discrete_sequence để chỉnh màu
st.plotly_chart(pie_Tier)

#############################################################################################################################################
st.subheader("Breakdown by LKAM")

df_ADO_GMV_byLKAM

barline_ADObyLKAM = go.Figure()

barline_ADObyLKAM.add_trace(go.Bar(x = df_ADO_GMV_byLKAM["LKAM"],y = df_ADO_GMV_byLKAM["ADO"],name = "ADO", yaxis = 'y',marker_color="#df979e"))
barline_ADObyLKAM.add_trace(go.Scatter(x = df_ADO_GMV_byLKAM["LKAM"],y = df_ADO_GMV_byLKAM["ADO/slot"],name = "ADO/slot",
                                       yaxis = "y2",mode = "markers+lines",marker_color="#b61867"))

barline_ADObyLKAM.update_layout(xaxis=dict(domain=[0.7, 0.3]
                                           ),
                                yaxis=dict(title="ADO",
                                           titlefont=dict(color="#df979e"),
                                           tickfont=dict(color="#df979e")
                                           ),
                                yaxis2=dict(title="ADO/slot",
                                            titlefont=dict(color="#b61867"),
                                            tickfont=dict(color="#b61867"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "ADO & ADO/slot by LKAM",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_ADObyLKAM.update_xaxes(tickangle=300)
barline_ADObyLKAM.update_yaxes(showgrid = False)
barline_ADObyLKAM.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_ADObyLKAM)

barline_GMVbyLKAM = go.Figure()

barline_GMVbyLKAM.add_trace(go.Bar(x = df_ADO_GMV_byLKAM["LKAM"],y = df_ADO_GMV_byLKAM["GMV"],name = "GMV", yaxis = 'y',marker_color="#ffd0b5"))
barline_GMVbyLKAM.add_trace(go.Scatter(x = df_ADO_GMV_byLKAM["LKAM"],y = df_ADO_GMV_byLKAM["GMV/slot"],name = "GMV/slot",
                                       yaxis = "y2",mode = "markers+lines",marker_color="#A75D5D"))

barline_GMVbyLKAM.update_layout(xaxis=dict(domain=[0.7, 0.3]
                                           ),
                                yaxis=dict(title="GMV",
                                           titlefont=dict(color="#ffd0b5"),
                                           tickfont=dict(color="#ffd0b5")
                                           ),
                                yaxis2=dict(title="GMV/slot",
                                            titlefont=dict(color="#A75D5D"),
                                            tickfont=dict(color="#A75D5D"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "GMV & GMV/slot by LKAM",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_GMVbyLKAM.update_xaxes(tickangle=300)
barline_GMVbyLKAM.update_yaxes(showgrid = False)
barline_GMVbyLKAM.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_GMVbyLKAM)

########################################
st.subheader("Breakdown by Campaign")

df_ADO_GMV_byCP
barline_ADObyCP = go.Figure()

barline_ADObyCP.add_trace(go.Bar(x = df_ADO_GMV_byCP["Campaign name"],y = df_ADO_GMV_byCP["ADO"],name = "ADO", yaxis = 'y',marker_color="#98d1d1"))
barline_ADObyCP.add_trace(go.Scatter(x = df_ADO_GMV_byCP["Campaign name"],y = df_ADO_GMV_byCP["ADO/slot"],name = "ADO/slot",
                                     yaxis = "y2",mode = "markers+lines",marker_color="#228181"))

barline_ADObyCP.update_layout(xaxis=dict(domain=[0.7, 0.3]),
                              yaxis=dict(title="ADO",
                                         titlefont=dict(color="#98d1d1"),
                                         tickfont=dict(color="#98d1d1")),
                                yaxis2=dict(title="ADO/slot",
                                            titlefont=dict(color="#228181"),
                                            tickfont=dict(color="#228181"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "GMV & GMV/slot by Campaign",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_ADObyCP.update_xaxes(tickangle=300)
barline_ADObyCP.update_yaxes(showgrid = False)
barline_ADObyCP.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_ADObyCP)

barline_GMVbyCP = go.Figure()

barline_GMVbyCP.add_trace(go.Bar(x = df_ADO_GMV_byCP["Campaign name"],y = df_ADO_GMV_byCP["GMV"],name = "GMV", yaxis = 'y',marker_color="#a3d5ef"))
barline_GMVbyCP.add_trace(go.Scatter(x = df_ADO_GMV_byCP["Campaign name"],y = df_ADO_GMV_byCP["GMV/slot"],name = "GMV/slot",
                                     yaxis = "y2",mode = "markers+lines",marker_color="#1984c5"))

barline_GMVbyCP.update_layout(xaxis=dict(domain=[0.7, 0.3]),
                              yaxis=dict(title="GMV",
                                         titlefont=dict(color="#a3d5ef"),
                                         tickfont=dict(color="#a3d5ef")),
                                yaxis2=dict(title="GMV/slot",
                                            titlefont=dict(color="#1984c5"),
                                            tickfont=dict(color="#1984c5"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "GMV & GMV/slot by Campaign",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_GMVbyCP.update_xaxes(tickangle=300)
barline_GMVbyCP.update_yaxes(showgrid = False)
barline_GMVbyCP.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_GMVbyCP)

########################################
st.subheader("Breakdown by CAT")

df_ADO_GMV_byCAT
barline_ADObyCAT = go.Figure()

barline_ADObyCAT.add_trace(go.Bar(x = df_ADO_GMV_byCAT["CAT"],y = df_ADO_GMV_byCAT["ADO"],name = "ADO", yaxis = 'y',marker_color="#a7b0e1"))
barline_ADObyCAT.add_trace(go.Scatter(x = df_ADO_GMV_byCAT["CAT"],y = df_ADO_GMV_byCAT["ADO/slot"],name = "ADO/slot",
                                      yaxis = "y2",mode = "markers+lines",marker_color="#4e60c9"))

barline_ADObyCAT.update_layout(xaxis=dict(domain=[0.7, 0.3]),
                              yaxis=dict(title="ADO",
                                         titlefont=dict(color="#a7b0e1"),
                                         tickfont=dict(color="#a7b0e1")),
                                yaxis2=dict(title="ADO/slot",
                                            titlefont=dict(color="#4e60c9"),
                                            tickfont=dict(color="#4e60c9"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "ADO & ADO/slot by CAT",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_ADObyCAT.update_xaxes(tickangle=300)
barline_ADObyCAT.update_yaxes(showgrid = False)
barline_ADObyCAT.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_ADObyCAT)

barline_GMVbyCAT = go.Figure()

barline_GMVbyCAT.add_trace(go.Bar(x = df_ADO_GMV_byCAT["CAT"],y = df_ADO_GMV_byCAT["GMV"],name = "GMV", yaxis = 'y',marker_color="#dedad2"))
barline_GMVbyCAT.add_trace(go.Scatter(x = df_ADO_GMV_byCAT["CAT"],y = df_ADO_GMV_byCAT["GMV/slot"],name = "GMV/slot",
                                      yaxis = "y2",mode = "markers+lines",marker_color="#74726c"))

barline_GMVbyCAT.update_layout(xaxis=dict(domain=[0.7, 0.3]),
                              yaxis=dict(title="GMV",
                                         titlefont=dict(color="#dedad2"),
                                         tickfont=dict(color="#dedad2")),
                                yaxis2=dict(title="GMV/slot",
                                            titlefont=dict(color="#74726c"),
                                            tickfont=dict(color="#74726c"),
                                            anchor="x", overlaying="y",
                                            side="right", position=0.15
                                            ),
                                title_text = "GMV & GMV/slot by CAT",
                                legend=dict(xanchor="center", x=1.2,yanchor="middle", y=1)
                                )
barline_GMVbyCAT.update_xaxes(tickangle=300)
barline_GMVbyCAT.update_yaxes(showgrid = False)
barline_GMVbyCAT.update_layout(xaxis = dict(tickmode = 'linear'))

st.plotly_chart(barline_GMVbyCAT)
