import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import random

def userIdToIndex(userSet, userId=None):
    userIdToIndexMap = {uid: idx for idx, uid in enumerate(list(userSet))}
    return userIdToIndexMap if userId is None else userIdToIndexMap[userId]

def movieIdToIndex(movieSet, movieId=None):
    movieIdToIndexMap = {mid: idx for idx, mid in enumerate(list(movieSet))}
    return movieIdToIndexMap if movieId is None else movieIdToIndexMap[movieId]

def loadData():
    data = pd.read_csv('ratings.csv', usecols=['userId', 'movieId', 'rating'])
    uniqueUsers = sorted(data['userId'].unique())
    uniqueMovies = sorted(data['movieId'].unique())
    
    ratingsMatrix = np.zeros((len(uniqueUsers), len(uniqueMovies)))
    userIdxMap = {uid: idx for idx, uid in enumerate(uniqueUsers)}
    movieIdxMap = {mid: idx for idx, mid in enumerate(uniqueMovies)}

    userIndices = data['userId'].map(userIdxMap)
    movieIndices = data['movieId'].map(movieIdxMap)
    ratingsMatrix[userIndices, movieIndices] = data['rating']

    return ratingsMatrix, uniqueUsers, uniqueMovies

def findNearestUsers(targetUserId, ratingsMatrix, numNeighbors, uniqueUsers):
    targetUserIdx = userIdToIndex(uniqueUsers, targetUserId)
    
    neighborsModel = NearestNeighbors(n_neighbors=numNeighbors + 1, metric='correlation')
    neighborsModel.fit(ratingsMatrix)
    
    indices = neighborsModel.kneighbors(ratingsMatrix[targetUserIdx].reshape(1, -1), return_distance=False).flatten()
    
    neighbors = [list(userIdToIndex(uniqueUsers).keys())[list(userIdToIndex(uniqueUsers).values()).index(idx)] for idx in indices]
    neighbors.remove(targetUserId)
    
    return neighbors

def suggestMovie(targetUserId, ratingsMatrix, neighbors, userSimilarity, uniqueUsers, uniqueMovies):
    targetUserIdx = userIdToIndex(uniqueUsers, targetUserId)
    unratedMovies = np.where(ratingsMatrix[targetUserIdx] == 0)[0]
    movieRecommendations = {}

    for movieIdx in unratedMovies:
        movieId = list(movieIdToIndex(uniqueMovies).keys())[movieIdx]
        ratings = []
        similarities = []
        
        for neighborId in neighbors:
            neighborIdx = userIdToIndex(uniqueUsers, neighborId)
            rating = ratingsMatrix[neighborIdx, movieIdx]
            
            if rating != 0:
                similarity = userSimilarity[targetUserIdx, neighborIdx]
                ratings.append(rating)
                similarities.append(similarity)

        if ratings:
            weightedSum = np.dot(ratings, similarities)
            sumOfSimilarities = np.sum(similarities)
            movieRecommendations[movieId] = weightedSum / sumOfSimilarities

    return max(movieRecommendations, key=movieRecommendations.get)

userId = random.randint(1,610)

ratingsMatrix, uniqueUsers, uniqueMovies = loadData()
userSimilarityMatrix = 1 - pairwise_distances(ratingsMatrix, metric='correlation')
np.fill_diagonal(userSimilarityMatrix, 0)
nearestUsers = findNearestUsers(userId, ratingsMatrix, 10, uniqueUsers)
print(f"User: {userId}")
print(f"Neighbors: {nearestUsers}")
print("Recommended movie:", suggestMovie(userId, ratingsMatrix, nearestUsers, userSimilarityMatrix, uniqueUsers, uniqueMovies))
