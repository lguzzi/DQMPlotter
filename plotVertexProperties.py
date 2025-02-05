import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

import gc ; gc.disable()

from cls.DQMRatio   import draw_ratio_plot
from eras.Phase2    import *

import sys,os,subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

verbose = args.verbose
#reference = TRIMMING_legacy
#targets = [
#    TRIMMING_0p0,
#    TRIMMING_0p1,
#]
reference = TRIMMING_0p0
targets = [
    TRIMMING_0p1,
    TRIMMING_0p5,
]
from elements.phase2_elements import SIMvertex_properties, pixelVertex_properties, trimmedVertex_properties

plotDir = args.output
for e in SIMvertex_properties:
    draw_ratio_plot(e, reference, targets, args.output+'/SIM')
for e in pixelVertex_properties:
    draw_ratio_plot(e, reference, targets, args.output+'/pixel')
for e in trimmedVertex_properties:
    draw_ratio_plot(e, reference, targets, args.output+'/trimmed')