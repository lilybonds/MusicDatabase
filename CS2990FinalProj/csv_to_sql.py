import sqlite3
import csv

#Artists table
conn = sqlite3.connect('music_database.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Artists")
create_table="CREATE TABLE Artists('ArtistID','Name','Label','BirthPlace','Country','Genre')"
cur.execute(create_table)
file1=open('Artists.csv')
contents=csv.reader(file1)
headers=next(contents)
insert_records='''INSERT INTO Artists('ArtistID','Name','Label','BirthPlace','Country','Genre')
                VALUES (?,?,?,?,?,?)'''
cur.executemany(insert_records,contents)
conn.commit()
file1.close()

#Albums table
cur.execute("DROP TABLE IF EXISTS Albums")
create_table="CREATE TABLE Albums('AlbumID','ArtistID', 'AlbumName','NumSongs','YearReleased','RunTime')"
cur.execute( create_table)
file2=open('Albums.csv')
contents=csv.reader(file2)
headers=next(contents)
insert_records='''INSERT INTO Albums('AlbumID','ArtistID', 'AlbumName','NumSongs','YearReleased','RunTime')
                VALUES (?,?,?,?,?,?)'''
cur.executemany(insert_records,contents)
conn.commit()
file2.close()

#Songs table
cur.execute("DROP TABLE IF EXISTS Songs")
create_table="CREATE TABLE Songs('SongID','AlbumID','ArtistID','SongName','Runtime')"
cur.execute( create_table)
file3=open('Songs.csv')
contents=csv.reader(file3)
headers=next(contents)
insert_records='''INSERT INTO Songs('SongID','AlbumID','ArtistID','SongName','Runtime')
                VALUES (?,?,?,?,?)'''
cur.executemany(insert_records,contents)
conn.commit()
file3.close()
conn.close()