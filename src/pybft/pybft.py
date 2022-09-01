from __future__ import (print_function)

import ctypes as ct
from ctypes.util import find_library
import os.path as osp

import inspect
import sys
import numpy as np
from numpy import (c_, r_, zeros_like)

import pdb
# ----------------------------------------------------------------------------
# Import the beamformation library

try:
    dirname = osp.dirname(inspect.getabsfile(lambda x: None))
    if sys.platform == 'win32':
        libbft = ct.CDLL(osp.join(dirname, 'bft.dll'))
    elif sys.platform == 'darwin':
        libbft = ct.CDLL(osp.join(dirname, 'libbft.dylib'))
    else:
        libbft = ct.CDLL(osp.join(dirname, 'libbft.so'))
except:
    if find_library('bft'):
        libsvm = ct.CDLL(find_library('bft'))
    else:
        raise Exception('BFT (DLL) library not found.')

# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def fillprototype(f, restype, argtypes):
    'Add information about parameters and return type'
    f.restype = restype
    f.argtypes = argtypes
# fillprototype()


# ----------------------------------------------------------------------------
#  Call-back function for printing the messages.
#
def printer_py2(msg):
    print(msg, end="")

def printer_py3(msg):
    print(msg.decode('utf-8'), end="")


PRINTFUNC = ct.CFUNCTYPE(None, (ct.c_char_p))
print_func = PRINTFUNC(printer_py2) if sys.version_info.major == 2 else PRINTFUNC(printer_py3)
PtrDouble = ct.POINTER(ct.c_double)
PtrUint32 = ct.POINTER(ct.c_uint32)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .


fillprototype(libbft.bft_init, None, [PRINTFUNC, ct.c_uint32])

fillprototype(libbft.bft_end,  None, None)

fillprototype(libbft.bft_param, ct.c_double, [ct.c_char_p, ct.c_double])

fillprototype(libbft.bft_no_lines, ct.c_uint32, [ct.c_uint32])

fillprototype(libbft.bft_xdc, ct.c_void_p,
              [ct.POINTER(ct.c_double), ct.c_uint32])

fillprototype(libbft.bft_xdc_free, None, [ct.c_void_p])

fillprototype(libbft.bft_center_focus, None,
              [ct.POINTER(ct.c_double), ct.c_uint32])

fillprototype(libbft.bft_focus, None,
              [ct.c_void_p,              # xdc
               ct.POINTER(ct.c_double),  # times
               ct.POINTER(ct.c_double),  # focus points
               ct.c_uint32])

fillprototype(libbft.bft_focus_pixel, None,
              [ct.c_void_p,
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_focus_2way, None,
              [ct.c_void_p,
               ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_focus_times, None,
              [ct.c_void_p,
               ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_apodization, None,
              [ct.c_void_p,
               ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_dynamic_focus, None,
              [ct.c_void_p,
               ct.c_uint32,
               ct.c_double,
               ct.c_double])


#fillprototype(libbft.bft_beamform, ct.POINTER(ct.c_double),
#              [ct.POINTER(ct.c_double),
#               ct.c_double,
#               ct.c_uint32,
#               ct.c_uint32,
#               ct.c_uint32,
#               ct.POINTER(ct.c_double)])

fillprototype(libbft.bft_beamform, ct.POINTER(ct.c_double),
              [PtrUint32,
               PtrUint32,
               PtrDouble,
               ct.c_double,
               ct.c_uint32,
               ct.c_uint32,
               ct.c_uint32,
               ct.POINTER(ct.c_double)])
fillprototype(libbft.bft_sum_images, ct.POINTER(ct.c_double),
              [ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_double,
               ct.c_uint32])

fillprototype(libbft.bft_add_images, None,
              [ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_double,
               ct.c_uint32])

fillprototype(libbft.bft_sub_images, None,
              [ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_double,
               ct.c_uint32])

fillprototype(libbft.bft_set_filter_bank, None,
              [ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_delay, None,
              [ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.POINTER(ct.c_double),
               ct.POINTER(ct.c_double),
               ct.c_uint32,
               ct.c_double,
               ct.c_double,
               ct.c_uint32,
               ct.c_uint32])

fillprototype(libbft.bft_xdc_set, None,
              [ct.c_void_p,
               ct.POINTER(ct.c_double),
               ct.c_uint32])

fillprototype(libbft.bft_free_mem, None, 
              [ct.c_void_p])

# ---------------------------------------------------------------------------
class bft:

    '''Class encapsulating all functions from the Beamforming Toolbox.
The toolbox is implemented in pure C, and has no objects, hence it can
be used only as a singleton.

The user does not need to create an object of the class bft, and can call
the functions directly.

Allways start by calling `bft_init` first, which initializes memory and sets
some default parameters

    >>> from pybft import bft
    >>> bft.bft_init()
    >>> bft.bft_end()

Note:
All parameters and values are given in SI units.

    '''
    @staticmethod
    def bft_init(suppress=False):
        '''Initialize the BeamForming Toolbox. This command must be executed
        first in order to set some parameters and allocate necessary memory.

        Subsequent calls will result in clearing the memory.

        Parameters:
        -----------
        suppress: boolean, scalar
            A greeting message is displayed if False.
        '''
        libbft.bft_init(print_func, ct.c_uint32(suppress))
    # bft_init()

    # ------------------------------------------------------------------------
    @staticmethod
    def bft_end():
        '''Release all resources, allocated by the beamforming toolbox.'''
        libbft.bft_end()
    # bft_end()

    # ------------------------------------------------------------------------
    @staticmethod
    def bft_param(identifier, value):
        '''Set a paramater of the BeamForming Toolbox

    Parameters:
    -----------
    identifier: string,
        Identifier of the parameter to set
    value: scalar, double
        Value to set for that parameter

    ========================================================================
    identifier         Meaning                      Default value      Unit
    ---------- ------------------------------------ ----------------- ------
    'c'        Speef of sound                        1540              m/s
    'fs'       Sampling frequency                    40.0e6            Hz
    ========================================================================

    Returns:
    --------
    The value that was set. If not successful, the returned value will be
    negated. E.g. in case of failure,  if vaule=5, then return value is -5.
        '''
        if not(identifier in ['c', 'fs']):
            raise RuntimeError('Unknown identifier "{0}"'.format(identifier))

        return libbft.bft_param(identifier, ct.c_double(value))
    # bft_param

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_no_lines(no_lines):
        '''Set the number of lines that will be beamformed in parallel.
    After calling `bft_init`, the number of lines that are beamformed in
    parallel is 1. If the user wants to beamform a whole image in one
    command, then he/she must set the number of lines, and then specify the
    focal zones for each of the lines.

    Parameters:
    -----------
    no_lines: scalar, integer,
        Number of lines to beamform in parallel.

    Returns:
    --------
    The number of lines that will be beamformed in parallel
        '''
        return libbft.bft_no_lines(ct.c_uint32(no_lines))
    # bft_no_lines()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_xdc(centers):
        ''' Create a new transducer definition.
    The transducer definition is necessary for the calculation of
    the delays.

    Parameters:
    -----------
    centers: array_like, double
        Centers of the transducer elements. There must be 3 COLUMNS (x, y, z)

    Returns:
    --------
    xdc: A pointer to the allocated aperture. *NEVER MODIFY THIS VALUE*
        '''

        centers = np.array(centers)
        if (centers.shape[1] != 3):
            raise RuntimeError('centers must have 3 columns')

        no_elements = centers.shape[0]

        return libbft.bft_xdc(centers.ctypes.data_as(ct.POINTER(ct.c_double)),
                              ct.c_uint32(no_elements))
    # bft_xdc()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_linear_array(no_elements, *arg):
        ''' Create a linear array.

        Usage:
        ------

            >>> xdc = bft.bft_linear_array(no_elements, pitch)
            >>> xdc = bft.bft_linear_array(no_elements, width, kerf)

        Parameters:
        -----------
        no_elements: scalar, integer
            Number of elelements in the array

        pitch: scalar, double
            Distance between the centers of two elements [m]

        width: scalar, double
            Width in x-direction                         [m]

        kerf: scalar, double
            Distance between two elements                [m]

        Returns:
        xdc: Pointer to transducer def. *NEVER modify this value*
        '''
        if (len(arg) not in [1, 2]):
            raise RuntimeError(
                'Specify either pitch only, or element width and kerf')

        if (len(arg) == 2):
            pitch = arg[0] + arg[1]    # Specified width + kerf
        else:
            pitch = arg[0]

        x = r_[-(no_elements - 1) / 2.0: no_elements / 2.0] * pitch
        centers = c_[x, zeros_like(x), zeros_like(x)]

        return bft.bft_xdc(centers)
    # bft_linear_array

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_convex_array(no_elements, *arg):
        '''Define a curved linear array transducer.

    Usage:
    ------

        >>> xdc = bft.bft_convex_array(no_elements, width, kerf, Rconvex)
        >>> xdc = bft.bft_convex_array(no_elements, pitch, Rconvex)

    Parameters:
    -----------
    no_elements: scalara, integer
        Number of elements in the convex array

    width: scalar, double,
        Width of one element in x-direction

    kerf: scalar, double,
        Distance between 2 elements

    Rconvex: scalar, double
        Convex radius, also known as radius of curvature

    pitch: scalar, double
        Distance between the centers of two elements
        '''
        if (len(arg) not in[2, 3]):
            raise RuntimeError('Wrong number of inputs')

        if (len(arg) == 3):
            pitch = arg[0] + arg[1]
            Rconvex = arg[2]
        else:
            pitch = arg[0]
            Rconvex = arg[1]

        theta = r_[-(no_elements - 1) / 2.0: no_elements / 2.0] * \
            pitch / Rconvex

        x = Rconvex * np.sin(theta)
        z = Rconvex * np.cos(theta)
        z = z - np.max(z)
        y = np.zeros(no_elements)

        centers = c_[x, y, z]
        return bft.bft_xdc(centers)
    # bft_convex_array()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_xdc_free(xdc):
        """Release the memory allocated for a transducer definition.

    Parameters:
    -----------

    xdc: pointer,
        This is the handle (pointer) returned by aperture creation functions
        """
        libbft.bft_xdc_free(ct.c_void_p(xdc))
    # bft_xdc_free()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_center_focus(point, line_no=0):
        '''Set the reference point for beamforming a line.
    The point is typically on the surface of the transducer. It is also
    used as the "origin" of the line.

    Parameters:
    -----------
    point: array_like[3], double
        (x,y,z) coordinates of the center focus point

    line_no: scalar, integer
        Index of line whose center focus is being set.
        '''
        point = np.array(point)
        assert point.size == 3

        libbft.bft_center_focus(point.ctypes.data_as(PtrDouble),
                                ct.c_uint32(line_no))
    # bft_center_focus

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_focus(xdc, times, points, line_no=0):
        '''Create a focus time line defined by focal points.

        Parameters:
        -----------
        xdc: pointer(integer),
            Pointer to aperture.

        times: array_like, double
            Time after which the associated focus is valid

        points: array_like, double,
            Focus points. Matrix with three columns (x,y,z)
            and one row for each field point.

        line_no: scalar, integer
            Number of line for which we set the focus.
            If skipped, 'line_no' is assumed equal to '0'.
        '''
        times = np.array(times)
        points = np.array(points)
        no_times = times.size
        assert points.size == 3 * no_times
        if (no_times > 1):
            assert points.shape[0] == no_times

        libbft.bft_focus(ct.c_void_p(xdc),
                         times.ctypes.data_as(PtrDouble),
                         points.ctypes.data_as(PtrDouble),
                         ct.c_uint32(no_times),
                         ct.c_uint32(line_no))

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_focus_pixel(xdc, points, line_no=0):
        '''Set the coordinates of the focal pixels
    This type of focusing is meant to be based on pixels not
    on lines. Therefore the term "focus-time-line" is non
    valid. The user will get back as many focused samples as
    the number of points he/she has passed to this function.

    Parameters:
    -----------

    xdc: integer (pointer)
        Pointer to aperture.

    points: array_like, double,
        Focus points. Vector with three columns (x,y,z)
        and one row for each field point.

    line_no: scalar, integer
        Index of line for which we set the focus. Default value is 0.
        '''
        points = np.array_like(points)
        assert points.shape[1] == 3
        no_points = points.shape[0]

        libbft.bft_focus_pixel(ct.c_void_p(xdc),
                               points.ctypes.data_as(PtrDouble),
                               ct.c_uint32(no_points),
                               ct.c_uint32(line_no))
    # bft_focus_pixel()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_focus_2way(xdc, times, delays, line_no=0):
        '''Create a 2way focus time line defined by focal points.
    These focus settings are relevant only for synthetic aperture imaging.
    This is the classical monostatic synthetic aperture focusing

    Parameters:
    -----------

    xdc: integer (pointer)
        Pointer to aperture. Returned by the bff_***_transducer functions

    times: array_like, double
        Time after which the associated focus is valid

    points: array_like, double,
        Focus points. Vector with three columns (x,y,z) and one row for each
        field point.

    line_no: scalar, integer
        Number of line for which we set the focus. Default value 0.
        '''
        times = np.array(times)
        delays = np.array(delays)
        no_times = times.size
        assert delays.shape[0] == no_times

        libbft.bft_focus_2way(ct.c_void_p(xdc),
                              times.ctypes.data_as(PtrDouble),
                              delays.ctypes.data_as(PtrDouble),
                              ct.c_uint32(no_times),
                              ct.c_uint32(line_no))
    # bft_focus_2way

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_focus_times(xdc, times, delays, line_no=0):
        '''Create a focus time line defined by focus delays.
    The user supplies the delay times for each element.

    Parameters:
    -----------
    xdc: integer (pointer)
        Pointer to a transducer aperture.

    times: array_like, double,
        Time after which the associated delay is valid

    delays:  - Delay values. Matrix with one row for each
                   time value and a number of columns equal to the
                   number of physical elements in the aperture.
          line_no - Number of line. If skipped, 'line_no' is
                    assumed to be equal to 1.
        '''
        times = np.array(times)
        delays = np.array(delays)
        no_times = times.size
        assert delays.shape[0] == no_times

        libbft.bft_focus_times(ct.c_void_p(xdc),
                               times.ctypes.data_as(PtrDouble),
                               delays.ctypes.data_as(PtrDouble),
                               ct.c_uint32(no_times),
                               ct.c_uint32(line_no))
    # bft_focus_times

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_apodization(xdc, times, apodization, line_no=0):
        '''Create an apodization time line.

    Parameters:
    -----------

    xdc: integer (pointer)
        Pointer to a transducer aperture

    times: array_like, double,
        Times after which the associated apodization is valid

    values: array_like, double,
        Apodization values. Matrix with one row for each time value and a number
        of columns equal to the number of physical elements in the aperture.

    line_no: scalar, integer,
        Index of line to set the apodization for. Default value is 0.
        '''
        times = np.array(times)
        apodization = np.array(apodization)
        no_times = times.size

        if (no_times > 1):
            assert apodization.shape[0] == no_times

        libbft.bft_apodization(ct.c_void_p(xdc),
                               times.ctypes.data_as(PtrDouble),
                               apodization.ctypes.data_as(PtrDouble),
                               ct.c_uint32(no_times),
                               ct.c_uint32(line_no))
    # bft_apodization()

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_sum_apodization(xdc, times, apodization, line_no=0):
        '''Create an apodization time line used when beams from 2 emissions are summed.

    Parameters:
    -----------

    xdc: integer (pointer)
        Pointer to a transducer aperture

    times: array_like, double,
        Times after which the associated apodization is valid

    values: array_like, double,
        Apodization values. Matrix with one row for each time value and a number
        of columns equal to the number of physical elements in the aperture.

    line_no: scalar, integer,
        Index of line to set the apodization for. Default value is 0.
        '''

        times = np.array(times)
        apodization = np.array(apodization)
        no_times = times.size

        if (no_times > 1):
            assert apodization.shape[0] == no_times

        libbft.bft_sum_apodization(ct.c_void_p(xdc),
                                   times.ctypes.data_as(PtrDouble),
                                   apodization.ctypes.data_as(PtrDouble),
                                   ct.c_uint32(no_times),
                                   ct.c_uint32(line_no))
    # bft_sum_apodization

    # -----------------------------------------------------------------------
    @staticmethod
    def bft_dynamic_focus(xdc, dir_xz, dir_yz, line_no=0):
        ''' Set dynamic focusing for a line

    Parameters:
    -----------

    xdc: integer,
        Pointer to the transducer aperture

    dir_zx: scalar, double
        Direction (angle) in radians for the dynamic focus.
        The direction is taken from the center for the focus of the transducer
        in the z-x plane.

    dir_zy: scalar, double,
        Direction (angle) in radians for the dynamic focus.
        The direction is taken from the center for the focus of the transducer
        in the z-y plane.

    line_no: scalar, integer,
        Index of line to set focusing for. Default value is 0.
        '''
        libbft.bft_dynamic_focus(ct.c_void_p(xdc),
                                 ct.c_uint32(line_no),
                                 ct.c_double(dir_xz),
                                 ct.c_double(dir_yz))
    # bft_dynamic_focus

    # -------------------------------------------------------------------------
    @staticmethod
    def bft_beamform(data, time, **kwarg):
        '''Beamform a set of data and produce a set of beams.

    The number of the simultaneously formed beams is set
    by `bft_no_lines`. If `bft_no_lines` has not been called prior to invoking
    this function, , only one scan line will be beamformed.

    The normal behaviour is to use delays corresponding to the difference
    in one-way propagation times - from the focal point to the transducer
    elements.

    This function can be used also for synthetic transmit aperture
    beamforming. There are two possibilities to do so:

     * Specify the optional `elem` parameter
     * Specify the optional `xmt` parameter

    If this is the case, the delay applied onto the individual element signals
    will be the sum of the _normal_ receive delay, *and* of the difference
    in propagation time from the transmit position (defined by `elem` or `xmt`)

    Parameters:
    -----------
    data: array_like, double
        Data received on individual elements. Two dimensional array.

        >>> from numpy import zeros
        >>> data = zeros(192, 4096)
        >>> [number_of_elements, number_of_samples] = data.shape

    time: array_like, (or scalar), double
        Time instance of the first sample in the collected `data`

    Returns:
    --------
    beams: array_like, double

        '''
        options = {
            'elem': 65535,
            'xmt': None,
        }

        options.update(kwarg)

        elem = options['elem']
        xmt = options['xmt']

        if (elem < 65535) and (xmt is not None):
            print('Either choose element index, or transmit position.')
            raise RuntimeError('Confusing options for beamforming procedure.')

        if xmt is None:
            xmt = ct.cast(0, PtrDouble)
        else:
            xmt = ct.array(xmt).ctypes.data_as(PtrDouble)

        data = np.array(data)
        no_samples = data.shape[1]
        no_elements = data.shape[0]

        no_beams = ct.c_uint32(0)
        no_out_samples = ct.c_uint32(0)

        res = libbft.bft_beamform(ct.byref(no_beams),
                                  ct.byref(no_out_samples),
                                  data.ctypes.data_as(PtrDouble),
                                  ct.c_double(time),
                                  ct.c_uint32(no_samples),
                                  ct.c_uint32(no_elements),
                                  ct.c_uint32(elem),
                                  PtrDouble(xmt))

        # int(no_beams.value) does a conversion from ctypes to python type
        shp = (int(no_beams.value), int(no_out_samples.value))

        lores = np.ctypeslib.as_array(res, shape=shp).copy() 
        libbft.bft_free_mem(res)
        #return np.ctypeslib.as_array(res, shape=shp)
        return lores
    # bft_beamform()

    # -------------------------------------------------------------------------
    @staticmethod
    def bft_sum_images(image1, elem1, image2, elem2, Time):
        '''Sum 2 low resolution images in 1 high resolution.

    Parameters:
    -----------
    image1: array_like, double
        Matrix with the RF data for the image.

        >>> [no_lines, no_samples] = image1.shape

    ele1: scalar, integer
        Transmit element index, used to acquire `image1`

    image2: array_like, double
        Matrix with the RF data for the image. Same dimensions as `image1`

    ele2: scalar, integer
        Transmit element index used to acquire `image2`

    time   -  The arrival time of the first samples. The two images
                    must be aligned in time
        '''
        image1 = np.array(image1)
        image2 = np.array(image2)

        [no_lines, no_samples] = image1.shape
        assert (no_lines, no_samples) == image2.shape

        hirestmp = libbft.bft_sum_images(image1.ctypes.data_as(PtrDouble),
                                      ct.c_uint32(elem1),
                                      image2.ctypes.data_as(PtrDouble),
                                      ct.c_uint32(elem2),
                                      ct.c_double(Time),
                                      ct.c_uint32(no_samples))
        hires = np.ctypeslib.as_array(hirestmp, shape=(no_lines, no_samples)).copy()
        
        libbft.bft_free_mem(hirestmp)
        #return np.ctypeslib.as_array(hires, shape=(no_lines, no_samples))
        return hires
    # bft_sum_images()

    # -------------------------------------------------------------------------
    @staticmethod
    def bft_add_image(hires, lores, element, start_time):
        '''  Add a low resolution to a high resolution image.

    Parameters:
    -----------

    hires: array_like, double
        High resolution RF image. One row per scan line

    lores: array_like, double
        Low resolution RF image. Same dimensions as `hires`

        >>> assert hires.shape == lores.shape

    element: scalar, integer
        Element index, used to acquire the low resolution image

    start_time: scalar, double,
        Arrival time of the first sample of the RF lines.

    Returns:
    --------
    hires - The high resolution image
        '''
        hires = np.array(hires)
        lores = np.array(lores)

        assert hires.ndim == 2
        assert lores.shape == hires.shape
        assert hires.dtype == lores.dtype == np.float64
        (no_lines, no_samples) = hires.shape

        libbft.bft_add_images(hires.ctypes.data_as(PtrDouble),
                              lores.ctypes.data_as(PtrDouble),
                              ct.c_uint32(no_samples),
                              ct.c_double(start_time),
                              ct.c_uint32(element)
                              )
        return hires
    # bft_add_image()

    # -------------------------------------------------------------------------
    @staticmethod
    def bft_free_mem(ptr):
      "Release memory allocated by malloc() by the BFT DLL"
      libbft.bft_free_mem(ptr)
    # bft_free_mem()
# bft . . . . . . . . . .  . . . . . . . . . . . . . . . . . . . . . . . . . .

if __name__ == "__main__":
    from pylab import *
    ion()

    no_elements = 192
    f0 = 7.5e6
    fs = 40.0e6
    c = 1540.0
    elem1 = 0
    elem2 = 173

    wavelen = c / f0
    pitch = wavelen
    start_depth = 0.5 / 100.
    stop_depth = 5.5 / 100.
    start_time = 2 * start_depth / c
    apodization = np.hamming(no_elements)

    nsamples = int(2 * (stop_depth - start_depth) / c * fs)
    data = np.zeros((no_elements, nsamples))

    bft.bft_init()
    bft.bft_param('fs', fs)
    bft.bft_param('c', c)

    xdc = bft.bft_linear_array(no_elements, pitch)
    bft.bft_dynamic_focus(xdc, 0., 0.)
    bft.bft_focus(xdc, 0.0, r_[0, 0, 50.0] / 1000)
    bft.bft_apodization(xdc, 0.0, np.hamming(no_elements))
    bft.bft_sum_apodization(xdc, 0.0, np.hamming(no_elements))

    rf1 = bft.bft_beamform(data, start_time)
    rf2 = bft.bft_beamform(data, start_time)
    hires1 = bft.bft_sum_images(rf1, elem1, rf2, elem2, start_time)
    hires1 = bft.bft_add_image(hires1, rf1, elem1, start_time)
    print ('Here is done too')
    bft.bft_xdc_free(xdc)
    bft.bft_end()
