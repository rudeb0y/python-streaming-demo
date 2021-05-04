# Really Simple Python Stream Example.

### How to Run

The solution contains three elements:
- docker to host zoopkeepr, kafka
- producer.py - simulates a stream
- page_views.py - consumes the `page_views` topic


#### Create a virtual environment, install requirements.txt.
```
  python3 -m venv .venv
  pip install -r requirements.txt
```

#### In a terminal at the root of the project, start the docker containers.
```
  docker-compose up
```


#### In a terminal window, start a worker to consume the stream (from the src/ directory)
```
  faust -A page_views worker -l info
```
This starts an application ready to consume stream.

#### In another terminal from the src/ directory, run producer.py
```
  python producer.py
```
This will send events to the kafka topic and we should see them get cosumed
in the other terminal.

All going to plan:
- kafka will be running on docker
- producer.py will be producing dummy data, simulating a stream of events
- the faust application (page_views.py) will be displaying counts for the 3 most recent events.

You can tweak the
### Thoughts
This was my first time using the `faust` python library.

Ordinarily, we'd hook this up to some sort of database, I have not done that here.

Nor have I partitioned this by date. Faust does support hopping/tumnling windows, which could be useful for the purposes of aggregated in last 7 days as the task asked for,
or I could have put into an actual database table and queried the data for that as well.

I kept the page number and users artifically low so that we could witness the counts
incrementing.

If you want to clear out the topics, you can connect to the docker container and run the scripts to clear them out e.g:

```
docker exec -it kafka-docker_kafka_1 bash
```
then
```
cd kafka/bin
kafka-topics.sh --zookeeper kafka-docker_zookeeper_1 --list
kafka-topics.sh --zookeeper kafka-docker_zookeeper_1 --delete --topic '(p).*'
```