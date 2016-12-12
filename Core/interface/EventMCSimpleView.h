#ifndef EventMCSimpleView_h
#define EventMCSimpleView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"

class EventMCSimpleView: public EventViewBase{
   public:
      EventMCSimpleView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);
   private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);
};
#endif
