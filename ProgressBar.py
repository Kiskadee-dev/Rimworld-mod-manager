import sys
import time

class ProgressBar:
    def __init__(self):
        pass

    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        #sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        print('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix),end="", flush=True)
        time.sleep(.1)
        sys.stdout.flush()  # As suggested by Rom Ruben
