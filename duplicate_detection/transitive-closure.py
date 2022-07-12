import uuid
from elasticsearch import Elasticsearch, helpers
import networkx as nx

es = Elasticsearch('http://localhost:9200')


def main():
        duplicates = helpers.scan(client=es, scroll="5m", index="person_duplicates", preserve_order=True)

        G = nx.Graph()

        for duplicate in duplicates:
            G.add_edge(duplicate["_source"]["first"], duplicate["_source"]["second"])

        for component_id, component in enumerate(nx.connected_components(G)):
            for person_id in component:
                es.create(index="person_duplicates_complete", id=person_id, body={"group": component_id})

if __name__=="__main__":
    main()
