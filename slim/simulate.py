import numpy as np
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from pathlib import Path

root = Path.cwd().resolve().parent
sys.path.insert(0, str(root))
print("Setting root of the project to:", root)
print("This means we can bring in models from other directories (like ./models)")

def sampleAndSimulate(alpha, beta, sampled_totals, seed=42):
    gamma_samples = np.random.default_rng(seed=seed).gamma(shape=alpha, scale=1/beta, size=10_000)
    s_samples = (gamma_samples - 1)/1000
    pd.DataFrame(s_samples).to_csv(
        './slim/inputs/gamma_distributed_sample.csv', 
        index=False, 
        header=False
    )

    # Find fitness coefficients that work
    print(f"Simulating alpha={alpha}, beta={beta} ...")
    result = subprocess.run(
        ['time', 'slim', '-x', './slim/simulate_one.slim'], 
        capture_output=True, 
        text=True
    )

    print("Simulation complete - reading files ...")
    sim_df = pd.DataFrame()
    
    sim_df['position'] = pd.read_csv(
        "./slim/inputs/admixture_mapping_targets.csv", 
        header=None
    )
    for generation in range(2, 8):
        sim_i = pd.read_csv(f"./slim/tmp/65755-10000-0-_Cycle_{generation}0.txt")
        sim_df[f"sim_{generation-1}0"] = sim_i[f"Frequency_{generation}0"]

    # Turn mutations into allele frequencies
    for i in [10,20,30,40,50,60]:
        sim_df[f'sim_{i}'] = sim_df[f'sim_{i}'] * sampled_totals[f't{i}']

    # Deltas
    sim_df['simdelta_20'] = sim_df['sim_20'] - sim_df['sim_10']
    sim_df['simdelta_30'] = sim_df['sim_30'] - sim_df['sim_20']
    sim_df['simdelta_40'] = sim_df['sim_40'] - sim_df['sim_30']
    sim_df['simdelta_50'] = sim_df['sim_50'] - sim_df['sim_40']
    sim_df['simdelta_60'] = sim_df['sim_60'] - sim_df['sim_50']

    # Create file
    sim_df[['alpha', 'beta']] = alpha, beta
    file_path = f"./slim/outputs/alpha={alpha}_beta={beta}.csv"
    sim_df.to_csv(path_or_buf=file_path)
    print(f"written file to {file_path}")
    
    return sim_df

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
    return freq, total


def readAlleleFrequencyData(file_path="./data/chromosome_2L.sync", seed=42):
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

    rng = np.random.default_rng(seed)
    randomPositions = rng.choice(
        df['position'].unique(),
        size=10_000,
        replace=False
    )
    df = df[df['position'].isin(randomPositions)]

    for column in ['gen_0','gen_10','gen_20','gen_30','gen_40','gen_50','gen_60']:
        df[[column, f'total_{column}']] = [
            alleleFrequency(b, c) 
            for b, c in zip(df['base'], df[column])
        ]
        
    for generation in [10,20,30,40,50,60]:
        prev_generation = generation - 10
        df[f'delta_{generation}'] = df[f'gen_{generation}'] - df[f'gen_{prev_generation}']

    return df;

def simulateTotals(df, seed=42):
    simTotals = pd.DataFrame()
    for gen in [10, 20, 30, 40, 50, 60]:
        actuals = df[f'gen_{gen}'] * 2000
        totals = df[f'total_gen_{gen}']

        rng = np.random.default_rng(seed)
        simTotals[f't{gen}'] = hypergeometric_sampling(2000, df[f'gen_{gen}'], 20000)
    return simTotals;

def hypergeometric_sampling(N, freqs_T, S = None, seed = None):
    rng = np.random.default_rng(seed)
    M = 2 * N

    if S is None:
        S = int(0.2 * N)
    S = int(max(1, min(S, M)))  # clamp to [1, 2N]

    # convert true frequencies to integer counts in [0, M]
    K = np.rint(freqs_T * M).astype(int)  
    K = np.clip(K, 0, M) 

    # X ~ Hypergeom(ngood = K, nbad = M-K, nsample = S)
    X = rng.hypergeometric(ngood = K, nbad = M - K, nsample = S)

    freqs_sampled_T = X / S
    return freqs_sampled_T

def main():
    print("reading original data")
    df = readAlleleFrequencyData()
    sampled_totals = simulateTotals(df)

    print("starting simulation")
    ranges = []
    # for i in range(1, 36_000+1):
    # for i in range(86, 36_000+1): # start-stopping the process
    for i in np.linspace(1000, 36000, 200): # start-stopping the process
        X = np.linspace((0.975 * i), (1.025 * i), 3) # alpha/beta roughly between 0.95 & 1.05 for every iteration
        ranges.append(X)

    for range_i in ranges:
        for alpha in range_i:
            for beta in range_i:
                if 0.95 <= alpha / beta <= 1.05:
                    sampleAndSimulate(alpha=alpha, beta=beta, sampled_totals=sampled_totals)

if __name__ == "__main__":
    main()
