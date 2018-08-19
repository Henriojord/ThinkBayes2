"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

from thinkbayes2 import Pmf

class Bowl():
    """
    Represent a bowl of two types of cookies (cookies).
    Includes also a normalized representation of the bowl (normalized).
    """
    
    def __init__(self, vanilla=0, chocolate=0):
        """
        Initialize a Bowl.
        Args:
            vanilla (int): Number of vanilla cookie in the bowl.
            chocolate (int): Number of chocolate cookie in the bowl.
        """

        self.cookies = {'vanilla':vanilla, 'chocolate':chocolate}

        self.normalized = self.normalize()

    def normalize(self):
        """
        Normalize the number of cookies.
        """

        nb_cookies = sum(self.cookies.values())
        normalized = {}

        for c in self.cookies:
            normalized[c] = self.cookies[c] / nb_cookies

        return normalized

    def update(self, cookie):
        """
        Upate the number of cookies in the bowl after eating a cookie.
        Args:
            cookie (str): The eaten cookie type.
        """

        self.cookies[cookie] -= 1
        self.normalized = self.normalize()


class Cookie(Pmf):
    """A map from string bowl ID to probablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """

        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

        bowl1 = Bowl(vanilla=30, chocolate=10)
        bowl2 = Bowl(vanilla=20, chocolate=20)

        self.bowls = {
            'Bowl 1':bowl1,
            'Bowl 2':bowl2
        }

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """

        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

        for bowl in self.bowls:
            self.bowls[bowl].update(data)

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """

        mix = self.bowls[hypo]
        like = mix.normalized[data]

        return like


def main():
    hypos = ['Bowl 1', 'Bowl 2']

    pmf = Cookie(hypos)

    print('Before drawing vanilla')
    print(pmf.bowls['Bowl 1'].normalized)
    print(pmf.bowls['Bowl 2'].normalized)

    pmf.Update('vanilla')

    for hypo, prob in pmf.Items():
        print(hypo, prob)

    print('After drawing vanilla')
    print(pmf.bowls['Bowl 1'].normalized)
    print(pmf.bowls['Bowl 2'].normalized)

    pmf.Update('chocolate')

    for hypo, prob in pmf.Items():
        print(hypo, prob)

    print('After drawing chocolate')
    print(pmf.bowls['Bowl 1'].normalized)
    print(pmf.bowls['Bowl 2'].normalized)


if __name__ == '__main__':
    main()
