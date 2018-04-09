from radar_tools import *
import matplotlib.pyplot as plt
from survey_reader import survey_reader
import os 
from matplotlib.widgets import Button

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
from qgis import *
from qgis.core import *
from qgis.gui import *

class fig_gui:
    
    def __init__(self,name = None,rad_sample=[],gps_sample = []):
        if name is None:
            self.name ="None"
            self.rad_sample=[];
            self.gps_sample=[];
        else :
            self.name = name
            self.rad_sample=rad_sample;
            self.gps_sample=gps_sample;
            print (name)

     
        
        self.fig = plt.figure()
        
        
        
        seg = survey_reader(self.name)
# create a group of traces from seg-y 
        self.ax  = [self.fig.add_subplot(111)]
        self.update(self.rad_sample)                            # add data to plot

        cli = cursor()              # new cursors object
        self.fig.signal = cli          # connect it with fig object 

                #tr_list  = range(len(gps_sample[0]))       # list index

        cli.transform = lambda x,y: [self.gps_sample[1][x] ,self.gps_sample[0][x],self]
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        
	
        
    def update(self,data,plt_type=None , plot_number = 0):

                if plt_type == "equal":
                    print( "equalized")
                    data = exposure.equalize_hist(data)

                elif plt_type == "expos":
                    p2, p98 = np.percentile(data, (2, 98))
                    data = exposure.rescale_intensity(data, in_range=(p2, p98))

                self.ax[plot_number].imshow(data, interpolation='nearest', aspect='auto',clim=[np.min(data),np.max(data)])
                plt.show()
        
    def onclick(self,event):
        if self.fig.signal is None:
                  
            self.cursor = [int(event.xdata),int(event.ydata)]
        else :
           self.fig.signal.set_pos(event, self.name)







class cursor:
    
    def __init__(self):
        self.fig_to_update = None
        self.func_update = None
        self.transform = lambda x,y,z: [x,y,z]
        layer = QgsVectorLayer('Point?crs=epsg:4326&field=Trace:int&field=x&field=y', 'Mes points' , 'memory')
        prov = layer.dataProvider()
        QgsMapLayerRegistry.instance().addMapLayers([layer])
    def set_pos(self,event,name):
        print ("pos in pixel: ", int(event.xdata),int(event.ydata) )
        self.pos = self.transform(int(event.xdata),int(event.ydata))
        print("pos in data: ",self.pos)
        x = self.pos[0]
        y = self.pos[1]
            
        layer = iface.activeLayer()
        prov = layer.dataProvider()
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
        fet.setAttributes([0,float(x),float(y)])
        prov.addFeatures([fet])
        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        layer.updateExtents()

        #QgsMapLayerRegistry.instance().addMapLayers([layer])
        if self.fig_to_update is None:
            print ( "nothing to do")

        else:
          print "do something with matplotlib figure declare in: self.fig_to_update"


