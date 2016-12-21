#ifndef JetMCSimpleView_h
#define JetMCSimpleView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class JetMCSimpleView: public EventViewBase{
    public:
      JetMCSimpleView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);

    private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);

      edm::InputTag	m_JetsCollection;
      edm::InputTag	m_GenJetsCollection;
      std::string	m_JetsPayload;
      float		m_minPt;

      JetCorrectionUncertainty  * m_jecUnc;
};
#endif
