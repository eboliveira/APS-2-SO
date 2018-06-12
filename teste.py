import time
i = 1
while True:
    if time.clock() > i:
        print time.clock()
        i+=1