from elasticsearch import Elasticsearch, helpers
import plotly.graph_objects as go
es = Elasticsearch('http://localhost:9200')


def main():
    scan = helpers.scan(client=es, scroll="5m", index="group_to_spendings", preserve_order=True)

    results = [element["_source"] for element in list(scan)]

    results.sort(key=lambda x: x["number_of_lobbies"], reverse=True)

    xArray = [element["name"] for element in results][:20]
    yArray_number = [element["number_of_lobbies"] for element in results][:20]
    #yArray_amount = [element["amount_money"] for element in results][:20]

    hoverArray = ['<br>'.join(element["companies"]) for element in results][:20]

    hovertemp = '<b>Companies</b><br>'
    # for elem in hoverArray:
    hovertemp += '%{customdata}'
    
    fig = go.Figure([go.Bar(x=xArray, y=yArray_number, customdata=hoverArray)])
    fig.update_traces(hovertemplate=hovertemp)
    fig.show()

    results.sort(key=lambda x: x["amount_money"], reverse=True)

    xArray = [element["name"] for element in results][:20]
    #yArray_number = [element["number_of_lobbies"] for element in results][:20]
    yArray_amount = [element["amount_money"] for element in results][:20]

    hoverArray = ['<br>'.join(element["companies"]) for element in results][:20]

    hovertemp = '<b>Companies</b><br>'
    # for elem in hoverArray:
    hovertemp += '%{customdata}'
    
    fig = go.Figure([go.Bar(x=xArray, y=yArray_amount, customdata=hoverArray)])
    fig.update_traces(hovertemplate=hovertemp)
    fig.show()



    print(results)


if __name__=="__main__":
    main()
