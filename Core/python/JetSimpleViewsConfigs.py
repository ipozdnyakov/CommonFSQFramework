import FWCore.ParameterSet.Config as cms

def get(todo):

    defs = {}

    defs["slimmedJetsPt10"]= cms.PSet(
        miniView = cms.string("JetSimpleView"),
	branchPrefix = cms.untracked.string("slimmedJetsPt10_"),

	#For particular input and payload search:
	#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetAnalysis
	#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
        input = cms.InputTag("slimmedJets"),	
        payload = cms.string("AK4PFchs"),
        minPt = cms.double(10),
    )

    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


