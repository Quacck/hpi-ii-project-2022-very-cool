from elasticsearch import Elasticsearch, helpers
import uuid

es = Elasticsearch('http://localhost:9200')


def main():
    lobby_events = helpers.scan(client=es, scroll="5m", index="lobbyregister-events", preserve_order=True)

    person_to_spendings = {}

    for lobby_event in lobby_events:
        corporate_name = lobby_event["_source"]["registerEntryDetail"]["lobbyistIdentity"]["name"]
        # # print(corporate_name)

        query_body = {
            "query": {
                "match": {
                    "name": corporate_name
                }
            }
        }

        result = es.search(index="organization_events", body=query_body)

        # entsprechende(s?) registerbekanntmachungs-event finden vif (result["hits"]["hits"]):ia ES
        if result["hits"]["hits"]:
            best_result = result["hits"]["hits"][0]
            ## print (corporate_name, ' ======> ', best_result["_source"]["name"]) 

            for legal_representative in best_result["_source"]["legal_representatives"]:
                # dazu die person aus person_events via personid aus oben holen via ES
                # finde die duplikat-gruppe, falls vorhanden 

                person_query_body = {
                    "query": {
                        "match": {
                            "id": legal_representative["person_id"]
                        }
                    }
                }

                person_result = es.search(index="person-events", body=person_query_body)
                
                group_query_body = {
                    "query": {
                        "match": {
                            "_id": legal_representative["person_id"]
                        }
                    }
                }

                group_result = es.search(index="person_duplicates_complete", body=group_query_body)

                group_id = uuid.uuid4()

                if group_result["hits"]["hits"]:
                    group_id = group_result["hits"]["hits"][0]["_source"]["group"]


                if group_id in person_to_spendings: 
                    person_to_spendings[group_id]["number_of_lobbies"] += 1
                    person_to_spendings[group_id]["companies"] += [best_result["_source"]["name"]]
                    person_to_spendings[group_id]["amount_money"] += (lobby_event["_source"]["registerEntryDetail"]["financialExpensesEuro"] or {"to" : 0})["to"]

                else: 
                    person_to_spendings[group_id] = {
                        "number_of_lobbies": 1,
                        "amount_money": (lobby_event["_source"]["registerEntryDetail"]["financialExpensesEuro"] or {"to" : 0})["to"],
                        "companies": [best_result["_source"]["name"]],
                        "name": person_result["hits"]["hits"][0]["_source"]["first_name"] + ' ' + person_result["hits"]["hits"][0]["_source"]["last_name"]
                    }


        # abspeichern!
    to_sort = list(person_to_spendings.items())
    to_sort.sort(key=lambda x: x[1]["number_of_lobbies"], reverse=True)

    for spendings in person_to_spendings.items():
        es.create(index="group_to_spendings", id=spendings[0], body=spendings[1])

if __name__=="__main__":
    main()
