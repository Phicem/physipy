# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# __Straight to the results__ : 
#  https://mocquin.github.io/physipy/

# %% [markdown] tags=[]
# # A quickstart on AirSpeedVelocity

# %% [markdown]
# Install required packages : 
# ```
# pip install asv
# pip install virtualenv
# ```
# If first time using benchmarks : go to top package to setup the benchmarks:
# ```
# asv quickstart
# ```
# Creates json file, fill the matrix parameter with reqs packages.
#
# Once setup and benchmarks written : 
# ```
# asv run ALL  # to run all benchmarks on all comiits
# asv run v0.1..master # to all benchmarks from master to commit tagged v0.1
# asv publish  # convert results to html
# asv preview  # display html on server
# ```
#
# To profile a specific benchmark on a specific commit : 
# `asv profile benchmarks.BasicPhysipy.time_QuantityCreationByArray master --gui=snakeviz`
# (make sure to have pip install snakeviz).
#
# To benchmark only a list of commits : use `git log --pretty=oneline f1.py f2.py` to get the list of commits that modify files then : 
# ```
# asv run HASHFILE:hashestobenchmark.txt
# ```
#
# To benchmark only a specific commit, add ^! after the commit hash : 
# ```
# asv run 123azert^!
# ```
#
# See : https://www.youtube.com/watch?v=OsxJ5O6h8s0  
# Example : https://github.com/astropy/astropy-benchmarks
#  

# %% [markdown]
# # Bench of physipy

# %% [markdown]
# The list of commits that are benchmarked is available at : 
# https://github.com/mocquin/physipy/blob/master/hashestobenchmark.txt

# %% [markdown]
# The config file for asv is available at : https://github.com/mocquin/physipy/blob/master/asv.conf.json

# %% [markdown]
# Some benchmarks have aleardy been run on my personnal laptoop and the results are tracked in the repo at : https://github.com/mocquin/physipy/tree/master/.asv

# %% [markdown]
# To run the benchmark on your computer, download the repo content and run (make sure you installed asv):
# `asv run HASHFILE:hashestobenchmark.txt`

# %% [markdown]
# To launch a server and inspect results of benchmarks :   
# `asv publish  # convert results to html`  
# `asv preview  # display html on server`  

# %% [markdown]
# # Results

# %% [markdown]
# The results of benchmarks are available online at : 
# https://mocquin.github.io/physipy/

# %% [markdown]
# ![](./ressources/asv_screenshot.png)
