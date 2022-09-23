#importing all the modules needed
from pydoc import visiblename
import pandas as pd     
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv') #Reading data 
len(df) #91692
df.shape #(91692,25)

#Describing Data
df.info() #flaot64(6), int64(36), object(3)
df['COUNTY'].value_counts()
df_counties = df['COUNTY'].value_counts()
df_counties.head(20)

#Transforming Columns 
df['DATESTAMP']
#creaing a copy of existing column so we keep the orginal version
# we could also override the column if we wanted to, but beacuse we are unsure
# where we are going to take the analysis - lets just keep it

df['DATESTAMP_MOD'] = df['DATESTAMP']
print(df["DATESTAMP_MOD"].head(10))
print(df['DATESTAMP_MOD'].dtypes)

#for days 
df['DATESTAMP_MOD'] = pd.to_datetime(df['DATESTAMP_MOD'])
df['DATESTAMP_MOD'].dtypes
df[['DATESTAMP', 'DATESTAMP_MOD']]
df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.date
df['DATESTAMP_MOD_DAY']

#for years and months
df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year
df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month
df['DATESTAMP_MOD_YEAR']
df['DATESTAMP_MOD_MONTH']
df

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M')
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()

df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week
df['DATESTAMP_MOD_WEEK']

df['DATESTAMP_MOD_QUATER'] = df['DATESTAMP_MOD'].dt.to_period('Q')
df['DATESTAMP_MOD_QUATER'].sort_values()

df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)
df['DATETIME_STRING'] = df['DATESTAMP_MOD_MONTH_YEAR'].astype(str)
#Countries to anyalyze: Cobb, DeKalb, Fulton, Gwinnett, Hall
df['COUNTY']
countList = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countList

selectCounties = df[df['COUNTY'].isin(countList)]
len(selectCounties)

#Now looking for sepecific date/time frame we want
selectCountyTime = selectCounties
selectCountyTime['DATESTAMP_MOD_MONTH_YEAR']
selectCountTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountTime_april2020)

selectCountTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectCountTime_aprilmay2020)

# creating "final dataframe" 
# aka specfic columns,features, attributes, that we will need to anyalze
finalDF = selectCountTime_aprilmay2020[[
'COUNTY',
'DATESTAMP_MOD', 
'DATESTAMP_MOD_DAY', 
'DATESTAMP_MOD_DAY_STRING', 
'DATETIME_STRING', 
'DATESTAMP_MOD_MONTH_YEAR',
'C_New', #Cases- New
'C_Cum', #Cases-Total
'H_New', #hospitalization - New
'H_Cum', #Hospitalizations - Total
'D_New', #Deaths- New
'D_Cum'  #Deaths - Total
]]
finalDF
#we have dups we need to get rid of 
finalDF_dropdups = finalDF.drop_duplicates(subset=['COUNTY', 'DATETIME_STRING'], keep='last')
finalDF_dropdups


#visuals will not show up on VS 
pd.pivot_table(finalDF_dropdups, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)
visl = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finalDF_dropdups)

vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue='COUNTY', data=finalDF_dropdups)
print(visl)

#SHOWS ON BROWSING APPLICATION (GOOGLE, FIREFOX, OPERA, INTERNET EXPLORERER, etc)
plotly1 = px.bar(finalDF_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotly1.show()

#VIEWING TOTAL COVID CASES BY DAY 

daily =finalDF
daily 
len(daily)

pd.pivot_table(daily, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)

tempdf = pd.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'], columns=['COUNTY'], aggfunc=np.sum)
tempdf.head(50)

startdate = pd.to_datetime('2020-04-26').date()
enddate = pd.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <=enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']
vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')
vis4 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')
#C_Cum
plotly3 = px.bar(dailySpecific, x="DATESTAMP_MOD_DAY", y="C_Cum", color="COUNTY")
plotly3.show()
#H_New
plotly4 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='H_New', color="COUNTY", barmode='group')
plotly4.show()
#H_Cum
plotly5 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='H_Cum', color="COUNTY", barmode='group')
plotly5.show()
#D_new
plotly6 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='D_New', color="COUNTY", barmode='group')
plotly6.show()
#D_Cum
plotly7 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='D_Cum', color="COUNTY", barmode='group')
plotly7.show()


dailySpecific['newHospandDeathCOVID'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newHospandDeathCOVID']

plotly8 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='newHospandDeathCOVID', color="COUNTY", barmode='group')
plotly8.show()

dailySpecific['newHospandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int)
dailySpecific['newHospandDeath']

plotly9 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='newHospandDeathCOVID', color="COUNTY", 
                    title="Georgia 2020 Cvoid Data: Total New Hospitalization, Death, and COVID,cases by County", 
                    labels={"DATESTAMP_MOD_DAY" : "Time (Month, Day, Year)", 
                    "newHospandDeathCOVID" : "Total Count"
                    }, 
                    barmode='group')
plotly9.update_layout(
        xaxis = dict(
            tickmode = 'linear', 
            type='category'
        )
)
plotly9.show()