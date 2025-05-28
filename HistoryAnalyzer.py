import DataGrabber
import pandas as pd 
import DataPlotter


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class HistoryAnalyzer:

    def __init__(self, current_year, type = "list"):
        try:
            self.DataGrabber_object = DataGrabber.DataGrabber(current_year = current_year)
            self.df = self.DataGrabber_object.df
        except Exception as e:
            print(f'Error initalizing DataGrabber: {str(e)}')

        self.type = type

        # depreciated code
        #print(howManySongs(df), f' unique songs listened to in {dataGrabber_object.currentYear}')
        #print(f'Total time spent listening to music in {dataGrabber_object.currentYear}: ', totalListeningTime(df))
        #df['trackID'] = df.apply(lambda row: sah.getTrackID(row['trackName'], row['artistName']), axis=1)
        #print(df.head(5))
        #print(f'Top songs of {dataGrabber_object.currentYear}\n', topSongs(df, 100))
        #print(f'Top artists of {dataGrabber_object.currentYear}\n', topArtists(df, 5))
        #print(f'Top artists of {dg1.currentYear}\n', topArtistsIDS(df))

    def topSongs(self, list_size = 5):
        '''
        get the top songs played
        '''

        top_songs = self.df['track_name'].value_counts().head(list_size).reset_index()
        top_songs.index = top_songs.index + 1
        top_songs.columns = ['Track', 'Plays']

        print(f'Top songs of {self.DataGrabber_object.current_year}\n', top_songs)
        return 

    def topArtists(self, list_size = 5):
        '''
        get the top 10 artists played
        '''

        if self.type == 'list':

            top_artists = self.df['artist_name'].value_counts().head(list_size).reset_index()
            top_artists.index = top_artists.index + 1
            top_artists.columns = ['Artist', 'Plays']
            print(f'Top artists of {self.DataGrabber_object.current_year}\n', top_artists)

        if self.type == 'graph':

            top_artists = self.df['artist_name'].value_counts().head(list_size + 5).reset_index()
            top_artists.index = top_artists.index + 1
            top_artists.columns = ['Artist', 'Plays']

            DataPlotter.horizontalBarPlot(data = top_artists['Plays'], 
                            indices = top_artists['Artist'], 
                            title = 'Top Artists', 
                            xlabel = 'Plays', 
                            color = 'blue',
                            long_label = True) 

        #formatted_artists = []
        #for artist in top_artists['Artist']:
        #    if len(artist) < 8:
        #        formatted_artists.append(artist)
        #        continue
        #    words = artist.split()
        #    if len(words) > 1:
        #        formatted_artists.append(words[0] + '\n' + ' '.join(words[1:]))
        #    else:
        #        formatted_artists.append(artist)
        
        
        return 

    def listeningTimePerMonth(self):

        if self.type == 'list':

            listen_time = round(self.df['ms_played'].sum() / 1000 / 60)
            print(f'Total time spent listening to music in {self.DataGrabber_object.current_year}: ', listen_time, ' minutes')

        if self.type == 'graph':

            listen_time_per_month = self.df.groupby(self.df['end_time'].dt.month)['ms_played'].sum() / 1000 / 60

            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
            
            DataPlotter.verticalBarPlot(data = listen_time_per_month, 
                                indices = months, 
                                title = 'Minutes Listened per Month', 
                                ylabel = 'Minutes Listened', 
                                color = 'green')

        return

    def howManySongs(self):

        unique_songs = self.df['track_name'].nunique()
        print(unique_songs, f'unique songs listened to in {self.DataGrabber_object.current_year}')
        return

### DEPRECIATED FUNCTiONS
    def formatSeries(series):
        '''
        format series for printing
        '''
        return dict(series)
    
    def topAlbums(self, list_size = 5):
        '''
        get the top 10 albums played
        '''

        return self.df['album_name'].value_counts().head(list_size)