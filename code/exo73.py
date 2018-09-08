import thinkbayes2
import thinkplot

class Trap(thinkbayes2.Suite):

    def __init__(self, label):
        self.nb_trap = 100
        self.label = label
        pmf = thinkbayes2.MakeUniformPmf(0, self.nb_trap, self.nb_trap)
        thinkbayes2.Suite.__init__(self, pmf)

    def Likelihood(self, data, hypo):
        lam = hypo
        k = data
        like = thinkbayes2.EvalPoissonPmf(k, lam)

        return like

def after_two_days(trap):
    """
    Predict the posterior distribution after two days
    """

    mix = thinkbayes2.Pmf()

    for lam1, prob1 in trap.Items():
        for lam2, prob2 in trap.Items():
            if lam1 + lam2 <= trap.nb_trap:
                mix.Incr(lam1 + lam2, prob1 * prob2)

    mix.Normalize()

    return mix

#First day posterior distribution
suite = Trap('Day 1')
suite.Update(37)

#Predict traps after two days
prediction = after_two_days(suite)
thinkplot.Pmf(prediction)
thinkplot.Show()
