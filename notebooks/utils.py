import os, config
import pandas as pd
import geopandas as gpd

class Check_Valid:
  def __init__(
    self,
    source_data : gpd.GeoDataFrame,
    source_col : str,
    target_col : list
  ):
    """
    Extract valid data from a target compared with a source data

    Parameters
    ----------
    :param source_data: Actual district data which you want to check validity with
    :param source_col: Column name in your source data to compare with the target data
    :param target_col: Column name in your target data to compare with the source data(maximum check: 2)
    """
    self.source_data = source_data
    self.source_col = source_col
    self.target_col = target_col
  def print_out_valid(self, target, dir_path):
    directory = os.path.join(config.DATA_DIR, dir_path)
    files = os.listdir(directory)
    for f in files:
      if target in f:
        data_path = os.path.join(config.DATA_DIR, dir_path, f)
    try:
      df = pd.read_csv(data_path, encoding='cp949')
    except UnicodeDecodeError as encoding_err:
      print(f"Changing encoding method to utf-8: {encoding_err}")
      df = pd.read_csv(data_path, encoding='utf-8')
    year_list = df['기준_년분기_코드'].tolist()
    df = df[df['기준_년분기_코드']==max(year_list)] # 가장 최신 것
    try:
      df[self.target_col[0]] = df[self.target_col[0]].apply(lambda x : str(x))
      df = df.rename(columns={self.target_col[0]: self.source_col})
      source_df = self.source_data[[self.source_col, 'area_m2']]
      val_df = pd.merge(df, source_df, how='inner', on=self.source_col)
    except Exception as e:
      print(f"Trying with second target column: {e}")
      df[self.target_col[1]] = df[self.target_col[1]].apply(lambda x : str(x))
      df = df.rename(columns={self.target_col[1]: self.source_col})
      source_df = self.source_data[[self.source_col, 'area_m2']]
      val_df = pd.merge(df, source_df, how='inner', on=self.source_col)
    print(f'{os.path.splitext(os.path.basename(data_path))[0]} valid 상권 수: {len(val_df)}')
    return val_df

class MergeDF:
  def __init__(self, target_df):
    self.target_df = target_df
    self.merged_df = target_df
    self.on = ['TRDAR_CD', 'ALLEY_TRDA', 'ADSTRD_CD']

  def merge(self, source_df_list, select):
    # compute density
    for on, source_df in zip(self.on, source_df_list):
      source_df = source_df.copy()
      source_df[f"{select}_밀도"] = source_df[select] / source_df['area_m2']
      source_df[f"{select}_밀도"] = source_df[f"{select}_밀도"].fillna(0)

      lookup = source_df.set_index(on)[f"{select}_밀도"]

      if self.merged_df[on].apply(lambda x: isinstance(x, (list, tuple))).any():
        temp_df = self.merged_df[[on]].copy()
        temp_df['original_index'] = temp_df.index
        exploded = temp_df.explode(on)
        exploded[f'{on}_{select}_밀도'] = exploded[on].map(lookup)
        res = exploded.groupby('original_index')[f'{on}_{select}_밀도'].mean()
        self.merged_df[f'{on}_{select}_밀도'] = res
      else:
        self.merged_df = self.merged_df.merge(
          source_df[[on, f"{select}_밀도"]].rename(columns={f"{select}_밀도": f"{on}_{select}_밀도"}),
          on=on, how='left'
        )

  def average(self, select):
    cols = [f"{on}_{select}_밀도" for on in self.on]
    self.merged_df[f"{select}_밀도_평균"] = self.merged_df[cols].mean(axis=1, skipna=True)
    self.merged_df[f"{select}_밀도_평균"] = self.merged_df[f"{select}_밀도_평균"].astype(float)
    self.merged_df.drop(cols, axis=1, inplace=True)

  def reset(self):
    self.merged_df = self.target_df

  def run(self, source_df_list, select):
    """
    Merge & Average source df & target df

    Parameters
    ----------
    :param source_df_list: list of numeric source data for each area
    :param select: attribute you want to attach to target data
    :return: merged geopandas dataframe
    """
    self.merge(source_df_list, select)
    self.average(select)
    return self.merged_df

class BufferMergeDF(MergeDF):
  def __init__(self, target_df):
    super().__init__(target_df)

  def buffer_merge(self, gdf, name, radius):
    """
    Merge geopandas dataframe with exact location data using buffer

    Parameters
    ----------
    :param gdf: actual data
    :param name: name of the attribute
    :param radius: search range(circle buffer size)
    """
    buffer_gdf = self.merged_df.copy()
    try:
      buffer_gdf['geometry'] = buffer_gdf.rep_point.buffer(radius)
    except AttributeError as att_err:
      print("Attribute Error occurred in making buffer: Try centroids instead of rep_point")
      buffer_gdf['geometry'] = buffer_gdf.centroid.buffer(radius)
    joined = gdf.sjoin(buffer_gdf, how='inner', predicate='within')
    counts = joined.groupby('index_right').size()
    final_counts = counts.reindex(self.merged_df.index, fill_value=0)
    self.merged_df[f'{name}_수_{radius}m'] = final_counts