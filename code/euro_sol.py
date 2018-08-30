"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

"""This file contains a partial solution to a problem from
MacKay, "Information Theory, Inference, and Learning Algorithms."

    Exercise 3.15 (page 50): A statistical statement appeared in
    "The Guardian" on Friday January 4, 2002:

        When spun on edge 250 times, a Belgian one-euro coin came
        up heads 140 times and tails 110.  'It looks very suspicious
        to me,' said Barry Blight, a statistics lecturer at the London
        School of Economics.  'If the coin were unbiased, the chance of
        getting a result as extreme as that would be less than 7%.'

MacKay asks, "But do these data give evidence that the coin is biased
rather than fair?"

"""

import thinkbayes2
import thinkplot
import numpy as np

class Euro(thinkbayes2.Suite):
    """Represents hypotheses about the probability of heads."""

    def __init__(self, hypos, y, label=''):
        """
        Euro constructor
        Args:
            hypos (list): Range of float
            y (float): Observation bias
            label (str): Label (for plot)
        """

        super().__init__(hypos)

        self.y = y
        self.label = label

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: integer value of x, the probability of heads (0-100)
        data: string 'H' or 'T'
        """

        x = hypo / 100.0
        if data == 'H':
            return (x * self.y) + ((1 - x) * (1 - self.y))
        else:
            return ((1 - x) * self.y) + (x * (1 - self.y))

def Summarize(suite):
    """Prints summary statistics for the suite."""
    print(suite.Prob(50))

    print('MLE', suite.MaximumLikelihood())

    print('Mean', suite.Mean())
    print('Median', suite.Percentile(50))

    print('5th %ile', suite.Percentile(5))
    print('95th %ile', suite.Percentile(95))

    print('CI', suite.CredibleInterval(90))

def PlotSuites(suites, root):
    """Plots two suites.

    suite1, suite2: Suite objects
    root: string filename to write
    """
    thinkplot.Clf()
    thinkplot.PrePlot(len(suites))
    thinkplot.Pmfs(suites)

    thinkplot.Show(xlabel='Heads probability', ylabel='PMF')


def main():
    dataset = 'H' * 140 + 'T' * 110
    observation_bias = np.arange(0.1, 1., 0.1)

    suites = []

    for y in observation_bias:
        print("With a observation bias of {}".format(y))

        suite = Euro(range(0, 101), y, label=str(y))

        # update
        for data in dataset:
            suite.Update(data)

        Summarize(suite)

        suites.append(suite)

    # plot the posteriors
    PlotSuites(suites, 'euro1')

    """
    Their is a symetry on 0.5
    As y increases, the observations are more reliables.
    In other word, if the device outputs "head" it is more likely to really be a
    head. Thus, for low y < 0.5 the posteriors are the reverse of those with
    y > 0.5.
    This lack of reliability is expressed by the spread of the posteriors. When
    y is near 0.0 or 1.0, the posteriors are spiky. Because the device is either
    always wrong either always right. However, as y is near 0.5, their is a lot
    of uncertainty. The device is either wrong or either right. Therefore, the
    posteriors are well spread.
    When y = 0.5, the data are not informative at all. Thus, all hypothesis are
    equiprobable.
    """


if __name__ == '__main__':
    main()
