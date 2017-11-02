from WMCore.Configuration import Configuration
config = Configuration()

config.section_("User")

config.section_("General")
#config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'treemaker_DiJets_76.py'
#config.JobType.outputFiles = ['trees.root']

config.section_("Data")
#config.Data.outLFNDirBase = '/store/user/%s/'

config.section_("Site")
config.Site.storageSite = "T2_RU_ITEP"
config.General.workArea='decorrelations_mc_pythia8'
config.General.requestName='decorrelations_mc_pythia8_QCD_Pt10to35_FB_13TeV_pythia8_noPU'
config.Data.outputDatasetTag='decorrelations_mc_pythia8_QCD_Pt10to35_FB_13TeV_pythia8_noPU'
config.Data.inputDataset='/QCD_Pt-10to35_fwdJet_bwdJet_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-noPU_castor_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting='EventAwareLumiBased'
config.Data.unitsPerJob=100000
