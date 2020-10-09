class Runner:
    def __init__(self,season_best,date_ran):
        self.season_best=season_best
        self.date_ran=date_ran
        self.time=self.simplify(self.season_best)

    def simplify(self,season_best):
        a=season_best.split(':')
        for i in range(0,len(a)):
            a[i]=int(a[i])
        while a[0]>0:
            a[0]-=1
            a[1]+=60
        return a[1]

