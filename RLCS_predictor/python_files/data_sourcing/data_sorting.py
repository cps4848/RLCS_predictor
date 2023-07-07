import pandas as pd

# List of possible options for input vars:
# Split: fall, spring, winter
# Event: reg1,l reg2, reg3, major
# Season: 22-23 (as of now)
# Region: NA, EU (as of now)
reg_list = ['reg1', 'reg2', 'reg3']
split_list = ['winter', 'fall',] #spring major 22-23 hasn't happened yet

def get_event_df(split, event, season, region=None):
    if region:
        event_df = pd.read_csv(f'../ballchasing_csvs/{str(split)}_{str(event)}_{str(region)}_{str(season)}.csv', sep=';',header=0)
    else:
        event_df = pd.read_csv(f'../ballchasing_csvs/{str(split)}_{str(event)}_{str(season)}.csv', sep=';',header=0)
    #remove unnecessary/redundant columns
    event_df = event_df.drop(columns=['replay id', 'opposing team name', 'amount collected big pads',
       'amount collected small pads',
       'count collected small pads', 'amount stolen', 'amount stolen big pads',
       'amount stolen small pads', 'count stolen big pads',
       'count stolen small pads',
       'amount used while supersonic', 'amount overfill total',
       'amount overfill stolen', 'time slow speed',
       'time boost speed', 'time in front of ball.1', 'time defensive half', 'time offensive half',
       ])
    # convert date column to datetime and sort values by date
    event_df['date'] = pd.to_datetime(event_df['date'], yearfirst=True, format="%Y-%m-%d %H:%M:%S")
    event_df.sort_values(by='date', inplace=True)
    #Split, label and merge rows 2 by 2 for each match
    event_df_1 = event_df.iloc[0::2,:]
    event_df_2 = event_df.iloc[1::2,:]
    event_df_2 = event_df_2.drop(columns=['map', 'result', 'replay title'])
    event_df_2 = event_df_2.add_suffix('_2')
    event_df_1 = event_df_1.add_suffix('_1')
    event_df_1.rename(columns={'replay title_1': 'replay title', 'map_1': 'map', 'date_1':'date'}, inplace=True)
    event_df_2.rename(columns={'date_2': 'date'}, inplace=True)
    event_df_merged = event_df_1.merge(event_df_2, 'outer', 'date')
    return event_df_merged

def get_split_regionals_df(split, season, region):
    reg_dfs = [get_event_df(split, reg, season, region) for reg in reg_list]
    regional_split_df = pd.concat(reg_dfs)
    return regional_split_df

def get_split_with_major(split, season, regions):
    major_df = get_event_df(split, 'major', season)
    if type(regions) == str:
        split_regionals_df = get_split_regionals_df(split, season, regions)
        split_with_major_dfs = [split_regionals_df, major_df]
        split_with_major_df = pd.concat(split_with_major_dfs)
        return split_with_major_df
    else:
        split_regionals_dfs = [get_split_regionals_df(split, season, region) for region in regions]
        split_regionals_dfs.append(major_df)
        splits_with_major_df = pd.concat(split_regionals_dfs)
        return splits_with_major_df

def get_majors(season):
    major_dfs_list = [get_event_df(split, 'major', season) for split in split_list]
    majors_df = pd.concat(major_dfs_list)
    return majors_df
