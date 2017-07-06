import sys
import wx
import wx.grid as gridlib
import wx.lib.ogl as ogl

########################################################################

#map
w, h = 10, 10;
map = [[0 for x in range(w)] for y in range(h)]

for x in range(w):
    for y in range(h):
        map [ x ][ y ] = "."
        
for x in range(w):
    for y in range(h):
        sys.stdout.write(map [ x ][ y ] + '  ')
    print("\n")

turn = "player"
    
counter = 0

# game_state is "ship_placement" or "battle"
gameState = "ship_placement"

# type of placing ship depends on selected radio button: "patrol_ship" / "frigate" / "kruiser" / "submarine" / "aicraft_carrier"
shipType = "Place Patrol ship"

#orientation of ship - "vertical" or "horizontal"
shipOrient = "vertical"

#ship types: 1) patrol ship - p , 2)Frigate - ff 3)kruiser - ccc 4) submarine - ssss 5) aircraft carrier - aaaaa

########################################################################

class SyncPanels(object):

    def __init__(self, panel1, panel2):
        self.panel1 = panel1
        self.panel2 = panel2
        self.panel1.grid.Bind(wx.EVT_SCROLLWIN, self.onScrollWin1)
        self.panel2.grid.Bind(wx.EVT_SCROLLWIN, self.onScrollWin2)
 
    def onScrollWin1(self, event):
        if event.Orientation == wx.SB_HORIZONTAL:
            self.panel2.grid.Scroll(event.Position, -1)
        else:
            self.panel2.grid.Scroll(-1, event.Position)
        event.Skip()
 
    def onScrollWin2(self, event):
        if event.Orientation == wx.SB_HORIZONTAL:
            self.panel1.grid.Scroll(event.Position, -1)
        else:
            self.panel1.grid.Scroll(-1, event.Position)
        event.Skip()

########################################################################

class EnemyGridPanel( wx.Panel ):

    def __init__( self, parent, margin ):
    
        """Constructor"""
        wx.Panel.__init__( self, parent )    
        
        fieldSize = 10
        global map
        
        self.margin = margin
        self.grid = gridlib.Grid( self, style = wx.BORDER_SUNKEN )
        self.grid.CreateGrid( fieldSize, fieldSize )
        #self.grid.Bind( gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect )
        
        for row in range( 0, fieldSize ):
            for col in range( 0, fieldSize ):
            
                self.grid.SetRowSize( row, 30 )
                self.grid.SetColSize( col, 30 )
                
                
        for x in range(w):
                for y in range(h):
                    
                    if map [ x ][ y ] is "p":
                        self.grid.SetCellBackgroundColour( x, y, wx.RED )
                        self.grid.ForceRefresh()
                        
 
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add( self.grid, 1, wx.EXPAND )
        self.SetSizer( sizer )

########################################################################

class GridPanel( wx.Panel ):
 
    def __init__( self, parent, margin ):
    
        """Constructor"""
        wx.Panel.__init__( self, parent )    
        
        fieldSize = 10
        
        self.margin = margin
        self.grid = gridlib.Grid( self, style = wx.BORDER_SUNKEN )
        self.grid.CreateGrid( fieldSize, fieldSize )
        self.grid.Bind( gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect )
        #self.grid.Bind( gridlib.EVT_GRID_SELECT_CELL, self.refreshGrid )
        
        for row in range( 0, fieldSize ):
            for col in range( 0, fieldSize ):
            
                self.grid.SetRowSize( row, 30 )
                self.grid.SetColSize( col, 30 )
 
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add( self.grid, 1, wx.EXPAND )
        self.SetSizer( sizer )
		
    #------------------------------------------------------------------------------------------------------------
		
    def onSingleSelect( self, event ):
        """
        Get the selection of a single cell by clicking or 
        moving the selection with the arrow keys
        """
        
        row = event.GetRow()
        col = event.GetCol()
        
        print ("Field %s : You selected Row %s, Col %s" % ( self.margin, row, col ) )
        self.currentlySelectedCell = ( row, col )
 
        global shipOrient
        global map
        global counter 
        counter += 1
        
        #if self.margin == "enemy_field":
        
        if counter%2 == 0:
            self.grid.SetCellBackgroundColour( 3, 3, wx.GREEN )
        else:
            self.grid.SetCellBackgroundColour( 3, 3, wx.RED )
            
        self.grid.ForceRefresh() 
            
        #if shipOrient == "vertical":
        
            #self.grid.SetCellBackgroundColour( 1, 1, wx.BLUE )
            #self.grid.SetCellBackgroundColour( 1, 2, wx.BLUE )
            #self.grid.SetCellBackgroundColour( 1, 3, wx.BLUE )
            
        #else:
        
            #self.grid.SetCellBackgroundColour( 1, 1, wx.BLUE )
            #self.grid.SetCellBackgroundColour( 2, 1, wx.BLUE )
            #self.grid.SetCellBackgroundColour( 3, 1, wx.BLUE )
        
        if shipOrient == "horizontal":#counter % 2 == 0 and
              
            if  shipType == "Place Kruiser":
            
                self.grid.SetCellBackgroundColour( row, col, wx.BLUE )
                self.grid.SetCellBackgroundColour( row, col + 1, wx.BLUE )
                self.grid.SetCellBackgroundColour( row, col + 2, wx.BLUE )
                map[ row ][ col ] = "p"
                map[ row ][ col + 1 ] = "p"
                map[ row ][ col + 2 ] = "p"
           
            self.grid.ForceRefresh()      

            for x in range(w):
                for y in range(h):
                    sys.stdout.write(map [ x ][ y ] + '  ')
                print("\n")
            
        else:
        
            if  shipType == "Place Kruiser":
            
                self.grid.SetCellBackgroundColour( row, col, wx.YELLOW )
                self.grid.SetCellBackgroundColour( row + 1, col, wx.YELLOW )
                self.grid.SetCellBackgroundColour( row + 2, col, wx.YELLOW )
                map[ row ][ col ] = "p"
                map[ row + 1 ][ col ] = "p"
                map[ row + 2 ][ col ] = "p"
           
            self.grid.ForceRefresh()      

            for x in range(w):
                for y in range(h):
                    sys.stdout.write(map [ x ][ y ] + '  ')
                print("\n")
            
        
            #self.grid.SetCellBackgroundColour( row, col, wx.YELLOW )
            #self.grid.SetCellBackgroundColour( row + 1, col, wx.YELLOW )
            #self.grid.ForceRefresh()
            
            #map[ row ][ col ] = "p"
            #map[ row + 1 ][ col ] = "p"       

            for x in range(w):
                for y in range(h):
                    sys.stdout.write(map [ x ][ y ] + '  ')
                print("\n")
        
        #self.currentlySelectedCell = ( event.GetRow(), event.GetCol() )
        
        print ( "counter = %s" % counter )
        event.Skip()

    #------------------------------------------------------------------------------------------------------------
        
    def paintCell( self, x, y ):
        
        self.grid.SetCellBackgroundColour( x, y, wx.GREEN )
        self.grid.ForceRefresh()
        
    def refreshGrid( self ):
        
        if self.margin == "enemy_field":
        
            if counter%2 == 0:
                self.grid.SetCellBackgroundColour( 3, 3, wx.GREEN )
            else:
                self.grid.SetCellBackgroundColour( 3, 3, wx.RED )
             
        self.grid.ForceRefresh()
 
########################################################################

class RegularPanel( wx.Panel ):

    def __init__( self, parent, panel1, panel2 ):
	
        """Constructor"""
        wx.Panel.__init__( self, parent )
		
        self.SetBackgroundColour( "cyan" )
        
        self.panel1 = panel1
        self.panel2 = panel2
        
        self.m_buttonFinishEditing = wx.Button( self, wx.ID_ANY, u"Finish placing", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buttonBattleStart = wx.Button( self, wx.ID_ANY, u"BATTLE!", wx.DefaultPosition, wx.DefaultSize, 0 ) 
        self.m_buttonFire = wx.Button( self, wx.ID_ANY, u"Feuer frei!!!", wx.DefaultPosition, wx.DefaultSize, 0 ) 
        
        self.m_buttonFire.Bind( wx.EVT_BUTTON, self.refreshPanel )
        
        sizer1 = wx.BoxSizer( wx.VERTICAL )
        sizer1.AddSpacer( 55 )
        self.SetSizer( sizer1 )
        
        sizer = wx.BoxSizer( wx.HORIZONTAL )
   
        sizer.AddSpacer( 15 )
   
        sizer.Add( self.m_buttonFinishEditing )      
        sizer.AddSpacer( 15 )
        sizer.Add( self.m_buttonBattleStart )
        sizer.AddSpacer( 25 )
        sizer.Add( self.m_buttonFire )
        
        self.SetSizer( sizer )
        
        #splitter = wx.SplitterWindow(self)    
        #leftP = LeftPanel(splitter)
        #rightP = RightPanel(splitter)
        # split the window
        #splitter.SplitVertically(leftP, rightP)
        #splitter.SetMinimumPaneSize(20)  
        #sizer.Add(splitter, 5, wx.EXPAND)    
        #sizer = wx.BoxSizer(wx.HORIZONTAL)     
        #sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer.AddSpacer( 25 )
        
        lblList = ['Place Patrol ship', 'Place Frigate', 'Place Kruiser', 'Place Submarine', 'Place Aircraft carrier' ] 
		  
        self.radioBoxShipType = wx.RadioBox( self, label = 'Place ship', pos = (80,10), choices = lblList, majorDimension = 1 ) 
        self.radioBoxShipType.Bind( wx.EVT_RADIOBOX, self.onRadioBoxShipType )        
        sizer.Add( self.radioBoxShipType )
        
        sizer.AddSpacer( 25 )
        
        lblList = ['vertical', 'horizontal'] 
		  
        self.radioBoxShipOrient = wx.RadioBox( self, label = 'Choose ship orientation', pos = ( 80, 10 ), choices = lblList, majorDimension = 1 ) 
        self.radioBoxShipOrient.Bind( wx.EVT_RADIOBOX, self.onRadioBoxShipOrient )        
        sizer.Add( self.radioBoxShipOrient )
        
        self.SetSizer( sizer )
		#gSizer1.Add( self.m_button1, 0, wx.ALL, 5 )
        
    #--------------------------------------------------------------------------------------------------------
        
    def onRadioBoxShipType( self, e ): 
    
        global shipType
    
        if self.radioBoxShipType.GetStringSelection() == "Place Kruiser":
            
            shipType = "Place Kruiser"
            print( self.radioBoxShipType.GetStringSelection(),' is clicked from Radio Box' )
    
        
      
    #--------------------------------------------------------------------------------------------------------
      
    def onRadioBoxShipOrient( self, e ): 
    
        #orientation of ship - "vertical" or "horizontal"
        global shipOrient
        
        if self.radioBoxShipOrient.GetStringSelection() == "vertical":
            
            shipOrient = "vertical"
            print( shipOrient )
            print( self.radioBoxShipOrient.GetStringSelection(),' is clicked from Radio Box' )
            
        else:
        
            shipOrient = "horizontal"
            print( shipOrient )
            print( self.radioBoxShipOrient.GetStringSelection(),' is clicked from Radio Box' )
            
    def refreshPanel( self, event ):
        
        #self.panel1.ForceRefresh()
        self.panel2.refreshGrid()
        print( 'fired...' )
        
    
########################################################################    

class MainPanel(wx.Panel):

    def __init__(self, parent):
    
        self.panelOne = None
        self.panelTwo = None
    
        """Constructor"""
        wx.Panel.__init__(self, parent)
 
        notebook = wx.Notebook(self)
 
        page = wx.SplitterWindow(notebook)
        notebook.AddPage(page, "Splitter")
        hSplitter = wx.SplitterWindow(page)
 
        self.panelOne = GridPanel(hSplitter, "my_field")     
        #self.panelTwo = EnemyGridPanel(hSplitter, "enemy_field")            
        self.panelTwo = GridPanel(hSplitter, "enemy_field")
        
        global counter
        
        if counter % 2 == 0:
        
            self.panelTwo.refreshGrid()
            
        else:
        
            self.panelTwo.refreshGrid()
 
        hSplitter.SplitVertically(self.panelOne, self.panelTwo)
        hSplitter.SetSashGravity(0.5)
 
        self.panelThree = RegularPanel(page, self.panelOne, self.panelTwo)
        page.SplitHorizontally(hSplitter, self.panelThree)
        page.SetSashGravity(0.6)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
    #------------------------------------------------------------------------------------------------------------
        
    def paint(self, x, y):
        
        self.panelOne.paintCell(x, y)
    
 
########################################################################

class MainFrame(wx.Frame):

    def __init__(self):

        self.panel = None
    
        """Constructor"""
        wx.Frame.__init__(self, None, title="Nested Splitters", size=(1100,700))
        self.panel = MainPanel(self)
        
        #self.Show()
		
	#def refresh(self):
	
		#self.panel.Update()
        
    def paintGreen(self, x, y):
    
        self.panel.paint(x, y)
 
#====== MAIN ============================

i = int(sys.argv[ 1 ])

app = wx.App(False)
frame = MainFrame()

if i == 0:
	frame.paintGreen(1,1)
	#frame.refresh()
else:
	frame.paintGreen(8,1)
	#frame.refresh()

frame.Show()
app.MainLoop()

#if __name__ == "__main__":

    #app = wx.App(False)
	#inp = int(input('Give me a number: '))
    
    #****************************************
    
    #frame = MainFrame()
	
    #frame.paintGreen(i,1)
    #frame.paintGreen(3,1)
    #frame.Show()
    
    #****************************************
    
    #app.MainLoop()