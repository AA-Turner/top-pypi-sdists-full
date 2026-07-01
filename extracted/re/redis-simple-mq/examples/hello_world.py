from redis import Redis

from simple_mq import SimpleMQ

conn = Redis()
q = SimpleMQ(conn)
q.enqueue("Hello, World!")
message = q.dequeue()
print(message)
