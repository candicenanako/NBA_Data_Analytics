import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn.preprocessing import StandardScaler
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from sklearn.decomposition import PCA


# Clustering

def plot(label, component_number, X_scaled, title, calculate_silhouette=False):
    print("clustering components:", component_number)
    if calculate_silhouette:
        print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X_scaled, label))

    fig = plt.figure()
    ax = p3.Axes3D(fig)
    ax.view_init(7, -80)
    for l in np.unique(label):
        ax.scatter(X_scaled[label == l, 0], X_scaled[label == l, 1], X_scaled[label == l, 2],
                   color=plt.cm.jet(np.float(l) / (np.max(label + 1) + 1)),
                   s=20, edgecolor='k')
    plt.title(title + " : " + str(component_number))
    plt.show()


def process_pca(X, components):
    X_pca = PCA(n_components=components).fit_transform(X)
    return X_pca


def clustering():
    player_career_stats = pd.read_csv('player_career_stats_cleaned.csv')

    # Drop none numeric columns
    X = player_career_stats.drop(columns=['Name', 'Season', 'Lg'])

    # Drop making no sense columns
    # FG%: Field Goal Percentage
    # 3PA: 3-point field goal attempts per game
    # 3P%: 3-point field goal percentage
    # 2PA: 2-point field goal attempts per game
    # 2p%: 2-point field goal percentage
    # eFG%: effective field goal percentage (This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal)
    X.drop(columns=['FG%', '3PA', '3P%', '2PA', '2P%', 'eFG%'], inplace=True)

    # Standardise dataset
    X_scaled = StandardScaler().fit_transform(X)

    # 1. 1 Ward Hierarchy Clustering
    print('Ward Clustering begins: \n')
    for n in range(3, 8, 2):
        # Hierarchy Clustering method
        X_pca = process_pca(X_scaled, components=7)
        ward = AgglomerativeClustering(n_clusters=n, linkage='ward').fit(X_pca)
        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='Ward')

    # 1.2 K-Means Clustering
    print('\nK-Mean clustering begins: \n')
    for n in range(3, 8, 2):
        X_pca = process_pca(X_scaled, components=7)
        ward = KMeans(n_clusters=n).fit(X_pca)
        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='K-Means')

    # 1.3 DBSCAN clustering
    print('\nDBSCAN clustering begins: \n')
    for n in range(3, 8, 2):
        X_pca = process_pca(X_scaled, components=3)
        ward = DBSCAN(min_samples=n).fit(X_pca)

        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='DBSCAN')

    # Use Silhouette score to measure under Ward
    print('\n Use Silhouette score to measure the different components under Ward: \n')
    for n in range(3, 8, 2):
        ward = AgglomerativeClustering(n_clusters=n).fit(X_scaled)

        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='The Silhouette of Ward',
             calculate_silhouette=True)

    # Use Silhouette score to measure under K-Means
    print('\n Use Silhouette score to measure the different components under K-Means: \n')
    for n in range(3, 8, 2):
        ward = KMeans(n_clusters=n).fit(X_scaled)

        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='The Silhouette of K-Means',
             calculate_silhouette=True)

    # Use Silhouette score to measure under DBSCAN
    print('\n Use Silhouette score to measure the different components under DBSCAN: \n')
    for n in range(3, 8, 2):
        X_pca = process_pca(X_scaled, components=7)
        ward = KMeans(n_clusters=n).fit(X_pca)

        label = ward.labels_
        plot(label=label, component_number=n, X_scaled=X_pca, title='K-Means', calculate_silhouette=True)


# Association Rules / Frequent itemset Mining Analysis

def print_apriori(sparse_df, min_support_value):
    print("min_support_value", min_support_value)
    result = apriori(sparse_df, min_support=min_support_value, use_colnames=True, verbose=1)
    print(result)
    print('\n')


def association():
    salary_of_player = pd.read_csv('salary_of_players.csv', header=None)

    # manually added column to make sense
    salary_of_player.columns = ['name', 'serving_year', 'team', 'career', 'salary']

    # Let's data mine the players on different teams over all years
    X = salary_of_player.groupby(['team'])['name'].apply(list)
    print("teams number:", len(X.index))
    print("first team name:", X.index[0])
    print("players who served in first team:", set(X.values[0]))

    # setup dataset
    dataset = []
    for index in X.index:
        dataset.append(list(set(X[index])))

    # Setup Transaction encoder
    te = TransactionEncoder()
    # sparse matrix
    oht_ary = te.fit(dataset).transform(dataset, sparse=True)
    sparse_df = pd.SparseDataFrame(oht_ary, columns=te.columns_, default_fill_value=False)

    print_apriori(sparse_df, 0.28)
    print_apriori(sparse_df, 0.25)
    print_apriori(sparse_df, 0.125)


def execute():
    clustering()
    association()


# call main function
if __name__ == "__main__":
    execute()
