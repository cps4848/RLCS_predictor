import pandas as pd

# List of possible options for input vars:
# Split: fall, spring, winter
# Event: reg1,l reg2, reg3, major
# Season: 22-23 (as of now)
# Region: NA, EU (as of now)
reg_list = ['reg1', 'reg2', 'reg3']

def get_event_df(split, event, season, region=None):
    if region:
        event_df = pd.read_csv(f'../ballchasing_csvs/{str(split)}_{str(event)}_{str(region)}_{str(season)}.csv', sep=';',header=0)
    else:
        event_df = pd.read_csv(f'../ballchasing_csvs/{str(split)}_{str(event)}_{str(season)}.csv', sep=';',header=0)
    #remove
    event_df = event_df.drop(columns=['replay id', 'date', 'opposing team name', 'amount collected big pads',
       'amount collected small pads',
       'count collected small pads', 'amount stolen', 'amount stolen big pads',
       'amount stolen small pads', 'count stolen big pads',
       'count stolen small pads',
       'amount used while supersonic', 'amount overfill total',
       'amount overfill stolen', 'time slow speed',
       'time boost speed', 'time in front of ball.1', 'time defensive half', 'time offensive half',
       ])
    #Split, label and merge rows 2 by 2 for each match
    event_df_1 = event_df.iloc[0::2,:]
    event_df_2 = event_df.iloc[1::2,:]
    event_df_2 = event_df_2.drop(columns=['map', 'result'])
    event_df_2 = event_df_2.add_suffix('_2')
    event_df_1 = event_df_1.add_suffix('_1')
    event_df_1.rename(columns={'replay title_1': 'replay title', 'map_1': 'map'}, inplace=True)
    event_df_2.rename(columns={'replay title_2': 'replay title'}, inplace=True)
    event_df_merged = event_df_1.merge(event_df_2, 'outer', 'replay title')
    return event_df_merged

def get_split_regionals_df(split, season, region):
    reg_dfs = [get_event_df(split, reg, season, region) for reg in reg_list]
    return reg_dfs
