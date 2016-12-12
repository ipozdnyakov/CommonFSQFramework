#include "CommonFSQFramework/Core/interface/EventMCSimpleView.h"

EventMCSimpleView::EventMCSimpleView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig, tree)
{

    // register branches
    registerInt("run", tree);
    registerInt("lumi", tree);
    registerInt("event", tree);
}


void EventMCSimpleView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    // common part
    setI("run", iEvent.eventAuxiliary().run());
    setI("lumi", iEvent.eventAuxiliary().luminosityBlock());
    setI("event", iEvent.eventAuxiliary().event());
    
}
