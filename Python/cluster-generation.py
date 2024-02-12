# %%
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.wkt import loads
from sklearn.cluster import KMeans
import numpy as np

# %% [markdown]
# 

# %%
gdf = gpd.read_file("../data/SANGIS/BUSINESS_SITES/BUSINESS_SITES.shp")

# %%
gdf = gdf.to_crs(crs='EPSG:4326')
gdf = gdf[gdf['POINT_X']!=0]
gdf['x'] = gdf['geometry'].x
gdf['y'] = gdf['geometry'].y

# %% [markdown]
# Generate Hexbins
# (note - gridsize was manually calculated based on width of SD County to generate roughly 1/4 mile radius hexbins:
# SD County is roughly 86 miles east to west, and the grid size takes the quantity of hexbins by width
# )

# %%
hexes = matplotlib.pyplot.hexbin( x= gdf['x'], y=gdf['y'],mincnt=1,gridsize=86*2)

# %%
hexbins = gpd.points_from_xy(x=[i[0] for i in hexes.get_offsets()],y=[i[1] for i in hexes.get_offsets()])[1:]

# %% [markdown]
# Merge the data with the newly generated hexbins

# %%
left_merge = gpd.GeoDataFrame(hexbins, geometry=0)

# %%
full_merge = gpd.sjoin_nearest(left_merge,gdf,how='right')

# %% [markdown]
# Count the # of datapoints in each hexbin

# %%


# %%


# %%


# %%
labels = pd.read_csv('../generate_labels.csv')
final_merge = full_merge.merge(labels, how='left', left_on='BUSTYPE',right_on='Items')
final_merge = final_merge[~final_merge['Categories'].isna()]

# %%


# %% [markdown]
# Clustering techniques - use maxima as cluster centers and run kmeans for distance

# %%
def clustering(dfin):
    index_and_counts = dfin.groupby('index_left').count().sort_values(by='x').reset_index()[['index_left','APN',]]
    def get_x(index):
        return hexbins[index].x
    def get_y(index):
        return hexbins[index].y
    index_and_counts['x'] = index_and_counts['index_left'].apply(get_x)
    index_and_counts['y'] = index_and_counts['index_left'].apply(get_y)
    index_and_counts['geometry'] = gpd.points_from_xy(index_and_counts['x'], index_and_counts['y'])
    df = gpd.GeoDataFrame(index_and_counts)
    # idea 1 - could we use 70 biggest maxima as centers?
    df['is_center'] = df['APN']>=df['APN'].sort_values(ascending=False).reset_index(drop=True)[70]
    # clustering based off local maxima centers using kmeans
    cluster_centers = df[df['is_center']==True][['x', 'y']].values
    other_points = df[['x', 'y']].values
    k = len(cluster_centers)
    kmeans = KMeans(n_clusters=k, init=cluster_centers, n_init=1)
    kmeans.fit(other_points)
    df['cluster'] = kmeans.labels_
    return df

# %%
cats = list(labels['Categories'].value_counts().index)

# %%
# TODO: have at least 5 hexbins per cluster?/count of businesses per cluster?
activity_groups = {}
for i in cats:
    activity_groups[i] = clustering(final_merge[final_merge['Categories']==i])
activity_groups['Overall']= clustering(final_merge)
for i,j in activity_groups.items():
    j.plot(column='cluster', legend=True, markersize=2).set_title(i)

# %%
df = activity_groups['Overall']

# %% [markdown]
# Generate Polygons from local maxima approach

# %%
# TODO: potentially consolidate with block groups on intersects with hexbins
poly_df = full_merge.merge(df[['index_left','cluster']],how='left')

geometry = poly_df['geometry'].apply(Point)
gpdf = gpd.GeoDataFrame(poly_df, geometry=geometry)

grouped = gpdf.groupby('cluster')

polygons = []
for cluster, group in grouped:
    polygon = group['geometry'].unary_union.convex_hull
    polygons.append({'cluster': cluster, 'geometry': polygon})

polygons_gdf = gpd.GeoDataFrame(polygons)

polygons_gdf.plot(column='cluster')


# %% [markdown]
# create geometries based on nearest block group

# %%
blocks = gpd.read_file('../data/Census_Blocks_20231127.csv').drop(columns=['geometry'])
blocks['the_geom'] = blocks['the_geom'].apply(loads)
blocks = blocks.set_geometry('the_geom')

# %%
groupby = blocks.sjoin(gpdf.drop(columns=['index_left']), how='left', predicate='contains').groupby('the_geom')['cluster']

# %%
clusters = groupby.agg(lambda x:x.value_counts().index[0] if x.any() else -1).to_frame()
clusters = clusters[clusters['cluster']!=-1].reset_index()
clusters = clusters.set_geometry('the_geom')

# %%
clusters.plot(column='cluster')

# %%
# clusters[clusters['cluster']==1].explore()
# clusters.explore()

# %% [markdown]
# OK that isn't great, lets try tracts instead?

# %%
tracts = gpd.read_file('../data/tracts.csv').drop(columns=['geometry'])
tracts['the_geom'] = tracts['the_geom'].apply(loads)
tracts = tracts.set_geometry('the_geom')

# %%
groupby_tracts = tracts.sjoin(gpdf.drop(columns=['index_left']), how='left', predicate='contains').groupby('the_geom')['cluster']

# %%
clusters_tracts = groupby_tracts.agg(lambda x:x.value_counts().index[0] if x.any() else -1).to_frame()
clusters_tracts = clusters_tracts[clusters_tracts['cluster']!=-1].reset_index()
clusters_tracts = clusters_tracts.set_geometry('the_geom')

# %%
clusters_tracts.plot(column='cluster')

# %%
# clusters[clusters['cluster']==1].explore()
# clusters_tracts.explore()

# %%
dissolved = clusters_tracts.dissolve(by='cluster').reset_index()
dissolved.plot(column='cluster')

# %%
# dissolved.explore()

# %%
dissolved.to_csv('../Output/clusters.csv')

# %%



