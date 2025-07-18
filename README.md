# CPG SERVER

## Install Steps

1. create a venv: `conda create -n cpg-server python=3.12`
2. install dependencies: `pip install jep "fastapi[standard]"`

## Run server

1. activate venv: `conda activate cpg-server`
2. run command: `LD_LIBRARY_PATH=~/miniforge3/envs/cpg-server/lib/python3.12/site-packages/jep CPG_EXECUTABLE_PATH=~/cpg/cpg-neo4j/build/install/cpg-neo4j/bin/cpg-neo4j fastapi run main.py`

> [!NOTE]
> Assign `LD_LIBRARY_PATH` to installed jep path, and `CPG_EXECUTABLE_PATH` to cpg-neo4j executable path.

## Debug

Goto <http://0.0.0.0:8000/docs>

## Develop

use `fastapi dev main.py` instead.