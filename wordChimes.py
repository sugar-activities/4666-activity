#! /usr/bin/env python

import pygame
from pygame.locals import *
import gtk
import os

MIXER_FREQ = 22050
MIXER_BITSIZE = -16
MIXER_CHANNELS = 2
MIXER_BUFFER = 4096
MIXER_VOLUME = 0.6

SCREENWIDTH = 1200
SCREENHEIGHT = 700
FPS = 20
ANIM_FRAME_TIME = 17
ANIM_SPEED_INCREASE = 1.5
ANIM_SPEED_START = 2.1
colorMod = 0

#the note object that will assend the screen
class Note():
    def __init__(self, image, Xcord,  Ycord, speed, keyData):
        self.speed = speed
        self.image = image
        self.keyData = keyData
        self.pos = image.get_rect().move(Xcord, Ycord)
        self.frame = 0
        self.subpixel = 0
        
    def move(self):
        self.pos = self.pos.move(0, -self.speed)
        self.subpixel += (self.speed * 10) % 10
        if self.subpixel > 9:
            self.pos = self.pos.move(0, -1)
            self.subpixel = self.subpixel % 10
        self.frame += 1
        
    def isDone(self):
        return self.frame >= ANIM_FRAME_TIME
        
    def play(this):
        this.keyData.playSound()
        
class KeyData:
    def __init__(this,  ascii,  imageFile,  soundFile, position):
        this.ascii = ascii
        this.imageFile = imageFile
        this.soundFile = soundFile
        this.sound = None
        this.position = position
    def loadSound(this):
        try:
            file = os.getcwd() + '/sound/' + this.soundFile
            this.sound = pygame.mixer.Sound(file)
        except:
            pass
    def playSound(this):
        if (this.sound != None):
            this.sound.play()
            
        
        
class WordChimes:
    letterMap = {".":KeyData('.','period.png', 'Period.ogg', 0), \
              ",":KeyData(',',',.png', 'comma.ogg', 1), \
              "'":KeyData('\'','\'.png', 'quotes.ogg', 1),  \
              "a":KeyData('a','01.png', 'A.ogg', 2), \
              "b":KeyData('b','02.png', 'B.ogg', 3), \
              "c":KeyData('c','03.png', 'C.ogg', 4), \
              "d":KeyData('d','04.png', 'D.ogg', 5), \
              "e":KeyData('e','05.png', 'E.ogg', 6), \
              "f":KeyData('f','06.png', 'F.ogg', 7), \
              "g":KeyData('g','07.png', 'G.ogg', 8), \
              "h":KeyData('h','08.png', 'H.ogg', 9), \
              "i":KeyData('i','09.png', 'I.ogg', 10), \
              "j":KeyData('j','10.png', 'J.ogg', 11), \
              "k":KeyData('k','11.png', 'K.ogg', 12), \
              "l":KeyData('l','12.png', 'L.ogg', 13), \
              "m":KeyData('m','13.png', 'M.ogg', 14), \
              "n":KeyData('n','14.png', 'N.ogg', 15), \
              "o":KeyData('o','15.png', 'O.ogg', 16), \
              "p":KeyData('p','16.png', 'P.ogg', 17), \
              "q":KeyData('q','17.png', 'Q.ogg', 18), \
              "r":KeyData('r','18.png', 'R.ogg', 19), \
              "s":KeyData('s','19.png', 'S.ogg', 20), \
              "t":KeyData('t','20.png', 'T.ogg', 21), \
              "u":KeyData('u','21.png', 'U.ogg', 22), \
              "v":KeyData('v','22.png', 'V.ogg', 23), \
              "w":KeyData('w','23.png', 'W.ogg', 24), \
              "x":KeyData('x','24.png', 'X.ogg', 25), \
              "y":KeyData('y','25.png', 'Y.ogg', 26), \
              "z":KeyData('z','26.png', 'Z.ogg', 27), \
              "/":KeyData('/','Qmark.png', '?.ogg', 28), \
              " ":KeyData(' ','transparent.png', None, 0)}
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.background = self.loadImage('mountainBG.png')
        self.letters = ""
        self.typedKeyData = []
        self.colorMod = 0
        self.bottomTiles = []
        self.screen = 0
        self.quit = False
        self.initMixer()
        self.initSounds()
        #pygame.key.set_repeat(200,  200)
        
        self.animating = False
        self.afterAnimating = False
        self.notes = None
        self.notesDone = []
        self.constantRefreshFrameCount = 0
        self.caretOn = True
        self.caretState = True
        self.caretFrame = 0
        self.hideCursor = False
            
    def initMixer(self):
        # Initialize mixer
        # The mixer is used by pygame to load and play the sound files
         pygame.mixer.init(MIXER_FREQ, MIXER_BITSIZE, MIXER_CHANNELS, MIXER_BUFFER)
         pygame.mixer.music.set_volume(MIXER_VOLUME)
    
    def initSounds(this):
        for keyCode in this.letterMap:
            this.letterMap[keyCode].loadSound()
            
    def initTyping(self):
        self.colorMod = 0
        #this also clears the whole screen
        self.renewCaret()
        #update the display
        pygame.display.update()
        
    def initAnimating(self):
        self.animating = True
        self.notes = []
        self.notesDone = []
        self.colorMod = 0
        self.currentNote = 0
        self.hideCursor = True
        for x in range(len(self.letters)):
            if ord(self.letters[x]) == 32:
                noteImage = self.loadLetter("transparent.png")
            else:
                noteImage = self.loadLetter("Note.png")
            note = Note(noteImage, x*40+10, self.screen.get_height() - 50,  3,  self.letterMap[self.letters[x]])
            note.speed = ANIM_SPEED_START + self.letterMap[self.letters[x]].position * ANIM_SPEED_INCREASE
            self.notes.append(note)
            self.colorMod += 1
    
    def run(self):
        #get screen
        self.screen = pygame.display.get_surface()
        self.initTyping()
        #update the display
        pygame.display.flip()
        #print screen.get_height()
        
        #start the game loop
        while not self.quit:
            
            self.constantRefreshFrameCount += 1
            self.caretFrame += 1
            if (self.caretFrame > 10):
                self.caretState = not self.caretState
                self.caretFrame = 0
                self.updateCaret()
            if (self.constantRefreshFrameCount > 20):
                self.doPaint = True
                self.constantRefreshFrameCount = 0
            
            #Yield to GTK?
            while gtk.events_pending():
                gtk.main_iteration()
                
            if self.animating:
                self.doPaint = True
                note = self.notes[self.currentNote]
                note.move()
                #clear the whole screen
                self.screen.blit(self.background, (0, 0))
                #draw the moving note
                self.screen.blit(note.image, note.pos)
                
                if self.currentNote >= len(self.notes):
                    self.stopAnimating()
                #redraw the bottom letters that have reached their destination
                for letterTile in self.bottomTiles:
                    self.screen.blit(letterTile.image, letterTile.pos) 
                #redraw the notes that have reached there destination
                for finalNote in self.notesDone:
                    self.screen.blit(finalNote.image, finalNote.pos)
                if note.isDone():
                    note.play()
                    self.notesDone.append(note)
                    self.currentNote += 1
                    if self.currentNote >= len(self.notes):
                        self.stopAnimating()
                
            #Event processing loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                    break
                elif event.type == KEYDOWN:
                    self.doKeyDown(event)
            #End of event processing loop
            
            if self.doPaint:
                pygame.display.update()
                self.doPaint = False
            self.clock.tick(FPS)
        print "quiting"    
        #End of main loop
        pygame.quit()
                
    #Processes all KEYDOWN events
    def doKeyDown(self,  event):
        #Don't worry about any other keypresses while animating
        if self.animating == True:
            if (event.key == K_ESCAPE):
                self.stopAnimating()
                self.afterAnimating = False
                self.initTyping()
                self.renewCaret()
            return
        self.hideCursor = False
        #If a button has been pressed after animating is finished, then start fresh
        if self.afterAnimating:
            self.initTyping()
            self.afterAnimating = False
        #if len(self.letters) == 0:
            #clear the whole screen
        #    self.screen.blit(self.background, (0, 0))
            #update the display
        #    pygame.display.update()
        if len(self.letters) < 29:
            if event.unicode in self.letterMap:
                self.letters += event.unicode
                self.addTile(self.screen,  self.bottomTiles,  event.unicode)
        if event.key == K_BACKSPACE:
            if len(self.letters) > 0:
                self.colorMod -= 1
                self.letters = self.letters[:-1]
                self.bottomTiles.pop()
                self.redrawTiles(self.screen,  self.background, self.bottomTiles)
        elif (event.key == K_RETURN):
            if (len(self.bottomTiles)):
                self.initAnimating()
        if (not self.animating):
            self.renewCaret()
    def renewCaret(this):
        this.caretState = True
        this.caretFrame = 0
        this.updateCaret()
    def updateCaret(this):
        if (not this.caretOn):
            return
        if (this.hideCursor):
            return
        if (this.caretState):
            this.redrawTiles(this.screen, this.background, this.bottomTiles)
            pygame.draw.line(this.screen, (0, 0, 0), (((len(this.bottomTiles) )*40+10), this.screen.get_height() - 20), (((len(this.bottomTiles) )*40+30), this.screen.get_height() - 20), 4)
        else:
            this.redrawTiles(this.screen, this.background, this.bottomTiles)
        this.doPaint = True
    
    def stopAnimating(self):
        self.animating = False
        self.afterAnimating = True
        self.letters = ""
        self.notes = None
        self.notesDone = None
        self.bottomTiles = []

    def loadImage(this,  name):
        path = os.path.join(os.path.dirname(__file__), 'Images', name)
        image = pygame.image.load(path)
        return image
    
    #
    #getPath(this) : String
    #Uses the current character position to figure out the proper
    #subfolder to use for loading images of a certain color.
    #
    #Returns:
    #   A String representing a single folder name.
    #
    def getPath(this):
        colorFile = ""
        colorModTemp = this.colorMod  % 8
        
        if colorModTemp == 0:
            colorFile = "LettersBlue"
        elif colorModTemp == 1:
            colorFile = "LettersGreen"
        elif colorModTemp == 2:
            colorFile = "LettersOrange"
        elif colorModTemp == 3:
            colorFile = "LettersGrey"
        elif colorModTemp == 4:
            colorFile = "LettersPurple"
        elif colorModTemp == 5:
            colorFile = "LettersRed"
        elif colorModTemp == 6:
            colorFile = "LettersTeal"
        elif colorModTemp == 7:
            colorFile = "LettersYellow"
        return colorFile
        
    #loadLetter(self, fileName) : Surface
    #Load a letter image file from storage into memory.
    #
    #Parameters:
    #   fileName
    #       The desired image's file name
    #
    #Returns:
    #   A Pygame Surface object containing the letter image.
    #
    def loadLetter(self,  fileName):
        colorFolder = self.getPath()
        #self.colorMod = 1
        path = os.path.join(os.path.dirname(__file__), 'LettersColor', colorFolder, fileName)
        return pygame.image.load(path) 
    
    #
    #redrawTiles(self, screen, background, bottomTiles) : None
    #
    def redrawTiles(self,  screen,  background,  bottomTiles):
        #clear the whole screen
        screen.blit(background, (0, 0))
        #Redraw the bottom letters that have reached their destination.
        for letterTile in bottomTiles:
            screen.blit(letterTile.image, letterTile.pos)
        #Mark the display for updating.
        self.doPaint = True
        
        
    def addTile(this,  screen,  bottomTiles,  unicode):
        
        #load the image
        letterTileImage = this.loadLetter(this.letterMap[unicode].imageFile)
        letterTile = Note(letterTileImage,  (len(bottomTiles)*40+10), screen.get_height() - 50, 1, this.letterMap[unicode])
        #draw the image
        screen.blit(letterTile.image, letterTile.pos)
        #add to array
        bottomTiles.append(letterTile)
        #update the display
        this.doPaint = True
        this.colorMod += 1
#first to run when program starts
def main():    
    pygame.init()
    pygame.display.set_mode((1200, 700), pygame.RESIZABLE)
    game = WordChimes()
    game.run()
    
if __name__ == '__main__': 
    main()
