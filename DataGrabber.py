import json
import glob
import os
import re
import pandas as pd

class DataGrabber:

    def __init__(self, current_year):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.target_directory = os.path.join(self.script_dir, 'spotify-account-data', '*')
        self.jsonDump = list()
        self.usedFiles = list()
        self.current_year = current_year
        self.processFiles()
        self.df = self.createDF()
        
    def processFiles(self):
        '''
        go through all files in target directory and load data into jsonDump

        Args: 
            None

        Returns:
            None

        Raises:
            None
        '''

        for file in glob.glob(self.target_directory):
            match = re.search(r'[/\\]StreamingHistory_music_\d+\.json$', file)
            if match:
                print(f"Adding: '{match.group(0)}'")
                self.jsonDump.append(self.getData(file))

        self.flattenedJSONdata = [item for sublist in self.jsonDump for item in sublist] if self.jsonDump \
            else print("No matching files found or all files failed to load")

    def getData(self, file):
        '''
        read json and return data as list of dictionaries

        Args:
            file (str): path to JSON file

        Returns:
            list[dict]: list of dictionaries
            None: if file cannot be read or parsed

        Raises:
            FileNotFoundError: if file does not exist
            json.JSONDecodeError: if file is not valid JSON
        '''

        try:
            with open(file, 'r', encoding = 'utf-8') as open_file:
                data = json.load(open_file)
            return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading file {file}: {str(e)}")
            return None

    def createDF(self):
        '''
        creates a pandas DataFrame from jsonDump data, 
        sorts by date and time, 
        removes entries from before the current year, 
        and removes entries after Nov 15

        also writes the DataFrame to CSV

        Args:
            None
        
        Returns:
            songs (pd.DataFrame): listening history dataframe 

        Raises: 
            None
        '''

        if not self.flattenedJSONdata:
            print("No data to write to CSV")
            return

        songs = pd.DataFrame(self.flattenedJSONdata)

        songs.rename(columns = {
            'endTime': 'end_time', 
            'artistName': 'artist_name', 
            'trackName': 'track_name', 
            'msPlayed': 'ms_played'}, 
            inplace = True)
        
        # helper function to remove entries before current year and after Nov 15
        def cutoffDate(date):
            if date.year != self.current_year:
                return False
            if date.month > 11:
                return False
            if date.month == 11:
                return True if date.day <= 15 else False
            return True

        # sort by date and time ascending order
        songs['end_time'] = pd.to_datetime(songs['end_time'])
        songs = songs.sort_values('end_time', ascending = True)

        # remove songs listened to for less than 60 seconds
        songs = songs[songs['ms_played'] >= 60837]

        # remove listening entries after Nov 15
        songs = songs[songs['end_time'].apply(cutoffDate)]   

        songs = songs[(songs['artist_name'] != 'Unknown Artist') & (songs['track_name'] != 'Unknown Track')]
        songs = songs.reset_index(drop = True)

        # write DataFrame to CSV
        self.writeCSV(songs)

        return songs

    def writeCSV(self, dataframe):
        output_path = os.path.join(self.script_dir, 'output' ,'spotify_history.csv')
        dataframe.to_csv(output_path, index = False)
        formatted_path = f'"{os.path.abspath(output_path)}"'
        #print(f"Data written to {formatted_path}")

        return
    
