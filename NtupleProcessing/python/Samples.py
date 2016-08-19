#!/usr/bin/python

import shelve, pickle
import Dataset as DS
import os,sys,subprocess
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
import config.datasets_configuration as dcfg
filename = dcfg.shelve_filename

#
#   Specify the full list of CMSSW Datasets
#
datadatasets = {
    "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015
    ),
    "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015
    ),
    "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-PromptReco-v4/MINIAOD",
        isData=True,
        year=2015
    ),
    "/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015
    ),
    "/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015
    ),
    "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016
    ),
    "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016
    ),
    "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016
    ),
    "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016
    )
}

mcdatasets = {
        #
        #   Signal Datasets
        #
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        isData=False,
        year=2015,
        isSignal=True,
        initial_cmssw = "74X"
    ),
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X"
    ),
    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "74X"
    ),
    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X"
    ),

    #
    #   Background Datasets
    #
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,isData=False,
        isSignal=False,
        initial_cmssw = "74X"
    ),
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X"
    ),
    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="74X"
    ),
    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="76X"
    )
}

#
#   jsons
#
jsonfiles = {
    #   ReReco of 2015
    "2015_ReReco" : DS.JsonFile(
        filename="Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2318.
    ),

    #   Prompt of 2015
    "2015_Prompt" : DS.JsonFile(
        filename="Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2169.
    ),

    #   Prompt of 2016 up to the point where MC/Data Mismatch was not present
    "2016_Prompt_7648" : DS.JsonFile(
        filename="Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt",
        intlumi = 7648.
    ),

    #   Prompt of 2016 - MC/Data Mismatch is present - Trigger inefficiency!???
    "2016_Prompt_12900" : DS.JsonFile(
        filename="Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 12900.
    ),

    #   latest
    "2016_Prompt_16900" : DS.JsonFile(
        filename="Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 16900.
    )
}

#
#   list all the pileup files
#
pileups = {}
for k in jsonfiles.keys():
    jfilename = jsonfiles[k].filename
    for cs in ["68", "69", "70", "71", "72", "71p3"]:
        s = "pileup_%s_%s" % (jfilename[:-4], cs)
        pileups[s] = DS.PileUp(
            cross_section=cs, datajson=jfilename
        )

#
#   Useful functions to build up the name
#
def buildDatasetTagName(ntuple):
    if ntuple.isData:
		return "%s_%s" % (ntuple.label.split(".")[1],ntuple.json[:-4])
    else:
        return "%s_%s" % (ntuple.label.split(".")[0], ntuple.cmssw)

def isReReco(dataset):
	if dataset.year==2015:
		if "16Dec2015" in dataset.name:
			return True
		else:
			return False
	else:
		return False

def discoverNtuples(ntuple):
    prefix = ""
    if ntuple.storage=="EOS":
        prefix+="/eos/cms"
        tstamp = getTimeStamp(ntuple)
        ntuple.timestamp = tstamp
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple), tstamp, "0000")
        x = subprocess.check_output(["eos", "ls %s/*.root" % pathstring]).split("\n")
        return pathstring,x
    else:
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple))
        x = subprocess.check_output(["eos", "ls %s/*.root" % pathstring]).split("\n")
        return pathstring,x

def getFileList(ntuple):
    pass

#
#   
#
datantuples = {}
mcntuples = {}

def initializeForce():
    f = open(filename, "r")
    ds = pickle.load(f)
    f.close()
    ds["DataDatasets"] = datadatasets
    ds["MCDatasets"] = mcdatasets
    ds["jsonfiles"] = jsonfiles
    ds["pileups"] = pileups
    pickle.dump(ds, open(filename, "w"))

def printShelve():
    ds = pickle.load(open(filename, "r"))
    print "Datasets DB @filename=%s" % filename
    for key in ds.keys():
        for k in ds[key]:
            print ds[key][k]

if __name__=="__main__":
	initializeForce()
	printShelve()
