# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .time_interval_object import TimeIntervalObject

__all__ = ["AudioAnalysisRetrieveResponse", "Meta", "Section", "Segment", "Track"]


class Meta(BaseModel):
    analysis_time: Optional[float] = None
    """The amount of time taken to analyze this track."""

    analyzer_version: Optional[str] = None
    """The version of the Analyzer used to analyze this track."""

    detailed_status: Optional[str] = None
    """A detailed status code for this track.

    If analysis data is missing, this code may explain why.
    """

    input_process: Optional[str] = None
    """The method used to read the track's audio data."""

    platform: Optional[str] = None
    """The platform used to read the track's audio data."""

    status_code: Optional[int] = None
    """The return code of the analyzer process.

    0 if successful, 1 if any errors occurred.
    """

    timestamp: Optional[int] = None
    """The Unix timestamp (in seconds) at which this track was analyzed."""


class Section(BaseModel):
    confidence: Optional[float] = None
    """
    The confidence, from 0.0 to 1.0, of the reliability of the section's
    "designation".
    """

    duration: Optional[float] = None
    """The duration (in seconds) of the section."""

    key: Optional[int] = None
    """The estimated overall key of the section.

    The values in this field ranging from 0 to 11 mapping to pitches using standard
    Pitch Class notation (E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on). If no key was
    detected, the value is -1.
    """

    key_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the key.

    Songs with many key changes may correspond to low values in this field.
    """

    loudness: Optional[float] = None
    """The overall loudness of the section in decibels (dB).

    Loudness values are useful for comparing relative loudness of sections within
    tracks.
    """

    mode: Optional[Literal[-1, 0, 1]] = None
    """
    Indicates the modality (major or minor) of a section, the type of scale from
    which its melodic content is derived. This field will contain a 0 for "minor", a
    1 for "major", or a -1 for no result. Note that the major key (e.g. C major)
    could more likely be confused with the minor key at 3 semitones lower (e.g. A
    minor) as both keys carry the same pitches.
    """

    mode_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `mode`."""

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    start: Optional[float] = None
    """The starting point (in seconds) of the section."""

    tempo: Optional[float] = None
    """The overall estimated tempo of the section in beats per minute (BPM).

    In musical terminology, tempo is the speed or pace of a given piece and derives
    directly from the average beat duration.
    """

    tempo_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the tempo.

    Some tracks contain tempo changes or sounds which don't contain tempo (like pure
    speech) which would correspond to a low value in this field.
    """

    time_signature: Optional[int] = None
    """An estimated time signature.

    The time signature (meter) is a notational convention to specify how many beats
    are in each bar (or measure). The time signature ranges from 3 to 7 indicating
    time signatures of "3/4", to "7/4".
    """

    time_signature_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `time_signature`.

    Sections with time signature changes may correspond to low values in this field.
    """


class Segment(BaseModel):
    confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the segmentation.

    Segments of the song which are difficult to logically segment (e.g: noise) may
    correspond to low values in this field.
    """

    duration: Optional[float] = None
    """The duration (in seconds) of the segment."""

    loudness_end: Optional[float] = None
    """The offset loudness of the segment in decibels (dB).

    This value should be equivalent to the loudness_start of the following segment.
    """

    loudness_max: Optional[float] = None
    """The peak loudness of the segment in decibels (dB).

    Combined with `loudness_start` and `loudness_max_time`, these components can be
    used to describe the "attack" of the segment.
    """

    loudness_max_time: Optional[float] = None
    """The segment-relative offset of the segment peak loudness in seconds.

    Combined with `loudness_start` and `loudness_max`, these components can be used
    to desctibe the "attack" of the segment.
    """

    loudness_start: Optional[float] = None
    """The onset loudness of the segment in decibels (dB).

    Combined with `loudness_max` and `loudness_max_time`, these components can be
    used to describe the "attack" of the segment.
    """

    pitches: Optional[List[float]] = None
    """
    Pitch content is given by a “chroma” vector, corresponding to the 12 pitch
    classes C, C#, D to B, with values ranging from 0 to 1 that describe the
    relative dominance of every pitch in the chromatic scale. For example a C Major
    chord would likely be represented by large values of C, E and G (i.e. classes 0,
    4, and 7).

    Vectors are normalized to 1 by their strongest dimension, therefore noisy sounds
    are likely represented by values that are all close to 1, while pure tones are
    described by one value at 1 (the pitch) and others near 0. As can be seen below,
    the 12 vector indices are a combination of low-power spectrum values at their
    respective pitch frequencies. ![pitch vector](/assets/audio/Pitch_vector.png)
    """

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    start: Optional[float] = None
    """The starting point (in seconds) of the segment."""

    timbre: Optional[List[float]] = None
    """
    Timbre is the quality of a musical note or sound that distinguishes different
    types of musical instruments, or voices. It is a complex notion also referred to
    as sound color, texture, or tone quality, and is derived from the shape of a
    segment’s spectro-temporal surface, independently of pitch and loudness. The
    timbre feature is a vector that includes 12 unbounded values roughly centered
    around 0. Those values are high level abstractions of the spectral surface,
    ordered by degree of importance.

    For completeness however, the first dimension represents the average loudness of
    the segment; second emphasizes brightness; third is more closely correlated to
    the flatness of a sound; fourth to sounds with a stronger attack; etc. See an
    image below representing the 12 basis functions (i.e. template segments).
    ![timbre basis functions](/assets/audio/Timbre_basis_functions.png)

    The actual timbre of the segment is best described as a linear combination of
    these 12 basis functions weighted by the coefficient values: timbre = c1 x b1 +
    c2 x b2 + ... + c12 x b12, where c1 to c12 represent the 12 coefficients and b1
    to b12 the 12 basis functions as displayed below. Timbre vectors are best used
    in comparison with each other.
    """


class Track(BaseModel):
    analysis_channels: Optional[int] = None
    """The number of channels used for analysis.

    If 1, all channels are summed together to mono before analysis.
    """

    analysis_sample_rate: Optional[int] = None
    """The sample rate used to decode and analyze this track.

    May differ from the actual sample rate of this track available on Spotify.
    """

    code_version: Optional[float] = None
    """
    A version number for the Echo Nest Musical Fingerprint format used in the
    codestring field.
    """

    codestring: Optional[str] = None
    """
    An
    [Echo Nest Musical Fingerprint (ENMFP)](https://academiccommons.columbia.edu/doi/10.7916/D8Q248M4)
    codestring for this track.
    """

    duration: Optional[float] = None
    """Length of the track in seconds."""

    echoprint_version: Optional[float] = None
    """A version number for the EchoPrint format used in the echoprintstring field."""

    echoprintstring: Optional[str] = None
    """
    An [EchoPrint](https://github.com/spotify/echoprint-codegen) codestring for this
    track.
    """

    end_of_fade_in: Optional[float] = None
    """The time, in seconds, at which the track's fade-in period ends.

    If the track has no fade-in, this will be 0.0.
    """

    key: Optional[int] = None
    """The key the track is in.

    Integers map to pitches using standard
    [Pitch Class notation](https://en.wikipedia.org/wiki/Pitch_class). E.g. 0 = C, 1
    = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
    """

    key_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `key`."""

    loudness: Optional[float] = None
    """The overall loudness of a track in decibels (dB).

    Loudness values are averaged across the entire track and are useful for
    comparing relative loudness of tracks. Loudness is the quality of a sound that
    is the primary psychological correlate of physical strength (amplitude). Values
    typically range between -60 and 0 db.
    """

    mode: Optional[int] = None
    """
    Mode indicates the modality (major or minor) of a track, the type of scale from
    which its melodic content is derived. Major is represented by 1 and minor is 0.
    """

    mode_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `mode`."""

    num_samples: Optional[int] = None
    """The exact number of audio samples analyzed from this track.

    See also `analysis_sample_rate`.
    """

    offset_seconds: Optional[int] = None
    """An offset to the start of the region of the track that was analyzed.

    (As the entire track is analyzed, this should always be 0.)
    """

    rhythm_version: Optional[float] = None
    """A version number for the Rhythmstring used in the rhythmstring field."""

    rhythmstring: Optional[str] = None
    """A Rhythmstring for this track.

    The format of this string is similar to the Synchstring.
    """

    sample_md5: Optional[str] = None
    """This field will always contain the empty string."""

    start_of_fade_out: Optional[float] = None
    """The time, in seconds, at which the track's fade-out period starts.

    If the track has no fade-out, this should match the track's length.
    """

    synch_version: Optional[float] = None
    """A version number for the Synchstring used in the synchstring field."""

    synchstring: Optional[str] = None
    """A [Synchstring](https://github.com/echonest/synchdata) for this track."""

    tempo: Optional[float] = None
    """The overall estimated tempo of a track in beats per minute (BPM).

    In musical terminology, tempo is the speed or pace of a given piece and derives
    directly from the average beat duration.
    """

    tempo_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `tempo`."""

    time_signature: Optional[int] = None
    """An estimated time signature.

    The time signature (meter) is a notational convention to specify how many beats
    are in each bar (or measure). The time signature ranges from 3 to 7 indicating
    time signatures of "3/4", to "7/4".
    """

    time_signature_confidence: Optional[float] = None
    """The confidence, from 0.0 to 1.0, of the reliability of the `time_signature`."""

    window_seconds: Optional[int] = None
    """
    The length of the region of the track was analyzed, if a subset of the track was
    analyzed. (As the entire track is analyzed, this should always be 0.)
    """


class AudioAnalysisRetrieveResponse(BaseModel):
    bars: Optional[List[TimeIntervalObject]] = None
    """The time intervals of the bars throughout the track.

    A bar (or measure) is a segment of time defined as a given number of beats.
    """

    beats: Optional[List[TimeIntervalObject]] = None
    """The time intervals of beats throughout the track.

    A beat is the basic time unit of a piece of music; for example, each tick of a
    metronome. Beats are typically multiples of tatums.
    """

    meta: Optional[Meta] = None

    published: Optional[bool] = None
    """
    The playlist's public/private status (if it should be added to the user's
    profile or not): `true` the playlist will be public, `false` the playlist will
    be private, `null` the playlist status is not relevant. For more about
    public/private status, see
    [Working with Playlists](/documentation/web-api/concepts/playlists)
    """

    sections: Optional[List[Section]] = None
    """Sections are defined by large variations in rhythm or timbre, e.g.

    chorus, verse, bridge, guitar solo, etc. Each section contains its own
    descriptions of tempo, key, mode, time_signature, and loudness.
    """

    segments: Optional[List[Segment]] = None
    """Each segment contains a roughly conisistent sound throughout its duration."""

    tatums: Optional[List[TimeIntervalObject]] = None
    """
    A tatum represents the lowest regular pulse train that a listener intuitively
    infers from the timing of perceived musical events (segments).
    """

    track: Optional[Track] = None
