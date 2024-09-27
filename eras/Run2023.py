import os, sys ; sys.path.append(os.getcwd())
from cls.era import Era_DQMGUI
Run2023B_DQMGUI_SHM = Era_DQMGUI(label='Run 2023B', dataset='StreamHLTMonitor', year=2023, first=366365, last=367079, color=1, marker=20)
Run2023C_DQMGUI_SHM = Era_DQMGUI(label='Run 2023C', dataset='StreamHLTMonitor', year=2023, first=367080, last=369802, color=2, marker=20)
Run2023D_DQMGUI_SHM = Era_DQMGUI(label='Run 2023D', dataset='StreamHLTMonitor', year=2023, first=369803, last=372415, color=3, marker=20)