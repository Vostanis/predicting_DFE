# Predicting the Distribution of Finess Effects

In a Wright-Fisher model, with selection, we would prefer to model the _selection coefficient_
as a distribution (compared to a constant, for example). These require estimation, and this 
project attempts to provide a Machine Learning (specifically Deep Learning) approach to
estimating this distribution in a more computationally-friendly way.

Other projects include:
1. PolyDFE, for _natural populations_.
   <https://github.com/paula-tataru/polyDFE>

3. Bait-ER, for _Evolve & Resequence_ experiments.
   <https://github.com/mrborges23/Bait-ER>

---------------------------------------------------------------------------------------------

## To do
- [ ] Get SLiM data
  - [ ] what is SLiM?
- [ ] Learn about PolyDFE
- [ ] Learn about STGNN (2021)
- [ ] Learn about STWave (2023)
- [ ] Learn about PatchSTG (2025)
- [ ] Is this a travel problem; i.e. would Djikstra's algorithm play into this?

## Questions for Rui & Diogo:
- [ ] Am I understanding the dataset correctly?
  - [ ] @Rui: is my table correct?
  - [ ] @Rui: Relationships between chromosomes?
- [ ] @Rui: what was wrong with the BAIT-ER?
  - [ ] specific results that were bad
- [ ] Any problems with capturing distance between positions?
  - [ ] should this captured for each base? 
- [ ] How do generations & different populations play into *selection coefficient*?

## Models
1. STGNN <https://github.com/LMissher/STGNN>
2. STWave <https://github.com/LMissher/STWave>
3. PatchSTG <https://github.com/LMissher/PatchSTG>
