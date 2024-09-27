import ROOT
class DQMRatio(ROOT.TRatioPlot):
  COLORS = [i+1 for i in range range(100)]
  ''' custom class to handle ratio plots.
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.SetSeparationMargin(0.0)
    self.SetSplitFraction(0.2)
  
  def Draw(self, *args, **kwargs):
    ''' apply cosmetics before drawing.
    '''
    for hist in self.GetUpperPad().GetListOfPrimitives():
      tar.SetLineColor(DQMPlotter1D.COLORS[ii])
      tar.SetMarkerColor(DQMPlotter1D.COLORS[ii])
    super().Draw(*args, **kwargs)
