#name of the analysis
anaType="decorrelations"

#file with list of samples
dsFile="CommonFSQFramework/Skim/python/ds_data_run2016H.txt"

###################################################################################
# root path needs proper XXX
# some stuff needed for crab configuration, e.g. blacklisting
preamble='''
cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"
'''

# define the util decorator. Functions marked with this wont turn into ds attribute
def util(func):
    setattr(func, "ignore", 1)
    return func
setattr(util, "ignore", 1) # for this function only
###################################################################################

def DS(ds):
    split=ds.split(":") 
    if len(split) == 1: return ds    
    else: return split[1]

def name(ds):
    split1=ds.split(":") 
    if len(split1) > 1:
        split = split1[1].split("/")
    else:
        split = ds.split("/") 
    if len(split) == 0: return None    
    if not isData(ds): return split1[0]
    if isData(ds): return "data_"+split[1]

def isData(ds):
    realData = False
    if "Run2016H" in ds: realData = True
    return realData

def json(ds):
    realData = isData(ds)
    if realData:
        if "Run2016H" in ds: return "CommonFSQFramework/Skim/lumi/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_LowPU.txt"
    else:
        return ""

def crabJobs(ds):
    return 50
    #return int(round(numEvents(ds)/100000.0))


def numEvents(ds):
    #if "%%%" in name(ds): return %%%
    #if nothing found...
    return -1

def GT(ds):
    if isData(ds) and "Run2016" in ds and "Prompt" in ds: return "80X_dataRun2_Prompt_v16"
    if isData(ds) and "Run2016" in ds: return "80X_dataRun2_2016SeptRepro_v7"
    
def XS(ds):
    #Note: all cross sections given in pb -- http://iopscience.iop.org/0295-5075/96/2/21002 --- LHCtotal= 73.5 mili b
    #if real data return nothing, not needed here but keep for other Templates
    realData = isData(ds)
    if realData:
        return -1

    # list all datasets
    # Give all XS in pb
    s = {}
    s["x"] = 0.0 # from DAS - McM


    dsName = name(ds)
    if dsName in s:
        return s[dsName]
    else:
        print "FIXME - XS missing for", dsName
        print '    s["'+dsName+'"] = '
    return -1

@util
def getLumi(ds, trg):
    '''
    all lumi values here should be given in picob
    '''
    
    realData = isData(ds)
    if realData:
        return -1
    
    # for MC just do something very simple for now
    lumi = float(numEvents(ds)/XS(ds)) # pb, Nevents/XS
    return lumi

def lumiMinBias(ds):
    return getLumi(ds,"minbias")


# could useful in the future
@util
def onTheFlyCustomization():
    ret = ""

    return ret
#setattr(onTheFlyCustomization, "ignore", 1)


fun = {}
import copy,types
glob = copy.copy(globals())
for f in glob:
    if type(glob[f])==types.FunctionType:
        if hasattr(glob[f],"ignore"): 
            print "Skip", f
            continue
        #print f
        fun[f]=glob[f]
