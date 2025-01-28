import sqlite3
import csv
from datetime import date
import math
import matplotlib.pyplot as plt
import numpy as np

 #connect or create if doesn’t exist (same folder)
conn = sqlite3.connect('music_database.db')

#create database cursor - enables traversal of records in db
cur = conn.cursor()

def mainMenu():
    selectionCheck = True
    print('welcome to our music database!')
    while selectionCheck:
        print('please select from the following options:\na) Edit\nb) Algorithms\nc) Create Queries\nd) Visualization\ne) End Program')
        mainSelect = input('=>')
        if mainSelect.capitalize() == 'A':
            #selectionCheck = False
            editMenu()
        elif mainSelect.capitalize() == 'B':
            #selectionCheck = False
            algorithmMenu()

        elif mainSelect.capitalize() == 'C':
            #selectionCheck = False
            queryMenu()

        elif mainSelect.capitalize() == 'D':
            #selectionCheck = False
            visualizationMenu()

        elif mainSelect.capitalize() == 'E':
            selectionCheck = False
            endProgram()
        else:
            print("not a correct selection, try again")
            mainSelect = input('=>')
            selectionCheck = True

#edit menu where user can choose to edit the database, this includes: displaying database tables, add to tables, remove from tables and modify tables
def editMenu():
    
    print('please select one of the following choices:\na) display table\nb) add to table\nc) remove from table\nd) modify table')
    editSelection = input('=>')
    userCheck = True
    while userCheck:
        if editSelection.capitalize() == 'A':
            #call the display function 
            userCheck = False
            display()
            
        elif editSelection.capitalize() == 'B':
            #call the add function
            userCheck = False
            add()
        elif editSelection.capitalize() == 'C':
            #call the remove function 
            userCheck = False
            remove()
        elif editSelection.capitalize() == 'D':
            #call the modify function
            userCheck = False
            modify()
        else:
            print('not a correct selection, try again')
            editSelection = input('=>')
            userCheck = True

def display():
     #first, connect and read all data from tables
    cur.execute('SELECT * FROM Artists')
    artists = cur.fetchall()
    cur.execute('SELECT * FROM Albums')
    albums = cur.fetchall()
    cur.execute('SELECT * FROM Songs')
    songs = cur.fetchall()
    print('select which table to display\na) Artists\nb) Albums\nc) Songs')
    userInput = input('=>')
    userCheck = True
    if userCheck:
        if userInput.capitalize() == 'A':
            userCheck = False
            printArtistString = ''
            for artist in artists:
                artistIndex = len(artist)
                for ai in range(artistIndex):
                    if ai < (artistIndex-1):
                        printArtistString += str(artist[ai]) + ', '
                    if ai == (artistIndex-1):
                        printArtistString += str(artist[ai]) + '\n'
            print(printArtistString)

        elif userInput.capitalize() == 'B':
            userCheck = False
            printAlbumString = ''
            for album in albums:
                albumIndex = len(album)
                for alI in range(albumIndex):
                    if alI < (albumIndex-1):
                        printAlbumString += str(album[alI]) + ', '
                    if alI == (albumIndex-1):
                        printAlbumString += str(album[alI]) + '\n'
            print(printAlbumString)
                
            
        elif userInput.capitalize() == 'C':
            userCheck = False
            printSongString = ''
            for song in songs: 
                songIndex = len(song)
                for si in range(songIndex):
                    if si < (songIndex-1):
                        printSongString += str(song[si]) + ', '
                    if si == (songIndex -1):
                        printSongString += str(song[si]) + '\n'
            print(printSongString)
                
        else:
            print('incorrect selection! try again')
            userInput = input('=>')
            userCheck = True

def add():
    print('which table do you wish to add to?\na) artist\nb) album\nc) songs')
    userChoice = input('=>')
    #check the user input
    userCheck = True
    while userCheck:
        if userChoice.capitalize() == 'A':
           
            userCheck = False
            addArtist()

        elif userChoice.capitalize() == 'B':
            userCheck = False
            addAlbum()

        elif userChoice.capitalize() == 'C':
            userCheck = False
            addSong()

        else:
            print("incorrect choice. try again!")
            userChoice = input('=>')
            userCheck = True

def addArtist():
    select = 'SELECT ArtistID FROM Artists'
    cur.execute(select)
    artistIDs =  cur.fetchall()
    #find the last id then add 1 to this value for the new artist
    length = len(artistIDs)
    lastID = int(artistIDs[length-1][0])
    newArtistID= lastID+1
    print('Ok. Here a few questions for you.\nArtist Name?')
    artistName = input('=>')
    print('Great! Lets continue\nLabel the Artist is apart of?')
    artistLabel = input('=>')
    print('Fantastic. What city is this artist from?')
    artistCity = input('=>')
    print('Great Place!\nAnd which country?')
    artistCounty = input('=>')
    print('Wonderful, finally, which genre is this artist?')
    artistGenre = input('=>')

    insert = f'''INSERT INTO Artists('ArtistID','Name','Label','BirthPlace','Country','Genre')
                VALUES ("{newArtistID}","{artistName}","{artistLabel}","{artistCity}","{artistCounty}","{artistGenre}")'''
    cur.execute(insert)
    conn.commit()

def checkArtist(inputArtistName):
    selectArtist = 'SELECT ArtistID, Name FROM Artists'
    cur.execute(selectArtist)
    artistValues = cur.fetchall()
    returnartistID = 0
    #run through the values lists to see if there is an artist with the input name
    artistCheck = False
    for artistVal in artistValues:
        artistID = artistVal[0]
        artistName = artistVal[1]
        if artistName == inputArtistName:
            artistCheck = True
            returnartistID = int(artistID)
            break          
        else:
            artistCheck = False
    
    if artistCheck:
        return returnartistID
    else:
        return 0 
                


def addAlbum():
    select = 'SELECT AlbumID FROM Albums'
    cur.execute(select)
    albumIDs =  cur.fetchall()
    #find the last id then add 1 to this value for the new artist
    length = len(albumIDs)
    lastID = int(albumIDs[length-1][0])
    newAlbumID= lastID+1
    #get the artist name
    print('Ok. Here a few questions for you.\nArtist Name?')
    artistName = input('=>')
    artistID = checkArtist(artistName)
    if artistID > 0:
        print('Great! That artist is already in our Data!\nWhats the Album Name')
        albumName = input('=>')
        #check to see if the album already exists in the database this will be case insensitive 
        #first, select all album names that exist for the artist ID
        #NOTE: CHANGE sql statement to have name be ArtistID in main file, along with in csv_to_sql
        selectAlbums = f'SELECT AlbumName FROM Albums WHERE ArtistID = "{artistID}"'
        cur.execute(selectAlbums)
        compareAlbums = cur.fetchall()
        compareCheck = True
        for compare in compareAlbums:
            toCompare = compare[0]
            if toCompare.lower() == albumName.lower():
                print('that album already exists in the database')
                compareCheck = False
                break
            
                
        if compareCheck:
            print('Fantastic. How many songs?')
            albumNumSongs = input('=>')
            print('Great!\nWhat year was the album released?')
            albumYear = input('=>')
            print('Wonderful, finally, how long is the album? In minutes.')
            albumRuntime = input('=>')
            insert = f'''INSERT INTO Albums('AlbumID','ArtistID', 'AlbumName','NumSongs','YearReleased','RunTime')
                    VALUES ("{newAlbumID}","{artistID}","{albumName}","{albumNumSongs}","{albumYear}","{albumRuntime}")'''
            cur.execute(insert)
            conn.commit()

            print("do you wish to add the songs of this album (y/n)")
            userChoice= input('=>')
            #check the user choice
            if userChoice.capitalize() == 'Y':
                addAlbumSongs(artistID, newAlbumID, albumNumSongs)
                #otherwise do nothing
        
    else:
        print("that artist does not exist, add that artist then try again!")

#add song will allow for the user to add only one song to the database
#this will be called in the main menu
def addSong():
    select = 'SELECT SongID FROM Songs'
    cur.execute(select)
    songIDs =  cur.fetchall()
    #find the last id then add 1 to this value for the new artist
    length = len(songIDs)
    lastID = int(songIDs[length-1][0])
    newSongID = lastID+1
    print('what is artist of this song?')
    userArtist= input('=>')
    #compare the artist name to all the artist names
    artistCheck = False
    selectArist = 'SELECT ArtistID, Name FROM Artists'
    cur.execute(selectArist)
    artistInfo= cur.fetchall()
    insertID = 0
    for info in artistInfo:
        artistID = info[0]
        name = info[1]
        if name.lower() == userArtist.lower():
            #the artist exists in the database
            artistCheck = True
            insertID = artistID
            break

    if artistCheck:
        print("Great! the artist exists in our data!\n\nWe have a few questions about the song\nFirst, what is the song name?")
        #we are going to assume there is no album for the song 
        songName = input('=>')
        print('Fantastic!\nwe have a we questions about the song length:')
        userCheck = False
        try:
            userInputMins = input('minutes: ')
            if int(userInputMins) > 0:
                mins = userInputMins
                userCheck = True
        except ValueError:
            print('invalid input, please enter an integer')
           
                
        try:
            userInputSecs = input('remaining seconds: ')
            if int(userInputSecs) >= 0:
                secs = userInputSecs
                userCheck = True       
        except ValueError:
            print('invalid input. please try again\n')
            
        if userCheck:
            runtime = (int(mins)*60)+(int(secs))
            #at this moment the albumID Will be 0, in the future it may be wise to change this to NULL
            insert =f'''INSERT INTO Songs('SongID','AlbumID','ArtistID','SongName','Runtime')
                    VALUES ("{newSongID}","{0}","{insertID}","{songName}","{runtime}")'''
            cur.execute(insert)
            conn.commit()
        
    else:
        print("The artist does not exist in our data\nTry Again after adding the artist!")



#add songs will allow the user to add a whole albumn of songs to the database 
#this will be call in addAlbum()
def addAlbumSongs(artistID, albumID, numSongs):
    select = 'SELECT SongID FROM Songs'
    cur.execute(select)
    songIDs =  cur.fetchall()
    #find the last id then add 1 to this value for the new artist
    length = len(songIDs)
    lastID = int(songIDs[length-1][0])
    #this value will be the first ID of the new list of songs
    firstNewSongID = lastID+1
    #create an empty list 
    newSongs = []
    songlengthMins = []
    songlengthSec = []
    #add songs to the list with user input
    print('Great!\n We are going to ask you to enter some information\nEnter the song titles first\nThen, the minutes of the song\nAlong with the remaining seconds')
    for song in range(int(numSongs)):
        print('\nsong '+ str(song+1) +':')
        song = input('name: ')
        newSongs.append(song)
        try:
            mins = input('minutes: ')
            if int(mins) > 0:
                songlengthMins.append(mins)
        except ValueError:
            print('invalid input, please enter an integer')
            #exit the loop
            exit()
        
        try:
            secs = input('remaining seconds: ')
            if int(secs) >= 0:
                songlengthSec.append(secs)
        except ValueError:
            print('error saving the seconds, please try again')
            #exit the loop
            exit()
        #check user input to make sure mins and seconds are integers
        
         
        
    #finally we can add all the information into the song database
    for index in range(int(numSongs)):
        #calculate the runtime
        runtime = (int(songlengthMins[index])*60)+int(songlengthSec[index])
        songName = newSongs[index]
        insert_records=f'''INSERT INTO Songs('SongID','AlbumID','ArtistID','SongName','Runtime')
                VALUES ("{firstNewSongID}","{albumID}","{artistID}","{songName}","{runtime}")'''
        cur.execute(insert_records)
        conn.commit()
        #add one value to songID
        firstNewSongID+= 1


def remove():
    print('which table do you wish to remove from?\na) artist\nb) album\nc) songs')
    userChoice = input('=>')
    #check the user input
    userCheck = True
    while userCheck:
        if userChoice.capitalize() == 'A':
            userCheck = False
            removeArtist()

        elif userChoice.capitalize() == 'B':
            userCheck = False
            removeAlbum()

        elif userChoice.capitalize() == 'C':
            userCheck = False
            removeSong()

        else:
            print("incorrect choice. try again!")
            userChoice = input('=>')
            userCheck = True

def removeArtist():
    print("Which artist do you wish to remove?")
    toRemove = input('=>')
    #check to see if the artist exists in the database
    artistID =checkArtist(toRemove)
    if artistID > 0:
        remove= f'''DELETE FROM Artists WHERE ArtistID = "{artistID}"'''
        cur.execute(remove)
        conn.commit()
          #check if the user wants to remove all albums and songs from artist
        print("do you wish to remove all references of this artist? (y/n)")
        userChoice= input('=>')
        #check the user choice
        if userChoice.capitalize() == 'Y':
            removeArtistRef(artistID)
            #otherwise do nothing
    else:
        print('the artist does not exist in the database!')
          

def removeArtistRef(artistID):
  
    #find the album names of the artist 
    selectAlbums = f'SELECT AlbumID, AlbumName FROM Albums WHERE ArtistID = "{artistID}"'
    cur.execute(selectAlbums)
    compareAlbums = cur.fetchall()
    compareCheck = False
    albumIDs= []
    albumNames =[]
    for compare in compareAlbums:
        albumNames.append(compare[1])
        albumIDs.append(compare[0])
        compareCheck = True
        

    if compareCheck:
        for index in range(len(albumIDs)):
            remove= f'''DELETE FROM Albums WHERE AlbumID = "{albumIDs[index]}" AND ArtistID = "{artistID}"'''
            cur.execute(remove)
            conn.commit()

            print(f'do you want to remove the corresponding songs from {albumNames[index]}? (y/n)')
            userChoice = input('=>')
            if userChoice.capitalize() == 'Y':
                removeAlbumSongs(artistID,id)
        
    else:
        print('the album does not exist in the database!')


def removeAlbum():
    print('which albumn do you wish to remove?')
    albumToRemove = input('=>')
    print('who is the artist of the album?')
    artistToRemove = input('=>')
    artistID = checkArtist(artistToRemove)

    #find the album names of the artist 
    selectAlbums = f'SELECT AlbumID, AlbumName FROM Albums WHERE ArtistID = "{artistID}"'
    cur.execute(selectAlbums)
    compareAlbums = cur.fetchall()
    compareCheck = False
    albumID= 0
    for compare in compareAlbums:
        albumName = compare[1]
        if albumName.lower() == albumToRemove.lower():
            albumID = compare[0]
            compareCheck = True
            break
    
    if compareCheck:
        remove= f'''DELETE FROM Albums WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'''
        cur.execute(remove)
        conn.commit()

        print('do you want to remove the corresponding songs to this album? (y/n)')
        userChoice = input('=>')
        if userChoice.capitalize() == 'Y':
            removeAlbumSongs(artistID,albumID)
        
    else:
        print('the album does not exist in the database!')


def removeAlbumSongs(artistID,albumID):
    songsID = []
    selectSongs = f'SELECT SongID FROM Songs WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
    cur.execute(selectSongs)
    songs = cur.fetchall()
    for song in songs:
        songsID.append(song[0])
    
    for songID in songsID:
        remove = f'''DELETE FROM Songs WHERE SongID = "{songID}" AND AlbumID = "{albumID}" AND ArtistID = "{artistID}"'''
        cur.execute(remove)
        conn.commit()

def removeSong():
    print('which song do you wish to remove?')
    songToRemove = input('=>')
    print('who is the artist of the song?')
    artistToRemove = input('=>')
    artistID = checkArtist(artistToRemove)

    if artistID > 0:
        #find the album names of the artist 
        selectSongs = f'SELECT SongID, SongName FROM Songs WHERE ArtistID = "{artistID}"'
        cur.execute(selectSongs)
        compareSongs = cur.fetchall()
        compareCheck = False
        songID= 0
        for compare in compareSongs:
            songName = compare[1]
            if songName.lower() == songToRemove.lower():
                songID = compare[0]
                compareCheck = True
                break
        
        if compareCheck:
            remove= f'''DELETE FROM Songs WHERE SongID = "{songID}" AND ArtistID = "{artistID}"'''
            cur.execute(remove)
            conn.commit()
    else:
        print('the arist and song does not exist in our data')

def modify():
    print('which table do you wish to modify from?\na) artist\nb) album\nc) songs')
    userChoice = input('=>')
    #check the user input
    userCheck = True
    while userCheck:
        if userChoice.capitalize() == 'A':
            userCheck = False
            modifyArtist()

        elif userChoice.capitalize() == 'B':
            userCheck = False
            modifyAlbum()

        elif userChoice.capitalize() == 'C':
            userCheck = False
            modifySong()

        else:
            print("incorrect choice. try again!")
            userChoice = input('=>')
            userCheck = True

def modifyArtist():
    print('which artist do you wish to update?')
    artistSelect = input('=>')
    artistID = checkArtist(artistSelect)
    if artistID > 0:
        print('great! that artist exists in our data\nwhat do you wish to modify?\na)Artist Name\nb)Label\nc)City\nd)Country\ne)Genre')
        userChoice = input('=>')
        if userChoice.capitalize() == 'A':
            print('OK. You chose Artist Name\nWhat do you wish to modify it to?')
            newName = input('=>')
            updateName = f'UPDATE Artists SET Name = "{newName}" WHERE ArtistID = "{artistID}"'
            cur.execute(updateName)
            conn.commit()
        elif userChoice.capitalize() == 'B':
            print('OK. You chose Label\nWhat do you wish to modify it to?')
            newLabel = input('=>')
            updateLabel = f'UPDATE Artists SET Label = "{newLabel}" WHERE ArtistID = "{artistID}"'
            cur.execute(updateLabel)
            conn.commit()
        elif userChoice.capitalize() == 'C':
            print('OK. You chose City, State\nWhat do you wish to modify it to?\nUse the format City, State')
            newCity = input('=>')
            updateCity = f'UPDATE Artists SET BirthPlace = "{newCity}" WHERE ArtistID = "{artistID}"'
            cur.execute(updateCity)
            conn.commit()
        elif userChoice.capitalize() == 'D':
            print('OK. You chose Country\nWhat do you wish to modify it to?')
            newCountry = input('=>')
            updateCountry = f'UPDATE Artists SET Country = "{newCountry}" WHERE ArtistID = "{artistID}"'
            cur.execute(updateCountry)
            conn.commit()
        elif userChoice.capitalize() == 'E':
            print('OK. You chose Genre\nWhat do you wish to modify it to?')
            newGenre = input('=>')
            updateGenre = f'UPDATE Artists SET Genre = "{newGenre}" WHERE ArtistID = "{artistID}"'
            cur.execute(updateGenre)
            conn.commit()
        else:
            print('incorrect selection, you will not be able to modify the artist')
    else:
        print('the artist does not exists in our data')

def modifyAlbum():
    print('which albumn do you wish to modify?')
    albumToRemove = input('=>')
    print('who is the artist of the album?')
    artistToRemove = input('=>')
    artistID = checkArtist(artistToRemove)

    compareCheck = False
    #find the album names of the artist 
    selectAlbums = f'SELECT AlbumID, AlbumName FROM Albums WHERE ArtistID = "{artistID}"'
    cur.execute(selectAlbums)
    compareAlbums = cur.fetchall()
    for compare in compareAlbums:
        albumName = compare[1]
        if albumName.lower() == albumToRemove.lower():
            albumID = compare[0]
            compareCheck = True
            break
    
    if compareCheck:
        print("great.\nThis album exists in our data\nWhat do you wish to modify?\na)Album Name\nb)Number of Songs\nc)Year Released\nRuntime")
        userChoice = input('=>')
        if userChoice.capitalize() == 'A':
            print('OK. You chose Album Name\nWhat do you wish to modify it to?')
            newName = input('=>')
            updateName = f'UPDATE Albums SET AlbumName = "{newName}" WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
            cur.execute(updateName)
            conn.commit()
        elif userChoice.capitalize() == 'B':
            print('OK. You chose Number of Songs\nWhat do you wish to modify it to?')
            newNum = input('=>')
            updateNumber = f'UPDATE Albums SET NumSongs = "{newNum}" WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
            cur.execute(updateNumber)
            conn.commit()
        elif userChoice.capitalize() == 'C':
            print('OK. You chose Year Released\nWhat do you wish to modify it to?')
            newYear = input('=>')
            updateYear = f'UPDATE Albums SET YearReleased = "{newYear}" WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
            cur.execute(updateYear)
            conn.commit()
        elif userChoice.capitalize() == 'D':
            print('OK. You chose Runtime in minutes\nWhat do you wish to modify it to? ')
            newRuntime = input('=>')
            updateCountry = f'UPDATE Albums SET Runtime = "{newRuntime}" WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
            cur.execute(updateCountry)
            conn.commit()
        else:
            print('incorrect selection, you will not be able to modify the the album')

        print('do you want to remove the corresponding songs to this album? (y/n)')
        userChoice = input('=>')
        if userChoice.capitalize() == 'Y':
            modifyAlbumSongs(artistID,albumID)
        
    else:
        print('the album does not exist in our data!')

def modifyAlbumSongs(artistID, albumID):
    #get the number of songs in the album
    selectSongs= f'SELECT SongID, SongName FROM Songs WHERE AlbumID = "{albumID}" AND ArtistID = "{artistID}"'
    cur.execute(selectSongs)
    songs = cur.fetchall()
    count = 1
    songNameList = []
    songIDList = []
    print('which song do you wish to modify?')
    for song in songs:
        songName = song[1]
        songID = song[0]
        print(str(count)+": " + songName)
        songNameList.append(songName)
        songIDList.append(songID)
        count+=1
    
    userChoice = input('=>')
    if int(userChoice) > 0 and int(userChoice) < count:
        #get the corresponding song name and ID from the song list
        songNameChoice = songNameList[int(userChoice) -1]
        songIDChoice =songIDList[int(userChoice) -1]
    
    print('what do you wish to modify?\na)Song Name\nb)Runtime')
    AorB = input('=>')
    if AorB.capitalize() == 'A':
        print('OK. You chose Song Name\nWhat do you wish to modify it to? ')
        newSongName = input('=>')
        updateSongName = f'UPDATE Songs SET SongName = "{newSongName}" WHERE SongID = "{songIDChoice}"'
        cur.execute(updateSongName)
        conn.commit()
    elif AorB.capitalize() == 'B':
        print('OK. You chose runtime\nHow many minutes will you modify it to? ')
        newSongMins = input('=>')
        print('great. how many remaining seconds?')
        newSongSecs = input('=>')
        newSongRuntime = (int(newSongMins)*60) + newSongSecs
        updateSongRuntime = f'UPDATE Songs SET Runtime = "{newSongRuntime}" WHERE SongID = "{songIDChoice}"'
        cur.execute(updateSongRuntime)
        conn.commit()

    else:
        print('incorrect selection, you will not modify the song')


def modifySong():
    print('which song do you wish to modify?')
    songToModify = input('=>')
    print('who is the artist of the song?')
    artist = input('=>')
    artistID = checkArtist(artist)

    if artistID > 0:
        #find the album names of the artist 
        selectSongs = f'SELECT SongID, SongName FROM Songs WHERE ArtistID = "{artistID}"'
        cur.execute(selectSongs)
        compareSongs = cur.fetchall()
        compareCheck = False
        songID= 0
        for compare in compareSongs:
            songName = compare[1]
            if songName.lower() == songToModify.lower():
                songID = compare[0]
                compareCheck = True
                break
        
        if compareCheck:
            print('what do you wish to modify?\na)Song Name\nb)Runtime')
            AorB = input('=>')
            if AorB.capitalize() == 'A':
                print('OK. You chose Song Name\nWhat do you wish to modify it to? ')
                newSongName = input('=>')
                updateSongName = f'UPDATE Songs SET SongName = "{newSongName}" WHERE SongID = "{songID}"'
                cur.execute(updateSongName)
                conn.commit()
            elif AorB.capitalize() == 'B':
                print('OK. You chose runtime\nHow many minutes will you modify it to? ')
                newSongMins = input('=>')
                print('great. how many remaining seconds?')
                newSongSecs = input('=>')
                newSongRuntime = (int(newSongMins)*60) + newSongSecs
                updateSongRuntime = f'UPDATE Songs SET Runtime = "{newSongRuntime}" WHERE SongID = "{songID}"'
                cur.execute(updateSongRuntime)
                conn.commit()
            else:
                print('the selected song does not exist in our data')
    else:
        print('the artist and song does not exist in our data')
    
#algorithm menu will allow users to choose which algorithm to look at
def algorithmMenu():
    print('algoritm menu')
    print('select which values to analyze:\na)number of songs in album\nb)length of songs\nc)years of releases\nd)album runtimes\ne)exit')
    userCheck = True
    while userCheck:
        userChoice = input('=>')
        if userCheck:
            if userChoice.capitalize() == 'A':
                valid=False
                while valid==False:
                    print("Select Algorithm:\na)mean\nb)median\nc)max\nd)min\ne)standard deviation")
                    useralg=input('=>')
                    if useralg.capitalize()=='A':
                        valid=True
                        print("mean number of songs per album:")
                        mean=cur.execute("SELECT AVG(NumSongs) FROM Albums")
                        for item in mean:
                            print(item[0])
                    elif useralg.capitalize()=='B':
                        valid=True
                        print("median number of songs per album:")
                        print(median(userChoice))
                    elif useralg.capitalize()=='C':
                        valid=True
                        print("maximum number of songs per album:")
                        max=cur.execute("SELECT Albumname, MAX(NumSongs) FROM Albums")
                        for item in max:
                            print("{0}:{1} songs".format(item[0], item[1]))
                    elif useralg.capitalize()=='D':
                        valid=True
                        print("minimum number of songs per album:")
                        min=cur.execute("SELECT AlbumName, MIN(NumSongs) FROM Albums")
                        for item in min:
                            print("{0}:{1} songs".format(item[0], item[1]))
                    elif useralg.capitalize()=='E':
                        valid=True
                        print("standard deviation of songs per album:")
                        print(stdev(userChoice))
                    else:
                        print("invalid. enter again.")
                userCheck = False
            elif userChoice.capitalize() == 'B':
                valid=False
                while valid==False:
                    print("Select Algorithm:\na)mean\nb)median\nc)max\nd)min\ne)standard deviation")
                    useralg=input('=>')
                    if useralg.capitalize()=='A':
                        valid=True
                        print("mean length of songs (seconds):")
                        mean=cur.execute("SELECT AVG(Songs.Runtime) FROM Songs")
                        for item in mean:
                            print(item[0])
                    elif useralg.capitalize()=='B':
                        valid=True
                        print("median length of songs (seconds):")
                        print(median(userChoice))
                    elif useralg.capitalize()=='C':
                        valid=True
                        print("maximum length of songs (seconds):")
                        max=cur.execute("SELECT SongName, MAX(Songs.Runtime) FROM Songs")
                        for item in max:
                            print("{0}:{1} seconds".format(item[0], item[1]))
                    elif useralg.capitalize()=='D':
                        valid=True
                        print("minimum length of songs (seconds)")
                        min=cur.execute("SELECT SongName, MIN(Songs.Runtime) FROM Songs")
                        for item in min:
                            print("{0}:{1} seconds".format(item[0], item[1]))
                    elif useralg.capitalize()=='E':
                        valid=True
                        print("standard deviation of length of songs (seconds):")
                        print(stdev(userChoice))
                    else:
                        print("invalid. enter again.")
                userCheck = False
            elif userChoice.capitalize() == 'C':
                valid=False
                while valid==False:
                    print("Select Algorithm:\na)mean\nb)median\nc)max\nd)min\ne)standard deviation")
                    useralg=input('=>')
                    if useralg.capitalize()=='A':
                        valid=True
                        print("mean year of releases:")
                        mean=cur.execute("SELECT AVG(YearReleased) FROM Albums")
                        for item in mean:
                            print(item[0])
                    elif useralg.capitalize()=='B':
                        valid=True
                        print("median year of releases:")
                        print(median(userChoice))
                    elif useralg.capitalize()=='C':
                        valid=True
                        print("maximum year of releases:")
                        max=cur.execute("SELECT AlbumName, MAX(YearReleased) FROM Albums")
                        for item in max:
                            print("{0}:{1}".format(item[0], item[1]))
                    elif useralg.capitalize()=='D':
                        valid=True
                        print("minimum year of releases:")
                        min=cur.execute("SELECT AlbumName, MIN(YearReleased) FROM Albums")
                        for item in min:
                            print("{0}:{1}".format(item[0], item[1]))
                    elif useralg.capitalize()=='E':
                        valid=True
                        print("standard deviation of release years:")
                        print(stdev(userChoice))
                    else:
                        print("invalid. enter again.")
                userCheck = False
            elif userChoice.capitalize() == 'D':
                valid=False
                while valid==False:
                    print("Select Algorithm:\na)mean\nb)median\nc)max\nd)min\ne)standard deviation")
                    useralg=input('=>')
                    if useralg.capitalize()=='A':
                        valid=True
                        print("mean album runtime (minutes):")
                        mean=cur.execute("SELECT AVG(Albums.Runtime) FROM Albums")
                        for item in mean:
                            print(item[0])
                    elif useralg.capitalize()=='B':
                        valid=True
                        print("median album runtime (minutes):")
                        print(median(userChoice))
                    elif useralg.capitalize()=='C':
                        valid=True
                        print("maximum album runtime (minutes):")
                        max=cur.execute("SELECT AlbumName, MAX(Albums.Runtime) FROM Albums")
                        for item in max:
                            print("{0}:{1} minutes".format(item[0], item[1]))
                    elif useralg.capitalize()=='D':
                        valid=True
                        print("minimum album runtime (minutes):")
                        min=cur.execute("SELECT AlbumName, MIN(Albums.Runtime) FROM Albums")
                        for item in min:
                            print("{0}:{1} minutes".format(item[0], item[1]))
                    elif useralg.capitalize()=='E':
                        valid=True
                        print("standard deviation of album runtimes (minutes):")
                        print(stdev(userChoice))
                    else:
                        print("invalid. enter again.")
                userCheck = False
            elif userChoice.capitalize()=='E':
                usercheck=False
            else:
                print("incorrect choice. try again!")
                userCheck = True

def median(choice):
    if choice.capitalize()=='A':
        column=cur.execute("SELECT NumSongs FROM Albums ORDER BY NumSongs DESC")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        midpoint=len(mylist)//2
        return mylist[midpoint]
    elif choice.capitalize()=='B':
        column=cur.execute("SELECT Songs.Runtime FROM Songs ORDER BY Songs.Runtime DESC")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        midpoint=len(mylist)//2
        return mylist[midpoint]
    elif choice.capitalize()=='C':
        column=cur.execute("SELECT YearReleased FROM Albums ORDER BY YearReleased DESC")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        midpoint=len(mylist)//2
        return mylist[midpoint]
    elif choice.capitalize()=='D':
        column=cur.execute("SELECT Album.Runtime FROM Albums ORDER BY Album.Runtime DESC")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        midpoint=len(mylist)//2
        return mylist[midpoint]
    return 0

def stdev(choice):
    if choice.capitalize()=='A':
        meanlist=cur.execute("SELECT AVG(NumSongs) FROM Albums")
        for item in meanlist:
            mean=item[0]
        column=cur.execute("SELECT NumSongs FROM Albums")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        sum=0
        for value in mylist:
            sum+=((int(value)-mean)*(int(value)-mean))
        variance=sum/len(mylist)
        return math.sqrt(variance)
    elif choice.capitalize()=='B':
        meanlist=cur.execute("SELECT AVG(Songs.Runtime) FROM Songs")
        for item in meanlist:
            mean=item[0]
        column=cur.execute("SELECT Songs.Runtime FROM Songs")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        sum=0
        for value in mylist:
            sum+=((int(value)-mean)*(int(value)-mean))
        variance=sum/len(mylist)
        return math.sqrt(variance)
    elif choice.capitalize()=='C':
        meanlist=cur.execute("SELECT AVG(YearReleased) FROM Albums")
        for item in meanlist:
            mean=item[0]
        column=cur.execute("SELECT YearReleased FROM Albums")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        sum=0
        for value in mylist:
            sum+=((int(value)-mean)*(int(value)-mean))
        variance=sum/len(mylist)
        return math.sqrt(variance)
    elif choice.capitalize()=='D':
        meanlist=cur.execute("SELECT AVG(Albums.Runtime) FROM Albums")
        for item in meanlist:
            mean=item[0]
        column=cur.execute("SELECT Albums.Runtime FROM Albums")
        mylist=[]
        for item in column:
            mylist.append(item[0])
        sum=0
        for value in mylist:
            sum+=((int(value)-mean)*(int(value)-mean))
        variance=sum/len(mylist)
        return math.sqrt(variance)
    return 0

#query menu
def queryMenu():
    check=False
    print('query menu')
    print("what do you wish to look for:\na)sort by song lengths\nb)Year of Release\nc)song containing a certain word\nd)album containing a certain word\ne)see all songs by an artist\nf)see all songs in an album\ng)exit")
    while check==False:
        userInput=input("=>")
        if userInput.capitalize()=="A":
            check=True
            option=False
            while option==False:
                minormax=input("select one to enter: \na)minimum length\nb)maximum song length\n=>")
                if minormax.capitalize()=="A":
                    option=True
                    minlen=input("Enter a minimum song length: ")
                    print("Songs over {0} seconds".format(minlen))
                    songs=cur.execute("SELECT SongName, Songs.Runtime FROM Songs WHERE Songs.Runtime>{0}".format(minlen))
                    for item in songs:
                        print("{0}: {1} seconds".format(item[0],item[1]))
                elif minormax.capitalize()=="B":
                    option=True
                    maxlen=input("Enter a maximum song length: ")
                    print("Songs under {0} seconds".format(maxlen))
                    songs=cur.execute("SELECT SongName, Songs.Runtime FROM Songs WHERE Songs.Runtime<{0}".format(maxlen))
                    for item in songs:
                        print("{0}: {1} seconds".format(item[0],item[1]))
                else:
                    print("Not a valid input. Choose again.")
        elif userInput.capitalize()=="B":
            check=True
            year=input("enter year to search for: ")
            albumsandsongs=cur.execute("SELECT AlbumName,SongName FROM Albums JOIN Songs WHERE Albums.AlbumID=Songs.AlbumID AND YearReleased='{0}'".format(year))
            albumlist=[]
            for item in albumsandsongs:
                if item[0] not in albumlist:
                    albumlist.append(item[0])
            albumsandsongs=cur.execute("SELECT AlbumName,SongName FROM Albums JOIN Songs WHERE Albums.AlbumID=Songs.AlbumID AND YearReleased='{0}'".format(year))
            for album in albumlist:
                print("{0}:".format(album))
                albumsandsongs=cur.execute("SELECT AlbumName,SongName FROM Albums JOIN Songs WHERE Albums.AlbumID=Songs.AlbumID AND YearReleased='{0}'".format(year))
                for item in albumsandsongs:
                    if album==item[0]:
                        print("-{0}".format(item[1]))
        elif userInput.capitalize()=="C":
            check=True
            word=input("Enter a word to search for:")
            print("Songs that contain '{0}':".format(word))
            songs=cur.execute("SELECT SongName FROM Songs WHERE SongName LIKE '% {0} %'".format(word))
            for item in songs:
                print(item[0])
        elif userInput.capitalize()=="D":
            check=True
            word=input("Enter a word to search for:")
            print("Albums that contain '{0}':".format(word))
            albums=cur.execute("SELECT AlbumName FROM Albums WHERE AlbumName LIKE '% {0} %'".format(word))
            for item in albums:
                print(item[0])
        elif userInput.capitalize()=="E":
            check=True
            artist=input("Enter an artist to see their songs:")
            print("Songs by '{0}':".format(artist))
            songs=cur.execute("SELECT SongName FROM Songs JOIN Artists WHERE Name='{0}' AND Songs.ArtistID=Artists.ArtistID".format(artist))
            for item in songs:
                print(item[0])
        elif userInput.capitalize()=="F":
            check=True
            album=input("Enter an album to see the tracklist:")
            print("Songs from '{0}':".format(album))
            songs=cur.execute("SELECT SongName FROM Songs JOIN Albums WHERE AlbumName='{0}' AND Songs.AlbumID=Albums.AlbumID".format(album))
            for item in songs:
                print(item[0])
        elif userInput.capitalize()=="G":
            check=True
        else:
            print("not a valid entry. Enter again: ")


#visualization menu
def visualizationMenu():
    print('you chose the visualizaiton menu\nselect one to visualize \na) runtimes of albums for all artist\nb) runtime of songs in any album\nc) years of all albums')
    userChoice = input('=>')
    #check the user input
    userCheck = True
    while userCheck:
        if userChoice.capitalize() == 'A':
            userCheck = False
            visualizeAlbums()

        elif userChoice.capitalize() == 'B':
            userCheck = False
            visualizeSongs()

        elif userChoice.capitalize() == 'C':
            userCheck = False
            visualizeYears()

        else:
            print("incorrect choice. try again!")
            userChoice = input('=>')
            userCheck = True

def visualizeAlbums():
    selectAlbumName = 'SELECT AlbumName, RunTime FROM Albums'
    cur.execute(selectAlbumName)
    albumData= cur.fetchall()
     #x asis will be the album names
    x = []
    #y axis will be the runtime of songs
    y = []
    for data in albumData:
        x.append(data[0])
        y.append(data[1])

    plt.bar(x,y)
    plt.xticks(rotation=90, ha='right')
    plt.title("Runtime of Albums for All Artists")
    plt.xlabel("Albums")
    plt.ylabel("Runtime")
    plt.show()

def visualizeSongs():
    print('select which album you wish to visualize')
    selectAlbums = 'SELECT AlbumID, AlbumName FROM Albums'
    cur.execute(selectAlbums)
    albumData= cur.fetchall()
    count = 1
    albums = []
    ids = []
    for data in albumData:
        print(str(count)+': '+ data[1])
        albums.append(data[1])
        ids.append(data[0])
        count += 1
    userChoice = input('=>')

      #x asis will be the song names
    x = []
    #y axis will be the runtime of songs
    y = []

    
    #check the users input
    if int(userChoice) > 0 and int(userChoice) < count:
        print('great! you selected: ' + albums[int(userChoice)-1])
        selectSpecificSong = f'SELECT SongName, Runtime FROM Songs WHERE AlbumID = "{ids[int(userChoice)-1]}"'
        cur.execute(selectSpecificSong)
        songData= cur.fetchall()
        for dataS in songData:
            x.append(dataS[0])
            y.append(dataS[1])

    plt.bar(x,y)
    plt.xticks(rotation=90, ha='right')
    plt.title(f"Runtime of Songs for {albums[int(userChoice)-1]}")
    plt.xlabel("Songs")
    plt.ylabel("Runtime")
    plt.show()
    

def visualizeYears():
    selectAlbums = 'SELECT AlbumName, YearReleased FROM Albums' 
    cur.execute(selectAlbums)
    albumData= cur.fetchall()
    #sort the list by year
    
    #x asis will be the years
    xpointsArray = []
    #y axis will be the albun names
    ypointsArray = []
    for data in albumData:
        ypointsArray.append(data[0])
        xpointsArray.append(data[1])
    
    xpoints = np.array(xpointsArray)
    ypoints = np.array(ypointsArray)

    idxs = np.argsort(xpoints)
    xpoints = xpoints[idxs]
    ypoints = ypoints[idxs]
    print(xpoints)
    print(ypoints)
    plt.plot(xpoints,ypoints)
   
    plt.title("Years of Release")
    plt.xlabel("Year")
    plt.ylabel("Album Name")
    plt.show()

    
#end the program, close connections and exit the app
def endProgram():
    print("ending program now...")
    conn.close()
    exit()

mainMenu()