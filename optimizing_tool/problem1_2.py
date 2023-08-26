import multiprocessing
import time

def busy_loop():
    count = 0
    while count < 10**8:
        count += 1

process = []

for _ in range(10):
    t = multiprocessing.Process(target=busy_loop)
    t.start()
    process.append(t)

for t in process:
    t.join()
