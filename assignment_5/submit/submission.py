
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: solution.ipynb

import numpy as np
from helper_functions import *

def get_initial_means(array, k):
    """
    Picks k random points from the 2D array
    (without replacement) to use as initial
    cluster means

    params:
    array = numpy.ndarray[numpy.ndarray[float]] - m x n | datapoints x features

    k = int

    returns:
    initial_means = numpy.ndarray[numpy.ndarray[float]]
    """
    m, n = array.shape
    idxs = np.random.choice(m, size=k, replace=False)
    return array[idxs, :]

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def k_means_step(X, k, means):
    """
    A single update/step of the K-means algorithm
    Based on a input X and current mean estimate
    calculate new means and predict clusters for each of the pixel
    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n | pixels x features (already flattened)
    k = int
    means = numpy.ndarray[numpy.ndarray[float]] - k x n

    returns:
    (new_means, clusters)
    new_means = numpy.ndarray[numpy.ndarray[float]] - k x n
    clusters = numpy.ndarray[int] - m sized vector
    """
    # X = np.array([[0,0,0], [0,1,0], [1,0,0],[6,6,6],[5,6,6],[6,5,6]])
    # means = np.array([[0,0,0],[6,6,6]])
    # import pdb
    # pdb.set_trace()
    m, n = X.shape
    dist = np.zeros((m, k))
    new_means = np.zeros((k, n))

    X_k = np.repeat(np.reshape(X, (m,n,1)), repeats=k, axis=2)
    means = np.transpose(np.reshape(means, (k,n,1)), [2, 1, 0])

    dist = np.reshape(np.sqrt(np.sum((X_k - means)**2, axis=1)), (m, k))

    assign = np.argmin(dist, axis=1)

    for _k in range(k):
        new_means[_k, :] = X[assign==_k].mean(axis=0)

    return (new_means, assign)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def k_means_segment(image_values, k=3, initial_means=None):
    """
    Separate the provided RGB values into
    k separate clusters using the k-means algorithm,
    then return an updated version of the image
    with the original values replaced with
    the corresponding cluster values.

    params:
    image_values = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - r x c x ch
    k = int
    initial_means = numpy.ndarray[numpy.ndarray[float]] or None

    returns:
    updated_image_values = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - r x c x ch
    """
    # import pdb
    # import matplotlib.pyplot
    # pdb.set_trace()
    height, width, channels = image_values.shape
    # plt.imshow(image_values)
    # plt.show()
    X = np.copy(image_values)
    X = np.reshape(X, (height*width, channels))

    if initial_means is None:
        prev_means = get_initial_means(X, k)
    else:
        prev_means = initial_means

    prev_assign = -1*np.ones((height*width))
    # import pdb
    # pdb.set_trace()
    cnt = 0
    while True:
        cnt += 1
        new_means, assign = k_means_step(X, k, prev_means)

        if np.all(assign == prev_assign): break
        else:
            prev_assign = assign
            prev_means = new_means

    for _k in range(k): X[assign == _k] = new_means[_k, :]
    new_image_values = np.reshape(X, (height,width,channels))
    # plt.imshow(new_image_values)
    # plt.show()
    # pdb.set_trace()
    return new_image_values

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def initialize_parameters(X, k):
    """
    Return initial values for training of the GMM
    Set component mean to a random
    pixel's value (without replacement),
    based on the mean calculate covariance matrices,
    and set each component mixing coefficient (PIs)
    to a uniform values
    (e.g. 4 components -> [0.25,0.25,0.25,0.25]).

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int

    returns:
    (MU, SIGMA, PI)
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k x 1
    """

    m, n = X.shape
    idxs = np.random.choice(m, size=k, replace=False)

    MU = X[idxs, :]
    SIGMA = np.repeat(np.eye(n)[None,:,:], repeats=k, axis=0)
    PI = np.reshape(np.array([1.0/k]*k), (1,k))

    return (MU, SIGMA, PI)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def compute_sigma(X, MU):
    """
    Calculate covariance matrix, based in given X and MU values

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n

    returns:
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    """
    m, n = X.shape
    k, _ = MU.shape
    SIGMA = np.zeros((k,n,n))

    # import pdb
    # pdb.set_trace()

    # for _k in range(k):
        # for _m in range(m):
            ## pdb.set_trace()
            # vec = np.reshape(X[_m,:] - MU[_k,:], (n,1))
            # SIGMA[_k, :, :] += (vec).dot(vec.T)
    # pdb.set_trace()
    _X = np.repeat(X[:,:,None], repeats=k, axis=2)
    _X -= (MU.T)[None,:,:]

    _Xt = np.transpose(_X, [1,0,2])

    for _k in range(k):
        SIGMA[_k, :, :] += _Xt[:,:,_k].dot(_X[:,:,_k])

    SIGMA /= m
    return SIGMA
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def prob(x, mu, sigma):
    """Calculate the probability of a single
    data point x under component with
    the given mean and covariance.
    # NOTE: there is nothing to vectorize here yet,
    # it's a simple check to make sure you got the
    # multivariate normal distribution formula right
    # which is given by N(x;MU,SIGMA) above

    params:
    x = numpy.ndarray[float]
    mu = numpy.ndarray[float]
    sigma = numpy.ndarray[numpy.ndarray[float]]

    returns:
    probability = float
    """
    d = x.size
    p = (1/((2*np.pi)**(d/2))) * (np.linalg.det(sigma))**(-1/2) * np.exp(-0.5 * (((x-mu).T).dot(np.linalg.pinv(sigma))).dot(x-mu))
    # print(sigma)
    return p
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def E_step(X,MU,SIGMA,PI,k):
    """
    E-step - Expectation
    Calculate responsibility for each
    of the data points, for the given
    MU, SIGMA and PI.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k x 1
    k = int

    returns:
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """
    m, n = X.shape
    k, _ = MU.shape
    R_ = np.zeros((k,m))
    PI = np.reshape(PI, (1,k))
    X_mu = np.repeat(X[None, :, :], repeats=k, axis=0) - MU[:,None,:]
    probs = np.zeros((k, m))
    for _k in range(k):
        X_muk = X_mu[_k, :, :][:, None, :]
        sigmak = np.linalg.inv(SIGMA[_k, :, :])

        X_sigma = np.dot(X_muk, sigmak)
        X_exp = (1.0 / ((2*np.pi)**(n/2.0)*np.linalg.det(SIGMA[_k,:,:])**(0.5))) * np.exp(np.sum(X_muk * X_sigma, axis=2) * (-0.5))
        probs[_k, :] = X_exp.T
    R_ = PI.T * probs
    R_ /= np.sum(R_, axis=0)
    return R_

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def M_step(X, r, k):
    """
    M-step - Maximization
    Calculate new MU, SIGMA and PI matrices
    based on the given responsibilities.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    r = numpy.ndarray[numpy.ndarray[float]] - k x m
    k = int

    returns:
    (new_MU, new_SIGMA, new_PI)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k x 1
    """

    m, n = X.shape
    k, _ = r.shape

    # import pdb
    # pdb.set_trace()

    new_MU = np.zeros((k,n))
    new_SIGMA = np.zeros((k,n,n))
    new_PI = np.zeros((1,k))

    m = np.sum(r)

    for _k in range(k):
        mc = np.sum(r[_k, :])
        new_PI[0, _k] = mc / m
        new_MU[_k, :] = (1.0 / mc) * r[_k, :].dot(X) # kxm, mxn => kxn
        x_mu = (X - new_MU[_k,:])
        new_SIGMA[_k,:,:] = (1.0/mc) * (r[_k,:] * x_mu.T).dot(x_mu) # 1xm, nxm, mxn => nxn
    # pdb.set_trace()
    return (new_MU, new_SIGMA, new_PI)
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def likelihood(X, PI, MU, SIGMA, k):
    """Calculate a log likelihood of the
    trained model based on the following
    formula for posterior probability:

    log10(Pr(X | mixing, mean, stdev)) = sum((n=1 to N), log10(sum((k=1 to K),
                                      mixing_k * N(x_n | mean_k,stdev_k))))

    Make sure you are using log base 10, instead of log base 2.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k x 1
    k = int

    returns:
    log_likelihood = float
    """
    m, n = X.shape
    R_ = np.zeros((k,m))
    PI = np.reshape(PI, (-1,PI.size))
    X_mu = np.repeat(X[None, :, :], repeats=k, axis=0) - MU[:,None,:]
    probs = np.zeros((k, m))
    for _k in range(k):
        X_muk = X_mu[_k, :, :][:, None, :]
        sigmak = np.linalg.inv(SIGMA[_k, :, :])

        X_sigma = np.dot(X_muk, sigmak)
        X_exp = (1.0 / ((2*np.pi)**(n/2.0)*np.linalg.det(SIGMA[_k,:,:])**(0.5))) * np.exp(np.sum(X_muk * X_sigma, axis=2) * (-0.5))
        probs[_k, :] = X_exp.T
    R_ = PI.T * probs
    likelihood = np.sum(np.log10(np.sum(R_, axis=0)))
    return likelihood

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def train_model(X, k, convergence_function, initial_values = None):
    """
    Train the mixture model using the
    expectation-maximization algorithm.
    E.g., iterate E and M steps from
    above until convergence.
    If the initial_values are None, initialize them.
    Else it's a tuple of the format (MU, SIGMA, PI).
    Convergence is reached when convergence_function
    returns terminate as True,
    see default convergence_function example
    in `helper_functions.py`

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    convergence_function = func
    initial_values = None or (MU, SIGMA, PI)

    returns:
    (new_MU, new_SIGMA, new_PI, responsibility)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k x 1
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """
    m, n = X.shape

    if initial_values is None:
        prev_MU, prev_SIGMA, prev_PI = initialize_parameters(X,k)
    else:
        prev_MU, prev_SIGMA, prev_PI = initial_values
    prev_likelihood = likelihood(X, prev_PI, prev_MU, prev_SIGMA, k)
    conv_ctr = 0
    while True:
        # E-Step
        R = E_step(X,prev_MU,prev_SIGMA,prev_PI,k)
        # M-Step
        new_MU, new_SIGMA, new_PI = M_step(X,R,k)
        # check convergence
        # pdb.set_trace()
        new_likelihood = likelihood(X, new_PI, new_MU, new_SIGMA, k) # np.sum(np.log10(np.sum(R, axis=0))) #
        conv_ctr, converged = convergence_function(prev_likelihood, new_likelihood, conv_ctr)
        if converged: break
        else:
            prev_MU, prev_SIGMA, prev_PI = new_MU, new_SIGMA, new_PI
            prev_likelihood = new_likelihood

    return (new_MU, new_SIGMA, new_PI, R)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def cluster(r):
    """
    Based on a given responsibilities matrix
    return an array of cluster indices.
    Assign each datapoint to a cluster based,
    on component with a max-likelihood
    (maximum responsibility value).

    params:
    r = numpy.ndarray[numpy.ndarray[float]] - k x m - responsibility matrix

    return:
    clusters = numpy.ndarray[int] - m x 1
    """
    # import pdb
    # pdb.set_trace()
    return np.argmax(r, axis=0)
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def segment(X, MU, k, r):
    """
    Segment the X matrix into k components.
    Returns a matrix where each data point is
    replaced with its max-likelihood component mean.
    E.g., return the original matrix where each pixel's
    intensity replaced with its max-likelihood
    component mean. (the shape is still mxn, not
    original image size)

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    k = int
    r = numpy.ndarray[numpy.ndarray[float]] - k x m - responsibility matrix

    returns:
    new_X = numpy.ndarray[numpy.ndarray[float]] - m x n
    """
    m,n = X.shape
    pixel_map = cluster(r)
    new_X = X
    new_X = MU[pixel_map]
    return new_X

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def best_segment(X,k,iters):
    """Determine the best segmentation
    of the image by repeatedly
    training the model and
    calculating its likelihood.
    Return the segment with the
    highest likelihood.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    iters = int

    returns:
    (likelihood, segment)
    likelihood = float
    segment = numpy.ndarray[numpy.ndarray[float]]
    """

    best_likelihood, best_MU, best_R = float("-inf"), None, None
    for _iter in range(iters):
        (MU, SIGMA, PI, R) = train_model(X, k, default_convergence, initial_values = None)
        l = likelihood(X, PI, MU, SIGMA, k)
        if l > best_likelihood:
            best_likelihood = l
            best_MU = MU
            best_R = R
    best_segment = segment(X, best_MU, k, best_R)
    return (best_likelihood, best_segment)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def improved_initialization(X,k):
    """
    Initialize the training
    process by setting each
    component mean using some algorithm that
    you think might give better means to start with,
    based on the mean calculate covariance matrices,
    and set each component mixing coefficient (PIs)
    to a uniform values
    (e.g. 4 components -> [0.25,0.25,0.25,0.25]).

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int

    returns:
    (MU, SIGMA, PI)
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k x 1
    """

    m, n = X.shape
    SIGMA = np.zeros((k,n,n))
    MU = np.zeros((k,n))
    PI = np.array([1.0/k] * k)

    prev_assign = -1*np.ones((m))

    init_iters = 10000
    means = get_initial_means(X, k)
    for _init_iters in range(init_iters):
        means, assign = k_means_step(X, k, means)
        if np.all(assign == prev_assign): break
        else:
            prev_assign = assign
            prev_means = means

    MU = means
    SIGMA = compute_sigma(X, MU)

    return (MU, SIGMA, PI)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def new_convergence_function(previous_variables, new_variables, conv_ctr,
                             conv_ctr_cap=20):
    """
    Convergence function
    based on parameters:
    when all variables vary by
    less than 10% from the previous
    iteration's variables, increase
    the convergence counter.

    params:
    previous_variables = [numpy.ndarray[float]]
                         containing [means, variances, mixing_coefficients]
    new_variables = [numpy.ndarray[float]]
                    containing [means, variances, mixing_coefficients]
    conv_ctr = int
    conv_ctr_cap = int

    return:
    (conv_crt, converged)
    conv_ctr = int
    converged = boolean
    """
    diff = np.max((np.abs(previous_variables - new_variables)) / previous_variables)
    if diff < 0.1:
        conv_ctr += 1
    else:
        conv_ctr = 0

    return conv_ctr, conv_ctr > conv_ctr_cap

def train_model_improved(X, k, convergence_function=new_convergence_function, initial_values = None):
    """
    Train the mixture model using the
    expectation-maximization algorithm.
    E.g., iterate E and M steps from
    above until convergence.
    If the initial_values are None, initialize them.
    Else it's a tuple of the format (MU, SIGMA, PI).
    Convergence is reached when convergence_function
    returns terminate as True. Use new_convergence_fuction
    implemented above.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    convergence_function = func
    initial_values = None or (MU, SIGMA, PI)

    returns:
    (new_MU, new_SIGMA, new_PI, responsibility)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k x 1
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """
    m, n = X.shape

    if initial_values is None:
        prev_MU, prev_SIGMA, prev_PI = improved_initialization(X,k)
    else:
        prev_MU, prev_SIGMA, prev_PI = initial_values
    prev_likelihood = likelihood(X, prev_PI, prev_MU, prev_SIGMA, k)
    conv_ctr = 0
    while True:
        # E-Step
        R = E_step(X,prev_MU,prev_SIGMA,prev_PI,k)
        # M-Step
        new_MU, new_SIGMA, new_PI = M_step(X,R,k)
        # check convergence
        # pdb.set_trace()
        new_likelihood = likelihood(X, new_PI, new_MU, new_SIGMA, k) # np.sum(np.log10(np.sum(R, axis=0))) #
        conv_ctr, converged = convergence_function(prev_likelihood, new_likelihood, conv_ctr)
        if converged: break
        else:
            prev_MU, prev_SIGMA, prev_PI = new_MU, new_SIGMA, new_PI
            prev_likelihood = new_likelihood

    return (new_MU, new_SIGMA, new_PI, R)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
# Unittest below will check both of the functions at the same time.
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def bayes_info_criterion(X, PI, MU, SIGMA, k):
    """
    See description above
    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[nu
    mpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k x 1
    k = int

    return:
    bayes_info_criterion = int
    """
    m, n = X.shape
    R_ = np.zeros((k,m))
    k = PI.size
    PI = np.reshape(PI, (-1,k))
    X_mu = np.repeat(X[None, :, :], repeats=k, axis=0) - MU[:,None,:]
    probs = np.zeros((k, m))
    for _k in range(k):
        X_muk = X_mu[_k, :, :][:, None, :]
        sigmak = np.linalg.inv(SIGMA[_k, :, :])

        X_sigma = np.dot(X_muk, sigmak)
        X_exp = (1.0 / ((2*np.pi)**(n/2.0)*np.linalg.det(SIGMA[_k,:,:])**(0.5))) * np.exp(np.sum(X_muk * X_sigma, axis=2) * (-0.5))
        probs[_k, :] = X_exp.T
    R_ = PI.T * probs
    L = np.sum(np.log10(np.sum(R_, axis=0)))

    bic = ((n*(n+1)/2) + n + 1)*k*np.log10(m*n) - 2*L
    return bic

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######
################ END OF LOCAL TEST CODE SECTION ######################

def BIC_likelihood_model_test(image_matrix, comp_means):
    """Returns the number of components
    corresponding to the minimum BIC
    and maximum likelihood with respect
    to image_matrix and comp_means.

    params:
    image_matrix = numpy.ndarray[numpy.ndarray[float]] - m x n
    comp_means = list(numpy.ndarray[numpy.ndarray[float]]) - list(k x n) (means for each value of k)

    returns:
    (n_comp_min_bic, n_comp_max_likelihood)
    n_comp_min_bic = int
    n_comp_max_likelihood = int
    """
    X = image_matrix
    k_bic, k_likelihood, min_bic, max_likelihood = None, None, float("inf"), float("-inf")
    for MU in comp_means:
        # import pdb
        # pdb.set_trace()
        k, _ = MU.shape
        SIGMA = compute_sigma(X, MU)
        PI = np.array([1.0/k] * k)
        (new_MU, new_SIGMA, new_PI, R) = train_model_improved(X, k, convergence_function=new_convergence_function, initial_values = (MU, SIGMA, PI))

        new_likelihood = likelihood(X, new_PI, new_MU, new_SIGMA, k)
        new_bic = bayes_info_criterion(X, new_PI, new_MU, new_SIGMA, k)
        if new_likelihood > max_likelihood:
            max_likelihood = new_likelihood
            k_likelihood = k
        if new_bic < min_bic:
            min_bic = new_bic
            k_bic = k
    return (k_bic, k_likelihood)

def return_your_name():
    return "Advait"

def bonus(X, means):
    """
    Return the distance from every point in points_array
    to every point in means_array.

    returns:
    dists = numpy array of float
    """
    m, n = X.shape
    k, _ = means.shape
    dist = np.zeros((m, k))
    X_k = np.repeat(np.reshape(X, (m,n,1)), repeats=k, axis=2)
    means = np.transpose(np.reshape(means, (k,n,1)), [2, 1, 0])

    dist = np.reshape(np.sqrt(np.sum((X_k - means)**2, axis=1)), (m, k))
    return dist

# There are no local test for thus question, fill free to create them yourself.
# Feel free to play with it in a separate python file, and then just copy over
# your implementation before the submission.
