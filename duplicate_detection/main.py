from elasticsearch import Elasticsearch, helpers

es = Elasticsearch('http://localhost:9200')


def main():
        window_size = 10
        generator = helpers.scan(client=es, query= {"sort": ["city"]}, scroll="5m", index="person-events", preserve_order=True)
        window = [next(generator)]

        # LOOP:
        while len(window) > 0:
            window.append(next(generator))
            print(window[-1]["_source"]["city"])
            if len(window) >= window_size: # fill up the window in the beginning
                window.pop(0)

            for to_be_compared_element in window[:-1]:

                if check_for_duplicate(to_be_compared_element, window[-1]):
                    print('oh snap!')

def check_for_duplicate(a, b):
    # print(f'{a["_source"]["city"]} gets compared to {b["_source"]["city"]}')
    return a["_source"]["first_name"] == b["_source"]["first_name"]

if __name__=="__main__":
    main()
