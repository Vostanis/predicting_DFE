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

def sampleAndSimulate(alpha, beta, num_genomes=2000, seed=42):
    gamma_samples = np.random.default_rng(seed=seed).gamma(shape=alpha, scale=beta, size=10_000)
    s_samples = gamma_samples - 1
    pd.DataFrame(s_samples).to_csv('../slim/inputs/gamma_distributed_sample.csv', index=False, header=False)

    # Find fitness coefficients that work
    print(f"Simulating alpha={alpha}, beta={beta} ...")
    result = subprocess.run(['time', 'slim', '-x', '../slim/simulate_one.slim'], capture_output=True, text=True)
    # print(result.stdout)
    if result.stderr:
        print("STDERR:\n", result.stderr)

    print("Simulation complete - reading files ...")
    sim_df = pd.DataFrame()
    
    sim_df['position'] = pd.read_csv("../slim/inputs/admixture_mapping_targets.csv", header=None)
    for generation in range(1, 7):
        sim_i = pd.read_csv(f"../slim/tmp/65755-10000-0-_Cycle_{generation}0.txt")
        sim_df[f"sim_{generation}0"] = sim_i[f"Frequency_{generation}0"]

    # Turn mutations into allele frequencies
    for i in [10,20,30,40,50,60]:
        sim_df[f'sim_{i}'] = sim_df[f'sim_{i}'] / num_genomes

    # Deltas
    sim_df['simdelta_20'] = sim_df['sim_20'] - sim_df['sim_10']
    sim_df['simdelta_30'] = sim_df['sim_30'] - sim_df['sim_20']
    sim_df['simdelta_40'] = sim_df['sim_40'] - sim_df['sim_30']
    sim_df['simdelta_50'] = sim_df['sim_50'] - sim_df['sim_40']
    sim_df['simdelta_60'] = sim_df['sim_60'] - sim_df['sim_50']

    # Create file
    sim_df[['alpha', 'beta']] = alpha, beta
    file_path = f"../slim/outputs/alpha={alpha}_beta={beta}.csv"
    sim_df.to_csv(path_or_buf=file_path)
    print(f"written file to {file_path}")
    
    return sim_df

def main():
    alphas = np.linspace(1, 36_000, 10)
    betas = np.linspace(0.1, 1, 10)
    for alpha in alphas:
        for beta in betas:
            sampleAndSimulate(alpha=alpha, beta=1/beta)

if __name__ == "__main__":
    main()
