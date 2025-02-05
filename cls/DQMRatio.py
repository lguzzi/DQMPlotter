import ROOT
from cls.DQMCanvas import DQMCanvasCMS
import os

class DQMRatioPlot(ROOT.TH1F):
  ''' class to handle ratio plots cosmetics. 
  We do not use TRatioPlot because it brings more problems than solutions.
  '''
  def __init__(self, numerator, denominator):
    numerator.Sumw2()
    denominator.Sumw2()
    super().__init__(numerator)
    self.Divide(denominator)