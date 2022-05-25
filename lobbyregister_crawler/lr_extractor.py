import logging
from time import sleep

import json
import requests

# from build.gen.lobbyregister.lobby_pb2 import *
import build.gen.lobbyregister.lobby_generated_pb2 as lobby
from google.protobuf.descriptor import FieldDescriptor
# from lr_producer import LrProducer

log = logging.getLogger(__name__)


class LrExtractor:
    def __init__(self):
        pass
        # self.producer = LrProducer()

    def extract_everything(self):
        with open('data/not_all.json') as file:
            data = json.load(file)
            for entry in data['results']:
                # somehow_produce_entry(entry)
                log.info(f"Found new Entry with ID: {entry['registerNumber']}")
                registerEntry = self.parse_default(entry, lobby.Entry())
                log.info(registerEntry)


    def parse_default(self, jsonTree, current):

        for field in current.DESCRIPTOR.fields:
            if field.type != FieldDescriptor.TYPE_MESSAGE:
                if field.label != FieldDescriptor.LABEL_REPEATED:
                    self.smart_set(current, field, jsonTree[field.name])
                else:
                    self.smart_set(getattr(current, field.name), [self.parse_default() for element in ])

            else:
                class_ = getattr(lobby, field.message_type.name)
                child_instance = class_()
                self.smart_set(current, field, self.parse_default(jsonTree[field.name], child_instance))
        return current

    def smart_set(self, object, field, content):
        if isinstance(object, list):
            object.append(content)

        if field.label == FieldDescriptor.LABEL_REPEATED:
            getattr(object, field.name).extend(content)
        else:
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                getattr(object, field.name).CopyFrom(content)
            else:
                setattr(object, field.name, content)




    # def parse_register_entry(self, root):
    #     registerEntry = lobby.RegisterEntry()
    #     registerEntry.registerNumber = root['registerNumber']
    #     registerEntry.registerEntryDetail.CopyFrom(self.parse_detail(root['registerEntryDetail']))
    #     return registerEntry

    # def parse_detail(self, root):
    #     registerEntryDetail = lobby.Detail()
    #     registerEntryDetail.id = root["id"]
    #     registerEntryDetail.employeeCount.CopyFrom(self.parse_range(root['employeeCount']))
    #     registerEntryDetail.activityDescription = root['activityDescription']
    #     return registerEntryDetail

    # def parse_range(self, root):
    #     rangeData = lobby.Range()
    #     rangeData.begin = root['from']
    #     rangeData.end = root['to']
    #     return rangeData
