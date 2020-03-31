'''Auto Update Calibration.py
Part of the "Microscope Measurement Tools" scripts 
by Demis D. John, Praevium Research Inc., 2015-05-25 
 
Added JPH 2020 - to quickly get the calibration from a loaded file. 
Hacked together from bits of the Microscope Measurement Tools scripts. 
 
'''
 
MC_DEBUG = False     # Print debugging info to the console? 
 
## Import some modules: 
from ij import IJ, ImagePlus, WindowManager #, gui 
from ij.gui import GenericDialog, YesNoCancelDialog 
 
from java.awt import Color as jColor    # for setting color 
from java.awt import Font as jFont      # for setting text font 
 
import sys, os 
 
import csv 
 
# add the path to this script, so we can find the user-settings 
libpth = os.path.split(os.path.split( sys.path[0] )[0]  )[0]  # split-off the "/jars/lib" part 
#print  libpth 
libpth = os.path.join(libpth, 'plugins', 'Scripts', 'Analyze', 'MScopeCals - JPH') 
# hard-coded path, within the Fiji directory. 
 
try: 
    sys.path.index(libpth )    # see if search-path is already added 
except ValueError: 
    # path wasn't included yet, so add it:
    sys.path.append(libpth) 
 
# microscope settings should be in the file `Microscope_Calibrations_user_settings.py`: 
import Microscope_Calibrations_user_settings_JPHEdit as sets # imports `linethickness`, `linecolor` etc under namespace `sets.linethickness` etc. 
 
 
# the run() function is called at the end of this script: 
def run(): 
    '''This is the main function run when the plugin is called.''' 
     
    #print dir(IJ) 
    ip = IJ.getProcessor() 
     
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object 
    #print "imp=", type(imp), imp 
    #print dir(imp) 
     
    roi = imp.getRoi()  # get the drawn ROI 
    #print "roi=", roi, roi.getClass() 
 
    newcal = imp.getCalibration().copy()   # make a copy of current calibration object 
 
    if MC_DEBUG: print("Assume calibration is a custom function.") 
    # call the class' `classObj.cal( ImagePlusObject )` function to get the scale value:
    try: 
        calObject = sets.autoupdatecal_name 
        calName = calObject.name 
        newPixelPerUnit = calObject.cal( imp ) 
    except AttributeError: 
        raise ValueError('This calibration Name value is invalid, please check your Settings.py file!/n/tFor Calibration Number %i, got: `'%(CalIdx) + str(cal.names[CalIdx]) + '`. Expected a String or a Class instance with ".cal()" method, but got type ' + str( type(cal.names[CalIdx]) ) + ' with no ".cal()" method.' ) 
    #end try 
     
    newUnit = calObject.unit 
    newAspect = calObject.aspect_ratio 
     
    newPixelWidth = 1. / newPixelPerUnit 
    newPixelHeight = newPixelWidth * newAspect 
 
    # the following translated from "Microscope_Scale.java": 
    newcal.setUnit(  newUnit  ) 
    newcal.pixelWidth =  newPixelWidth 
    newcal.pixelHeight = newPixelHeight     
     
    imp.setGlobalCalibration(None) 
    imp.setCalibration( newcal )    # set the new calibration 
    imp.getWindow().repaint()     # refresh the image? 
   
#end run() 
 
if( __name__ == '__builtin__'): 
	run() 
#run()       # Finally, Run the script function! 
 
