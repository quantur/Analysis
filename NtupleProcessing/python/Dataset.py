#!/usr/bin/python

class Dataset(object):
    def __init__(self, *kargs, **wargs):
        """
        name - dataset name as in CMS DAS
        label - shorthand name for this DataSet
        isData - if this is a data or MC
        """
        if len(kargs)>0: 
            Dataset.startup(self, kargs[0])
            return

        object.__init__(self)
        self.name = wargs["name"]
        self.isData = wargs["isData"]
        if 'label' not in wargs.keys():
			self.label = self.name.replace("/", ".")[1:]
        else:
            self.label = wargs["label"]
        self.year = wargs["year"]
        if 'test_file' not in wargs.keys():
            self.test_file = self.label+".files"
        else:
            self.test_file = wargs["test_file"]

    def startup(self, other):
        object.__init__(self)
        self.name = other.name
        self.label = other.label
        self.isData = other.isData
        self.year = other.year
        self.test_file = other.test_file

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = "-"*80 + "\n" +\
            "Dataset:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            "-"*80 +\
            "\n"
        return s

class MCDataset(Dataset):
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            MCDataset.startup(self, kargs[0])
            return

        Dataset.__init__(self, **wargs)
        if "isSignal" not in wargs.keys():
            self.isSignal = None
        else:
            self.isSignal = wargs["isSignal"]
        if "initial_cmssw" not in wargs.keys():
            self.initial_cmssw = None
        else:
            self.initial_cmssw = wargs["initial_cmssw"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "MCDataset:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            ">>> isSignal="+str(self.isSignal)+"\n"+\
            ">>> initial_cmssw="+str(self.initial_cmssw)+"\n"+\
            "-"*80 +\
            "\n"
        return s
    def __repr__(self):
        return self.__str__()

    def startup(self, other):
        Dataset.__init__(self, other)
        if hasattr(other, "isSignal"):
            self.isSignal = other.isSignal
        else:
            self.isSignal = None
        if hasattr(other, "initial_cmssw"):
            self.initial_cmssw = other.initial_cmssw
        else:
            self.initial_cmssw = None

class Ntuple(MCDataset):
    """
    Data/MC Ntuple - the output of CMSSW Ntuple Making
    Location of Ntuples:
    rootpath<storagebased>/DATA.jsontag/label/timestamp/counter/files.root
    rootpath<storagebased>/MC.cmssw/label/timestamp/counter/files.root
    """
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            Ntuple.startup(self, kargs[0], **wargs)
            return

        MCDataset.__init__(self, **wargs)
        self.globaltag = wargs["globaltag"]
        self.json = wargs["json"]
        self.cmssw = wargs["cmssw"]

        self.timestamp = wargs["timestamp"]
        self.storage = wargs["storage"]
        self.rootpath = wargs["rootpath"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "Ntuple:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            ">>> isSignal="+str(self.isSignal)+"\n"+\
            ">>> initial_cmssw="+str(self.initial_cmssw)+"\n"+\
            ">>> globaltag="+str(self.globaltag)+"\n"+\
            ">>> json="+str(self.json)+"\n"+\
            ">>> cmssw="+str(self.cmssw)+"\n"+\
            ">>> timestamp="+str(self.timestamp)+"\n"+\
            ">>> storage="+str(self.storage)+"\n"+\
            ">>> rootpath="+str(self.rootpath)+"\n"+\
            "-"*80 +\
            "\n"
        return s
    
    def __repr__(self):
        return self.__str__()

    def startup(self, otherds, **wargs):
        MCDataset.__init__(self, otherds)
        self.globaltag = wargs["globaltag"]
        self.json = wargs["json"]
        self.cmssw = wargs["cmssw"]

        self.timestamp = wargs["timestamp"]
        self.storage = wargs["storage"]
        self.rootpath = wargs["rootpath"]

class DataResult(Ntuple):
    """
    Data Result of Data Ntuple Processing
    """
    def __init__(self, **wargs):
        Ntuple.__init__(self, **wargs)

class PileUp:
    """
    Represents the Pile up file information for MC
    """
    def __init__(self, **wargs):
        self.cross_section = wargs["cross_section"]
        self.pileupdatajson = wargs["pileupdatajson"]

class JsonFile(object):
    """
    Represents our Json files
    """
    def __init__(self, **wargs):
        object.__init__(self)
        self.filename = wargs["filename"]
        self.intlumi = wargs["intlumi"]
        self.url = None
        if "url" in wargs:
            self.url = wargs["url"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "JsonFile:" + "\n" +\
            ">>> filename="+str(self.filename)+"\n"+\
            ">>> intlumi="+str(self.intlumi)+"\n"+\
            ">>> url="+str(self.url)+"\n"+\
            "-"*80 +\
            "\n"
        return s

    def __repr__(self):
        return self.__str__()

class MCResult(Ntuple, PileUp):
    """
    MC Result of MC Ntuple Processing
    """
    def __init__(self, *wargs):
        Ntuple.__init__(self, **wargs)
        PileUp.__init__(self, **wargs)

if __name__=="__main__":
    ds = Dataset(name="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015, test_file="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD")
    ntuple = Ntuple(ds, globaltag="test", cmssw="test", json="test", timestamp="",
        storage="test", rootpath="test")
    print ds
    print "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD".replace("/", ".")[1:]
    print ntuple