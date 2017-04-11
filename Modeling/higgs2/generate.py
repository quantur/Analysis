"""
"""
import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

import categories
from generatingFunctions import *
from common import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int, default=0, help="number identifies the function to run")
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
args = parser.parse_args()

if args.mode == "Iowa":
    import Configuration.higgs.Iowa_settings as settings
    from Configuration.higgs.Iowa_settings import *
    from categories import *
elif args.mode == "UF_AWB":
    import Configuration.higgs.UF_AWB_settings as settings
    from Configuration.higgs.UF_AWB_settings import *
    from categories_UF_AWB import *
elif args.mode == "UF_AMC":
    import Configuration.higgs.UF_AMC_settings as settings
    from Configuration.higgs.UF_AMC_settings import *
    from categories_UF_AMC import *

def generate_backgroundFits():
    for category in categoriesToUse:
        for modelGroup in backgroundModelGroups:
            ws = R.RooWorkspace("higgs")
            aux.buildMassVariable(ws, **diMuonMass125)
            modelsToUse = modelGroup.models
            counter = 0;
            for m in modelsToUse:
                m.color = colors[counter]
                counter+=1
            backgroundFits((category, diMuonMass125), ws, data, modelsToUse,
                settings,
                pathToDir=backgroundfitsDir,groupName=modelGroup.name)

def generate_datacardsTripleGaus():
    modelGroupToUse = modelGroupForMultiPdf
    workspaceName = "higgs"
    for category in categoriesToUse:
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = tripleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        
        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)
        hdata = fdata.Get(category + "/" + "DiMuonMass")
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Triple Gaus Splines"
        print "*"*80
        vbfmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, tripleGaus120, diMuonMass120),
                (vbf125, tripleGaus125, diMuonMass125),
                (vbf130, tripleGaus130, diMuonMass130),
            ], 
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        glumodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, tripleGaus120, diMuonMass120),
                (glu125, tripleGaus125, diMuonMass125),
                (glu130, tripleGaus130, diMuonMass130),
            ],
            settings, 
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wpmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, tripleGaus120, diMuonMass120),
                (wp125, tripleGaus125, diMuonMass125),
                (wp130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wmmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, tripleGaus120, diMuonMass120),
                (wm125, tripleGaus125, diMuonMass125),
                (wm130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        zhmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, tripleGaus120, diMuonMass120),
                (zh125, tripleGaus125, diMuonMass125),
                (zh130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )

        #
        # Create the Background Model
        #
        counter = 0
        for model in modelGroupToUse.models:
            model.color = colors[counter]
            counter += 1
        backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            modelGroupToUse.models, settings, pathToDir=backgroundfitswithroomultipdfDir,
            groupName=modelGroupToUse.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsworkspacesDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        ws.SaveAs(os.path.join(datacardsworkspacesDir, workspaceFileName))

def generate_datacardsDoubleGaus():
    modelGroupToUse = modelGroupForMultiPdf
    workspaceName = "higgs"
    for category in categoriesToUse:
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = doubleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        
        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)
        hdata = fdata.Get(category + "/" + "DiMuonMass")
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Double Gaus Splines"
        print "*"*80
        vbfmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, doubleGaus120, diMuonMass120),
                (vbf125, doubleGaus125, diMuonMass125),
                (vbf130, doubleGaus130, diMuonMass130),
            ],
            settings, 
            pathToDir=signalfitinterpolationswithsplineDir
        )
        glumodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, doubleGaus120, diMuonMass120),
                (glu125, doubleGaus125, diMuonMass125),
                (glu130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wpmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, doubleGaus120, diMuonMass120),
                (wp125, doubleGaus125, diMuonMass125),
                (wp130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wmmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, doubleGaus120, diMuonMass120),
                (wm125, doubleGaus125, diMuonMass125),
                (wm130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        zhmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, doubleGaus120, diMuonMass120),
                (zh125, doubleGaus125, diMuonMass125),
                (zh130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )

        #
        # Create the Background Model
        #
        counter = 0
        for model in modelGroupToUse.models:
            model.color = colors[counter]
            counter += 1
        backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            modelGroupToUse.models, settings, pathToDir=backgroundfitswithroomultipdfDir,
            groupName=modelGroupToUse.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsworkspacesDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        ws.SaveAs(os.path.join(datacardsworkspacesDir, workspaceFileName))

def generate_datacardsSingleGaus():
    modelGroupToUse = modelGroupTest
    workspaceName = "higgs"
    for category in categoriesToUse:
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = singleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)

        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)
        hdata = fdata.Get(category + "/" + "DiMuonMass")
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Single Gaus Splines"
        print "*"*80
        vbfmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        glumodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, singleGaus120, diMuonMass120),
                (glu125, singleGaus125, diMuonMass125),
                (glu130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wpmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, singleGaus120, diMuonMass120),
                (wp125, singleGaus125, diMuonMass125),
                (wp130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        wmmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, singleGaus120, diMuonMass120),
                (wm125, singleGaus125, diMuonMass125),
                (wm130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        zhmodel = signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, singleGaus120, diMuonMass120),
                (zh125, singleGaus125, diMuonMass125),
                (zh130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )

        #
        # Create the Background Model
        #
        counter = 0
        for model in modelGroupToUse.models:
            model.color = colors[counter]
            counter += 1
        backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            modelGroupToUse.models, settings,
            pathToDir=backgroundfitswithroomultipdfDir,
            groupName=modelGroupToUse.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsworkspacesDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        print "*"*80
        print "*** Final RooWorkspace contents ***"
        print "*"*80
        ws.Print("v")
        ws.SaveAs(os.path.join(datacardsworkspacesDir, workspaceFileName))

def generate_backgroundsWithRooMultiPdf():
    modelGroupToUse = modelGroupForMultiPdf
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        counter = 0;
        for model in modelGroupToUse.models:
            model.color = colors[counter]
            counter += 1
        backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            modelGroupToUse.models, settings, pathToDir=backgroundfitswithroomultipdfDir,
            groupName=modelGroupToUse.name)

def generate_signalFitInterpolations():
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        signalFitInterpolation(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=singalfitinterpolationsDir
        )

def generate_signalFitInterpolationsWithSpline():
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        print "*"*80
        print "Generating Single Gaus Splines"
        print "*"*80
        signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, singleGaus120, diMuonMass120),
                (glu125, singleGaus125, diMuonMass125),
                (glu130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, singleGaus120, diMuonMass120),
                (wp125, singleGaus125, diMuonMass125),
                (wp130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, singleGaus120, diMuonMass120),
                (wm125, singleGaus125, diMuonMass125),
                (wm130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, singleGaus120, diMuonMass120),
                (zh125, singleGaus125, diMuonMass125),
                (zh130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        print "*"*80
        print "Generating Double Gaus Splines"
        print "*"*80
        signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, doubleGaus120, diMuonMass120),
                (vbf125, doubleGaus125, diMuonMass125),
                (vbf130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, doubleGaus120, diMuonMass120),
                (glu125, doubleGaus125, diMuonMass125),
                (glu130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, doubleGaus120, diMuonMass120),
                (wp125, doubleGaus125, diMuonMass125),
                (wp130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, doubleGaus120, diMuonMass120),
                (wm125, doubleGaus125, diMuonMass125),
                (wm130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, doubleGaus120, diMuonMass120),
                (zh125, doubleGaus125, diMuonMass125),
                (zh130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        print "*"*80
        print "Generating Triple Gaus Splines"
        print "*"*80
        signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, tripleGaus120, diMuonMass120),
                (vbf125, tripleGaus125, diMuonMass125),
                (vbf130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, tripleGaus120, diMuonMass120),
                (glu125, tripleGaus125, diMuonMass125),
                (glu130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, tripleGaus120, diMuonMass120),
                (wp125, tripleGaus125, diMuonMass125),
                (wp130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, tripleGaus120, diMuonMass120),
                (wm125, tripleGaus125, diMuonMass125),
                (wm130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )
        signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, tripleGaus120, diMuonMass120),
                (zh125, tripleGaus125, diMuonMass125),
                (zh130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalfitinterpolationswithsplineDir
        )

def generate_signalFits():
    initialValuesFromTH1 = True
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        for modelToUse in [singleGaus125, doubleGaus125, tripleGaus125]:
            modelToUse.color = R.kRed
            signalFit((category, diMuonMass125), ws, vbf125, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass125), ws, glu125, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass125), ws, wm125, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass125), ws, wp125, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass125), ws, zh125, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
        aux.buildMassVariable(ws, **diMuonMass120)
        for modelToUse in [singleGaus120, doubleGaus120, tripleGaus120]:
            modelToUse.color = R.kRed
            signalFit((category, diMuonMass120), ws, vbf120, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass120), ws, glu120, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass120), ws, wm120, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass120), ws, wp120, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass120), ws, zh120, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
        aux.buildMassVariable(ws, **diMuonMass130)
        for modelToUse in [singleGaus130, doubleGaus130, tripleGaus130]:
            modelToUse.color = R.kRed
            signalFit((category, diMuonMass130), ws, vbf130, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass130), ws, glu130, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass130), ws, wm130, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass130), ws, wp130, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)
            signalFit((category, diMuonMass130), ws, zh130, modelToUse, settings, pathToDir=signalfitsDir, initialValuesFromTH1=initialValuesFromTH1)

def generate_distributions():
    logY = True
    for category in categoriesToUse:
        for vname in varNames:
            variable = {}
            variable["name"]=vname
            variable["min"]=-0.999
            variable["max"]=-0.999
            if category!="NoCats" and vname=="DiMuonMass":
                variable["min"] = 110
                variable["max"] = 160
            distributions((category, variable), data, 
                [glu125, vbf125, wm125, wp125, zh125],
                [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy], settings,
                pathToDir=distributionsDir,
                logY=logY)

if __name__=="__main__":
    if args.number == 0:
        generate_distributions()
    elif args.number == 1:
        generate_signalFits()
    elif args.number == 2:
        generate_backgroundFits()
    elif args.number == 3:
        generate_signalFitInterpolations()
    elif args.number == 4:
        generate_signalFitInterpolationsWithSpline()
    elif args.number == 5:
        generate_backgroundsWithRooMultiPdf()
    elif args.number == 6:
        generate_datacardsSingleGaus()
    elif args.number == 7:
        generate_datacardsDoubleGaus()
    elif args.number == 8:
        generate_datacardsTripleGaus()
    else:
        pass
