import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Dict


def convert(list) :
    """ Function to convert a list to a tuple """
    
    return tuple(i for i in list)

def frequency(data : pd.DataFrame) -> pd.DataFrame :
    """ Function to find the most frequent answer to each question/feature """
    most_frequent = []
    for col in data.columns :
        top_values = []
        top_values = data[col].mode()
        most_frequent.append(pd.DataFrame({col: top_values}).reset_index(drop=True))
    most_frequent = pd.concat(most_frequent,axis=1)
    most_frequent = pd.DataFrame(most_frequent.iloc[0,:]).T
    return most_frequent

def perc(data : pd.DataFrame, most_frequent : pd.DataFrame) :
    """ Function to compute the percentage of the most frequent answer for each feature """
    percentages = np.array([])
    for i in range(data.shape[1]):
        count = 0
        for j in range(data.shape[0]):
            if data.iloc[j, i] == most_frequent.iloc[0, i] :
                count += 1
        percentage = count*100/data.shape[0]
        percentages = np.append(percentages, percentage)
    percentages = pd.DataFrame(percentages)
    return percentages
    

def makeTree(data : pd.DataFrame, percentages : pd.DataFrame, most_frequent : pd.DataFrame) : 
    """ Makes the tree for the most similar feature method """
    if percentages.isin([100]).any().iloc[0] == True :
        print('End of this branch')
        data2 = makeSingleBranch(data, percentages, most_frequent)
        return data2
    else :
        print('Branch can still split')
        data_max, data_min = makeDoubleBranches(data, percentages, most_frequent)
        return data_max, data_min
    

def makeDoubleBranches(data : pd.DataFrame, percentages : pd.DataFrame, most_frequent : pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame] :
    """ Splits the dataframe by finding the question with the highest 
    percentage of same answers and creates two dataframes without said question """
    feature_max = pd.Series.argmax(percentages)
    print(f'Feature max :', data.iloc[:,feature_max].name, 'value', most_frequent.iloc[0, feature_max], 'with percentage :', percentages.iloc[feature_max, 0], '%')
    data_max = data.where(data.iloc[:, feature_max] == most_frequent.iloc[0, feature_max])
    data_min = data.where(data.iloc[:, feature_max] != most_frequent.iloc[0, feature_max])
    data_max = data_max.dropna()
    data_min = data_min.dropna()
    data_max = data_max.drop(data_max.columns[[feature_max]], axis=1)
    data_min = data_min.drop(data_min.columns[[feature_max]], axis=1)
    print(f'data_max shape :', data_max.shape)
    print(f'data_min shape :', data_min.shape)
    if data_min.shape[0] == 1:
        print("Clustering done on 'min' branch, sample is alone")
    if data_max.shape[0] == 1:
        print("Clustering done on 'max' branch, sample is alone")
    return data_max, data_min
    
    
def makeSingleBranch(data : pd.DataFrame, percentages : pd.DataFrame, most_frequent : pd.DataFrame) -> pd.DataFrame :
    """ If all samples have one or more common answer, the feature(s) are removed from the dataset """
    f_max = percentages[percentages.iloc[:,0] == 100]
    features_max = np.array([])
    for i in range(f_max.shape[0]):
        feature_max = f_max.iloc[i, :].name
        features_max = np.append(features_max, feature_max)
        print(f'Feature max :', data.iloc[:,feature_max].name, 'value', most_frequent.iloc[0, feature_max], 'with percentage :', percentages.iloc[feature_max, 0], '%')
    indices = features_max.tolist()
    int_indices=[]
    for intt in indices:
       int_indices.append(int(intt))
    data2 = data.drop(data.columns[convert([int_indices])], axis=1)
    print(f'data_new shape :', data2.shape)
    if data2.shape[0] == 1 :
        print("Clustering done on this branch, sample is alone")
    return data2
    
    
def makeTree50(data : pd.DataFrame):
    """ Function to make the tree for the most different feature method """
    most_frequent = frequency(data)
    percentages = perc(data, most_frequent)
    feature_min = pd.Series.argmin(abs(50-percentages))
    print(f'Feature min :', data.iloc[:,feature_min].name, 'value', most_frequent.iloc[0, feature_min], 'with percentage :', percentages.iloc[feature_min, 0], '%')
    data_max = data.where(data.iloc[:, feature_min] == most_frequent.iloc[0, feature_min])
    data_min = data.where(data.iloc[:, feature_min] != most_frequent.iloc[0, feature_min])
    data_max = data_max.dropna()
    data_min = data_min.dropna()
    data_max = data_max.drop(data_max.columns[[feature_min]], axis=1)
    data_min = data_min.drop(data_min.columns[[feature_min]], axis=1)
    print(f'data_max shape :', data_max.shape)
    print(f'data_min shape :', data_min.shape)
    if data_min.shape[0] == 1:
        print("Clustering done on 'min' branch, sample is alone")
    if data_max.shape[0] == 1:
        print("Clustering done on 'max' branch, sample is alone")
    return data_max, data_min

def exploreFeature(data: pd.DataFrame, data_red : pd.DataFrame, column : str):
    """ Function to explore answers to one question for a subgroup  """
    feature = []
    for i in range(data_red.shape[0]):
        index = data_red.iloc[i,:].name
        feat = data.loc[index, column]
        feature.append(feat)
    feature = pd.DataFrame(feature)
    most_frequent = frequency(feature)
    percentages = perc(feature, most_frequent)
    answer_max = pd.Series.argmax(percentages)
    print(f'Feature', column, 'for cluster')
    print(feature)
    print(f'Dominant answer :', most_frequent.iloc[0, answer_max], 'with percentage :', percentages.iloc[answer_max, 0], '%')