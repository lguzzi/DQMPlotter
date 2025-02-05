import ROOT
from glob import glob
from copy import deepcopy

class Era:
  ''' base class for defining the needed structure
  '''
  def __init__(self, label, color, marker, dataset=None, year=None, first=None, last=None):
    self.label  = label
    self.dataset= dataset
    self.year   = year
    self.first  = first
    self.last   = last
    self.marker = marker
    self.color  = color 
  
  def __iter__(self):
    ''' used in dict() casting of the class
    '''
    yield 'label'     , self.label
    yield 'files'     , self.files
    yield 'dirs'      , self.dirs
    yield 'color'     , self.color
    yield 'marker'    , self.marker
  
  def clone(self, newlabel):
    newone = deepcopy(self)
    newone.label = newlabel
    return newone
  
  def get(self, element, normalise=False):
    ''' return the requested element from all the files
    '''
    histos = [f.Get(element) for f in self.files]
    histos = [h.Clone(h.GetName()+self.label) for h in histos if h]
    if not histos: return
    for i,h in enumerate(histos):
      h.SetLineColor(self.color)
      h.SetMarkerColor(self.color)
      h.SetMarkerStyle(self.marker)
      if not i: continue
      histos[0].Add(h)
    if normalise and histos[0].Integral():
      histos[0].Scale(1./histos[0].Integral())
    return histos[0]

class Era_DQMGUI(Era):
  ''' define getters for fetching DQMGUI files from /eos
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.path  = '/eos/cms/store/group/comm_dqm/DQMGUI_data/Run{Y}/{D}/000*xx/*.root'.format(Y=self.year,D=self.dataset)
  
    lastversion = lambda l: sorted(l, key=lambda e: int(e[e.find('DQM_V')+5:e.find('DQM_V')+9]))[-1]
    self.files  = [f for f in glob(self.path) if any(str(r) in f for r in range(self.first, self.last+1))]
    self.files  = [lastversion([f for f in self.files if str(r) in f]) for r in range(self.first, self.last+1) if any(str(r) in f for f in self.files)]
    self.files  = [f for f in self.files if f]
    self.dirs   = [r for r in range(self.first, self.last+1) if any(str(r) in f for f in self.files)]
    print('[INFO] fetched {} files for {}'.format(len(self.files), self.label))

class Era_custom(Era):
  ''' class for handling user-defined file lists
  '''
  def __init__(self, files, runs, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.files = files
    self.dirs  = runs