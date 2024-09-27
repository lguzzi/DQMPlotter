from glob import glob

class Era:
  ''' base class for defining the needed structure
  '''
  def __init__(self, label, dataset, year, first, last, color, marker):
    self.label  = label
    self.dataset= dataset
    self.year   = year
    self.first  = first
    self.last   = last
    self.marker = marker
    self.color  = color  
    self.files, self.dirs, self.link = None,None,None
  
  def __iter__(self):
    ''' used in dict() casting of the class
    '''
    yield 'label' , self.label
    yield 'files' , self.files
    yield 'dirs'  , self.dirs
    yield 'color' , self.color
    yield 'marker', self.marker

class Era_DQMGUI(Era):
  ''' define getters for fetching DQMGUI files from /eos
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.link  = '/eos/cms/store/group/comm_dqm/DQMGUI_data/Run{Y}/{D}/000*xx/*.root'.format(Y=self.year,D=self.dataset)
  
  def fetch(self, verbose=False):
    lastversion = lambda l: sorted(l, key=lambda e: int(e[e.find('DQM_V')+5:e.find('DQM_V')+9]))[-1]
    self.files  = [f for f in glob(self.link) if any(str(r) in f for r in range(self.first, self.last+1))]
    self.files  = [lastversion([f for f in self.files if str(r) in f]) for r in range(self.first, self.last+1) if any(str(r) in f for f in self.files)]
    self.files  = [f for f in self.files if f]
    self.dirs   = [r for r in range(self.first, self.last+1) if any(str(r) in f for f in self.files)]

    print('[INFO] fetched {} files for {}'.format(len(self.files), self.label))
    if verbose:
      print('\n'.join(['\t{}'.format(f) for f in self.files]))
