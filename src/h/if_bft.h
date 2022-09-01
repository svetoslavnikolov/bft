/**
 *   @file     if_bft.h
 *   @Author   Svetoslav Nikolov (nikolov.svetoslav@gmail.com)
 *   @date     October, 2014
 *   @brief    Interface to the beamforming toolbox. 
 *             Simple C interface, similar to the interface exposed to users
 *             in Python and Matlab
 */

#pragma once

#ifdef __cplusplus
#define EXTERNC    extern "C"
#else
#define EXTERNC
#endif


#if defined( WIN32 )

#ifdef BFT_DLL
#define BFT_API EXTERNC __declspec(dllexport)
#else
#define BFT_API EXTERNC __declspec(dllimport)
#endif

#elif defined( __APPLE__ )

#ifdef BFT_DLL
#define BFT_API EXTERNC __attribute__((visibility("default")))
#else
#define BFT_API EXTERNC
#endif

#endif

BFT_API void bft_init(TMsgFunc msg, ui32 suppress);

BFT_API void bft_end(void);

BFT_API double bft_param(char* id, double val);

BFT_API ui32 bft_no_lines(ui32 no_lines);

BFT_API void* bft_xdc(double* centers, ui32 nelem);

BFT_API void bft_xdc_free(void* xdc);

BFT_API void bft_center_focus(double* point, ui32 line_no);

BFT_API void bft_focus(void* xdc, double* times, double* focus, 
    ui32 no_times, ui32 line_no);

BFT_API void bft_focus_pixel(void* xdc, double* points,
    ui32 no_points, ui32 line_no);

BFT_API void bft_focus_2way(void* xdc, double* times, double* delays, 
    ui32 no_times, ui32 line_no);

BFT_API void bft_focus_times(void* xdc, double* times, double* delays,
    ui32 no_times, ui32 line_no);

BFT_API void bft_apodization(void* xdc, double* times, double* apodization,
    ui32 no_times, ui32 line_no);

BFT_API void bft_sum_apodization(void* xdc, double* times, double* apodization,
    ui32 no_times, ui32 line_no);

BFT_API void bft_dynamic_focus(void* xdc, ui32 line_no, double dir_xz, double dir_yz);

/*
BFT_API double* bft_beamform(double* data, double Time, ui32 no_samples,
    ui32 no_elements, ui32 element_no, double* xmt);
*/

BFT_API double* bft_beamform(ui32* no_lines, ui32 *no_out_samples, double* data,
    double Time, ui32 no_samples, ui32 no_elements, ui32 element_no, double* xmt);

BFT_API double * bft_sum_images(double* data1, ui32 element1, double* data2,
    ui32 element2, double time, ui32 no_samples);

BFT_API void bft_add_images(double *hires, double *lores, ui32 no_samples,
    double time, ui32 element);

BFT_API void bft_sub_images(double *hires, double *lores, ui32 no_samples,
    double time, ui32 element);

BFT_API void bft_set_filter_bank(double* coef, ui32 Nf, ui32 Ntaps);

BFT_API double* bft_delay(double*src, ui32 src_len, double* times, double* delays, 
    ui32 times_len, double src_start_time, double dest_start_time, 
    ui32 dest_len, ui32 method);

BFT_API void bft_xdc_set(void* xdc, double* centers, ui32 no_elements);

BFT_API void bft_free_mem(void * ptr);