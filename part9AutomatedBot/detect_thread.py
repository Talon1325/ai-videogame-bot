from threading import Thread, Lock


class DetectThread:
    stopping = True
    lock = None
    

    def __init__(self):
        # thread lock object
        self.lock = Lock()

    def start(self):
        self.stopping = False
        t = Thread(target = self.run)
        t.start()
        

    def stop(self):
        self.stopping = True
        

    def run(self):
        pass