#include "CommonFSQFramework/Core/interface/EventSimpleView.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

EventSimpleView::EventSimpleView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig, tree)
{

    // register branches
    registerInt("run", tree);
    registerInt("lumi", tree);
    registerInt("event", tree);
    registerInt("nPV", tree);

    m_nPVCol = iConfig.getParameter<edm::InputTag>("vtx_col");

    // register data access
    iC.consumes<std::vector<reco::Vertex>>(m_nPVCol);
}


void EventSimpleView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    // common part
    setI("run", iEvent.eventAuxiliary().run());
    setI("lumi", iEvent.eventAuxiliary().luminosityBlock());
    setI("event", iEvent.eventAuxiliary().event());
    
    // pile-up
    edm::Handle<std::vector<reco::Vertex>> vtx;
    iEvent.getByLabel(m_nPVCol, vtx);
	//all is valid for miniAOD
	//for(unsigned int i = 0; i < vtx->size(); i++){
	//	std::cout << vtx->at(i).isValid() <<"\n"; 
	//}
    setI("nPV", vtx->size());
}
