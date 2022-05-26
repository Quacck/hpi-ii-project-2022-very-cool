#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
LOBBY_CONFIG=${3:-"$(dirname $0)/elastic_sink_corporate.json"}
CORPORATE_CONFIG=${3:-"$(dirname $0)/elastic_sink_lobby.json"}

KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

LOBBY_NAME=$(jq -r .name $LOBBY_CONFIG)
CORPORATE_NAME=$(jq -r .name $CORPORATE_CONFIG)

curl -Is -X DELETE $KAFKA_CONNECT_API/$LOBBY_NAME
curl -Is -X DELETE $KAFKA_CONNECT_API/$CORPORATE_NAME
