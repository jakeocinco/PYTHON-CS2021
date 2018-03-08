"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
#from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from utils import distance, mean, zip, enumerate, sample


##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location. If
    multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    minimum = 1000000
    minIndex = 0
    j = 0
    for i in centroids:
        dist = distance(location, i)
        if dist < minimum:
            minIndex = j
            minimum = dist
        j += 1
    return centroids[minIndex]
    "*** REPLACE THIS LINE ***"
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4

    # Creates list of the closest location in the same order as restaurant passed in
    closest = []
    for r in restaurants:
        closest += [find_closest(r['location'], centroids)]

    # Empty list for final grouping of restaurant name
    groups = [[] for Null in range(len(centroids))]

    """Iterates through closest and centroids to find matches and append empty list
    when the locations are the same
    """
    for i in range(len(closest)):
        for j in range(len(centroids)):
            if closest[i] == centroids[j]:
                # groups[j].append(restaurants[i])
                groups[j] += [restaurants[i]]

    return groups
    # END Question 4

# r1 = make_restaurant('A', [-10, 2], [], 2, [make_review('A', 4),])
# r2 = make_restaurant('B', [-9, 1], [], 3, [make_review('B', 5),make_review('B', 3.5),])
# r3 = make_restaurant('C', [4, 2], [], 1, [make_review('C', 5) ])
# r4 = make_restaurant('D', [-2, 6], [], 4, [make_review('D', 2)])
# r5 = make_restaurant('E', [4, 2], [], 3.5, [make_review('E', 2.5), make_review('E', 3),])
# c1 = [0, 0]
# c2 = [3, 4]
# groups = group_by_centroid([r1, r2, r3, r4, r5], [c1, c2])
#
# # correct grouping is  [[r1, r2], [r3, r4, r5]])
# print([list (map (lambda r: r ['name'], c)) for c in groups])
# # [['A', 'B'], ['C', 'D', 'E']]

def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"
    x = []
    y = []
    for r in cluster:
        loc = restaurant_location(r)
        x += [loc[0]]
        y += [loc[1]]

    return [mean(x), mean(y)]
    # END Question 5
# cluster1 = [make_restaurant('A', [-3, -4], [], 3, [make_review('A', 2)]), make_restaurant('B', [1, -1],  [], 1, [make_review('B', 1)]), make_restaurant('C', [2, -4],  [], 1, [make_review('C', 5)]),]
# print(find_centroid(cluster1)) # should be a pair of decimals
# #[0.0, -3.0]

def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    centroids = [0] * k
    # Select initial centroids randomly by choosing k different restaurants

    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    # print(centroids)
    while old_centroids != centroids and n < max_updates:

        n += 1
        old_centroids = []

        for c in centroids:
            old_centroids += [c]

        # return [[y for x, y in pairs if x == key] for key in keys]
        old_centroids = centroids
        groups = group_by_centroid(restaurants, centroids)


        distances = []


        centroids = [] * k
        for g in groups:
            centroids += [find_centroid(g)]

    return centroids
#
# restaurants1 = [make_restaurant('A', [-3, -4], [], 3, [make_review('A', 2)]), make_restaurant('B', [1, -1],  [], 1, [make_review('B', 1)]), make_restaurant('C', [2, -4],  [], 1, [make_review('C', 5)]),]
# # centroids = k_means(restaurants1, 1)
# # print(centroids) # should be 2-element lists of decimals
# # [[0.0, -3.0]]
# restaurants2 = [make_restaurant('D', [2, 3], [], 2, [make_review('D', 2)]), make_restaurant('E', [0, 3], [], 3, [make_review('E', 1)]),]
# # centroids = k_means(restaurants2, 1)
# # print(centroids) # should be 2-element lists of decimals
# # [[1.0, 3.0]]
# # print(k_means(restaurants1 + restaurants2, 1))
# # [[0.4, -0.6]]
# # `print(k_means(restaurants1 + restaurants2, 2))
# # [[0.0, -3.0], [1.0, 3.0]]
# print(k_means(restaurants1 + restaurants2, 3))
# print([[-0.5, -4.0], [1.0, -1.0], [1.0, 3.0]])
# print(k_means(restaurants1 + restaurants2, 4))
# print([[-3.0, -4.0], [1.5, -2.5], [2.0, 3.0], [0.0, 3.0]])
# print(k_means(restaurants1 + restaurants2, 5))
# [[-3.0, -4.0], [1.0, -1.0], [2.0, -4.0], [2.0, 3.0], [0.0, 3.0]]


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"
    b, a, r_squared = 0, 0, 0  # REPLACE THIS LINE WITH YOUR SOLUTION
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    # END Question 9


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]
