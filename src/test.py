from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


@tl.job(interval=timedelta(seconds=2))
def browse_twitter():
    print('is it working ?')


tl.start()
