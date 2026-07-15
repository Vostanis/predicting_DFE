import numpy as np
import subprocess
import pandas as pd
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import os

# take a hypergeometric sample for 1 mutation reading
def singleHypergeometricSample(num_mutations, actual_total=401, seed=42):
    rng = np.random.default_rng(seed=seed)
    num_non_mutations = 2000 - num_mutations
    
    return rng.hypergeometric(
        size=len(num_mutations), 
        ngood=num_mutations, 
        nbad=num_non_mutations, 
        nsample=actual_total
    )

# read simulated data
def readSamples():
    dir_path = "./slim/outputs/"
    file_paths = []
    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        if os.path.isfile(full_path):
            file_paths.append(full_path)

    df_list = []
    print('reading files')
    for file_path in file_paths:
        tmp = pd.read_csv(file_path)
        tmp.drop(columns=['Unnamed: 0'], inplace=True)
        df_list.append(tmp)

    print('concatenating dataframes')
    df = pd.concat(df_list, ignore_index=True)

    print('hypergeometric sampling')
    for t in [10, 20, 30, 40, 50, 60]:
        df.loc[:, f'sim_{t}'] = singleHypergeometricSample(num_mutations=df[f'sim_{t}'])

    DL = df[
        ['position', 'alpha', 'beta', 'sim_10', 'sim_20', 'sim_30', 'sim_40', 'sim_50', 'sim_60']
    ].copy()

    del df
    
    DL = DL.sort_values(['alpha', 'beta', 'position'])
    DL['norm_position'] = DL.groupby(['alpha', 'beta']).cumcount() + 1
    
    id_vars = ['norm_position', 'alpha', 'beta']
    value_vars = ['sim_10', 'sim_20', 'sim_30', 'sim_40', 'sim_50', 'sim_60']
    DM = DL.melt(id_vars=id_vars, value_vars=value_vars, var_name='time', value_name='diff')
    
    # Extract time as clean numbers (1 to 6)
    DM['time'] = DM['time'].str.replace("sim_", "").str.replace("0", "").astype(int)
    
    # 1. Pivot using numeric variables. Pandas automatically sorts integers numerically!
    # Rows: alpha & beta, Columns: norm_position first (1-10000), then time (1-6)
    DW = DM.pivot(index=['alpha', 'beta'], columns=['norm_position', 'time'], values='diff')
    
    # 2. Because it's sorted perfectly, we can generate the strings safely now
    # This loops through the correctly ordered numeric columns and builds the string names
    DW.columns = [f"p{p}_t{t}" for p, t in DW.columns]
    
    # 3. Bring back alpha and beta as regular columns
    DW = DW.reset_index()
    
    return DW;

# train (can i save at checkpoints?)
# def trainConv2D():
#     # save model to file
#     nn.save_to("./conv2d_model")
#     return;

def main():
    df = readSamples()
    print(df.head(10))

if __name__ == "__main__":
    main()