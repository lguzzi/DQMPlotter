import ROOT
from ROOT import *
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

from cls.DQMCanvas      import DQMCanvasCMS
from vertexProperties   import *
from eras.Run2024       import *

import sys,os,subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

verbose = args.verbose
eras = [
    Run2024Gv1_DQMGUI_SHM,
    Run2024Gv2_DQMGUI_SHM,
    Run2024H_DQMGUI_SHM,
]

for era in eras: era.fetch(verbose=True)
runs = [dict(e) for e in eras]
runs = {r['label']: r for r in runs}
selectedRuns = [k for k in runs.keys()]

plotDir = args.output

collections  = ["hltPixelVertices", "hltTrimmedPixelVertices", "hltVerticesPFFilter"]
canv = DQMCanvasCMS(lumitext='Run 3 (13.6 TeV)', extratext='Internal')

print("\nStarting...")

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(11111)

# Upper and lower pads:
upperPad = ROOT.TPad("upper_pad", "", 0.0, 0.25, 1.0, 1.00);
ratioPad = ROOT.TPad("lower_pad", "", 0.0, 0.00, 1.0, 0.25);

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
for col in collections:
    outDir = plotDir+"/%s/"%col
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for plot in vertexProperties + {"hltPixelVertices":hltPixelVertices, "hltTrimmedPixelVertices":hltTrimmedPixelVertices, "hltVerticesPFFilter":hltVerticesPFFilter}.get(col, []):
        subDir = plotDir+"/%s/%s/"%(col,plot[:plot.find("/")])
        if not os.path.exists(subDir):
            os.makedirs(subDir)        
        canv.cd()
        upperPad.Clear()
        ratioPad.Clear()

        upperPad.cd()

        files = {}
        hists = {}

        for r, run in enumerate(selectedRuns):
            if verbose: print("Processing files for " + run)

            # Add histograms from input files
            for i, filename in enumerate(runs[run]['files']):
                if verbose: print(" - " + filename)
                files[filename] = TFile(filename)
                dir = "/DQMData/Run %s/HLT/Run summary/Vertexing/%s/"%(runs[run]['dirs'][i],col)

                if i == 0:
                    hists[plot+"_"+run] = files[filename].Get(dir+plot)
                    try:
                        hists[plot+"_"+run].SetName(plot+"_"+run)
                    except:
                        assert False, "missing "+plot
                    hists[plot+"_"+run].Sumw2()

                else:
                    hists[plot+"_"+run].Add(files[filename].Get(dir+plot))

            hists[plot+"_"+run].ClearUnderflowAndOverflow()
            hists[plot+"_"+run].GetXaxis().SetTitle(plot)
            if hists[plot+"_"+run].Integral():
                hists[plot+"_"+run].Scale(1.0/hists[plot+"_"+run].Integral())
            hists[plot+"_"+run].SetLineColor(runs[run]['color'])
            hists[plot+"_"+run].SetMarkerColor(runs[run]['color'])
            hists[plot+"_"+run].SetMarkerStyle(runs[run]['marker'])
            hists[plot+"_"+run].SetMarkerSize(1.25)
            if hists[plot+"_"+run].GetMarkerStyle() in [22,23,26,28,32,33,34,46,47,45]:
                hists[plot+"_"+run].SetMarkerSize(1.5)
            label = hists[plot+"_"+run].GetYaxis().GetTitle()
            if "Number of Tracks" in label or "Number of Events" in label or "Number of events" in label:
                if verbose: print("Integral 0, -1:             " + str(hists[plot+"_"+run].Integral(0,-1)))
                if verbose: print("Integral:                   " + str(hists[plot+"_"+run].Integral()))
                if verbose: print("Underflow:                  " + str(hists[plot+"_"+run].GetBinContent(0)))
                if verbose: print("Overflow:                   " + str(hists[plot+"_"+run].GetBinContent(hists[plot+"_"+run].GetNbinsX()+1)))
                if verbose: print("Integral w/ over+underflow: " + str(hists[plot+"_"+run].Integral(0,hists[plot+"_"+run].GetNbinsX()+1)))
                hists[plot+"_"+run].Scale(1.0/hists[plot+"_"+run].Integral())
                hists[plot+"_"+run].GetYaxis().SetTitle("a.u. (normalized)")
            if col == "tracks" and "NumberOfTracks" in plot:
                hists[plot+"_"+run].GetXaxis().SetRangeUser(0,1500)
            elif col == "tracks" and "NumberEventsVsLUMI" in plot:
                hists[plot+"_"+run].GetXaxis().SetRangeUser(0,25000)
            elif "GoodPVtx" in plot:
                hists[plot+"_"+run].GetXaxis().SetRangeUser(0,65)
                hists[plot+"_"+run].GetXaxis().SetTitle("Number of pixel vertices")                
            elif "NumberEventsVsLUMI" in plot:
                hists[plot+"_"+run].GetXaxis().SetTitle("Online lumi [1e30 Hz cm^{-2}]")   
            if r == 0:
                hists[plot+"_"+run].GetXaxis().SetTitleFont(43)
                hists[plot+"_"+run].GetXaxis().SetTitleSize(30)
                hists[plot+"_"+run].GetXaxis().SetTitleOffset(3.2)

                hists[plot+"_"+run].GetYaxis().SetTitleFont(43)
                hists[plot+"_"+run].GetYaxis().SetTitleSize(30)
                hists[plot+"_"+run].GetYaxis().SetTitleOffset(1.5)
                hists[plot+"_"+run].GetYaxis().SetLabelFont(43)
                hists[plot+"_"+run].GetYaxis().SetLabelSize(20)
                hists[plot+"_"+run].GetYaxis().SetLabelOffset(0.005)
                hists[plot+"_"+run].GetYaxis().SetTickLength(0.03)
                hists[plot+"_"+run].GetYaxis().SetMaxDigits(5)
                hists[plot+"_"+run].Draw()
            else:
                hists[plot+"_"+run].Draw("same")

                # Ratio plots
                if hists[plot+"_"+run].ClassName() == "TProfile":
                    if r == 1:
                        hists[plot+"_"+selectedRuns[0]+"_ratio"] = hists[plot+"_"+selectedRuns[0]].ProjectionX(plot+"_"+selectedRuns[0]+"_ratio")
                    hists[plot+"_"+run+"_ratio"] = hists[plot+"_"+run].ProjectionX(plot+"_"+run+"_ratio")
                    hists[plot+"_"+run+"_ratio"].Divide(hists[plot+"_"+selectedRuns[0]+"_ratio"])
                    hists[plot+"_"+run+"_ratio"].SetLineColor(hists[plot+"_"+run].GetLineColor())
                    hists[plot+"_"+run+"_ratio"].SetMarkerColor(hists[plot+"_"+run].GetMarkerColor())
                    hists[plot+"_"+run+"_ratio"].SetMarkerStyle(hists[plot+"_"+run].GetMarkerStyle())
                    hists[plot+"_"+run+"_ratio"].SetMarkerSize(hists[plot+"_"+run].GetMarkerSize())

                else:
                    hists[plot+"_"+run+"_ratio"] = hists[plot+"_"+run].Clone(plot+"_"+run+"_ratio")
                    hists[plot+"_"+run+"_ratio"].Divide(hists[plot+"_"+selectedRuns[0]])

                ratioPad.cd()

                if r == 1:
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
                    hists[plot+"_"+run+"_ratio"].GetYaxis().SetMaxDigits(5)
                    hists[plot+"_"+run+"_ratio"].GetYaxis().SetNdivisions(505)
                    hists[plot+"_"+run+"_ratio"].Draw()

                    one = ROOT.TLine(hists[plot+"_"+selectedRuns[0]].GetXaxis().GetXmin(),1.0,hists[plot+"_"+selectedRuns[0]].GetXaxis().GetXmax(),1.0)
                    if "GoodPVtx" in plot:
                        ratioPad.Update()
                        one.SetX2(upperPad.GetUxmax())
                    one.SetLineColor(1)
                    one.SetLineStyle(3)
                    one.Draw("same")

                else:
                    hists[plot+"_"+run+"_ratio"].Draw("same")

                upperPad.cd()
            print(plot+"_"+run, hists[plot+"_"+run].GetMean(), hists[plot+"_"+run].GetRMS())

        # Adjust y axis:
        upperMin = hists[plot+"_"+selectedRuns[0]].GetMinimum()
        upperMax = hists[plot+"_"+selectedRuns[0]].GetMaximum()

        ratioMin = hists[plot+"_"+selectedRuns[1]+"_ratio"].GetMinimum()
        ratioMax = hists[plot+"_"+selectedRuns[1]+"_ratio"].GetMaximum()

        for r, run in enumerate(selectedRuns):
            if r == 0: continue

            if hists[plot+"_"+run].GetMinimum() < upperMin:
                upperMin = hists[plot+"_"+run].GetMinimum()

            if hists[plot+"_"+run].GetMaximum() > upperMax:
                upperMax = hists[plot+"_"+run].GetMaximum()

            if r == 1: continue

            if hists[plot+"_"+run+"_ratio"].GetMinimum() < ratioMin:
                ratioMin = hists[plot+"_"+run+"_ratio"].GetMinimum()

            if hists[plot+"_"+run+"_ratio"].GetMaximum() > ratioMax:
                ratioMax = hists[plot+"_"+run+"_ratio"].GetMaximum()

        if ratioMax < 1: ratioMax = 1
        if ratioMin > 1: ratioMin = 1

        hists[plot+"_"+selectedRuns[0]].GetYaxis().SetRangeUser(upperMin-0.05*(upperMax-upperMin), upperMax+0.45*(upperMax-upperMin))
        #hists[plot+"_"+selectedRuns[1]+"_ratio"].GetYaxis().SetRangeUser(ratioMin-0.25*(ratioMax-ratioMin), ratioMax+0.25*(ratioMax-ratioMin))
        yMin = ratioMin-0.25*(ratioMax-ratioMin) if ratioMin > 0 else 0
        yMax = ratioMax+0.25*(ratioMax-ratioMin) if ratioMax < 5 else 5
        hists[plot+"_"+selectedRuns[1]+"_ratio"].GetYaxis().SetRangeUser(yMin,yMax)

        upperPad.RedrawAxis()
        ratioPad.RedrawAxis()

        latexCMS = TLatex()
        latexCMS.SetNDC(True)

        # COM energy
        latexCMS.SetTextFont(43)
        latexCMS.SetTextAlign(31)
        latexCMS.SetTextSize(30)
        latexCMS.DrawLatex(0.925, 0.915, "Run 3 (13.6 TeV)")

        # CMS
        latexCMS.SetTextFont(63)
        latexCMS.SetTextAlign(11)
        latexCMS.SetTextSize(40)
        latexCMS.DrawLatex(0.125,0.915,"CMS")

        # Preliminary
        latexCMS.SetTextFont(53)
        latexCMS.SetTextSize(30)
        latexCMS.DrawLatex(0.24,0.915,"Preliminary")

        leg = TLegend(0.155, 0.7, 0.905, 0.875)
        leg.SetMargin(0.125)
        leg.SetTextFont(43)
        leg.SetTextSize(20)
        leg.SetBorderSize(1)
        if len(selectedRuns) > 3:
            leg.SetNColumns(2)
        for run in selectedRuns:
            leg.AddEntry(plot+"_"+run,runs[run]['label'],"LP")
        leg.Draw()

        if "DistanceOfClosestApproachToPVVsPhi" in plot or "NumberEventsVsLUMI" in plot:
            ratioPad.Clear()
            latexCMS.SetTextFont(43)
            latexCMS.SetTextAlign(33)
            latexCMS.SetTextSize(30)
            if "DistanceOfClosestApproachToPVVsPhi" in plot:
                latexCMS.DrawLatex(0.925,0.99,hists[plot+"_"+selectedRuns[1]+"_ratio"].GetXaxis().GetTitle())
            elif "NumberEventsVsLUMI" in plot:
                latexCMS.DrawLatex(0.925,0.99,"Online lumi [1e30 Hz cm^{-2}]")

        canv.Update()

        # Save PDF and PNG files

        canv.Print("%s/%s.pdf"%(outDir,plot))
        canv.Print("%s/%s.png"%(outDir,plot))
        print("")
