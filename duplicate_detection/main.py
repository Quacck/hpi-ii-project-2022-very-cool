import requests
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')

doc = {
    'id': 'ZRYONlLXXgeJmfdnKNt15eseoxr6qAfcxhBzkyHs2UI'
}

def main():
        offset = 0
        windows_size = 20
        while True:
            resp = es.search(index="person-events", from_=offset, sort=["city"] , size=windows_size, expand_wildcards="all")
            offset += windows_size
            for hit in resp['hits']['hits']:
                print(f'{hit["_source"]["city"]}')
            print("====================================================================")



if __name__=="__main__":
    main()
