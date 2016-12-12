#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "CommonFSQFramework/Core/interface/JetMCSimpleView.h"
#include <cmath>
#include <sstream>
#include <algorithm>
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include <DataFormats/Math/interface/deltaR.h>

JetMCSimpleView::JetMCSimpleView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
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

    registerVecFloat("gen_pt", tree);
    registerVecFloat("gen_eta", tree);
    registerVecFloat("gen_phi", tree);
    registerVecFloat("gen_rap", tree);


    // register consumes
    iC.consumes<pat::JetCollection>(m_JetsCollection);
}


void JetMCSimpleView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){
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
        addToFVec("cor", hJets->at(i).jecFactor("Uncorrected")); //factor from current level to uncorrected level

        m_jecUnc->setJetPt(pt);
        m_jecUnc->setJetEta(eta);
        unc = m_jecUnc->getUncertainty(true);
        addToFVec("unc", unc);
    }

    // vector<reco::GenJet> "GenJets"  ""  "SIM"          recoGenJets_ak4GenJets__SIM
    edm::Handle<std::vector<reco::GenJet> > hGenJets;
    iEvent.getByLabel(m_JetsCollection, hGenJets);

    for (unsigned int i = 0; i<hGenJets->size(); ++i){
	pt = hGenJets->at(i).pt();
        if ( pt <  m_minPt) continue;
        addToFVec("gen_pt", pt);
        addToFVec("gen_eta", hGenJets->at(i).eta());
        addToFVec("gen_phi", hGenJets->at(i).phi());
        addToFVec("gen_rap", hGenJets->at(i).rapidity());
    }

}
