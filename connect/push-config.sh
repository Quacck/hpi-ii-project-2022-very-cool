#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
LOBBY_CONFIG=${3:-"$(dirname $0)/elastic_sink_lobby.json"}
CORPORATE_CONFIG=${3:-"$(dirname $0)/elastic_sink_corporate.json"}

KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

lobby_data=$(cat $LOBBY_CONFIG | jq -s '.[0]')
corporate_data=$(cat $CORPORATE_CONFIG | jq -s '.[0]')

curl -X POST $KAFKA_CONNECT_API --data "$lobby_data" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$corporate_data" -H "content-type:application/json"
