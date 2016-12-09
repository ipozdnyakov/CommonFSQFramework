#ifndef JetSimpleView_h
#define JetSimpleView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class JetSimpleView: public EventViewBase{
    public:
      JetSimpleView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);

    private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);

      edm::InputTag	m_JetsCollection;
      std::string	m_JetsPayload;
      float		m_minPt;

      JetCorrectionUncertainty  * m_jecUnc;
};
#endif
