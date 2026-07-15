### Code
- [ ] talk to Mahamadou about cluster
  - [ ] "can I do a 2nd/3rd run later with different models?"
  - [ ] "how to access?"
  - [ ] "can i install packages? with nix, docker, etc.?"
  
- [ ] sim new data
  - [ ] need caching strategy: sqlite or simple file

- [ ] detailed understanding of CNN2D

- [ ] consider 2nd strategy
  - [ ] PatchSTG? requires node format - maybe it takes matrix inputs instead?

- [ ] expand on **RECONCILIATION**
  - [x] is predicting multiple y-variables sensible for building a *manifold-like structure*?
    - AI: if outputs are related to same data, model has to learn underlying structure
  - [x] finish reformulation of variance
    - the model implicity suggests an INDEX (1, 36_000) that we can compare against the variance
      to see if the relationship between expected_value and variance are sensible

- [ ] include Effective Population Size
  - [ ] max mutation size in SLiM needs to be sample of UNIF(1, 50, 2000)
        write out the SLiM script as text within python

### Write-up
- [ ] rewrite intro

- [ ] methods
  - [ ] simulation: SLiM & sampling
  - [ ] models

- [ ] limitations & assumptions
  - [ ] exposure to randomness given so much sampling
  - [ ] requires good knowledge of distributions
  - [ ] real y variable not known (because of dependency issues) 
