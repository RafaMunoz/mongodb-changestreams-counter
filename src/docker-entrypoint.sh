#!/bin/sh
set -e

if [[ -z $URI_MONGODB_SRC ]]; then
	echo "A URI_MONGODB_SRC is required to run this container."
	exit 1
fi

if [[ -z $COLLECTION_SRC ]]; then
	echo "A COLLECTION_SRC is required to run this container."
	exit 1
fi

if [[ -z $URI_MONGODB_DST ]]; then
	export URI_MONGODB_DST=$(echo $URI_MONGODB_SRC)
fi

if [[ -z $COLLECTION_DST ]]; then
	export COLLECTION_DST=changestreams_count
fi

if [[ -z $COMMIT_SECONDS ]]; then
	export COMMIT_SECONDS=10
fi

exec "$@"



