from WMCore.Configuration import Configuration
config = Configuration()

config.section_("User")

config.section_("General")
#config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'treemaker_DiJets_80.py'
#config.JobType.outputFiles = ['trees.root']

config.section_("Data")
#config.Data.outLFNDirBase = '/store/user/%s/'

config.section_("Site")
config.Site.storageSite = "T2_RU_ITEP"
