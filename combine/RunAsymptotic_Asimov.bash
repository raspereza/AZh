#!/bin/bash
dir=${CMSSW_BASE}/src/CombineHarvester/bbHRun2Legacy/output/cards
ulimit -s unlimited
proc=$1
mass=$2
frozen=$3

combineTool.py -M AsymptoticLimits --noFitAsimov --rMin=0 --rMax=50 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --cminDefaultMinimizerTolerance=0.01 -d datacards_${proc}/Run2/${mass}/ws.root -t -1 -n .limit_${proc}_method1.exp -m $mass

combineTool.py -M AsymptoticLimits --noFitAsimov --setParameters r_bbA=0,r_ggA=0 --setParameterRanges r_${proc}=-30,30 --redefineSignalPOIs r_${proc} --freezeParameters r_${frozen} --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --cminDefaultMinimizerTolerance=0.01 -d datacards/Run2/${mass}/ws.root -t -1 -n .limit_${proc}_method2.exp -m $mass

combineTool.py -M AsymptoticLimits --noFitAsimov --setParameters r_bbA=0,r_ggA=0 --setParameterRanges r_ggA=-30,30:r_bbA=-30,30 --redefineSignalPOIs r_${proc} --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --cminDefaultMinimizerTolerance=0.01 -d datacards/Run2/${mass}/ws.root -t -1 -n .limit_${proc}_method3.exp -m $mass


