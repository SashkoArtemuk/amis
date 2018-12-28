import re
import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

dataset={}

def getNumber(line):
    number=re.findall("^\d+",line)
    newLine=re.sub(number[0]+",",'',line)
    return number[0],newLine

def getJob(line):
    if(line[0]=="\""):
        result = re.split("\",", line, 1)
    else:
        result = re.split(",", line, 1)
    job=re.sub("^ +","",result[0])
    job = re.sub("$ +", "", result[0])
    job=re.sub("\"","",job)
    return job,result[1]

def getLocation(line):
    result = re.split("\",",line,1)
    location = re.sub("\"", "", result[0])
    return location,result[1]

def getCountry(line):
    result = re.split(",",line,1)
    return result[0],result[1]

def getEstate(line):
    result = re.split(",", line, 1)
    result[0]=re.sub(" ", "", result[0])
    if len(result)==1 or len(result[0])>2:
        return None,result[0]
    return result[0], result[1]

def getCity(line):
    city=line.lower()
    city = re.sub("^ +", "", city)
    if not city:
        return None
    city=city[0].upper()+city[1:]
    temp=re.findall(" [a-z]",city)
    if temp:
        for el in temp:
            index=city.find(el)+1
            city=city[0:index]+city[index].upper()+city[index+1:]
    return city

def getDate(line):
    result = re.split("\",",line,1)
    result[0] = re.sub("^\"",'',result[0])
    return result[0],result[1]

def getBasicQualifications(line):
    line=re.sub("\\n",'',line)
    result=re.split("\",\"",line)
    if len(result)==1:
        return result[0],None
    if not len(result[1]):
        return result[0],None
    return result[0],result[1]

def getDatasetFromFile(filename):
    try:
        with open(filename,'r',encoding="utf-8") as file:
            header=file.readline().rstrip().upper().replace(" ",'')
            header_nice=re.split(",",header)
            #print(header_nice)
            currentLine=0
            for line in file:
                currentLine+=1
                if(line.rstrip()):
                    number,line=getNumber(line)
                    job,line=getJob(line)
                    location,line=getLocation(line)
                    country,location=getCountry(location)
                    estate,location=getEstate(location)
                    city=getCity(location)
                    date,line=getDate(line)
                    basicQualifications,line=getBasicQualifications(line)
                    dataset[number]={"job":job,"location":{"country":country,"estate":estate,"city":city},"date":date,"basicQualifications":basicQualifications,"requiredQualifications":line}
                    #print(number,'\n',basicQualifications,"\n",line)



    except IOError:
        print("Input/Output error")
    except ValueError:
        print("Error in data, line: ",currentLine)

def printDataset(currentDataset):
    for el in dataset:
        print(el, '\n', currentDataset[el]["job"], '\n', currentDataset[el]["location"], '\n', currentDataset[el]["date"], '\n',
              currentDataset[el]["basicQualifications"], '\n', currentDataset[el]["requiredQualifications"], '\n')

def plots(currentDataset):
    jobsPerYear={}
    jobsInCountry={}
    jobsCount={}
    for el in currentDataset:
        year=re.findall("\d{4}",currentDataset[el]["date"])[0]
        if not year in jobsPerYear:
            jobsPerYear[year]=1
        else:
            jobsPerYear[year]+=1

        country=currentDataset[el]["location"]["country"]
        if not country in jobsInCountry:
            jobsInCountry[country]=1
        else:
            jobsInCountry[country]+=1

        job=currentDataset[el]["job"]
        if not job in jobsCount:
            jobsCount[job]=1
        else:
            jobsCount[job]+=1

    """plot1=go.Scatter(x=list(jobsPerYear.keys()),y=list(jobsPerYear.values()),xaxis="x1")
    plot2=go.Bar(x=list(jobsInCountry.keys()),y=list(jobsInCountry.values()),xaxis="x2")
    plot3=go.Pie(labels=list(jobsCount.keys()),values=list(jobsCount.values()),domain={'x': [0.5, 1], 'y': [0.2, 1]},showlegend=True)

    traces=[plot1,plot2,plot3]

    fig=go.Figure(layout=go.Layout(width=1800), data=traces)

    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}
    fig.layout.xaxis.update({'domain': [0, 0.25]})
    fig.layout.xaxis2.update({'domain': [0.26, 0.49]})


    plotly.offline.plot(fig,filename="plot.html")"""
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='DataScience'),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': list(jobsPerYear.keys()), 'y': list(jobsPerYear.values()), 'type': 'bar', 'name': 'Amount'},
                ],
                'layout': {
                    'title': 'Jobs per year'
                }
            }
        ),
        dcc.Graph(
            id='example-graph2',
            figure={
                'data': [
                    {'x':list(jobsInCountry.keys()), 'y': list(jobsInCountry.values()), 'type': 'bar', 'name': 'Amount'},
                ],
                'layout': {
                    'title': 'Jobs per country'
                }
            }
        ),
        dcc.Graph(
            id='example-graph3',
            figure={
                'data': [
                    {'labels':list(jobsCount.keys()), 'values': list(jobsCount.values()), 'showlegend':False, 'type': 'pie', 'name': 'Amount'},
                ],
                'layout': {
                    'title': 'Jobs amount'
                }
            }
        )

    ])
    app.run_server(debug=True)



getDatasetFromFile("amazon_jobs_dataset.csv")
#printDataset(dataset)
plots(dataset)
