#!/bin/bash
# $1 - process (ggA or bbA)
# $2 - mass
ulimit -s unlimited

PROC=${1}
MASS=${2}
ANALYSIS=${3}
OUTDIR=exp_impacts_AZh_${PROC}${MASS}
if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
fi
cd $OUTDIR
rm *
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_${PROC}/Run2/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin -10 --rMax 10 --robustFit 1 -t -1 --doInitialFit 
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_${PROC}/Run2/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin -10 --rMax 10 --robustFit 1 -t -1 --job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 4 --doFits
cd -

