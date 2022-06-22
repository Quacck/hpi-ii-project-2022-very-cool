import requests
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

doc = {
    'id': 'ZRYONlLXXgeJmfdnKNt15eseoxr6qAfcxhBzkyHs2UI'
}

def main():
        resp = es.search(index="person-events", expand_wildcards="all")
        print("Got %d Hits:" % resp['hits']['total']['value'])
        for hit in resp['hits']['hits']:
            print("%(first_name)s %(last_name)s" % hit["_source"])



if __name__=="__main__":
    main()
