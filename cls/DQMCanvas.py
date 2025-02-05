import ROOT
import sys ; sys.path.append('.')
from cls.DQMLatex import DQMLatex

class DQMCanvas (ROOT.TCanvas):
  ROOT.gStyle.SetOptStat(0)
  ''' class for handling the TCanvas style
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.SetGridx()
    self.SetGridy()
    self.SetBottomMargin(0.1)

class DQMCanvasCMS(DQMCanvas):
  ''' apply default CMS cosmetics to the canvas
  '''
  def __init__(self, **kwargs):
    super().__init__(kwargs.get('name', 'c1'),'',800,800)
    self.SetTopMargin(0.10)
    self.SetLeftMargin(0.05)
    self.SetRightMargin(0.05)

    self.cmstext = DQMLatex(self.GetRightMargin(), 1-0.9*self.GetTopMargin(), 'CMS ')
    self.cmstext.SetNDC()
    self.cmstext.SetTextFont(63)
    self.cmstext.SetTextSize(0.7*self.GetTopMargin())
    self.cmstext.SetTextAlign(11)
    self.extratext = DQMLatex(self.GetRightMargin()+self.cmstext.GetXsize(), 1-0.9*self.GetTopMargin(), kwargs.get('extratext', ''))
    self.extratext.SetNDC()
    self.extratext.SetTextFont(53)
    self.extratext.SetTextSize(0.7*self.GetTopMargin()*0.75)
    self.extratext.SetTextAlign(11)
    self.lumitext = DQMLatex(1-self.GetRightMargin(), 1-0.9*self.GetTopMargin(), kwargs.get('lumitext' , ''))
    self.lumitext.SetNDC()
    self.lumitext.SetTextFont(43)
    self.lumitext.SetTextSize(0.7*self.GetTopMargin()*0.75)
    self.lumitext.SetTextAlign(31)

  def SaveAs(self, *args, **kwargs):
    ''' this is needed for cosmetics to appear
    '''
    self.cmstext  .Draw()
    self.extratext.Draw()
    self.lumitext .Draw()
    super().SaveAs(*args, **kwargs)

  def Print(self, *args, **kwargs):
    ''' this is needed for cosmetics to appear
    '''
    self.cmstext  .Draw()
    self.extratext.Draw()
    self.lumitext .Draw()
    super().Print(*args, **kwargs)

class DQMRatioCanvasCMS(DQMCanvasCMS):
  UP_BOTTOM_RATIO = 0.3
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.Divide(1,2)
    self.GetPad(1).SetPad(0, DQMRatioCanvasCMS.UP_BOTTOM_RATIO, 1, 1)
    self.GetPad(2).SetPad(0, 0, 1, DQMRatioCanvasCMS.UP_BOTTOM_RATIO)
    self.GetPad(1).SetBottomMargin(0)
    self.GetPad(2).SetTopMargin(0)
    self.GetPad(2).SetBottomMargin(0.3)

if __name__ == '__main__':
  can = DQMRatioCanvasCMS()
  can.cd(1)
  h = ROOT.TH1F('h', 'h', 100, -5, 5)
  h.FillRandom('gaus', 1000)
  h.Draw()
  can.cd(2)
  h.Draw()
  can.SaveAs('test.pdf')
  can.Print('test.png')
  import pdb; pdb.set_trace()