#ifndef Analysis_Core_Meta_DiMuon_h
#define Analysis_Core_Meta_DiMuon_h

/**
 *	file:
 *	Author:
 *	Description:
 */

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace dimuon
	{
		class Meta : public analysis::core::Object
		{
			public:
				Meta() : Object() {}
				virtual ~Meta() {}
	
				virtual void reset()
				{
					_sumEventWeights = 0;
					_isMC = 0;
					_triggerNames.clear();
					_nMuons = 0;
					_checkTrigger = 0;
	
					//	cuts used at ntuple production stage
					_isGlobalMuon = 0;
					_isTrackerMuon = 0;
					_isStandAloneMuon = 0;
					_minPt = 0;
					_maxeta = 0;
					_maxNormChi2 = 0;
					_minMuonHits = 0;
					_minPixelHits = 0;
					_minStripHits = 0;
					_minTrackerHits = 0;
					_minSegmentMatches = 0;
					_minMatchedStations = 0;
					_minPixelLayers = 0;
					_minTrackerLayers = 0;
					_minStripLayers = 0;
					_minValidFractionTracker = 0;
					_maxd0 = 0;
					_maxTrackIsoSumPt = 0;
					_maxRelCombIso = 0;
				}

				int _sumEventWeights;
				bool _isMC;
				std::vector<std::string> _triggerNames;
				uint32_t _nMuons;
				bool _checkTrigger;
	
				//	cuts used at ntuple production stage
				bool _isGlobalMuon;
				bool _isTrackerMuon;
				bool _isStandAloneMuon;
				float _minPt;
				float _maxeta;
				float _maxNormChi2;
				int _minMuonHits;
				int _minPixelHits;
				int _minStripHits;
				int _minTrackerHits;
				int _minSegmentMatches;
				int _minMatchedStations;
				int _minPixelLayers;
				int _minTrackerLayers;
				int _minStripLayers;
				float _minValidFractionTracker;
				float _maxd0;
				float _maxTrackIsoSumPt;
				float _maxRelCombIso;

		};
	}
}

#endif