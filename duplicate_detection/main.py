from email.generator import Generator
import json
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')


def main():
        window_size = 10
        generator = get_next_event_batch()
        buffer = next(generator)
        window = [buffer.pop(0)]

        # LOOP:
        while len(window) > 0:
            window.append(buffer.pop(0))
            if len(window) < window_size: # fill up the window in the beginning
                window.pop(0)

            for to_be_compared_element in window[:-1]:
                if check_for_duplicate(to_be_compared_element, window[-1]):
                    print('oh snap!')

            if len(buffer) == 0:
                # TODO: Fehlerbehandlung falls generator leer ist
                buffer = next(generator)
            
def get_next_event_batch():
    offset = 0
    request_size = 100
    while True:
        new_response = es.search(index="person-events", from_=offset, sort=["city"] , size=request_size, expand_wildcards="all")
        offset += request_size
        yield list(new_response['hits']['hits']) 

def check_for_duplicate(a, b):
    print(f'{a["_source"]["first_name"]} gets compared to {b["_source"]["first_name"]}')
    return a["_source"]["first_name"] == b["_source"]["first_name"]

if __name__=="__main__":
    main()
