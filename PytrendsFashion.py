import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pytrends.request import TrendReq

pytrend = TrendReq()

## Fashion search terms we want to look up
sr_terms = ['dresses', 'sandals', 'shorts', 'swimsuits']

## Build dataframe to hold data
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
df = pd.DataFrame(states)
df.columns = ['states']

## For each search term, send a PyTrends request
## Each request must be separate, otherwise they are scored in relation to each other
## The data comes in alphabetically by US state, same as the [states] values
for term in sr_terms:
    pytrend.build_payload(kw_list = [term],
                          cat = 185,  ## cat 185 is the Fashion & Style subsection of Google search trends
                          timeframe ='today 3-m',
                          geo ='US',
                          gprop ='')
    sr_result = pytrend.interest_by_region(resolution='REGION').iloc[:,0].values
    df[term] = sr_result
    
## Set up variables for plotting the data
rows = 2
cols = 2
subtitles = [df.columns[i].title() for i in range(1, len(df.columns))]
                                  
fig = make_subplots(rows=rows, 
                    cols=cols, 
                    specs = [[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)],
                    subplot_titles = subtitles, vertical_spacing=0.1, horizontal_spacing=0)

## For each search term, format the plot
for srtrm in enumerate(sr_terms):
    fig.add_trace(go.Choropleth(locations=df['states'], z = df[srtrm[1]],
    locationmode = 'USA-states', zmin=1, zmax=100, colorscale='Blues',
    showscale = False, reversescale = False, text = df[srtrm[1]], marker_line_color = 'black',
    hoverinfo = 'text'),
    row = srtrm[0]//cols+1, col = srtrm[0]%cols+1)

## Update the master page setup
fig.update_layout(
    title={'text':'Fashion-Related Search Term Popularity, Past 3 Months', 'xanchor': 'center', 'x':0.5},
    coloraxis_showscale=False, margin={'r':10,'t':70,'l':10,'b':0})


## Update the maps and plot it
fig.update_geos(projection_type="albers usa")
fig.update_traces(showscale=True)
plot(fig, filename = 'templot.html')