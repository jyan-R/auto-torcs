from autorcs import torcs
from config import *

rj = torcs(FILEPATH)
rj.select_track('dirt-1')
#for p1 in np.arange(0.07,0.09,0.002):
#    print(p1)
#    rj.newrace(p1)
#    rj.nextrace()

#rj.saveresult()