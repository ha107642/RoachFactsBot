import time
from twitchobserver import Observer
import config
import random

ROACH_FACT_COOLDOWN = 5
ROACH_FACTS_FILENAME = "roach_facts.txt"
roach_facts = [line.decode("utf-8").rstrip('\n') for line in open(ROACH_FACTS_FILENAME)]

last_roach_fact = time.time()

def post_roach_fact(observer, channel):
    global last_roach_fact
    if time.time() < last_roach_fact + ROACH_FACT_COOLDOWN:
        return

    num = random.randint(1, len(roach_facts))
    
    roach_fact = roach_facts[num - 1]
    observer.send_message(u"Roach Fact " + unicode(num) + u": " + roach_fact, channel)

    last_roach_fact = time.time()

with Observer(config.username, config.oauth) as observer:
    for channel in config.channels:
        observer.join_channel(channel)

    while True:
        try:
            for event in observer.get_events():
                if event.type == "TWITCHCHATMESSAGE":
                    if event.message == u"!roachfact":
                        post_roach_fact(observer, event.channel)

            time.sleep(1)

        except KeyboardInterrupt:
            for channel in config.channels:
                observer.leave_channel(channel)
            break