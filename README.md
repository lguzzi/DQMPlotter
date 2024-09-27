*work in progress*

plot DQM files. The code will try to drive away from a single-script approach to a class-based approach, but this is a work in progress.

Data is fetched from /eos DQM directories, using only the last version of a file. File fetching is handled by the [Era class](cls/era.py), configuration files are pre-defined in the [eras](eras) folder.
In the actual plotting script, the ```fetch``` method of the Era instance is called to look for the needed files.

For the moment, plotting by the three scripts

- plotEfficiencies.py
- plotTrackProperties.py
- plotVertexProperties.py

for example:

```bash
python3 plotEfficiencies.py --pt-rebin --output out_directory
```

having defined correctly the needed era inside the file.  
Canvas cosmetics is (partially) handled by a [DQMCAnvas](cls/DQMCanvas.py) instance. Other classes inside cls are a work in progress and are not used at the moment.
