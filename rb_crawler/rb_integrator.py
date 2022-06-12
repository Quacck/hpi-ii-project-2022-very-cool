from cgi import test
import logging
import re
import uuid

from build.gen.bakdata.corporate.v1.corporate_person_pb2 import Person
from build.gen.bakdata.corporate.v1.corporate_pb2 import Adress

from rb_producer import RbProducer

log = logging.getLogger(__name__)


# produces integrated events
class RbIntegrator:
    def __init__(self, corporate_event: any):
        self.producer = RbProducer()
        self.parse(corporate_event)

    def parse(self, corporate_event: any):
        information = corporate_event.information
        corporate_event.adress.CopyFrom(self.get_adress(information))
        corporate_event.corporate_name = self.get_corporate_name(information)
        person = None
        person = self.get_people(information)
        if not person is None:
            corporate_event.person_id = person.id

            self.producer.produce_to_persons(person)
        log.info('')

        log.info(f'{corporate_event.id} : {corporate_event.corporate_name}, {corporate_event.adress}, {person}')
        self.producer.produce_to_corporate_events(corporate_event)

        return corporate_event

    def get_adress(self, information: str):
        # Doberlug-Kirchhain(Finsterwalder Str. 16, 03253  Doberlug - Kirchhain). Nicht mehr Geschäftsführer:;1. Rosenow, Christian-Matthias; Geschäftsführer
        # tenburg KG, Zossen(Hauptstraße 44, 15806  Zossen OT Kallinchen, Errichtung und Betrieb von Windkraftanlagen.). Vertretungsregelung: Jeder persönli

        # do not care about the city name because thats too hard and the postal code is
        # unique anyway
        match = re.search(r'\(((.*), (\d{5})) .*\)\.', information)
        adress = Adress()

        if not match is None:
            adress.street = match.group(2)
            adress.postal_code = match.group(3)
        return adress

    def get_corporate_name(self, information: str):
        return re.search(r'^[^,]*', information).group(0) # match everything up to the first ,

    def get_people(self, information: str):
        # ührer:; 2. Zimmermann, Peer, *30.10.1962, Finsterwalde; mit der Befugnis die Gesellschaft allein zu vertreten mit der Befugnis Rechtsgeschäfte mit sich selbst oder als Vertreter Dritter abzuschließenProkura: 1. Rabe, Ingbert, *10.08.1961, Dreiheide OT Süptitz; Einzelprokura..
        # NANOFIX OHG, Belzig(Briesener Straße 13, 14806  Belzig OT Lütte, Vertrieb von chemischen und technischen Produkten für Handwerk und Industrie.). Vertretungsregelung: Jeder persönlich haftende Gesellschafter vertritt die Gesellschaft allein. persönlich haftender Gesellschafter: 1. Wernitz, Torsten, *26.05.1073, Belzig OT Schwanebeck; persönlich haftender Gesellschafter: 2. Zarbock, René, *02.11.1977, Belzig OT Lütte; Offene Handelsgesellschaft.

        match = re.search(r'([\w]+), ([\w -]+, )?([\w.\/ -]+), \*(\d{2}.\d{2}.\d{4})(, )?([\w.\/ -]+)?', information)

        if not match:
            return None
        person = Person()
        person.first_name = match.group(3)
        person.second_name = match.group(1)
        person.birthday = match.group(4)
        person.place_of_birth = match.group(6)
        person.id = str(uuid.uuid4()) # this is a random id not related to the data

        return person



if __name__ == "__main__":
    teststring = "Vattenfall Europe Mining Aktiengesellschaft, Cottbus(Vom-Stein-Straße 39, 03050  Cottbus). Nicht mehr Prokurist: 12. Dr. Florin, Jan-Henrich. Gegenstand"
    teststring2 = "BHR Baustoffe, Handel und Recycling GmbH, Doberlug-Kirchhain(Finsterwalder Str. 16, 03253  Doberlug - Kirchhain). Nicht mehr Geschäftsführer:;1. Rosenow, Christian-Matthias; Geschäftsführer:; 2. Zimmermann, Peer, *30.10.1962, Finsterwalde; mit der Befugnis die Gesellschaft allein zu vertreten mit der Befugnis Rechtsgeschäfte mit sich selbst oder als Vertreter Dritter abzuschließenProkura: 1. Rabe, Ingbert, *10.08.1961, Dreiheide OT Süptitz; Einzelprokura.."
    integrator = RbIntegrator()
    assert integrator.get_adress(teststring) == "Cottbus(Vom-Stein-Straße 39, 03050  Cottbus)"
    assert integrator.get_corporate_name(teststring) == "Vattenfall Europe Mining Aktiengesellschaft"
    print(integrator.get_people(teststring2))
