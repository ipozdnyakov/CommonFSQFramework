import FWCore.ParameterSet.Config as cms

def get(todo):

    defs = {}

    defs["simpleMCEventInfo"]= cms.PSet(
        miniView = cms.string("EventMCSimpleView"),
	branchPrefix = cms.untracked.string("event_"),
    )

    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


