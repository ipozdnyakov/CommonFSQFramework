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
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	#setenv TMFSampleName data_FSQJets3:
	'/store/data/Run2015C_25ns/FSQJets3/MINIAOD/16Dec2015-v1/50000/002FBD2D-AEAF-E511-BB6D-00261894386F.root'
	#setenv TMFSampleName QCD_Pt-35toInf_TuneCUETP8M1_13TeV-pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1:
	#'/store/mc/RunIIFall15MiniAODv2/QCD_Pt-35toInf_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PU25nsData2015v1_castor_76X_mcRun2_asymptotic_v12-v1/10000/041D8DFF-E727-E611-AE47-0CC47A4C8EEA.root'
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
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.EventMCSimpleViewsConfigs.get(["simpleMCEventInfo"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.JetMCSimpleViewsConfigs.get(["slimmedMCJetsPt10"]))
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["LargeDyTriggerResultsView"]))


process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetTree)
