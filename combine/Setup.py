#!/usr/bin/env python

import ROOT
import os
import AZh.combine.utilsAZh as utils

########################################################################
# new tau ID scale factors for UL2016 are 5% higher than previous ones #
# updated scale factors have been released in summer 2023              #
# https://indico.cern.ch/event/1264653                                 #
# https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2  #
########################################################################
tauID_UL2016 = {
    'eeem' : 1.00,
    'eeet' : 1.06,
    'eemt' : 1.06,
    'eett' : 1.12,
    'mmem' : 1.00,
    'mmet' : 1.06,
    'mmmt' : 1.06,
    'mmtt' : 1.12
}

def MergeDataMC():
    os.system('cp root_files/backup/*root root_files')
    os.system('./Hadd_MC_data.bash')

def FixNegativeBins():

    years = utils.years
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    uncs = utils.azh_uncs
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    variations = utils.variations
    for year in years:
        for cat in cats:
            nameinput = folder + "/MC_data_"+cat+"_"+year+".root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
            
                hist = inputfile.Get(channel+'/data')
                histToWrite = hist.Clone(channel+'data_obs')
                inputfile.cd(channel)
                histToWrite.Write('data_obs')
                for template in templates:
                    hist = inputfile.Get(channel+'/'+template)
                    nbins = hist.GetNbinsX()
                    for ib in range(1,nbins+1):
                        x = hist.GetBinContent(ib)
                        if x<0:
                            print('negative bin %2i :  %7.5f in %s_%s_%s %s'
                                  %(ib,x,year,cat,channel,template))
                            hist.SetBinContent(ib,0.)
                            hist.SetBinError(ib,0.)
                    inputfile.cd(channel)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                for ib in range(1,nbins+1):
                                    x = histSys.GetBinContent(ib)
                                    if x<0:
                                        print('negative bin %2i : %7.5f in %s_%s_%s %s_%s%s'
                                              %(ib,x,year,cat,channel,template,unc,variation))
                                        histSys.SetBinContent(ib,0.)
                                        histSys.SetBinError(ib,0.)
                                inputfile.cd(channel)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()
    
def RescaleToTauID_2016():

    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    uncs = utils.azh_uncs
    masses = utils.azh_masses
    variations = utils.variations
    signals = utils.azh_signals
    folder = utils.BaseFolder+'/root_files'

    for cat in cats:
        nameinput = folder + "/MC_data_"+cat+"_2016.root"
        inputfile = ROOT.TFile(nameinput,'update')
        for channel in channels:
            scale = tauID_UL2016[channel]
            print('scaling backgrounds in %s category of %s channel by TauID of %5.2f'%(cat,channel,scale))
            for template in templates:
                hist = inputfile.Get(channel+'/'+template)
                hist.Scale(scale)
                inputfile.cd(channel)
                hist.Write(template)
                for unc in uncs:
                    for variation in variations:
                        histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                        if histSys!=None:
                            histSys.Scale(scale)
                            inputfile.cd(channel)
                            histSys.Write(template+'_'+unc+variation)
        inputfile.Close()

        for mass in masses:
            nameinput = folder + "/signal_"+mass+"_"+cat+"_2016.root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
                scale = tauID_UL2016[channel]
                print('scaling backgrounds in %s category of %s channel and mA=%s by TauID of %5.2f'%(cat,channel,mass,scale))
                for template in signals:
                    hist = inputfile.Get(channel+'/'+template)
                    hist.Scale(scale)
                    inputfile.cd(channel)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                histSys.Scale(scale)
                                inputfile.cd(channel)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()
    
def FixMetUnc():

    years = utils.years
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    unc = Unc
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    for year in years:
        for cat in cats:
            nameinput = folder + "/MC_data_"+cat+"_"+year+".root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
            
                hist = inputfile.Get(channel+'/data')
                histToWrite = hist.Clone(channel+'data_obs')
                inputfile.cd(channel)
                histToWrite.Write('data_obs')
                for template in templates:
                    hist = inputfile.Get(channel+'/'+template)
                    nbins = hist.GetNbinsX()
                    for ib in range(1,nbins+1):
                        x = hist.GetBinContent(ib)
                        if x<0:
                            print('negative bin %2i :  %7.5f in %s_%s_%s %s'
                                  %(ib,x,year,cat,channel,template))
                            hist.SetBinContent(ib,0.)
                            hist.SetBinError(ib,0.)
                    inputfile.cd(channel)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                for ib in range(1,nbins+1):
                                    x = histSys.GetBinContent(ib)
                                    if x<0:
                                        print('negative bin %2i : %7.5f in %s_%s_%s %s_%s%s'
                                              %(ib,x,year,cat,channel,template,unc,variation))
                                        histSys.SetBinContent(ib,0.)
                                        histSys.SetBinError(ib,0.)
                                inputfile.cd(channel)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()



############
### MAIN ###
############
if __name__ == "__main__":


    ROOT.gROOT.SetBatch(True)

    # merging data and MC into one file
    MergeDataMC()

    # fixing bins with negative content
    FixNegativeBins()

    # rescale MC shapes by new tau ID
    # RescaleToTauID_2016()

    # creating folders for figures, batch jobs
    pathdir=utils.BaseFolder+'/figures'
    if not os.path.isdir(): os.system('mkdir figures')
    pathdir=utils.BaseFolder+'/jobs'
    if not os.path.isdir(): os.system('mkdir jobs')
