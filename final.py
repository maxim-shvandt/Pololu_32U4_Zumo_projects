import sys
import wx
import wx.grid as gridlib
import wx.lib.ogl as ogl
import random

########################################################################

#======== Global variables ( flags ) ======================

#whose turn currently is it
turn = "player"

# game_state is "ship_placement" or "battle"
gameState = "ship_placement"

# type of placing ship depends on selected radio button: "patrol_ship" / "frigate" / "kruiser" / "submarine" / "aicraft_carrier"
#ship types: 1) patrol ship - p , 2)Frigate - ff 3)kruiser - ccc 4) submarine - ssss 5) aircraft carrier - aaaaa
shipType = "Patrol ship"

#orientation of ship - "vertical" or "horizontal"
shipOrient = "vertical"

#player last hit coordinates
playerXHit = 0
playerYHit = 0

########################################################################

class CFields():

    def __init__(self):
    
        self.playerPatrolBoatHit = 1
        self.playerFrigatemyHit = 2
        self.playerKruiserBoatHit = 3
        self.playerSubmarineBoatHit = 4
        self.playerAircraftCarrierBoatHit = 5
        
        self.enemyPatrolBoatHit = 1
        self.enemyFrigatemyHit = 2
        self.enemyKruiserBoatHit = 3
        self.enemySubmarineBoatHit = 4
        self.enemyAircraftCarrierBoatHit = 5
    
        self.w = 10
        self.h = 10
        self.myField = [[0 for x in range(self.w)] for y in range(self.h)]
        self.enemyField = [[0 for x in range(self.w)] for y in range(self.h)]
        
        for x in range(self.w):
            for y in range(self.h):
                self.myField[ x ][ y ] = "."
                
        for x in range(self.w):
            for y in range(self.h):
                self.enemyField[ x ][ y ] = "."
                
        self.enemyField = [ ["p",".",".",".","s","s","s","s",".","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         [".","f","f",".",".",".","k","k","k","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         ["a","a","a","a","a",".",".",".",".","."],
                         [".",".",".",".",".",".",".",".",".","."],
                         [".",".",".",".",".",".",".",".",".","."] ]
                
        #self.computer_place_ships() // to fix
                
                
        #self.enemyField[ 2 ][ 2 ] = "s"

    #-------------------------------------------------------------------------------------------
        
    def playerCellHit( self, xCoord, yCoord ):  
    
        if self.enemyField[ xCoord ][ yCoord ] == "p":
                self.enemyField[ xCoord ][ yCoord ] = "x"
                self.enemyPatrolBoatHit -= 1
        elif self.enemyField[ xCoord ][ yCoord ] == "f":
                self.enemyField[ xCoord ][ yCoord ] = "x"
                self.enemyFrigatemyHit -= 1
        elif self.enemyField[ xCoord ][ yCoord ] == "k":
                self.enemyField[ xCoord ][ yCoord ] = "x"
                self.enemyKruiserBoatHit -= 1
        elif self.enemyField[ xCoord ][ yCoord ] == "s":
                self.enemyField[ xCoord ][ yCoord ] = "x"
                self.enemySubmarineBoatHit -= 1
        elif self.enemyField[ xCoord ][ yCoord ] == "a":
                self.enemyField[ xCoord ][ yCoord ] = "x"
                self.enemyAircraftCarrierBoatHit -= 1
        elif self.enemyField[ xCoord ][ yCoord ] == ".":
            self.enemyField[ xCoord ][ yCoord ] = "o"
                
    #-------------------------------------------------------------------------------------------
        
    def enemyCellHit( self, xCoord, yCoord ):
    
        # to be done
    
        self.myField[ xCoord ][ yCoord ] = type
    
    #-------------------------------------------------------------------------------------------
    
    def placePlayerShip( self, x, y ): 
	    #place ship based on orientation
       
        #['Patrol ship', 'Frigate', 'Kruiser', 'Submarine', 'Aircraft carrier' ]
        
        global gameState
        global shipType      
        
        shipLength = 0
        shipSymbol = None
        
        if gameState == "ship_placement":  
        
            if shipType == "Patrol ship":
                shipLength = 1
                shipSymbol = "p"
            elif shipType == "Frigate":
                shipLength = 2
                shipSymbol = "f"
            elif shipType == "Kruiser":
                shipLength = 3
                shipSymbol = "k"
            elif shipType == "Submarine":
                shipLength = 4
                shipSymbol = "s"
            elif shipType == "Aircraft carrier":
                shipLength = 5
                shipSymbol = "a"
                    
            if shipOrient == "vertical":
                for i in range(shipLength):
                    self.myField[ x + i ][ y ] = shipSymbol
            elif shipOrient == "horizontal":
                for i in range(shipLength):
                    self.myField[ x ][ y + i ] = shipSymbol   
    
    #-------------------------------------------------------------------------------------------
    
    def getMyField( self ):
    
        return self.myField
        
    #-------------------------------------------------------------------------------------------
        
    def getEnemyField( self ):
        
        return self.enemyField
        
    #-------------------------------------------------------------------------------------------
            
    def printMyField( self ):
    
        for x in range(self.w):
            for y in range(self.h):
                sys.stdout.write( self.myField[ x ][ y ] + '  ')
            print("\n")
    
    #-------------------------------------------------------------------------------------------
    
    def printField( self ):
    
        for x in range(self.w):
            for y in range(self.h):
                sys.stdout.write( self.myField[ x ][ y ] + '  ')
            print("\n")
        
        print("===============================")
            
        for x in range(self.w):
            for y in range(self.h):
                sys.stdout.write( self.enemyField[ x ][ y ] + '  ')
            print("\n")
        
########################################################################

gameField = CFields()

gameField.printField()

########################################################################

class EnemyGridPanel( wx.Panel ):

    def __init__( self, parent ):
    
        """Constructor"""
        wx.Panel.__init__( self, parent )    
              
        fieldSize = 10
        global map
        
        global playerXHit
        global playerYHit
        
        playerXHit = 0
        playerYHit = 0

        self.grid = gridlib.Grid( self, style = wx.BORDER_SUNKEN )
        self.grid.CreateGrid( fieldSize, fieldSize )
        self.grid.Bind( gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect )
        
        for row in range( 0, fieldSize ):
            for col in range( 0, fieldSize ):          
                self.grid.SetRowSize( row, 30 )
                self.grid.SetColSize( col, 30 )
                
        sizer = wx.BoxSizer( wx.VERTICAL )
        sizer.Add( self.grid, 1, wx.EXPAND )
        self.SetSizer( sizer )
        
    #-----------------------------------------------------------------------------------
        
    def onSingleSelect( self, event ):
        """
        Get the selection of a single cell by clicking or 
        moving the selection with the arrow keys
        """
        
        global gameField
        global playerXHit
        global playerYHit
        
        row = event.GetRow()
        col = event.GetCol()
        
        playerXHit = row
        playerYHit = col
        
        print ("playerHit %s : %s" % ( playerXHit, playerYHit ) )
        gameField.playerCellHit( playerXHit, playerYHit )     
        gameField.printField()
        
        self.currentlySelectedCell = ( row, col )
        
    #------------------------------------------------------------------------------------
        
    def refreshGrid( self ):
              
        w, h = 10, 10;
        map = [[0 for x in range(w)] for y in range(h)]
        
        map = gameField.getEnemyField()

        for x in range(w):
            for y in range(h):
                if map[ x ][ y ] != "x":
                    self.grid.SetCellBackgroundColour( x, y, wx.RED )
                elif map[ x ][ y ] != "o":
                    self.grid.SetCellBackgroundColour( x, y, wx.CYAN )
              
        self.grid.ForceRefresh()

########################################################################

class MyGridPanel( wx.Panel ):
 
    def __init__( self, parent ):
    
        """Constructor"""
        wx.Panel.__init__( self, parent )    
        
        fieldSize = 10

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
        
        global gameField
        global shipOrient
        global map
        global counter 
        
        row = event.GetRow()
        col = event.GetCol()
        
        print ("You selected Row on MY field: %s, Col %s" % ( row, col ) )
        self.currentlySelectedCell = ( row, col )
             
        gameField.placePlayerShip( row, col )
            
        self.grid.ForceRefresh() 
        
        event.Skip()

    #------------------------------------------------------------------------------------------------------------
        
    def paintCell( self, x, y ):
        
        self.grid.SetCellBackgroundColour( x, y, wx.GREEN )
        self.grid.ForceRefresh()
        
    def refreshGrid( self ):
        
        global gameField
        
        w, h = 10, 10;
        map = [[0 for x in range(w)] for y in range(h)]
        
        map = gameField.getMyField()

        for x in range(w):
            for y in range(h):
                if map[ x ][ y ] != ".":
                    self.grid.SetCellBackgroundColour( x, y, wx.BLUE )
                
             
        self.grid.ForceRefresh()
        
###################################################################################################

class RegularPanel( wx.Panel ):

    def __init__( self, parent, panel1, panel2 ):
	
        """Constructor"""
        wx.Panel.__init__( self, parent )
		
        self.SetBackgroundColour( "cyan" )
        
        self.panel1 = panel1
        self.panel2 = panel2
        
        self.m_buttonFinishEditing = wx.Button( self, wx.ID_ANY, u"Finish placing one ship", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buttonBattleStart = wx.Button( self, wx.ID_ANY, u"BATTLE!", wx.DefaultPosition, wx.DefaultSize, 0 ) 
        self.m_buttonFire = wx.Button( self, wx.ID_ANY, u"Feuer frei!!!", wx.DefaultPosition, wx.DefaultSize, 0 ) 
        
        self.m_buttonFinishEditing.Bind( wx.EVT_BUTTON, self.refreshPlayerPanel )
        self.m_buttonBattleStart.Bind( wx.EVT_BUTTON, self.changeGameState )
        self.m_buttonFire.Bind( wx.EVT_BUTTON, self.refreshEnemyPanel )
        
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
        
        sizer.AddSpacer( 25 )
        
        lblList = ['Patrol ship', 'Frigate', 'Kruiser', 'Submarine', 'Aircraft carrier' ] 
		  
        self.radioBoxShipType = wx.RadioBox( self, label = 'Place ship:', pos = (80,10), choices = lblList, majorDimension = 1 ) 
        self.radioBoxShipType.Bind( wx.EVT_RADIOBOX, self.onRadioBoxShipType )        
        sizer.Add( self.radioBoxShipType )
        
        sizer.AddSpacer( 25 )
        
        lblList = ['vertical', 'horizontal'] 
		  
        self.radioBoxShipOrient = wx.RadioBox( self, label = 'Choose ship orientation:', pos = ( 80, 10 ), choices = lblList, majorDimension = 1 ) 
        self.radioBoxShipOrient.Bind( wx.EVT_RADIOBOX, self.onRadioBoxShipOrient )        
        sizer.Add( self.radioBoxShipOrient )
        
        self.SetSizer( sizer )
        
    #--------------------------------------------------------------------------------------------------------
        
    def onRadioBoxShipType( self, e ): 
    
        global shipType
  
        if self.radioBoxShipType.GetStringSelection() == "Patrol ship":
            
            shipType = "Patrol ship"
            print( self.radioBoxShipType.GetStringSelection(),' is clicked from Radio Box' )
            
        elif self.radioBoxShipType.GetStringSelection() == "Frigate":
            
            shipType = "Frigate"
            print( self.radioBoxShipType.GetStringSelection(),' is clicked from Radio Box' )
        
        elif self.radioBoxShipType.GetStringSelection() == "Kruiser":
            
            shipType = "Kruiser"
            print( self.radioBoxShipType.GetStringSelection(),' is clicked from Radio Box' )
            
        elif self.radioBoxShipType.GetStringSelection() == "Submarine":
            
            shipType = "Submarine"
            print( self.radioBoxShipType.GetStringSelection(),' is clicked from Radio Box' )
            
        elif self.radioBoxShipType.GetStringSelection() == "Aircraft carrier":
            
            shipType = "Aircraft carrier"
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
            
    #--------------------------------------------------------------------------------------------------------
    
    def changeGameState( self, event ):
        
        global gameState
        gameState = "battle"
    
    #--------------------------------------------------------------------------------------------------------
    
    def refreshPlayerPanel( self, event ):
        
        global gameField 
        global playerXHit
        global playerYHit
        
        self.panel1.refreshGrid()
        print( 'Refreshed player field:' )
        
        gameField.printMyField()
        
    #---------------------------------------------------------------------------------------------------------
            
    def refreshEnemyPanel( self, event ):
        
        global gameField 
        global playerXHit
        global playerYHit
        
        #self.panel1.refreshGrid()
        self.panel2.refreshGrid()
        print( 'fired...' )
        
        gameField.printField()
        
    
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
 
        self.panelOne = MyGridPanel(hSplitter)     
        self.panelTwo = EnemyGridPanel(hSplitter)            
        #self.panelTwo = GridPanel(hSplitter, "enemy_field")
        
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
        
    def paintGreen(self, x, y):
    
        self.panel.paint(x, y)
 
#====== MAIN ============================

app = wx.App(False)
frame = MainFrame()
frame.Show()
app.MainLoop()
