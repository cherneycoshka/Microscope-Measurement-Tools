'''
	FIJI Plugin
Additional Function for Choose_Microscope_Calibration.py
Demis D. John, Univ. of California Santa Barbara, 2019

Edited JPH 2019 - to load up the version of txt file I'm interested in.

It is Based on the HiRes SEM we have in Cardiff - 

[SemImageFile]
InstructName=SU8200
SemVersion=03-05

The class will be accessed by  `Choose_Microscope_Calibration.py`.
The class must have methods named as follows:
    MyClass() - class constructor, which defines MyClass.name attribute:
    MyClass.name - a string that shows up in the available calibrations list.
    MyClass.cal() - returns the Pixel-Per-Unit calibration (numeric)
    MyClass.unit - a string that is the measurement unit, eg. "cm" or "nm" etc.
    MyClass.aspect - numeric value of pixel aspect ratio, eg. 1.0

After you edit this file, be sure to delete the corresponding *.pyclass file and restart Fiji for the changes to take effect.
'''


"""
################################
   JPH SEM AutoCal from *.txt
################################


"""

MC_DEBUG = False     # Send debugging info to the log file?


class JPH_SEM_CalFromTxt(object):
    '''    Class with functions for automatic calibration of image scale.
    
    JPH_SEM_CalFromTxt() : (Constructor)
        Only sets the `name` to be used in the Calibrations list.
    
    JPH_SEM_CalFromTxt.name : string
        The name that shows up in the Calibrations list.
    
    JPH_SEM_CalFromTxt.cal(  ImagePlus_Object ) :
        Takes in the ImagePlusObject being analyzed.
        Returns the pixel-per-unit numeric value, using a custom function.
        Sets the following internal attributes:
            self.pixel_per_unit (unused)
            self.unit
            self.aspect_ratio
    
    JPH_SEM_CalFromTxt.unit : string
        String indicating the unit used in the pixel-per-unit returned by `self.cal()`.  The string will be used by annotations and set internally in ImageJ's "Set Scale" etc.  Should be the short abbreviation of the unit name.
        Examples: "mm", "cm", "um" (will be converted to greek `mu` by ImageJ)
    
    JPH_SEM_CalFromTxt.aspect_ratio
        Numeric aspect ratio (width/height) of the pixel-per-unit, typically 1.0.
    
    '''
    
    def __init__(self):
        ''' See `help(JPH_SEM_CalFromTxt)` for help on this constructor.'''
        self.name =     "JPH SEM: AutoCal from *.txt"
    #end __init__()
    

    def cal( self, imp ):
        '''
        Takes in the ImagePlusObject being analyzed.
        Returns the pixel-per-unit numeric value.
        For My (JPH) SEM image files, this is done by locating the accompying *.txt text-file and parsign it to find the image scale values.
		Looking for text which is Something like 'PixelSize=2.480469'
        Sets the following internal attributes:
            self.unit
            self.aspect_ratio
        '''
        
        import re   # RegEx matching, for parsing text file
        import os.path  # file-path manipulation functions
        
        filepath =    imp.getOriginalFileInfo().directory  +  os.path.sep  +  imp.getOriginalFileInfo().fileName
        if MC_DEBUG: 
            print( "imp=", imp )
            print( "ImagePath=", filepath )
        
        txtpath = os.path.splitext( filepath )[0] + ".txt"
        if MC_DEBUG: print "txtpath = ", txtpath
        if not os.path.isfile(txtpath): raise IOError("Text File not found at: \n\t" + txtpath)
        
        # set up regex search groups:
		# Previously... I think the other format expected to need to know the length of the bar - but here we have the pixel size directly.
        re_pixelsize = re.compile( r'^PixelSize=(\d*\.?\d*)$') # captures the digits in "PixelSize=2.480469" to a group
    
    
        # try to load the .txt file:
        BarLength_px = None
        BarLength_dist = None
        BarLength_unit = None
    
        txtfile = open(txtpath, 'r')
        try:
            while True:
                txtline = txtfile.readline()  # grab one line of text
                if len(txtline) == 0:
                    # end of file, exit the loop
                    break
                #end(if end-of-file)
            
            
                # # search for strings/values:
                # match1 = re_bar.search( txtline )
                # if match1:
                    # BarLength_px = float( match1.group(1)  )  # this is pixel width of the scale bar
                    # if MC_DEBUG: print 'Scale Bar Pixel Length found:', match1.groups(), ' --> ', BarLength_px    
                # #end if(match1)
            
            
                # match2 = re_barmark.search( txtline )
                # if match2:
                    # BarLength_dist = float( match2.group(1)  )  # this is physical width of the scale bar
                    # BarLength_unit = str( match2.group(2)  )
                    # if MC_DEBUG: print 'Scale Bar Distance Length found:', match2.groups(), ' --> ', BarLength_dist, BarLength_unit
                # #end if(match2)
				
				
				
                match3 = re_pixelsize.search( txtline )
                if match3:
					BarLength_px = float(1.0)
					BarLength_dist = float( match3.group(1))  # this is physical size of the pixel
					BarLength_unit = 'nm' # default to nm here.
					if MC_DEBUG: print 'Scale Bar Distance Length found:', match3.groups(), ' --> ', BarLength_dist, BarLength_unit
                #end if(match2)				
				
            
            #end while(file-reading)

        except IOError:
            raise IOError("Could not load text file that accompanies this image file.  Expected the text file to have the same filename as the image, except with '.txt' extension.  Expected file to be here:\n\t" + txtpath )
    
        finally:
            # make sure python closes the file no matter what
            txtfile.close()
        #end try(txtfile)
        
        self.pixel_per_unit = BarLength_px/BarLength_dist 
        self.unit = BarLength_unit
        self.aspect_ratio = 1.0
		
		
        
        # return pixel-per-unit
        return self.pixel_per_unit
    #end cal()
#end class(JPH_SEM_CalFromTxt)



'''
---------------------------------------------------------
Warn user if they run this file as a stand-alone plugin.
'''

def run():
    ''' If someone tries to run this file by itself, warn them of their error.  Unfortunately, since I was too lazy to make Microscope_Calibrations a full plugin (rather than a script), this accompanying settings file will show up in the Scripts menu.'''
    from ij.gui import GenericDialog
    
    gd = GenericDialog("Microscope_Calibrations_user_settings.py")
    gd.addMessage("This file is only for adding functionality to the plugin 'Microscope Measurement Tools'.\nNothing is done when this settings file is run by itself."  )
    
    gd.showDialog()
#end run()

if __name__ == '__main__':
    run()   # run the above function if the user called this file!


