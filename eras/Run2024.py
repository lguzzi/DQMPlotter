import os, sys ; sys.path.append(os.getcwd())
from cls.era import Era_DQMGUI
Run2024C_DQMGUI_SHM = Era_DQMGUI(label='Run 2024C', dataset='StreamHLTMonitor', year=2024, first=379412, last=380252, color=4, marker=20)
Run2024D_DQMGUI_SHM = Era_DQMGUI(label='Run 2024D', dataset='StreamHLTMonitor', year=2024, first=380253, last=380947, color=5, marker=20)
Run2024E_DQMGUI_SHM = Era_DQMGUI(label='Run 2024E', dataset='StreamHLTMonitor', year=2024, first=380948, last=400000, color=6, marker=20)

Run2024Gv1_DQMGUI_SHM = Era_DQMGUI(label='Run 2024G old data' , dataset='StreamHLTMonitor', year=2024, first=383946, last=385153, color=1, marker=20)
Run2024Gv2_DQMGUI_SHM = Era_DQMGUI(label='Run 2024G new data' , dataset='StreamHLTMonitor', year=2024, first=385154, last=385801, color=2, marker=21)
Run2024H_DQMGUI_SHM   = Era_DQMGUI(label='Run 2024H'          , dataset='StreamHLTMonitor', year=2024, first=385835, last=386070, color=4, marker=34)

# condition updates
Run2024G_beforeCMSALCA293_DQMGUI_SHM                  = Era_DQMGUI(label='Run 2024G before CMSALCA-293', dataset='StreamHLTMonitor', year=2024, first=385154, last=385355, color=4, marker=20)
Run2024G_afterCMSALCA293_beforeCMSALCA294_DQMGUI_SHM  = Era_DQMGUI(label='Run 2024G after CMSALCA-293' , dataset='StreamHLTMonitor', year=2024, first=385356, last=385558, color=5, marker=21)
Run2024G_afterCMSALCA294_DQMGUI_SHM                   = Era_DQMGUI(label='Run 2024G after CMSALCA-294' , dataset='StreamHLTMonitor', year=2024, first=385559, last=385801, color=6, marker=34)

# special runs
Run2024HlowPU_DQMGUI_SHM  = Era_DQMGUI(label='Run 2024H 386071'   , dataset='StreamHLTMonitor', year=2024, first=386071, last=386071, color=8, marker=20)
