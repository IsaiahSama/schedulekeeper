from threading import Thread
from time import sleep

class Test:
    def __init__(self):
        pass

    play = True

    def my_thread(self):
        i = 0
        while self.play or i < 20:
            print(i)
            sleep(1)
            i += 1

        print("Thread has been stopped")

    def main(self):
        print("Creating thread now")
        thread = Thread(target=self.my_thread)
        thread.start()
        sleep(10)
        print("Attempting to stop thread")
        self.play = False

test = Test()
test.main()