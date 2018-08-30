from __future__ import print_function, division

import thinkbayes2
import thinkplot
import random

class User(thinkbayes2.Suite):
    """
    Class representing a redditor
    """

    def Likelihood(self, data, hypo):
        """
        """

        reliability = hypo / 100.0
        vote, relevance = data

        if vote == 'up':
            return (reliability * relevance) + ((1 - reliability) * (1 - relevance))
        else:
            return ((reliability - 1) * relevance) + (reliability * (1 - relevance))

class Link(thinkbayes2.Suite):
    """
    Class representing a link posted on reddit
    """

    def Likelihood(self, data, hypo):
        """
        """

        relevance = hypo / 100.0
        vote, reliability = data

        if vote == 'up':
            return (relevance * reliability) + ((1 - relevance) * (1 - reliability))
        else:
            return ((relevance - 1) * reliability) + (relevance * (1 - reliability))

def update(users, link, data):
    """
    """

    for d in range(len(data)):
        link.update(data[d][0], data[d][1])
        user[d].update()

    return 0

def main():
    """
    """

    user = User(label='user')
    beta = thinkbayes2.Beta(2, 1)
    for val, prob in beta.MakePmf().Items():
        user.Set(val * 100, prob)
    thinkplot.Pdf(user)
    thinkplot.Show()
    print(user.Mean(), user.CredibleInterval(90))
    mean_r = user.Mean() / 100.0

    link = Link(range(0, 101), label='link')
    thinkplot.Pdf(link)
    thinkplot.Show()
    print(link.Mean(), link.CredibleInterval(90))
    mean_q = link.Mean() / 100.0

    user.Update(('up', mean_q))
    thinkplot.Pdf(user)
    thinkplot.Show()
    print(user.Mean(), user.CredibleInterval(90))

    link.Update(('up', mean_r))
    thinkplot.Pdf(link)
    thinkplot.Show()
    print(link.Mean(), link.CredibleInterval(90))

    return 0

if __name__ == '__main__':
    main()
