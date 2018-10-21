# -*- coding: utf-8 -*-

from minidata import dataset
from math import sqrt

def pearson_correlation(user, other):

    both_rated = {}
    for item in dataset[user]:
        if item in dataset[other]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    if number_of_ratings == 0:
        return 0

    user_preferences_sum = sum([dataset[user][item] for item in both_rated])
    other_preferences_sum = sum([dataset[other][item] for item in both_rated])

    user_square_preferences_sum = sum([pow(dataset[user][item],2) for item in both_rated])
    other_square_preferences_sum = sum([pow(dataset[other][item],2) for item in both_rated])

    product_sum_of_both_users = sum([dataset[user][item] * dataset[other][item] for item in both_rated])

    numerator_value = product_sum_of_both_users - (user_preferences_sum*other_preferences_sum/number_of_ratings)
    denominator_value = sqrt((user_square_preferences_sum - pow(user_preferences_sum,2)/number_of_ratings) * (other_square_preferences_sum -pow(other_preferences_sum,2)/number_of_ratings))

    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r

def most_similar_users(user, number_of_users):

    scores = [(pearson_correlation(user, other_user), other_user) for other_user in dataset if other_user != user]

    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def get_recommendations(person):

    totals = {}
    simSums = {}
    recommendataions_list = []

    for other in dataset:
        if other == person:
            continue
        sim = pearson_correlation(person,other)

        if sim <=0: 
            continue
        for item in dataset[other]:

            if item not in dataset[person]:

                totals.setdefault(item,0)
                totals[item] += dataset[other][item]* sim

                simSums.setdefault(item,0)
                simSums[item]+= sim

    rankings = [(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()

    for movie in rankings:
        if movie[0] > 3:
            recommendataions_list.append(movie[1])

    return recommendataions_list

print get_recommendations('Clara')