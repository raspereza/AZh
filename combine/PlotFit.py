#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
from array import array
import ROOT
import os

def ExtractHistoFromFit(hist,fitfile,**kwargs):

    fittype = kwargs.get('fittype','prefit')
    channel = kwargs.get('channel','mmtt')
    year = kwargs.get('year','2018')
    cat = kwargs.get('cat','0btag')
    mass = kwargs.get('mass','300')
    templ = kwargs.get('templ','ggA')
    
    histname = 'shapes_%s/azh_%s_%s_%s_%s/%s'%(fittype,year,cat,channel,mass,templ)
    reference = fitfile.Get(histname)
    norm = reference.GetSumOfWeights()
    is_positive = norm>0.0
    nbins = reference.GetNbinsX()
    for ib in range(1,nbins+1):
        x = 0
        e = 0
        if is_positive:
            x = reference.GetBinContent(ib)
            e = reference.GetBinError(ib)
        hist.SetBinContent(ib,x)
        hist.SetBinError(ib,e)
        
############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Plotting final discriminants")
    parser.add_argument('-year','--year',dest='year',default='all')
    parser.add_argument('-cat','--cat',dest='cat',default='0btag')
    parser.add_argument('-channel','--channel',dest='channel',default='all')
    parser.add_argument('-folder','--folder',dest='folder',default='datacards')
    parser.add_argument('-mass','--mass',dest='mass',required=True)
    parser.add_argument('-xmin','--xmin',dest='xmin',type=float,default=200)
    parser.add_argument('-xmax','--xmax',dest='xmax',type=float,default=2500)
    parser.add_argument('-logx','--logx',dest='logx',action='store_true')
    parser.add_argument('-fittype','--fittype',dest='fittype',default='prefit',choices=['prefit','fit_b','fit_s'])
    parser.add_argument('-unblind','--unblind',dest='unblind',action='store_true')
    args = parser.parse_args()

    blind = not args.unblind
    year = args.year
    cat = args.cat
    channel = args.channel
    mass = args.mass
    fittype = args.fittype
    logx = args.logx

    xmin = args.xmin
    xmax = args.xmax

    prefix = ''
    suffix = '_%s_%s_%s'%(year,cat,channel)
    group = utils.azh_groupbkgs
    bkgs = utils.azh_bkgs
    signals = {}

    years = []
    cats = []
    channels = []

    year_legend = year
    cat_legend = cat
    channel_legend = channel

    signals['bbA'] = 'bbA'+mass
    signals['ggA'] = 'ggA'+mass

    if year=='all':
        years = utils.years
        year_legend='Run2'
    else:
        years = [year]
        year_legend=year

    if cat.lower()=='all':
        cats = utils.azh_cats
        cat_legend=''
    else:
        cats = [cat]
        cat_legend=cat

    if channel.lower()=='all':
        channels = utils.azh_channels_noem
        channel_legend=''
    elif channel.lower()=='em':
        channels = ['eeem','mmem']
    elif channel.lower()=='et':
        channels = ['eeet','mmet']
    elif channel.lower()=='mt':
        channels = ['eemt','mmmt']
    elif channel.lower()=='tt':
        channels = ['eett','mmtt']
    else:
        channels = [channel]
 
    templates = ['data','other_bkg','reducible_bkg','ZZ_bkg','tot_bkg','ggA','bbA']
    templates_bkg = ['other_bkg','reducible_bkg','ZZ_bkg']
    templates_sig = ['ggA','bbA']
    templates_totbkg = ['tot_bkg']
    templates_data = ['data']
        
    print()
    print('plotting macro ->')
    print
    print('years ',years)
    print('categories ',cats)
    print('channels ',channels)
    print('templates ',templates)
    print

    hists = {}
    isFirst = True

    inputfile, inputfile_s = utils.GetInputFiles(
        analysis='azh',
        year='2018',
        cat='0btag',
        channel='mmtt',
        folder=args.folder,
        mass=mass)

    # creating templates
    dirname = 'mmtt/'
    templHist = inputfile.Get(dirname+prefix+'ZZ')
    bins = []
    nbins = templHist.GetNbinsX()
    for ib in range(1,nbins+2):
        bins.append(float(templHist.GetBinLowEdge(ib)))

    inputfile.Close()
    inputfile_s.Close()

    fitfilename = utils.BaseFolder + '/fit_Run2_mA' + mass + '_obs/fitDiagnosticsTest.root'
    if not os.path.isfile(fitfilename): 
        print('input file %s does not exist'%(fitfilename))
        print('Run script ./RunFit.py --sample Run2 --mass %s --saveShapes -obs --batch')
        exit()
    
    fitfile = ROOT.TFile(fitfilename)
   
    print
    print('histogram binning')
    for ib in range(1,nbins+1):
        print('[%4i,%4i]'%(bins[ib-1],bins[ib]))
        
    for template in templates:
        hists[template] = ROOT.TH1D(template,'',nbins,array('d',list(bins)))

    print

    for year in years:
        for cat in cats:
            for channel in channels:        
        
                hists_x = {}
                suffix = '_%s_%s_%s'%(year,cat,channel)
                dirname = channel+'/'

                # open input files
                inputfile, inputfile_s = utils.GetInputFiles(
                    analysis='azh',
                    year=year,
                    cat=cat,
                    channel=channel,
                    folder=args.folder,
                    mass=mass)

                # extract backgrounds
                hists_bkg = {} 
                for bkg in bkgs:
                    hist_bkg = inputfile.Get(dirname+prefix+bkg)
                    ExtractHistoFromFit(hist_bkg,
                                        fitfile,
                                        fittype=fittype,
                                        channel=channel,
                                        year=year,
                                        cat=cat,
                                        templ=bkg,
                                        mass=mass)
                    hists_bkg[bkg] = hist_bkg.Clone(bkg+suffix)
                    sumofweights = hists_bkg[bkg].GetSumOfWeights()
                    print('%15s %6.2f'%(bkg,sumofweights))

                # grouping backgrounds
                hists_grp = utils.GroupBackgrounds(hists_bkg,group)
                for grp in hists_grp:
                    hist_grp = hists_grp[grp]
                    hists_x[grp+suffix] = hist_grp.Clone(grp+suffix)
                    sumofweights = hists_x[grp+suffix].GetSumOfWeights()
                name = 'total'
                sumofweights = hists_x['tot_bkg'+suffix].GetSumOfWeights()
                print('----------------------')
                print('%15s %6.2f'%(name,sumofweights))

                print
                for sig in signals:
                    hist_sig = inputfile_s.Get(dirname+prefix+signals[sig])
                    ExtractHistoFromFit(hist_sig,
                                        fitfile,
                                        fittype=fittype,
                                        channel=channel,
                                        year=year,
                                        mass=mass,
                                        templ=sig,
                                        cat=cat)
                    hists_x[sig+suffix] = hist_sig.Clone(sig+suffix)
                    sigmass = sig+mass
                    sumofweights = hists_x[sig+suffix].GetSumOfWeights()
                    print('%15s %6.2f'%(sigmass,sumofweights))
    
                print
                hist_data = inputfile.Get(dirname+prefix+'data_obs')
                hists_x['data'+suffix] = hist_data.Clone('data'+suffix)
                sumofweights = hists_x['data'+suffix].GetSumOfWeights()
                name = 'data' 
                print('%15s %6.0f'%(name,sumofweights))
                print

                for template in templates:
                    name = template+suffix
                    hist = hists_x[name]
                    histTempl=hists[template]
                    utils.addHistos(histTempl,hist)

                inputfile.Close()
                inputfile_s.Close()

                print
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print


    print('accumulated yields ')
    print

    for template in templates_bkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_totbkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_sig:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_data:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.0f'%(template,sumofweights))

    print
    utils.Plot(hists,
               analysis='azh',
               year=year_legend,
               cat=cat_legend,
               channel=channel_legend,
               mass=mass,
               blind=blind,
               xmin=xmin,
               xmax=xmax,
               logx=logx,
               postfix=fittype)

