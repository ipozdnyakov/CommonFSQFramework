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
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'/store/data/Run2015C_25ns/FSQJets3/MINIAOD/16Dec2015-v1/50000/002FBD2D-AEAF-E511-BB6D-00261894386F.root'
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

import CommonFSQFramework.Core.JetViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs

process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["slimmedJetsPt10"]))

if isData:
	process.JetTree._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["HLT_DiPFJet15_NoCaloMatched_v*","HLT_DiPFJet15_FBEta2_NoCaloMatched_v*"]))

process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetTree)
