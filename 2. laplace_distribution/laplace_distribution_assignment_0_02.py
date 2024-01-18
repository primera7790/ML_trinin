# -*- coding: utf-8 -*-
"""laplace_distribution_assignment_0_02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/girafe-ai/ml-course/blob/23f_yandex_ml_trainings/homeworks/assignment02_laplace/laplace_distribution_assignment_0_02.ipynb

# Home assignment 02: Laplace distribution

Today your goal is to build a class for Laplace distribution. The part of the notebook copies the one from the practice session.

## Loading data
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets

matplotlib.rcParams['font.size'] = 11

"""First to load dataset we're going to use [`sklearn`](https://scikit-learn.org/stable/) package which we will extensively use during the whole course.

`sklearn` implement most of classical and frequently used algorithms in Machine Learning. Also it provides [User Guide](https://scikit-learn.org/stable/user_guide.html) describing principles of every bunch of algorithms implemented.

As an entry point to main `sklearn`'s concepts we recommend [getting started tutorial](https://scikit-learn.org/stable/getting_started.html) (check it out yourself). [Further tutorials](https://scikit-learn.org/stable/tutorial/index.html) can also be handy to develop your skills.
"""

dataset = datasets.load_iris()

print(dataset.DESCR)

"""If you aren't familiar with Iris dataset - take a minute to read description above (as always [more info about it in Wikipedia](https://en.wikipedia.org/wiki/Iris_flower_data_set)).

__TL;DR__ 150 objects equally distributed over 3 classes each described with 4 continuous features

Just pretty table to look at:
"""

ext_target = dataset.target[:, None]
pd.DataFrame(
    np.concatenate((dataset.data, ext_target, dataset.target_names[ext_target]), axis=1),
    columns=dataset.feature_names + ['target label', 'target name'],
)

"""Now give distinct names to the data we will use"""

features = dataset.data
target = dataset.target

features.shape, target.shape

"""__Please, remember!!!__

Anywhere in our course we have an agreement to shape design matrix (named `features` in code above) as

`(#number_of_items, #number_of_features)` if not stated explicitly.

## Distribution implementation

Let's implement class taking list of feature values, estimating Laplace distribution params and able to give probability density of any given feature value.

The file downloaded below contains the template for your class.
"""

!wget https://raw.githubusercontent.com/girafe-ai/ml-course/23s_dd_ml/homeworks/hw02_laplace/distribution.py

"""Denote the Laplace distribution $\mathcal{L}(\mu, b)$ PDF, where $\mu$ stand for location (loc), and $b$ stands for scale:
$$
f(x|\mu, b) = \frac{1}{2b}\exp(-\frac{|x - \mu|}{b})
$$
Let's implement the `LaplaceDistribution` class. (Of course in practice one could always use something like `scipy.stats.laplace`).

Please note, that making computations with log probabilities is more stable.


#### Description [from Wikipedia](https://en.wikipedia.org/wiki/Laplace_distribution#Statistical_inference):

Given $n$ independent and identically distributed samples $x_1, x_2, ..., x_n$, the maximum likelihood (MLE) estimator of $\mu$ is the sample median:
$$
\hat{\mu} = \mathrm{median}(x).
$$



The MLE estimator $b$ is the mean absolute deviation from the median
$$
\hat{b} = \frac{1}{n} \sum_{i = 1}^{n} |x_i - \hat{\mu}|.$$

revealing a link between the Laplace distribution and least absolute deviations.
A correction for small samples can be applied as follows:
$\hat{b}^* = \hat{b} \cdot n/(n-2)$

"""

# Commented out IPython magic to ensure Python compatibility.
# Run some setup code for this notebook.
import random
import numpy as np
import matplotlib.pyplot as plt

# Some more magic so that the notebook will reload external python modules;
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
# %load_ext autoreload
# %autoreload 2

# This dirty hack might help if the autoreload has failed for some reason
try:
    del LaplaceDistribution
except:
    pass

from distribution import LaplaceDistribution

"""### Distribution parameters check"""

import scipy

loc0, scale0 = scipy.stats.laplace.fit(features[:, 0])
loc1, scale1 = scipy.stats.laplace.fit(features[:, 1])

# 1d case
my_distr_1 = LaplaceDistribution(features[:, 0])

# # check the 1d median (loc parameter)
assert np.allclose(my_distr_1.loc, loc0), '1d distribution median error'
# # check the 1d scale (loc parameter)
assert np.allclose(my_distr_1.scale, scale0), '1d distribution scale error'


# 2d case
my_distr_2 = LaplaceDistribution(features[:, :2])

# check the 2d median (loc parameter)
assert np.allclose(my_distr_2.loc, np.array([loc0, loc1])), '2d distribution median error'
# check the 2d median (loc parameter)
assert np.allclose(my_distr_2.scale, np.array([scale0, scale1])), '2d distribution scale error'



print('Seems fine!')

"""### Distribution logpdf check"""

_test = scipy.stats.laplace(loc=[loc0, loc1], scale=[scale0, scale1])

assert np.allclose(
    my_distr_2.logpdf(features[:5, :2]),
    _test.logpdf(features[:5, :2])
), 'Logpdfs do not match scipy results!'
print('Seems fine!')