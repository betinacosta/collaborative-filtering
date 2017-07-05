# -*- coding: utf-8 -*-

from data import dataset
from math import sqrt

def pearson_correlation(user, other):

   # To get both rated items
    both_rated = {}
    for item in dataset[user]:
        if item in dataset[other]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    # Checking for ratings in common
    if number_of_ratings == 0:
        return 0

    # Add up all the preferences of each user
    user_preferences_sum = sum([dataset[user][item] for item in both_rated])
    other_preferences_sum = sum([dataset[other][item] for item in both_rated])

    # Sum up the squares of preferences of each user
    user_square_preferences_sum = sum([pow(dataset[user][item],2) for item in both_rated])
    other_square_preferences_sum = sum([pow(dataset[other][item],2) for item in both_rated])

    # Sum up the product value of both preferences for each item
    product_sum_of_both_users = sum([dataset[user][item] * dataset[other][item] for item in both_rated])

    # Calculate the pearson score
    numerator_value = product_sum_of_both_users - (user_preferences_sum*other_preferences_sum/number_of_ratings)
    denominator_value = sqrt((user_square_preferences_sum - pow(user_preferences_sum,2)/number_of_ratings) * (other_square_preferences_sum -pow(other_preferences_sum,2)/number_of_ratings))

    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r

def most_similar_users(user, number_of_users):

    # returns the number_of_users (similar users) for a given specific user
    scores = [(pearson_correlation(user, other_user), other_user) for other_user in dataset if other_user != user]

    # Sort the similar users so the highest scores user will appear at the first
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

def get_recommendations(person):

    #Gets recommendations for a person by using a weighted average of every other users rankings
    totals = {}
    simSums = {}
    recommendataions_list = []

    for other in dataset:
        # don't compare me to myself
        if other == person:
            continue
        sim = pearson_correlation(person,other)

        # ignore scores of zero or lower
        if sim <=0: 
            continue
        for item in dataset[other]:

            # only score movies i haven't seen yet
            if item not in dataset[person]:

            # Similrity * score
                totals.setdefault(item,0)
                totals[item] += dataset[other][item]* sim
                # sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+= sim

        # Create the normalized list

    rankings = [(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()

    print 'Media Ponderada: ', rankings

    for movie in rankings:
        if movie[0] > 3:
            recommendataions_list.append(movie[1])

    # returns the recommended items
    print 'Recomendacao: ', recommendataions_list
    return recommendataions_list

get_recommendations('Clara')
#print most_similar_users('Clara', 4)