from atexit import register
import logging
from time import sleep

import json

import build.gen.lobbyregister.lobby_generated_pb2 as lobby
from google.protobuf.descriptor import FieldDescriptor
from lr_producer import LrProducer

log = logging.getLogger(__name__)


class LrExtractor:
    def __init__(self):
        self.producer = LrProducer()

    def extract_everything(self):
        with open('data/all.json') as file:
            data = json.load(file)
            for entry in data['results']:
                log.info(f"Found new Entry with ID: {entry['registerNumber']}")
                protobuf_object = self.parse_default(entry, lobby.Entry())
                self.producer.produce_to_topic(protobuf_object)
                
                

    def parse_default(self, jsonTree, current):
        for field in current.DESCRIPTOR.fields:
            if field.name not in jsonTree:
                continue
            value = self.parse_field(field, jsonTree[field.name])
            if field.label == FieldDescriptor.LABEL_REPEATED:
                getattr(current, field.name).extend(value)
            elif field.type == FieldDescriptor.TYPE_MESSAGE:
                getattr(current, field.name).CopyFrom(value)
            else:
                setattr(current, field.name, self.parse_primitive(value))
            
        return current

    def parse_field(self, field: FieldDescriptor, jsonTree, useArray = True):
        if useArray and field.label == FieldDescriptor.LABEL_REPEATED:
            return self.parse_array(field, jsonTree)
        elif field.type == FieldDescriptor.TYPE_MESSAGE:
            return self.parse_message(field, jsonTree)
        else:
            return self.parse_primitive(jsonTree)

    def parse_array(self, field: FieldDescriptor, array: list):
        return [self.parse_field(field, element, False) for element in array]

    def parse_message(self, field, jsonTree):
        message = self.create_object_for_field(field)
        return self.parse_default(jsonTree, message)

    def parse_primitive(self, jsonTree):
        return jsonTree

    def create_object_for_field(self, field: FieldDescriptor):
        class_ = getattr(lobby, field.message_type.name)
        return class_()
