import sys
sys.path.append("re_synthesis/")

import librosa
from re_synthesis.const import SR, TEMPO



class PieceOfTrack:
    """ Class MixingPoint used for re-synthesis from differnet tracks.

    Attributes
    ----------
    name : str
        The full path name of the track
    t_in : int
        The temporal index of the entry point
    t_out : int
        The temporal index of the exit point
    tempo : int
        The original tempo of the track.

    """

    def __init__(self, track_name, beginning, end, tempo):
        """ PieceOfTrack constructor

        Parameters
        ----------
        name : str
            The full path name of the track
        beginning : int
            The temporal index of the entry point
        end : int
            The temporal index of the exit point
        tempo : int
            The original tempo of the track.

        """
        self.name = track_name
        self.t_in = beginning
        self.t_out = end
        self.tempo = tempo

    def __repr__(self):
        text = "Track " + str(self.name) + " from " + str(self.t_in) + \
            " to " + str(self.t_out) + " at " + str(self.tempo) + " bpm"
        return text


    def render(self, tempo_out = TEMPO):
        """ This method returns the audio samples of the track between the 
        entry point and the exit point, and stretches the song to a fixed tempo

        Parameters
        ----------
        tempo_out : int, optional
            The tempo of the output samples list.
            
        Returns
        -------
        list
            The audio samples list, corresponding to this piece of track, 
            at a fixed tempo.
        """
        try:           
            y, sr = librosa.load(self.name)
            y = y[self.t_in:self.t_out]
            if sr != SR :
                raise ValueError("Sampling rates are not all equal to "+str(SR))
        except ValueError as error:
            print(error)

        if (tempo_out != 0) & (self.tempo != 0):
            factor = float(tempo_out)/float(self.tempo)
            y = librosa.effects.time_stretch(y, factor)

        return y.tolist()

    def fadein_render(self, bars = 1, tempo_out = TEMPO):
        """ This method returns the audio samples of the track just before 
        the entry point, stretched to a fixed tempo

        Parameters
        ----------
        bars : int, optional
            The length (in bars) of the section returned.
        tempo_out : int, optional
            The tempo of the output samples list.
            
        Returns
        -------
        list
            The section that will be used for the fade

        """
        t_fade = int(60.0/self.tempo * 4*bars*SR)
        # print(t_fade,self.t_in-t_fade)
        try:           
            y, sr = librosa.load(self.name)
            y = y[self.t_in-t_fade:self.t_in]
            if sr != SR :
                raise ValueError("Sampling rates are not all equal to "+str(SR))
        except ValueError as error:
            print(error)

        if (tempo_out != 0) & (self.tempo != 0):
            factor = float(tempo_out)/float(self.tempo)
            y = librosa.effects.time_stretch(y, factor)

        return y.tolist()
