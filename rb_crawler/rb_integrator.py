import logging
import re

#from build.gen.bakdata.corporate.v1 import corporate_pb2
# from build.gen.bakdata.corporate.v1.corporate_pb2 import Corporate
# from rb_crawler.constant import SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVER, TOPIC

log = logging.getLogger(__name__)


class RbIntegrator:
    def __init__(self):
        pass

    def map(self, shitty_event):
        if shitty_event.event_type != 'create':
            return

        self.parse(shitty_event.information)

    def parse(self, information: str):
        # name_and_adress = re.search(r'(.*?)(?=. Gegenstand)',information)
        adress = re.search(r'\w+\((.*)\)', information) # match Word(anything)
        corporate_name = re.search(r'^[^,]*', information) # match everything up to the first ,
        print('found ', corporate_name.group(0), ' at ', adress.group(0))

if __name__ == "__main__":
    integrator = RbIntegrator()
    integrator.parse("Vattenfall Europe Mining Aktiengesellschaft, Cottbus(Vom-Stein-Straße 39, 03050  Cottbus). Nicht mehr Prokurist: 12. Dr. Florin, Jan-Henrich. Gegenstand")