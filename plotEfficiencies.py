import ROOT
from ROOT import *

from efficienciesAndFakeRates import *

import sys,os,subprocess
from array import array
import numpy as np

from eras.Run2023   import Run2023D_DQMGUI_SHM
from eras.Run2024   import Run2024C_DQMGUI_SHM, Run2024D_DQMGUI_SHM, Run2024E_DQMGUI_SHM
from eras.Run2024   import Run2024Gv1_DQMGUI_SHM,Run2024Gv2_DQMGUI_SHM,Run2024H_DQMGUI_SHM,Run2024HlowPU_DQMGUI_SHM
from eras.Run2024   import Run2024G_beforeCMSALCA293_DQMGUI_SHM,Run2024G_afterCMSALCA293_beforeCMSALCA294_DQMGUI_SHM,Run2024G_afterCMSALCA294_DQMGUI_SHM
from cls.DQMCanvas  import DQMCanvasCMS

#eras = [Run2024Gv1_DQMGUI_SHM,Run2024PreHV_DQMGUI_SHM,Run2024PostHV_DQMGUI_SHM]
eras = [Run2024Gv1_DQMGUI_SHM,Run2024G_beforeCMSALCA293_DQMGUI_SHM,Run2024G_afterCMSALCA293_beforeCMSALCA294_DQMGUI_SHM,Run2024G_afterCMSALCA294_DQMGUI_SHM]
for era in eras: era.fetch(verbose=True)

runs = [dict(e) for e in eras]
runs = {r['label']: r for r in runs}
selectedRuns = [k for k in runs.keys()]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output'  , required=True)
parser.add_argument('--verbose' , action='store_true')
parser.add_argument('--pt-rebin', action='store_true')
args = parser.parse_args()

plotDir     = args.output
verbose     = args.verbose
ptRebinning = args.pt_rebin

ptBins = np.concatenate(( 
    # Between 0.1 and 1 GeV, keep 0.1 GeV binning
    np.arange(0.1 ,1.0, 0.1), 
    # Between 1 and 100 GeV, use nBins = 40 
    # (approx. equally-sized in log space, rounding edges to 0.1 GeV)
    np.around(np.logspace(np.log10(1),np.log10(100), 41),1) 
))

print("\nStarting...")

outDir = plotDir + "/ValidationWRTOffline/"
if not os.path.exists(outDir):
    os.makedirs(outDir)

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

canv = DQMCanvasCMS(lumitext='Run 3 (13.6 TeV)', extratext='Internal')

# Upper and lower pads:
upperPad = ROOT.TPad("upper_pad", "", 0.0, 0.25, 1.0, 1.00)
ratioPad = ROOT.TPad("lower_pad", "", 0.0, 0.00, 1.0, 0.25)

upperPad.SetLeftMargin(0.125);
upperPad.SetRightMargin(0.075);
upperPad.SetTopMargin(0.10);
upperPad.SetBottomMargin(0.04);
upperPad.SetGrid()
upperPad.Draw()

ratioPad.SetLeftMargin(0.125);
ratioPad.SetRightMargin(0.075);
ratioPad.SetTopMargin(0.01);
ratioPad.SetBottomMargin(0.3);
ratioPad.SetGridx()
ratioPad.Draw()

for plot in efficienciesAndFakeRates:
    canv.cd()
    upperPad.Clear()
    ratioPad.Clear()

    if "_pt" in plot:
        upperPad.SetLogx(1)
        ratioPad.SetLogx(1)

    else:
        upperPad.SetLogx(0)
        ratioPad.SetLogx(0)

    upperPad.cd()

    files = {}
    hists = {}

    for r, run in enumerate(selectedRuns):
        if verbose: print("Processing files for " + run)

        # Add numerators and denominators separately
        for i, filename in enumerate(runs[run]['files']):
            if verbose: print(" - " + filename)
            files[filename] = TFile(filename)
            dir = "/DQMData/Run %s/HLT/Run summary/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/"%runs[run]['dirs'][i]

            if i == 0:
                hists['sumNum'] = files[filename].Get(dir+efficienciesAndFakeRates[plot]['num'])
                hists['sumDen'] = files[filename].Get(dir+efficienciesAndFakeRates[plot]['den'])

                hists['sumNum'].Sumw2()
                hists['sumDen'].Sumw2()

            else:
                hists['sumNum'].Add(files[filename].Get(dir+efficienciesAndFakeRates[plot]['num']))
                hists['sumDen'].Add(files[filename].Get(dir+efficienciesAndFakeRates[plot]['den']))

        if verbose: print("Num: " + str(hists['sumNum'].Integral()))
        if verbose: print("Den: " + str(hists['sumDen'].Integral()))

        if ptRebinning and "_pt" in plot:
            newNumHist = TH1F("", "", len(ptBins)-1, ptBins)
            newDenHist = TH1F("", "", len(ptBins)-1, ptBins)

            newNumHist.Sumw2()
            newDenHist.Sumw2()

            for i in range(hists["sumNum"].GetXaxis().GetNbins()):
                newHistBin = newNumHist.GetXaxis().FindBin(hists["sumNum"].GetXaxis().GetBinCenter(i))

                newNumHist.AddBinContent(newHistBin, hists["sumNum"].GetBinContent(i))
                newDenHist.AddBinContent(newHistBin, hists["sumDen"].GetBinContent(i))

                newNumHist.SetBinError(newHistBin, sqrt(newNumHist.GetBinError(newHistBin)**2 + hists["sumNum"].GetBinError(i)**2))
                newDenHist.SetBinError(newHistBin, sqrt(newDenHist.GetBinError(newHistBin)**2 + hists["sumDen"].GetBinError(i)**2))

            hists['sumNum'] = newNumHist
            hists['sumDen'] = newDenHist

        # Compute efficiency (or fake rate)
        hists[plot+"_"+run] = hists['sumNum'].Clone(plot+"_"+run)
        hists[plot+"_"+run].Divide(hists['sumDen'])

        # Set style and draw efficiency (or fake rate)
        hists[plot+"_"+run].SetLineColor(runs[run]['color'])
        hists[plot+"_"+run].SetMarkerColor(runs[run]['color'])
        hists[plot+"_"+run].SetMarkerStyle(runs[run]['marker'])
        hists[plot+"_"+run].SetMarkerSize(1.25)
        if hists[plot+"_"+run].GetMarkerStyle() in [22,23,26,28,32,33,34,46,47,45]:
            hists[plot+"_"+run].SetMarkerSize(1.5)
        if "_pt" in plot:
            hists[plot+"_"+run].GetXaxis().SetRangeUser(0.4,100)
        if r == 0:
            hists[plot+"_"+run].SetTitle(efficienciesAndFakeRates[plot]['title'])
            hists[plot+"_"+run].GetXaxis().SetTitleFont(43)
            hists[plot+"_"+run].GetXaxis().SetTitleSize(30)
            hists[plot+"_"+run].GetXaxis().SetTitleOffset(4)
            hists[plot+"_"+run].GetXaxis().SetLabelFont(43)
            hists[plot+"_"+run].GetXaxis().SetLabelSize(20)

            if "_pt" in plot:
                hists[plot+"_"+run].GetXaxis().SetLabelOffset(-0.01)

            hists[plot+"_"+run].GetYaxis().SetTitleFont(43)
            hists[plot+"_"+run].GetYaxis().SetTitleSize(30)
            hists[plot+"_"+run].GetYaxis().SetTitleOffset(1.5)
            hists[plot+"_"+run].GetYaxis().SetLabelFont(43)
            hists[plot+"_"+run].GetYaxis().SetRangeUser(0,1.)
            hists[plot+"_"+run].GetYaxis().SetLabelSize(20)
            hists[plot+"_"+run].GetYaxis().SetLabelOffset(0.005)
            hists[plot+"_"+run].GetYaxis().SetTickLength(0.03)
            hists[plot+"_"+run].GetYaxis().SetMaxDigits(3)
            hists[plot+"_"+run].GetYaxis().SetNdivisions(505)

            hists[plot+"_"+run].Draw()

        else:
            hists[plot+"_"+run].Draw("same")

            # Compute ratio (first run taken as reference)
            hists[plot+"_"+run+"_ratio"] = hists[plot+"_"+run].Clone(plot+"_"+run+"_ratio")
            hists[plot+"_"+run+"_ratio"].Divide(hists[plot+"_"+selectedRuns[0]])

            # Set style and draw ratio
            if "_pt" in plot:
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetRangeUser(0.4,100)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetLabelOffset(-0.03)

            ratioPad.cd()

            if r == 1:
                hists[plot+"_"+run+"_ratio"].SetTitle(efficienciesAndFakeRates[plot]['title'])

                hists[plot+"_"+run+"_ratio"].GetXaxis().SetTitleFont(43)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetTitleSize(30)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetTitleOffset(0.9)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetLabelFont(43)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetLabelSize(20)
                hists[plot+"_"+run+"_ratio"].GetXaxis().SetTickLength(0.09)
                
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetTitle('Ratio')
                hists[plot+"_"+run+"_ratio"].GetYaxis().CenterTitle()
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetTitleFont(43)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetTitleSize(30)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetTitleOffset(1.55)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetLabelFont(43)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetLabelSize(20)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetLabelOffset(0.005)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetTickLength(0.04)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetMaxDigits(3)
                hists[plot+"_"+run+"_ratio"].GetYaxis().SetNdivisions(505)
                hists[plot+"_"+run+"_ratio"].Draw()

                one = ROOT.TLine(hists[plot+"_"+selectedRuns[0]].GetXaxis().GetXmin(),1.0,hists[plot+"_"+selectedRuns[0]].GetXaxis().GetXmax(),1.0)
                if "_pt" in plot:
                    one.SetX1(ratioPad.GetUxmin())
                one.SetLineColor(1)
                one.SetLineStyle(3)
                one.Draw("same")

            else:
                hists[plot+"_"+run+"_ratio"].Draw("same")

            upperPad.cd()

    # Adjust axis ranges (top plot):
    if 'yRange' in efficienciesAndFakeRates[plot]:
        hists[plot+"_"+selectedRuns[0]].GetYaxis().SetRangeUser(efficienciesAndFakeRates[plot]['yRange'][0], efficienciesAndFakeRates[plot]['yRange'][1])

    else:    
        upperMin = hists[plot+"_"+selectedRuns[0]].GetMinimum()
        upperMax = hists[plot+"_"+selectedRuns[0]].GetMaximum()

        for r, run in enumerate(selectedRuns):
            if r == 0: continue

            if hists[plot+"_"+run].GetMinimum() < upperMin:
                upperMin = hists[plot+"_"+run].GetMinimum()

            if hists[plot+"_"+run].GetMaximum() > upperMax:
                upperMax = hists[plot+"_"+run].GetMaximum()

        hists[plot+"_"+selectedRuns[0]].GetYaxis().SetRangeUser(upperMin-0.05*(upperMax-upperMin), upperMax+0.45*(upperMax-upperMin))

    # Adjust axis ranges (ratio plot):
    if 'rRange' in efficienciesAndFakeRates[plot]:
        hists[plot+"_"+selectedRuns[1]+"_ratio"].GetYaxis().SetRangeUser(efficienciesAndFakeRates[plot]['rRange'][0], efficienciesAndFakeRates[plot]['rRange'][1])

    else: 
        ratioMin = 0.5 if len(selectedRuns)==1 else hists[plot+"_"+selectedRuns[1]+"_ratio"].GetMinimum()
        ratioMax = 1.5 if len(selectedRuns)==1 else hists[plot+"_"+selectedRuns[1]+"_ratio"].GetMaximum()

        for r, run in enumerate(selectedRuns):
            if r < 2: continue

            if hists[plot+"_"+run+"_ratio"].GetMinimum() < ratioMin:
                ratioMin = hists[plot+"_"+run+"_ratio"].GetMinimum()

            if hists[plot+"_"+run+"_ratio"].GetMaximum() > ratioMax:
                ratioMax = hists[plot+"_"+run+"_ratio"].GetMaximum()

        if ratioMax > 2: ratioMax=2

        if len(selectedRuns) > 1:
            hists[plot+"_"+selectedRuns[1]+"_ratio"].GetYaxis().SetRangeUser(ratioMin-0.25*(ratioMax-ratioMin), ratioMax+0.25*(ratioMax-ratioMin))


    upperPad.RedrawAxis()
    ratioPad.RedrawAxis()

    latexCMS = TLatex()
    latexCMS.SetNDC(True)

    # Legend
    leg = TLegend(0.155, 0.7, 0.905, 0.875)
    leg.SetMargin(0.125)
    leg.SetTextFont(43)
    leg.SetTextSize(30)
    leg.SetBorderSize(1)
    if len(selectedRuns) > 3:
        leg.SetNColumns(2)
    for run in selectedRuns:
        leg.AddEntry(plot+"_"+run,runs[run]['label'],"LP")
    leg.Draw()
    canv.Update()

    # Save PDF and PNG files
    canv.Print("%s/%s.pdf"%(outDir,plot))
    canv.Print("%s/%s.png"%(outDir,plot))
    print("")
