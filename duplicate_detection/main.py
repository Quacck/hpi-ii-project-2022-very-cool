import requests
from sympy import Q

def main():
    url ="http://localhost:9200/person-events/_search?pretty"
    query = """ 
    { \"query\": { 
            \"match_all\": { }
        }
    }
    """
    request = requests.get(url, headers={"Content-Type": "application/json"}, data=query)
    print(request.content)

    

if __name__=="__main__":
    main()
