#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "CommonFSQFramework/Core/interface/JetSimpleView.h"
#include <cmath>
#include <sstream>
#include <algorithm>
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include <DataFormats/Math/interface/deltaR.h>

JetSimpleView::JetSimpleView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig, tree), m_jecUnc(0)
{
    m_JetsCollection = iConfig.getParameter<edm::InputTag>("input");
    m_JetsPayload = iConfig.getParameter<std::string>("payload");
    m_minPt = iConfig.getParameter<double>("minPt");

    registerVecFloat("pt", tree);
    registerVecFloat("eta", tree);
    registerVecFloat("phi", tree);
    registerVecFloat("rap", tree);
    registerVecFloat("cor", tree);
    registerVecFloat("unc", tree);

    // register consumes
    iC.consumes<pat::JetCollection>(m_JetsCollection);
}


void JetSimpleView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){
    edm::Handle<pat::JetCollection> hJets;
    iEvent.getByLabel(m_JetsCollection, hJets);

    if (m_jecUnc == 0 && hJets->size()>0 ){
       edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;
       iSetup.get<JetCorrectionsRecord>().get(m_JetsPayload,JetCorParColl); 
       JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
       m_jecUnc = new JetCorrectionUncertainty(JetCorPar);
    }

    double pt = 0.;
    double eta = 0.;
    double unc = 0.;

    for (unsigned int i = 0; i<hJets->size(); ++i){
	pt = hJets->at(i).pt();
        if ( pt <  m_minPt) continue;
	eta = hJets->at(i).eta();

        addToFVec("pt", pt);
        addToFVec("eta", eta);
        addToFVec("phi", hJets->at(i).phi());
        addToFVec("rap", hJets->at(i).rapidity());
        addToFVec("cor", hJets->at(i).jecFactor("Uncorrected")); //

        m_jecUnc->setJetPt(pt);
        m_jecUnc->setJetEta(eta);
        unc = m_jecUnc->getUncertainty(true);
        addToFVec("unc", unc);
    }
}
