import thinkbayes2
import thinkplot

class Bulb(thinkbayes2.Suite):

    def __init__(self, label):
        #I assume that a light bulb is used 5 hours per day
        #A light bulb live for ~1000 hours => 200 days
        #I use the smallest increasing failure rate (1)
        self.nb_bulb = 100
        self.label = label
        pmf = thinkbayes2.MakeWeibullPmf(200, 1, self.nb_bulb, self.nb_bulb)
        thinkbayes2.Suite.__init__(self, pmf)

    def Likelihood(self, data, hypo):
        lam = hypo
        k = data
        like = thinkbayes2.EvalPoissonPmf(k, lam)

        return like

def after_two_months(bulb):
    """
    Predict the posterior distribution after two days
    """

    mix = thinkbayes2.Pmf()

    for lam1, prob1 in bulb.Items():
        for lam2, prob2 in bulb.Items():
            if lam1 + lam2 <= bulb.nb_bulb:
                mix.Incr(lam1 + lam2, prob1 * prob2)

    mix.Normalize()

    return mix

#First month posterior distribution
suite = Bulb('Month 1')
suite.Update(3)
#Predict failures after two months
prediction = after_two_months(suite)
max_lam, max_prob = 0, 0
for lam, prob in prediction.Items():
    if prob > max_prob:
        max_prob = prob
        max_lam = lam
print("Maximum likelihood lambda={} with probability={}".format(max_lam, max_prob))
thinkplot.Pmf(prediction)
thinkplot.Show()
