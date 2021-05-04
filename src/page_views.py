import faust
from collections import Counter, deque

app = faust.App(
    'example-count',
    broker='kafka://localhost:9092',
    topic_partitions=4,
)



class PageView(faust.Record):
    userId: str
    pageId: str
    timestamp: int


topic = app.topic('page_views', value_type=PageView)

page_views = app.Table(
    'page_views',
    default=int
)

# to demonstrate the point, tables support tumbling and hopping windows.
# could set this to expire in 7 days for that partiulcar count - or stream
# to a database and aggregate/report the last_7_days that way.
page_views_by_user = app.Table(
    'page_views_by_user',
    default=Counter,

)

# not the best way of doing it but as in rush implemented a deque to track
# last 3 visits to help with display later.
recent_visitors = deque()
@app.agent(topic)
async def track_recent_visitors(views):
    async for view in views.group_by(PageView.userId):

        if len(recent_visitors) > 2:
            recent_visitors.popleft()

        recent_visitors.append(view.userId)

@app.agent(topic)
async def count_page_views(views):
    """Capture the page count
    """
    async for view in views.group_by(PageView.pageId):
        page_views[view.pageId] += 1


@app.agent(topic)
async def count_page_views_by_user(stream):
    """Captures the user/page count
    """
    async for event in stream.group_by(PageView.userId):

        counter = Counter([event.pageId])
        old_value = page_views_by_user[event.userId]
        new_value = old_value + counter
        page_views_by_user[event.userId] = new_value


@app.agent(topic)
async def count_page_views_by_user(stream):
    """Captures the user/page count
    """
    async for event in stream.group_by(PageView.userId):

        counter = Counter([event.pageId])
        old_value = page_views_by_user[event.userId]
        new_value = old_value + counter
        page_views_by_user[event.userId] = new_value


@app.timer(10)
async def recent_activity():


    for user in recent_visitors:
        page_tracker = page_views_by_user[user]

        print(f'Page Vists by User - {user}')
        for page, count in page_tracker.items():
            print(f'\tPage: {page}, Count: {count}', sep='\n')
        # if i < 5:
        #     print(f'User: {user}', end='\n\n')
        #     for page, count in page_counts.items():
        #         print(f'Page: {page}, Count: {count}')
        # # user_views = page_views_by_user[user]
        # # for _, (page, count) in user_views.items():
        # #     print(f'user: {user}, page:{page}, count: {count}')

    print("\nTotal Page Visits\n")
    for page, count in page_views.items():
        print(f'the total number of visits to {page} is {count}.')
