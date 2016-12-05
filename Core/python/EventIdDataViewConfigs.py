import FWCore.ParameterSet.Config as cms

def get(todo):

    defs = {}

    defs["completeEventIdInfo"]= cms.PSet(
        miniView = cms.string("EventIdData"),
	branchPrefix = cms.untracked.string("completeEventIdInfo_"),
    )

    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


