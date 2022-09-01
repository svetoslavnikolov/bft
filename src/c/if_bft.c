#include "error.h"
#include "geometry.h"
#include "focus.h"
#include "beamform.h"
#include "sys_params.h"
#include "transducer.h"
#include "motion.h"
#include "if_bft.h"

#include <signal.h>
#include <string.h>
#include <stdlib.h>



static TSysParams sys;

static TFocusLineCollection *flc = NULL;
static TApoLineCollection *alc = NULL;
static TApoLineCollection *salc = NULL;   /* Sum apo-line collection*/

static int initialized = FALSE;
static int suppress_msg = FALSE;

#define myassert(x, msg)\
    if (!(x)){\
        msgprint(msg);\
        assert(x && msg);\
        }\
    

#define BFT_INITIALIZE\
    if (!initialized) {\
        bft_init(NULL, 0);\
    }

void bft_at_abort(int sig_no)
{
    printf("\t***********************************************************\n");
    printf("\t*                                                         *\n");
    printf("\t* BeamForming Toolbox  message :                          *\n");
    printf("\t*                                                         *\n");
    printf("\t* Signal 'abort' caught                                   *\n");
    printf("\t* One of the probable causes is bad memory pointer        *\n");
    printf("\t* Check if you have supplied wrong transducer definition  *\n");
    printf("\t*                                                         *\n");
    printf("\t***********************************************************\n");
    printf("Signal %d \n", sig_no);
}


void bft_init(TMsgFunc msg, ui32 suppress)
{
    SetMsgFunc(msg);

    if (initialized)
    {
        bft_end();
    }

    if (!suppress)
    {
        msgprint("**************************************************************\n");
        msgprint("*                                                            *\n");
        msgprint("*               Beamforming  Toolbox                         *\n");
        msgprint("*                       by                                   *\n");
        msgprint("*                Svetoslav Nikolov                           *\n");
        msgprint("*      (E-mail: nikolov.svetoslav@gmail.com)                 *\n");
        msgprint("*                                                            *\n");
        msgprint("*               (Ver 1.0,  Sep 7, 2000)                      *\n");
        msgprint("*              Version 1.5,  Oct 9, 2013                     *\n");
        msgprint("*                                                            *\n");
        msgprint("**************************************************************\n");
    }
    
    sys.fs = 40e6;
    sys.c = 1540;

    flc = (TFocusLineCollection *)calloc(1, sizeof(TFocusLineCollection));
    assert(flc != NULL);
    alc = (TApoLineCollection*)calloc(1, sizeof(TApoLineCollection));
    assert(alc != NULL);
    set_no_lines(alc, flc, 1);

    salc = (TApoLineCollection*)calloc(1, sizeof(TApoLineCollection));
    assert(salc != NULL);
    set_no_lines(salc, flc, 1);
    flc->use_filter_bank = 0;

    signal(SIGABRT, bft_at_abort);
    initialized = TRUE;
    suppress_msg = suppress;
}



/** Function called either when the DLL is unloaded or when bft_end() is called
 */
static void bft_at_exit(void)
{
    if (initialized == FALSE) return;

#ifdef  MALLOC_CHECK_
    printf("MALLOC_CHECK_ is %d \n", MALLOC_CHECK_);
#endif
    if (flc != NULL){
#ifdef DEBUG   
        printf("Freeing Focusing settings \n");
#endif      
        del_focus_line_collection(flc);
        free(flc); flc = NULL;
    }

    if (alc != NULL){
#ifdef DEBUG   
        printf("Freeing all apodization settings \n");
#endif      
        del_apo_line_collection(alc);
        free(alc); alc = NULL;
    }

    if (salc != NULL){
#ifdef DEBUG   
        printf("Freeing all summation apodization settings \n");
#endif      
        del_apo_line_collection(salc);
        free(alc); salc = NULL;
    }

#ifdef DEBUG   
    printf("Freeing all transducers \n");
#endif   
    bft_free_all_xdc();
    initialized = FALSE;

    msgprint("**************************************************************\n");
    msgprint("*       Exitting the BeamForming Toolbox                     *\n");
    msgprint("**************************************************************\n");
}


void bft_end(void)
{
    bft_at_exit();
    initialized = FALSE;
}


double bft_param(char* id, double val)
{
    struct {
        char id[80];
        double* valptr;
    } lut[] = {
            { "fs", &sys.fs },
            { "c",  &sys.c },
    };

    int nparam = sizeof(lut) / sizeof(lut[0]);

    BFT_INITIALIZE
    if (id == NULL) {
        eprintf("Found null pointer \n");
        return -val;
    }

    for (int n = 0; n < nparam; n++) {
        if (!strncmp(id, lut[n].id, sizeof(lut[0].id))) {
            *lut[n].valptr = val;
            return val;
        }
    }

    eprintf("Could not find argument %s \n", id);
    return -val;
}

ui32 bft_no_lines(ui32 no_lines)
{
    BFT_INITIALIZE

    set_no_lines(alc, flc, no_lines);
    set_no_lines(salc, flc, no_lines);

    return no_lines;
}


void* bft_xdc(double* centers, ui32 nelem)
{
    BFT_INITIALIZE;
    return bft_transducer(nelem, (TPoint3D*)centers);
}


void bft_xdc_free(void* xdc)
{
    BFT_INITIALIZE;
    bft_free_xdc((TTransducer*) xdc);
}


void bft_center_focus(double* point, ui32 line_no)
{
    BFT_INITIALIZE;

    set_center_focus(flc, (TPoint3D*)point, line_no);
}


void bft_focus(void* xdc, double* times, double* focus, ui32 no_times, ui32 line_no)
{
    BFT_INITIALIZE;
    set_focus(flc, &sys, (TTransducer*)xdc, times, (TPoint3D*)focus, no_times, line_no);
}


void bft_focus_pixel(void* xdc, double* points, ui32 no_points, ui32 line_no)
{
    BFT_INITIALIZE;
    set_focus_pixel(flc, &sys, (TTransducer*)xdc, (TPoint3D*)points, no_points, line_no);
}


void bft_focus_2way(void* xdc, double* times, double* delays, ui32 no_times, ui32 line_no)
{
    BFT_INITIALIZE;
    set_focus_times(flc, &sys, xdc, times, delays, no_times, line_no);
}


void bft_focus_times(void* xdc, double* times, double* delays, ui32 no_times, ui32 line_no)
{
    BFT_INITIALIZE;
    set_focus_times(flc, &sys, (TTransducer*)xdc, times, delays, no_times, line_no);
}


void bft_apodization(void* xdc, double* times, double* apodization, ui32 no_times, ui32 line_no)
{
    BFT_INITIALIZE;
    set_apodization(alc, &sys, (TTransducer*)xdc, times, apodization, no_times, line_no);
}


void bft_sum_apodization(void* xdc, double* times, double* apodization, ui32 no_times, ui32 line_no)
{
    BFT_INITIALIZE;
    set_apodization(alc, &sys, (TTransducer*)xdc, times, apodization, no_times, line_no);
}


void bft_dynamic_focus(void* xdc, ui32 line_no, double dir_xz, double dir_yz)
{
    BFT_INITIALIZE;
    set_dynamic_focus(flc, xdc, line_no, dir_xz, dir_yz);
}


double* bft_beamform(ui32* no_lines, ui32 *no_out_samples, double* data, double Time, ui32 no_samples, 
    ui32 no_elements, ui32 element_no, double* xmt)
{
    double* beam = NULL;
    double* ptr = NULL;
    double** rf_data = NULL;
    double** bf_data = NULL;

    BFT_INITIALIZE;

    rf_data = (double**)calloc(no_elements, sizeof(** rf_data));
    myassert(rf_data != NULL, "Could not allocate pointers to RF data\n");

    for (ui32 n = 0; n < no_elements; n++) {
        rf_data[n] = data + n * no_samples;
    }

    bf_data = beamform_image(
        flc, alc, &sys, Time, rf_data, no_samples, element_no, (TPoint3D*)xmt);
    myassert(bf_data != 0, "Calculations did not allocate mem for result.\n");

    free(rf_data);

    //TODO: How to handle the case when pixel == TRUE for more than 1 line
    if ((flc->no_focus_time_lines == 1) && (flc->ftl[0].pixel == TRUE)) {
        no_samples = flc->ftl[0].no_times;
    }
    
    beam = (double*)malloc(flc->no_focus_time_lines * no_samples * sizeof(double));
    
    myassert(beam != NULL, "Could not allocate beam\n");

    ptr = beam;
    for (ui32 n = 0; n < flc->no_focus_time_lines; n++) {
        memcpy(ptr, bf_data[n], no_samples*sizeof(beam[0]));
        ptr += no_samples;
        free(bf_data[n]);
    }

    free(bf_data);

    *no_out_samples = no_samples;
    *no_lines = flc->no_focus_time_lines;

    return beam;
}


double * bft_sum_images(double* data1, ui32 element1, double* data2,
    ui32 element2, double time, ui32 no_samples)
{
    double** rf1 = NULL;
    double** rf2 = NULL;
    double ** hi_res = NULL;
    double * hi_res_data = NULL;
    double *ptr = NULL;

    BFT_INITIALIZE;

    rf1 = (double**)malloc(flc->no_focus_time_lines*sizeof(double*));
    myassert(rf1, "Could not allocate memory for RF1");
  
    rf2 = (double**)malloc(flc->no_focus_time_lines * sizeof(double*));
    if (rf2 == NULL) {
        free(rf1); 
        myassert(rf2, "Could not allocate memory for RF2");
    }
    
    for (ui32 i = 0; i < flc->no_focus_time_lines; i++){
        rf1[i] = data1 + no_samples * i;
        rf2[i] = data2 + no_samples * i;
    }
    
    hi_res = sum_images(flc, alc, &sys, rf1, element1, rf2, element2,time, no_samples );

    hi_res_data = (double*)calloc( no_samples * flc->no_focus_time_lines ,sizeof(double));
    myassert(hi_res_data != NULL, "Could not allocate output result");
    ptr = hi_res_data;

    for (ui32 i = 0; i<flc->no_focus_time_lines; i++){
        memcpy(ptr, hi_res[i], no_samples * sizeof(ptr[0]));
        ptr += no_samples;
        free(hi_res[i]);
    }

    free(hi_res);
    free(rf1);
    free(rf2);

    return hi_res_data;
}


void bft_add_images(double *hires, double *lores, ui32 no_samples, double time, ui32 element)
{
   double **lo_res = NULL;
   double **hi_res = NULL;

   BFT_INITIALIZE;

   hi_res = (double **) malloc(flc->no_focus_time_lines * sizeof( double * ) );
   myassert(hi_res, "Canno get");

   lo_res = (double **) malloc(flc->no_focus_time_lines * sizeof( double * ) );

   if ( lo_res == NULL ) { free(hi_res); abort(); }

   for ( ui32 i = 0; i < flc->no_focus_time_lines; i++ ) {
      lo_res[i] = lores + no_samples * i;
      hi_res[i] = hires + no_samples * i;
   }

   add_images(flc, salc, &sys, hi_res, lo_res, element, time, no_samples);

   free(hi_res);
   free(lo_res);
}


void bft_sub_images(double *hires, double *lores, ui32 no_samples, double time, ui32 element)
{
    double **lo_res = NULL;
    double **hi_res = NULL;

    BFT_INITIALIZE;

    hi_res = (double **)malloc(flc->no_focus_time_lines * sizeof(double *));
    myassert(hi_res, "Canno get");

    lo_res = (double **)malloc(flc->no_focus_time_lines * sizeof(double *));

    if (lo_res == NULL) { free(hi_res); abort(); }

    for (ui32 i = 0; i < flc->no_focus_time_lines; i++) {
        lo_res[i] = lores + no_samples * i;
        hi_res[i] = hires + no_samples * i;
    }

    sub_images(flc, alc, &sys, hi_res, lo_res, element, time, no_samples);
}


void bft_set_filter_bank(double* coef, ui32 Nf, ui32 Ntaps)
{
    BFT_INITIALIZE;
    myassert(coef != NULL, "Received a null pointer \n");
    set_filter_bank(flc, Nf, Ntaps, coef);
}


double* bft_delay(double*src, ui32 src_len, double* times, double* delays, ui32 times_len, 
    double src_start_time, double dest_start_time, ui32 dest_len, ui32 method)
{

    switch (method)
    {
    case 0:
        myassert(&flc->filter_bank != NULL, "Set filter bank first !\n");
        return delay_line_filter(
            &sys, &flc->filter_bank, times, delays,
            times_len, src, src_len, src_start_time,
            dest_start_time, dest_len);

    default:
        return delay_line_linear(
            &sys, times, delays, times_len, src,
            src_len, src_start_time,
            dest_start_time, dest_len);
    }

}


void bft_xdc_set(void* xdc, double* centers, ui32 no_elements)
{
    BFT_INITIALIZE;
    
    myassert(xdc != NULL, "XDC is a null pointer\n");
    myassert(centers != NULL, "centers is a null pointer\n");
    bft_transducer_set(xdc, no_elements, (TPoint3D*) centers);
}


void bft_free_mem(void * ptr)
{
    myassert(ptr != NULL, "NULL pointer passed");
    if (ptr != NULL){
        free(ptr);
    }
}
