# MongoDB ChangeStreams Counter

If you want know how many Change there are in your collections MongoDB, you can use this Docker container for this.

The application subscribes to the changes of the collection that you indicate and will keep a count of the changes that have occurred. The number of changes will be stored every X seconds in another collection of the database or in another MongoDB database that you specify.

# Get Started

It can be easily launched with Docker using the image: **rafa93m/mongodb-changestreams-counter:latest**

## Environment Variables

| Name | Required | Default Value | Description |
|--|--|--|--|
|URI_MONGODB_SRC|Yes|-|Connection string for Source MongoDB database in standard format|
|URI_MONGODB_DST|No|The same database that you indicated in URI_MONGODB_SRC|Connection string for Destination MongoDB database in standard format|
|COLLECTION_SRC|Yes|-|Name of the source collection from which you want to obtain the number of changes|
|COLLECTION_DST|No|collection named changestream_count|Name of the collection in which you want to save the count|
|COMMIT_SECONDS|No|10 seconds|Value in seconds of how long the count is saved in the database|

## Data

If you run multiple containers, you can view count of any collections. An example of data stored on $COLLECTION_DST

```
/* 1 */
{
	 "_id" : ObjectId("6198127141999760038e467e"),
	 "date" : ISODate("2021-11-19T21:09:05.175Z"),
	 "collection" : "collection_test_1",
	 "count" : 31
}

/* 2 */
{
	 "_id" : ObjectId("6198129041999760038e467f"),
	 "date" : ISODate("2021-11-19T21:09:36.096Z"),
	 "collection" : "collection_test_2",
	 "count" : 28
}

/* 3 */
{
	 "_id" : ObjectId("619812af41999760038e4680"),
	 "date" : ISODate("2021-11-19T21:10:07.034Z"),
	 "collection" : "collection_test_1",
	 "count" : 127
}
```

## Volume

This container has a volume in `/app/data` that it is recommended to map.
In it the token of the last change of the Change Streams that has been read is saved, in this way if the container is restarted it is able to recover the count in the last change that was read.

## Docker Compose

An example of a Docker Compose to monitor a collection can be the following.

```yaml
version: '3.9'
services:
  changestreamsstats-coltest:
    image: rafa93m/mongodb-changestreams-counter:latest
    environment:
      URI_MONGODB_SRC: "mongodb+srv://user-1:password-1@cluster0.000z.mongodb.net/dbtest?retryWrites=true&w=majority"
      URI_MONGODB_DST: "mongodb+srv://user-2:password-2@cluster0.001z.mongodb.net/dbcount?retryWrites=true&w=majority"
      COLLECTION_SRC: "collection_test_1"
      COLLECTION_DST: "changestream_counter_1"
      COMMIT_SECONDS: 15
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```