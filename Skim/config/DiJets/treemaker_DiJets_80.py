import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

isData = False

if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on MC"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: print "Disabling MC-specific features for sample", s

##########################
##STANDARD CMSSW ELEMENTS#
##########################
process = cms.Process("Treemaker")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	#setenv TMFSampleName data_FSQJets:
	'/store/data/Run2016H/FSQJets/MINIAOD/03Feb2017_ver2-v1/110000/0A66D932-80ED-E611-B3B0-0025905B85C0.root'
	#setenv TMFSampleName data_ZeroBias:
	#'/store/data/Run2016H/ZeroBias/MINIAOD/03Feb2017_ver3-v1/100000/0A44B237-58EB-E611-AF46-002590E7E07A.root'
	#setenv TMFSampleName data_L1MinimumBias0:
	#'/store/data/Run2016H/L1MinimumBias0/MINIAOD/PromptReco-v3/000/284/068/00000/08FD41EC-6C9F-E611-8AA8-02163E012713.root'
    )
)

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.load("Configuration.StandardSequences.MagneticField_cff")

###############
##CFF ELEMENTS#
###############
import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

process.JetTree = cms.EDAnalyzer("CFFTreeProducer")

import CommonFSQFramework.Core.EventSimpleViewsConfigs
import CommonFSQFramework.Core.JetSimpleViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs

import CommonFSQFramework.Core.EventMCSimpleViewsConfigs
import CommonFSQFramework.Core.JetMCSimpleViewsConfigs

if isData:
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.EventSimpleViewsConfigs.get(["simpleEventInfo"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.JetSimpleViewsConfigs.get(["slimmedJetsPt10"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["LargeDyTriggerResultsView"]))
else:
#	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.EventMCSimpleViewsConfigs.get(["simpleMCEventInfo"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.EventSimpleViewsConfigs.get(["simpleEventInfo"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.JetMCSimpleViewsConfigs.get(["slimmedMCJetsPt10"]))

process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetTree)