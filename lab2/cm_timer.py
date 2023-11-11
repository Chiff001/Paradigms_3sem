import time

class cm_timer_1(): 
    def __init__(self): 
        self.start = 0.0
        self.end = 0.0
          
    def __enter__(self): 
        self.start = time.time()
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end = time.time()
        print('Время выполнения: {} секунд.'.format(self.end - self.start))

with cm_timer_1():
    time.altzonesleep(5.5)
