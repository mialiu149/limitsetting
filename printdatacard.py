# get number of yields in a bin
# print out data card
from ROOT import TH1F,TFile
import os

def printcard(masspoint,binN,backgrounds,errors,selection):
    sigN,sigE = grabnumber(os.environ["analysis_output"]+'/wh_'+masspoint+'_'+selection+'_hists.root','h_lep_event_NEventsSR_'+selection)
   
    card = open('cards/datacard_tch'+masspoint+'_'+str(binN)+'.txt','w')

    card.write("imax  1  number of channels\n")
    card.write("jmax  4  number of backgrounds\n")
    card.write("kmax  10  number of nuisance parameters\n")
    card.write("------------\n")
    card.write("# observations\n")
    card.write("bin        "+str(binN)+'\n')
    card.write("observation  " + str(2)+'\n')
    card.write("#now we list all expected number of events\n")
    bintoprint = str(binN)+' '
    card.write("bin "+5*bintoprint+'\n')
    card.write("process     sig       2l       1l       1ltop       diboson\n")
    card.write("process      0     1    2    3       4\n")
    binI = binN-1
    card.write("rate " +str(sigN[binI]) +' ' + str(backgrounds['2l'][binI]) +' ' + str(backgrounds['1l'][binI])+' ' + str(backgrounds['1ltop'][binI])+' ' + str(backgrounds['diboson'][binI]))
    card.write("\n------------\n")
    card.write("SigStat"+str(binI)+" lnN " +str(sigE[binI])+' - - - -\n')
    card.write("Bg2lStat"+str(binI)+"  lnN - " +str(errors['2l'][binI])+'  -  -  -\n')
    card.write("Bg1lStat"+str(binI)+"  lnN - - " +str(errors['1l'][binI])+'  -  - \n')
    card.write("Bg1ltopStat"+str(binI)+"  lnN  -  -  - " +str(errors['1ltop'][binI])+'  -\n')
    card.write("BgdibosonStat"+str(binI)+"  lnN  -  -  -  - " +str(errors['diboson'][binI])+'\n')
    card.write("MCSystSig       lnN 1.15  -  -  -  -\n")
    card.write("MCSyst2l        lnN  -  1.30 -  -  -\n")
    card.write("MCSyst1l        lnN  -  - 1.30  -  -\n")
    card.write("MCSyst1ltop     lnN  -  - - 1.30 -\n")
    card.write("MCSystdiboson   lnN  -  - - - 1.30\n")

def getbackgrounds(selection):  #hardcoded 
    hist_prefix = 'h_lep_event_NEventsSR_'+selection
    backgrounds = {'2l':[],'1l':[],'1ltop':[],'diboson':[]}
    errors = {'2l':[],'1l':[],'1ltop':[],'diboson':[]}
    print os.environ["analysis_output"]
    backgrounds['2l'],errors['2l'] = grabnumber(os.environ["analysis_output"]+'/'+'ttbar_'+selection+'_hists.root', hist_prefix.replace('lep','lep_dilep'))    
    backgrounds['1ltop'],errors['1ltop'] = grabnumber(os.environ["analysis_output"]+'/'+'ttbar_'+selection+'_hists.root', hist_prefix.replace('lep','lep_onelep'))    
    backgrounds['1l'],errors['1l'] = grabnumber(os.environ["analysis_output"]+'/'+'wbb_'+selection+'_hists.root',hist_prefix)
    backgrounds['diboson'],errors['diboson'] = grabnumber(os.environ["analysis_output"]+'/'+'diboson_'+selection+'_hists.root',hist_prefix)
    print backgrounds
    print errors
    return backgrounds,errors
 
def grabnumber(filename,histname):
    rootf = TFile(filename)
    hist = rootf.Get(histname)
    contents = []
    errors = []

    for i in range(2):
        contents.append(hist.GetBinContent(i+1)) 
        if hist.GetBinContent(i+1):error = float(1+(hist.GetBinError(i+1)/hist.GetBinContent(i+1)))
        else: error = 0
        errors.append(error)
    return contents,errors
if __name__ == "__main__":
   selection = "yield_2lCR_mbb"
   bkgs,err = getbackgrounds(selection) 
   printcard("250_1",1,bkgs,err,selection)
   printcard("250_1",2,bkgs,err,selection)

