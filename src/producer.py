from time import time, sleep
from json import dumps
from kafka import KafkaProducer
from uuid import uuid4
import random
import sys

# Assuming this was our website with limited number of pages.. so
# hard-coding to some known values.
# This helps with the tracking when the stream stops/starts as new
# new pages aren't introduced.
pages = [
    '443fb728-5f27-4500-8bc3-b6a8d544377b',
    '2af9e52f-5693-4219-9f7a-223f45e264c5',
    '19e7f2ea-a8f6-412a-8858-ae4486857894',
    'ea5b995f-4a06-4413-aafd-b0509fafcf31',
    '2af9e52f-5693-4219-9f7a-223f45e264c5',
]

users = [str(uuid4()) for _ in range(1, 50)]

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


class PageView:
    def __init__(self):
        self.userId = random.choice(users)
        self.pageId = random.choice(pages)
        self.timestamp = int(time() * 1000)

    def __str__(self):
        return str({
            "userId": self.userId,
            "pageId": self.pageId,
            "timestamp": self.timestamp
        })

    def __repr__(self):
        return f'PageView(userId={self.userId}, pageId={self.pageId}. timestamp=self.timestamp)'


def main():

    for j in range(int(9999)):
        print("Iteration", j)
        event = PageView()

        print(event)
        producer.send('page_views', value=event.__dict__)
        sleep(float(0.5))


if __name__ == "__main__":
    main()
