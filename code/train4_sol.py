"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

from dice import Dice
import thinkplot


class Train(Dice):
    """Represents hypotheses about how many trains the company has.

    The likelihood function for the train problem is the same as
    for the Dice problem.
    """

    def __init__(self, hypotheses, all_other):
        """
        hypotheses (list of int): List of Hypothetic number of trains
        all_other (int): Sum of trains of other companies
        """

        super().__init__(hypotheses)

        self.all_other = all_other

    def Likelihood(self, data, hypo):
        """
        data (int): Observed train's number
        hypo (int): Hypothetic number of trains

        This function can be simplified.
            p(data, company) = p(company) * p(data | company)
                             = (hypo / (hypo + all_other)) * (1 / hypo)
                             = 1 / (hypo + all_other)
        """

        see_company = hypo / (hypo + self.all_other)

        if hypo < data:
            likelihood = 0
        else:
            likelihood = 1 / hypo

        return likelihood * see_company

def main():
    hypos = range(1, 1001)
    all_other = [50, 100, 1000, 10000]

    for a in all_other:
        suite = Train(hypos, a)
        suite.Update(60)
        thinkplot.Pmf(suite, label='{} other trains'.format(a))

    thinkplot.Show(xlabel='Number of trains', ylabel='PMF')

if __name__ == '__main__':
    main()
