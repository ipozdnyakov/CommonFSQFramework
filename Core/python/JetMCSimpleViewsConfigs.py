import FWCore.ParameterSet.Config as cms

def get(todo):

    defs = {}

    defs["slimmedMCJetsPt10"]= cms.PSet(
        miniView = cms.string("JetMCSimpleView"),
	branchPrefix = cms.untracked.string("slimmedJetsPt10_"),

	#For particular input and payload search:
	#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetAnalysis
	#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
        input = cms.InputTag("slimmedJets"),	
        input_gen = cms.InputTag("slimmedGenJets"), #ak4 gen jets	
        payload = cms.string("AK4PFchs"),
        minPt = cms.double(10),
    )

    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


