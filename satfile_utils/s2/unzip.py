import os
import glob
import zipfile
import fnmatch
import logging

logger = logging.getLogger(__name__)


def unzip(infile, outdir):
    with zipfile.ZipFile(infile) as zipf:
        zipf.extractall(path=outdir)


def get_band_string(band):
    try:
        # band is integer
        return 'B{:02d}'.format(band)
    except ValueError:
        return 'B{}'.format(band)


def get_band_fnpattern(band, tile=None):
    bandstr = get_band_string(band)
    fnpattern = '*_{band}.jp2'.format(band=bandstr)
    if tile is not None:
        tile = tile.lstrip('T')
        fnpattern = '*T{tile}'.format(tile=tile) + fnpattern
    return fnpattern


def find_band_file_unzipped(folder, band, tile=None):
    fnpattern = get_band_fnpattern(band, tile=tile)
    pattern = os.path.join(folder, fnpattern)
    try:
        files = glob.glob(pattern)
        if len(files) > 1:
            logger.warn(
                    'More than one band file found with pattern: \'{}\'. '
                    'Using only first.'.format(pattern))
        return files[0]
    except IndexError:
        raise RuntimeError(
                'Unable to find file for band {} (and tile {}) in folder \'{}\'.'
                ''.format(band, tile, folder))


def find_band_file_in_archive(names, band, tile=None):
    fnpattern = get_band_fnpattern(band, tile=tile)
    try:
        files = list(fnmatch.filter(names, fnpattern))
        if len(files) > 1:
            logger.warn(
                    'More than one band file found with pattern: \'{}\'. '
                    'Using only first.'.format(fnpattern))
        return files[0]
    except IndexError:
        raise RuntimeError(
                'Unable to find file for band {} and tile {} in list {}'
                ''.format(band, tile, names))


def open_band_in_archive(zipf, band, tile=None):
    names = zipf.namelist()
    name = find_band_file_in_archive(names, band, tile=tile)
    logger.debug(
            'Found file {} for band {} (and tile {}).'.format(name, band, tile))
    return zipf.open(name)


def open_bandfiles_in_archive(infile, bands, tile=None):
    with zipfile.ZipFile(infile) as zipf:
        for band in bands:
            logger.info(
                    'Reading band {} (for tile {}) from zip file {} ...'
                    ''.format(band, tile, infile))
            yield open_band_in_archive(zipf, band, tile=tile)
