import uuid
from elasticsearch import Elasticsearch, helpers
import editdistance
from torch import threshold, threshold_

es = Elasticsearch('http://localhost:9200')


def main():
        window_size = 5
        generator = helpers.scan(client=es, query= {"sort": ["city"]}, scroll="5m", index="person-events", preserve_order=True)
        window = [next(generator)]

        duplicates: set[tuple[str]] = set()

        # LOOP:
        try:
            while len(window) > 0:
                window.append(next(generator))
                if len(window) >= window_size: # fill up the window in the beginning
                    window.pop(0)

                for to_be_compared_element in window[:-1]:

                    if similarity(to_be_compared_element, window[-1]) > 0.8:
                        first_id = to_be_compared_element["_source"]["id"]
                        second_id = window[-1]["_source"]["id"]
                        # print(f'{first_id} is similar to {second_id}')
                        duplicates.add((first_id, second_id))
                        duplicates.add((second_id, first_id)) # make symmetric

        except StopIteration:
            # yoink
            print(f'FOUND {len(duplicates)} DUPLICATES')
            for duplicate in duplicates:
                es.create(index="person_duplicates", id=uuid.uuid4(), body={"first": duplicate[0],"second": duplicate[1]})


def similarity(a, b):
    # 1 is most similar, 0 is not similar

    distance_first_names = 1 / max(editdistance.eval(a["_source"]["first_name"], b["_source"]["first_name"]), 1)
    distance_last_names = 1 / max(editdistance.eval(a["_source"]["last_name"], b["_source"]["last_name"]),1 )
    distance_city = 1 / max(editdistance.eval(a["_source"]["city"], b["_source"]["city"]), 1)
    distance_birthday = 1 if editdistance.eval(a["_source"]["birth_date"], b["_source"]["birth_date"]) < 2 else 0

    return 0.35 * distance_first_names + 0.25 * distance_last_names + 0.05 * distance_city + 0.35 * distance_birthday

if __name__=="__main__":
    main()
