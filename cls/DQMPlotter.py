# TODO a class is not needed here
class DQMPlotter1D:
  ''' main worker class for handling comparisons of a single observable.
  '''
  def __init__(self, reference, targets, plot):
    self.canvas = DQMCanvasCMS()
    self.ratios = [DQMRatio(self.reference.Get(plot), target.Get(plot)) 
      for target in targets]

    for ii, rat in enumerate(self.ratios[1:]):
      tar = DQMHisto(rat.GetUpperPad().GetListOfPrimitives()[2])
      rat = DQMHisto(rat.GetLowerPad().GetListOfPrimitives()[1])
      rat.SetName(tar.GetName()+'_ratio')
      
      self.ratios[0].GetUpperPad().cd()
      tar.Draw('PE')
      self.ratios[0].GetLowerPad().cd()
      rat.Draw('PE')

    self.ratios[0].Draw()
    self.canvas.Modified()
    self.canvas.Update()
