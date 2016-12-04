from WMCore.Configuration import Configuration
config = Configuration()

config.section_("User")

config.section_("General")

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'treemaker_DiJets_76.py'

config.section_("Data")

config.section_("Site")
config.Site.storageSite = "T2_RU_ITEP"
