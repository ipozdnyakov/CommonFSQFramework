import FWCore.ParameterSet.Config as cms

def get(todo):

    defs = {}

    defs["simpleEventInfo"]= cms.PSet(
        miniView = cms.string("EventSimpleView"),
	branchPrefix = cms.untracked.string("event_"),
	vtx_col = cms.InputTag("offlineSlimmedPrimaryVertices"),
    )

    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


