import pandas as pd
import numpy as np
import scipy.stats as stats
import plotext as plt
import sys
import subprocess
from pathlib import Path

RANDOM_SEED = 1

# Read a single allele frequency, i.e., "0:200:0:1:0:0"
def alleleFrequency(base, allele_count):
    # Allele count format: [A : T : C : G : N : del]
    base_dict = {
        'A': 0,
        'T': 1,
        'C': 2,
        'G': 3,
        'N': 4,   # unused
        'del': 5  # unsued, both defined to be explicit
    }
    base_index = base_dict.get(base)
    vector = [int(num) for num in allele_count.split(':')]

    # Sum all values
    total = sum(vector)

    # Error-handle for division-by-zero
    if total == 0:
        return 0.0

    # Find difference between base & total
    base_value = vector[base_index]
    mutations = total - base_value
    freq = mutations / total
    return freq;

def readAlleleFrequencyData(file_path="./data/chromosome_2L.sync"):
    columns = [
        'chromosome',
        'position',
        'base',
        'Dsim_Fl_Base_1',
        'Dsim_Fl_Hot_F10_1',
        'Dsim_Fl_Hot_F20_1', 
        'Dsim_Fl_Hot_F30_1',
        'Dsim_Fl_Hot_F40_1', 
        'Dsim_Fl_Hot_F50_1', 
        'Dsim_Fl_Hot_F60_1'
    ]

    df = pd.read_csv(
        filepath_or_buffer=file_path,
        sep='\t', # tab-separated values
        names=columns,
        usecols=columns,
        header=None # no headers provided
    )

    rename_dict = {
        'Dsim_Fl_Base_1':    'gen_0',
        'Dsim_Fl_Hot_F10_1': 'gen_10',
        'Dsim_Fl_Hot_F20_1': 'gen_20',
        'Dsim_Fl_Hot_F30_1': 'gen_30',
        'Dsim_Fl_Hot_F40_1': 'gen_40',
        'Dsim_Fl_Hot_F50_1': 'gen_50',
        'Dsim_Fl_Hot_F60_1': 'gen_60'
    }

    # Rename the columns (inplace=True modifies the original DataFrame)
    df.drop(columns=['chromosome'], inplace=True)
    df.rename(columns=rename_dict, inplace=True)

    for column in ['gen_0','gen_10','gen_20','gen_30','gen_40','gen_50','gen_60']:
        df[column] = [
            alleleFrequency(b, c) 
            for b, c in zip(df['base'], df[column])
        ]    

    return df;

def fitGammaDistribution(df, alpha, beta):
    cols = ['gen_0','gen_10','gen_20','gen_30','gen_40','gen_50','gen_60']
    return stats.gamma.pdf(x=df[cols], a=alpha, scale=beta);

# Find the fitness coefficient for a single row:
# - 7 generations
# - 1 position
def findFitnessCoefficient(alpha, beta, row):
    # Take an alpha, beta & make a gamma distribution
    

    # Find fitness coefficients that work for specific row
    return;
    
def main():
    # Read the data
    # df = readAlleleFrequencyData()
    # print("\n==THE DATASET" + ('='*73))
    # print(df.head(10))
    # print('='*86)
    # print(df.info())
    # print('='*86)

    # Gamma distribution
    alpha = 5
    gamma_samples = np.random.default_rng(seed=RANDOM_SEED).gamma(shape=alpha, scale=1/alpha, size=70_000)
    s_samples = gamma_samples - 1
    pd.DataFrame(gamma_samples).to_csv('./slim/inputs/gamma_distributed_sample.csv', index=False, header=False)

    # Find fitness coefficients that work
    result = subprocess.run(['slim', '-x', './slim/simulate_one.slim'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:\n", result.stderr)

if __name__ == "__main__":
    main()

