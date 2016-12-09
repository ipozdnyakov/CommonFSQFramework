#ifndef EventSimpleView_h
#define EventSimpleView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"

class EventSimpleView: public EventViewBase{
   public:
      EventSimpleView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);
   private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);
      edm::InputTag m_nPVCol;
};
#endif
