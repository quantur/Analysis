#ifndef Analysis_Core_Event_h
#define Analysis_Core_Event_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class Event : public Object
		{
			public:
				Event() : Object() {}

				virtual void reset()
				{
					_run = 0;
					_lumi = 0;
					_event = 0;
					_bx = 0;
					_orbit = 0;
				}
				virtual ~Event() {}

				int _run;
				int _lumi;
				long long int _event;
				int _bx;
				int _orbit;
		};

		typedef std::vector<analysis::core::Event> Events;
	}
}

#endif
